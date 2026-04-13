#!/usr/bin/env python3
"""
AIUI 文档爬取脚本
读取 config/urls.json，用 Playwright 无头浏览器抓取每个页面，
将正文转换为 Markdown 并保存到 raw_docs/{category}/{doc_id}.md。
最终生成 raw_docs/manifest.json 记录爬取结果。

用法：
    python3 scripts/crawl.py [--resume]  # --resume 跳过已存在文件
"""

import argparse
import json
import re
import time
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── 路径 ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
URLS_FILE = ROOT / "config" / "urls.json"
RAW_DOCS = ROOT / "raw_docs"
MANIFEST_FILE = RAW_DOCS / "manifest.json"

# ── 爬取参数 ──────────────────────────────────────────────────────────────────
DELAY_SEC = 1.5          # 每页间隔秒数
PAGE_TIMEOUT = 30_000    # 页面加载超时 ms
RETRY_TIMES = 2          # 失败重试次数

# ── markdownify 配置 ──────────────────────────────────────────────────────────
MD_OPTIONS = dict(
    heading_style="ATX",      # # 风格标题
    bullets="-",              # 无序列表用 -
    code_language_callback=None,
    strip=["script", "style", "svg", "button"],
)


def load_urls() -> dict:
    with open(URLS_FILE, encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs(categories: list[str]) -> None:
    for cat in categories:
        (RAW_DOCS / cat).mkdir(parents=True, exist_ok=True)


def fetch_page(page, url: str, retries: int = RETRY_TIMES) -> dict | None:
    """
    访问 URL，等待 .markdown-body 渲染完成后返回 {title, html}。
    失败时最多重试 retries 次，均失败返回 None。
    """
    for attempt in range(retries + 1):
        try:
            page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT)
            # 等待正文容器出现
            page.wait_for_selector(".markdown-body", timeout=PAGE_TIMEOUT)

            result = page.evaluate("""() => {
                // 标题：取 #doc-content 内的第一个 h1
                const h1 = document.querySelector('#doc-content .doc-info h1')
                         || document.querySelector('#doc-content h1')
                         || document.querySelector('h1');
                const title = h1 ? h1.innerText.trim() : '';

                // 正文：.markdown-body（即 #content）
                const body = document.querySelector('.markdown-body');
                const bodyHTML = body ? body.innerHTML : '';

                return { title, bodyHTML };
            }""")
            return result

        except PlaywrightTimeout:
            if attempt < retries:
                print(f"    [timeout] attempt {attempt + 1}/{retries + 1}, retrying…")
                time.sleep(2)
            else:
                return None
        except Exception as e:
            if attempt < retries:
                print(f"    [error] {e}, retrying…")
                time.sleep(2)
            else:
                return None


def clean_html(html: str) -> str:
    """用 BeautifulSoup 预处理：删除 style/script/svg 标签及内容，保留文本结构。"""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["style", "script", "svg", "button", "noscript"]):
        tag.decompose()
    return str(soup)


def html_to_markdown(title: str, html: str, source_url: str) -> str:
    """将 HTML 正文转为带 frontmatter 的 Markdown 字符串。"""
    html = clean_html(html)
    body_md = md(html, **MD_OPTIONS)

    # 清理多余空行（3+ 行变 2 行）
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)
    # 清理行尾空格
    body_md = "\n".join(line.rstrip() for line in body_md.splitlines())

    frontmatter = (
        "---\n"
        f"title: {title}\n"
        f"source_url: {source_url}\n"
        "---\n"
    )
    return frontmatter + "\n" + body_md.strip() + "\n"


def run(resume: bool) -> None:
    data = load_urls()
    categories = data["categories"]
    ensure_dirs(list(categories.keys()))

    # 加载已有 manifest
    manifest: dict = {}
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, encoding="utf-8") as f:
            manifest = json.load(f)

    total = sum(len(cat["docs"]) for cat in categories.values())
    done = 0
    skipped = 0
    failed = []

    print(f"共 {total} 篇文档待爬取（resume={resume}）\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            ignore_https_errors=True,    # 忽略自签名证书
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        for cat_key, cat_info in categories.items():
            cat_title = cat_info["title"]
            docs = cat_info["docs"]
            print(f"── {cat_title} ({len(docs)} 篇) ──")

            for doc in docs:
                doc_id = doc["id"]
                url = doc["url"]
                out_path = RAW_DOCS / cat_key / f"{doc_id}.md"

                done += 1
                prefix = f"[{done:3d}/{total}] {doc_id}"

                # resume 模式：跳过已存在且非空的文件
                if resume and out_path.exists() and out_path.stat().st_size > 50:
                    print(f"{prefix}  SKIP (已存在)")
                    skipped += 1
                    continue

                print(f"{prefix}  {doc['title']}", end="", flush=True)

                result = fetch_page(page, url)
                if result is None:
                    print(f"  [FAILED]")
                    failed.append({"doc_id": doc_id, "url": url, "category": cat_key})
                    manifest[doc_id] = {
                        "status": "failed",
                        "url": url,
                        "category": cat_key,
                        "title": doc["title"],
                    }
                    continue

                title = result["title"] or doc["title"]
                markdown = html_to_markdown(title, result["bodyHTML"], url)
                out_path.write_text(markdown, encoding="utf-8")

                size_kb = len(markdown.encode("utf-8")) / 1024
                print(f"  → {size_kb:.1f} KB")

                manifest[doc_id] = {
                    "status": "ok",
                    "url": url,
                    "category": cat_key,
                    "title": title,
                    "file": str(out_path.relative_to(ROOT)),
                    "size_bytes": len(markdown.encode("utf-8")),
                    "crawled_at": datetime.utcnow().isoformat() + "Z",
                }

                # 写入 manifest（每页更新，防止中途中断丢失进度）
                MANIFEST_FILE.write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

                time.sleep(DELAY_SEC)

        browser.close()

    # ── 最终汇总 ──────────────────────────────────────────────────────────────
    ok_count = sum(1 for v in manifest.values() if v.get("status") == "ok")
    fail_count = len(failed)

    print(f"\n{'='*50}")
    print(f"完成：{ok_count} 篇成功，{skipped} 篇跳过，{fail_count} 篇失败")
    print(f"Manifest 已保存至 {MANIFEST_FILE}")

    if failed:
        print(f"\n失败列表：")
        for item in failed:
            print(f"  {item['doc_id']}  {item['url']}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIUI 文档爬取脚本")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="跳过 raw_docs/ 中已存在的文件，断点续爬",
    )
    args = parser.parse_args()
    run(resume=args.resume)
