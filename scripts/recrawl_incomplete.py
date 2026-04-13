#!/usr/bin/env python3
"""
scripts/recrawl_incomplete.py

用 Playwright 重新爬取内容缺失的文档页面，
将 HTML 转为 Markdown 并写入 raw_docs/，
然后调用 build.py 的清洗逻辑输出到 docs/。
"""

import json
import re
import time
from pathlib import Path

import markdownify
from playwright.sync_api import sync_playwright

ROOT       = Path(__file__).parent.parent
CONFIG     = ROOT / "config"
RAW_DOCS   = ROOT / "raw_docs"
DOCS_DIR   = ROOT / "docs"

MAPPING    = json.loads((CONFIG / "mapping.json").read_text(encoding="utf-8"))
TERMINOLOGY = json.loads((CONFIG / "terminology.json").read_text(encoding="utf-8"))

BASE_URL   = "https://aiui-doc.xf-yun.com/project-1"

# 要重新爬取的目标文件
TARGETS = [
    "docs/custom-biz/skill-studio/design-guide.md",
    "docs/custom-biz/skill-studio/development/create.md",
    "docs/sdk-dev/llm-chain/personalization.md",
]


def find_entry(target_path: str) -> dict | None:
    for e in MAPPING["entries"]:
        if e["target_path"] == target_path:
            return e
    return None


def crawl_page(page, doc_id: str) -> str:
    """访问页面并提取正文 HTML。"""
    url = f"{BASE_URL}/{doc_id}/"
    print(f"  访问 {url} ...")
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(3)  # 等待 JS 渲染

    # 尝试多个可能的正文容器选择器
    selectors = [
        ".doc-content",
        ".markdown-body",
        ".content-body",
        "article",
        ".doc-main",
        "#content",
        ".ql-editor",
        "main",
    ]

    html = ""
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                html = el.inner_html()
                if len(html) > 100:
                    print(f"  选择器 {sel} 命中，HTML 长度 {len(html)}")
                    break
        except Exception:
            continue

    if not html or len(html) < 100:
        # Fallback: 获取 body 全部内容
        try:
            html = page.query_selector("body").inner_html()
            # 去掉 header/nav/footer
            html = re.sub(r'<(?:header|nav|footer)[^>]*>.*?</(?:header|nav|footer)>',
                         '', html, flags=re.DOTALL | re.IGNORECASE)
            print(f"  使用 body fallback，HTML 长度 {len(html)}")
        except Exception as e:
            print(f"  [ERROR] 无法获取页面内容: {e}")
            return ""

    return html


def html_to_markdown(html: str, title: str) -> str:
    """将 HTML 转换为 Markdown 并添加 frontmatter。"""
    md = markdownify.markdownify(
        html,
        heading_style="ATX",
        strip=["script", "style", "nav", "footer"],
    )

    # 添加 frontmatter
    frontmatter = f"---\ntitle: {title}\n---\n\n"

    return frontmatter + md


def apply_build_transforms(text: str, title: str, entry: dict) -> str:
    """应用 build.py 中相同的清洗逻辑。"""
    # 动态导入 build.py 中的函数
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import build

    url_map = build.build_url_map(MAPPING["entries"])
    term_maps = TERMINOLOGY["mappings"]

    text = build.update_frontmatter(text, title)
    text = build.remove_toc_jumps(text)
    text, _ = build.expand_card_links(text)
    text = build.rewrite_doc_links(text, url_map)
    text = build.fix_malformed_bracket_links(text)
    text = build.fix_relative_links(text)
    text = build.apply_terminology(text, term_maps)
    text = build.fix_image_paths(text)
    text = build.clean_double_brackets(text)
    text = build.normalize_closing_fences(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    if not text.endswith('\n'):
        text += '\n'

    return text


def main():
    print("开始重新爬取缺失文档...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            ignore_https_errors=True,
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        results = []

        for target_path in TARGETS:
            entry = find_entry(target_path)
            if not entry:
                print(f"[SKIP] {target_path}: mapping.json 中未找到对应条目")
                results.append({"file": target_path, "status": "not_found", "chars": 0})
                continue

            doc_id = entry["doc_id"]
            title = entry["title"]
            raw_path = ROOT / entry["raw_path"]
            docs_path = ROOT / entry["target_path"]

            print(f"处理 {doc_id} → {target_path}")

            # 爬取
            html = crawl_page(page, doc_id)
            if not html:
                print(f"  [FAIL] 无法获取内容")
                results.append({"file": target_path, "status": "crawl_failed", "chars": 0})
                continue

            # HTML → Markdown
            raw_md = html_to_markdown(html, title)

            # 保存到 raw_docs/
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(raw_md, encoding="utf-8")
            print(f"  raw_docs 已更新: {len(raw_md)} 字符")

            # 应用 build.py 清洗
            clean_md = apply_build_transforms(raw_md, title, entry)

            # 保存到 docs/
            docs_path.parent.mkdir(parents=True, exist_ok=True)
            docs_path.write_text(clean_md, encoding="utf-8")

            # 统计正文字数
            body = re.sub(r'^---\n.*?\n---\n', '', clean_md, flags=re.DOTALL)
            body_clean = re.sub(r'[#*\-_|`>\s\[\]\(\)]', '', body)
            char_count = len(body_clean)

            print(f"  docs/ 已写入: {len(clean_md)} 字符, 正文约 {char_count} 字")
            results.append({
                "file": target_path,
                "status": "success",
                "raw_chars": len(raw_md),
                "doc_chars": len(clean_md),
                "body_chars": char_count,
            })
            print()

        browser.close()

    # 汇总
    print("\n" + "=" * 60)
    print("补爬结果汇总")
    print("=" * 60)
    for r in results:
        status_icon = "✓" if r["status"] == "success" else "✗"
        if r["status"] == "success":
            print(f"  {status_icon} {r['file']}: {r['body_chars']} 字正文")
        else:
            print(f"  {status_icon} {r['file']}: {r['status']}")


if __name__ == "__main__":
    main()
