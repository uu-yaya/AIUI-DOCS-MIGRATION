#!/usr/bin/env python3
"""
scripts/fix_all_tocs.py

扫描 docs/ 下所有 .md 文件，将所有目录块统一转为
::: details 目录 容器，条目带锚点链接。

处理以下情况：
1. 已经在 ::: info 概述 中的目录列表（误包装）
2. 已经在 ::: details 目录 中但需要更新的
3. 独立的 **目录** / ## 目录 块
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

# 判断一段文本是否为目录列表（编号条目为主）
def is_toc_content(text: str) -> bool:
    """检测文本是否主要由编号条目组成。"""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    if not lines:
        return False
    numbered = sum(1 for l in lines if re.match(r'^\d+[\.．]', l))
    return numbered >= 2 and numbered / len(lines) > 0.5


def slugify(text: str) -> str:
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'^[\d]+[\.．]\s*', '', s)
    s = re.sub(r'^[\d]+[\.．][\d]+[\.．]?\s*', '', s)
    s = s.strip()
    s = s.lower()
    s = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s


def extract_headings(body: str) -> set[str]:
    headings = set()
    for m in re.finditer(r'^#{2,4}\s+(.+)$', body, re.MULTILINE):
        text = m.group(1).strip()
        headings.add(slugify(text))
        clean = re.sub(r'^[\d]+[\.．]\s*', '', text)
        clean = re.sub(r'^[\d]+[\.．][\d]+[\.．]?\s*', '', clean)
        if clean != text:
            headings.add(slugify(clean))
    return headings


def toc_lines_to_linked(lines: list[str], headings: set[str]) -> list[str]:
    """将目录文本行转为带锚点链接的列表。"""
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过非目录行
        if stripped.startswith('-') and '[' in stripped:
            result.append(line)  # 已有链接格式
            continue

        # 提取显示文字（去掉编号）
        display = re.sub(r'^[\d]+[\.．][\d]*[\.．]?[\d]*[\.．]?\s*', '', stripped).strip()
        if not display:
            continue

        slug = slugify(stripped)
        display_slug = slugify(display)

        # 判断缩进级别
        indent = 0
        # 子编号如 2.1. / 3.1.1.
        if re.match(r'^\d+\.\d+', stripped):
            indent = 1
        if re.match(r'^\d+\.\d+\.\d+', stripped):
            indent = 2
        # 原始缩进
        leading = len(line) - len(line.lstrip())
        if leading >= 4 and indent == 0:
            indent = 1

        prefix = '  ' * indent
        result.append(f'{prefix}- [{display}](#{display_slug})')

    return result


def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding='utf-8')

    m = FRONTMATTER_RE.match(text)
    if not m:
        return False
    fm = m.group(0)
    body = text[m.end():]

    headings = extract_headings(body)
    changed = False

    # Case 1: ::: info 概述 容器中包含目录列表
    info_re = re.compile(
        r'::: info 概述\n(.*?)\n:::',
        re.DOTALL,
    )
    info_match = info_re.search(body)
    if info_match:
        content = info_match.group(1)
        if is_toc_content(content):
            # 纯目录 → 转为 details
            lines = content.strip().split('\n')
            linked = toc_lines_to_linked(lines, headings)
            if linked:
                new_block = '::: details 目录\n' + '\n'.join(linked) + '\n:::'
                body = body[:info_match.start()] + new_block + body[info_match.end():]
                changed = True

    # Case 2: ## 目 录 / ## **目 录** 独立块（还没处理的）
    toc_h2_re = re.compile(
        r'^##\s+\*{0,2}目\s*录\*{0,2}\s*\n'
        r'((?:[\s\S]*?\n))'
        r'(?=^## )',
        re.MULTILINE,
    )
    for m2 in reversed(list(toc_h2_re.finditer(body))):
        content = m2.group(1).strip()
        if is_toc_content(content):
            lines = content.split('\n')
            linked = toc_lines_to_linked(lines, headings)
            if linked:
                new_block = '::: details 目录\n' + '\n'.join(linked) + '\n:::\n\n'
                body = body[:m2.start()] + new_block + body[m2.end():]
                changed = True

    if changed:
        filepath.write_text(fm + body, encoding='utf-8')

    return changed


def main():
    files = sorted(f for f in DOCS_DIR.rglob('*.md')
                   if 'node_modules' not in str(f) and '.vitepress' not in str(f))

    count = 0
    for f in files:
        if process_file(f):
            count += 1
            print(f'  {f.relative_to(DOCS_DIR)}')

    print(f'\n共处理 {count} 个文件')


if __name__ == '__main__':
    main()
