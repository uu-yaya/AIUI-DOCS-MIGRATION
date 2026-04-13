#!/usr/bin/env python3
"""
处理无法下载的防盗链图片：
1. 扫描 raw_docs/ 中所有外部图片链接
2. 生成 config/missing_images.json 清单
3. 创建 raw_docs/_images/placeholder.svg 占位图
4. 在 .md 文件中替换为带 TODO 注释的占位符
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DOCS = ROOT / "raw_docs"
IMAGES_DIR = RAW_DOCS / "_images"
CONFIG_DIR = ROOT / "config"

MISSING_JSON = CONFIG_DIR / "missing_images.json"
PLACEHOLDER_SVG = IMAGES_DIR / "placeholder.svg"

# 匹配目标 CDN 域名的图片（含可能残留的 "null" title）
BLOCKED_IMG_RE = re.compile(
    r'!\[([^\]]*)\]\('
    r'(https?://(?:aiui-file|xfyun-doc)\.cn-bj\.ufileos\.com/[^\)\s"]+)'
    r'(?:\s+"[^"]*")?'
    r'\)'
)

# ── 占位 SVG ─────────────────────────────────────────────────────────────────

PLACEHOLDER_SVG_CONTENT = """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="270" viewBox="0 0 480 270">
  <rect width="480" height="270" rx="6" fill="#f3f4f6"/>
  <rect x="1" y="1" width="478" height="268" rx="5" fill="none" stroke="#d1d5db" stroke-width="1.5" stroke-dasharray="8 4"/>
  <text x="240" y="126" text-anchor="middle" font-family="PingFang SC, Helvetica Neue, sans-serif"
        font-size="16" fill="#9ca3af">图片待补充</text>
  <text x="240" y="152" text-anchor="middle" font-family="PingFang SC, Helvetica Neue, sans-serif"
        font-size="12" fill="#d1d5db">Image Pending</text>
  <path d="M220 92 l20-20 l20 20" fill="none" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/>
  <path d="M240 72 l0 28" fill="none" stroke="#d1d5db" stroke-width="2" stroke-linecap="round"/>
</svg>
"""


# ── 上下文推断图片描述 ────────────────────────────────────────────────────────

def infer_description(alt: str, url: str, context_lines: list[str], line_idx: int) -> str:
    """
    优先用非空 alt text；否则从上下文段落文字推断；最后从 URL 文件名兜底。
    """
    # 1. 有意义的 alt text（过滤无意义的占位值）
    if alt and alt not in ('null', 'undefined', 'image', 'img', '图片', 'value', ''):
        return alt.strip()

    # 2. 从上下文往前查找，优先取：
    #    a) 最近一个包含中文的非图片行
    #    b) 最近一个 Markdown 标题行
    nearest_text = ''
    nearest_heading = ''
    for offset in range(-1, -12, -1):    # 向前最多查 12 行
        idx = line_idx + offset
        if idx < 0:
            break
        line = context_lines[idx].strip()
        if not line:
            continue
        # 跳过代码块围栏
        if line.startswith('```') or line.startswith('~~~') or line == '---':
            continue
        # 跳过包含图片链接的行（避免连续图片互相污染）
        if re.match(r'!\[', line):
            continue

        # 标题行
        heading_m = re.match(r'^#{1,4}\s+(.+)$', line)
        if heading_m and not nearest_heading:
            nearest_heading = re.sub(r'\*+|`', '', heading_m.group(1)).strip()

        # 含中文的正文行
        if re.search(r'[\u4e00-\u9fff]', line) and not nearest_text:
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)   # 链接 → 文字
            text = re.sub(r'\*+|_{1,2}|`|#+\s*|<!--.*?-->', '', text).strip()
            if len(text) >= 4:
                nearest_text = text[:30]

        if nearest_text:
            break

    if nearest_text:
        # 如果文字本身就是描述性短语（含"图"、"流程"、"架构"等），直接用
        if re.search(r'图|流程|架构|示例|截图|说明|规范', nearest_text):
            return nearest_text
        return nearest_text + '示意图'

    if nearest_heading:
        return nearest_heading + '示意图'

    # 3. 从 URL 文件名兜底（过滤纯数字、screenshot 等噪音前缀）
    url_path = url.split('?')[0]
    filename = Path(url_path).stem           # e.g. "post_process_flow"
    # 去掉纯数字/时间戳/screenshot 前缀
    clean_name = re.sub(r'^(screenshot_?|img_?)?\d+[_-]?', '', filename).strip('_-')
    if clean_name and len(clean_name) >= 3 and not re.match(r'^\d+$', clean_name):
        readable = clean_name.replace('_', ' ').replace('-', ' ').strip()
        return readable

    return '图片'


# ── 主逻辑 ───────────────────────────────────────────────────────────────────

def run() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # ── 1. 创建 placeholder.svg ──────────────────────────────────────────────
    PLACEHOLDER_SVG.write_text(PLACEHOLDER_SVG_CONTENT, encoding='utf-8')
    print(f"创建占位图：{PLACEHOLDER_SVG.relative_to(ROOT)}")

    # ── 2. 扫描所有外部图片链接 ──────────────────────────────────────────────
    entries = []
    files_to_patch: dict[Path, list] = {}   # path → [(line_idx, match_obj, description), ...]

    for md_file in sorted(RAW_DOCS.rglob('*.md')):
        lines = md_file.read_text(encoding='utf-8').splitlines()
        patches = []
        for i, line in enumerate(lines):
            for m in BLOCKED_IMG_RE.finditer(line):
                alt = m.group(1)
                url = m.group(2)
                desc = infer_description(alt, url, lines, i)
                patches.append((i, m, desc))

                # 上下文：图片行前后各2行
                ctx_start = max(0, i - 2)
                ctx_end   = min(len(lines), i + 3)
                context   = '\n'.join(lines[ctx_start:ctx_end])

                entries.append({
                    "file": str(md_file.relative_to(ROOT)),
                    "line": i + 1,
                    "original_url": url,
                    "inferred_description": desc,
                    "context": context,
                    "placeholder": f"![待补充：{desc}](/_images/placeholder.svg)",
                })

        if patches:
            files_to_patch[md_file] = patches

    # ── 3. 写入 missing_images.json ──────────────────────────────────────────
    MISSING_JSON.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f"写入清单：{MISSING_JSON.relative_to(ROOT)}（{len(entries)} 条）\n")

    # ── 4. 替换 .md 文件中的图片链接 ─────────────────────────────────────────
    for md_file, patches in sorted(files_to_patch.items()):
        text = md_file.read_text(encoding='utf-8')

        # 对每处匹配做替换（用 comment + placeholder 两行代替原来的 ![]()）
        # 从后往前替换，避免行号偏移
        lines = text.splitlines(keepends=True)

        # 将每行的所有匹配收集好再替换
        for i, m, desc in reversed(patches):
            url   = m.group(2)
            old   = m.group(0)      # 整个 ![...](...) 匹配
            new   = (
                f'<!-- TODO: 需手动补充图片，原始 URL: {url} -->\n'
                f'![待补充：{desc}](/_images/placeholder.svg)'
            )
            # 替换当前行中的 old → new（一行可能有多个，用 count=1 避免重复）
            lines[i] = lines[i].replace(old, new, 1)

        new_text = ''.join(lines)
        md_file.write_text(new_text, encoding='utf-8')

        n = len(patches)
        rel = md_file.relative_to(ROOT)
        for _, m, desc in patches:
            print(f"  [{rel}]  → 「{desc}」")

    # ── 5. 汇总 ──────────────────────────────────────────────────────────────
    print(f"\n共处理 {len(entries)} 处图片占位，涉及 {len(files_to_patch)} 个文件")


if __name__ == '__main__':
    run()
