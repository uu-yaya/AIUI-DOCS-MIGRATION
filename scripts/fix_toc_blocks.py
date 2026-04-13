#!/usr/bin/env python3
"""
scripts/fix_toc_blocks.py

将 docs/ 中 **目录** / ## 目录 块转为带锚点链接的 ::: details 容器。
TOC 条目自动与页面内的 ## / ### 标题匹配生成锚点链接。
"""

import re
import unicodedata
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)


def slugify(text: str) -> str:
    """生成与 VitePress 一致的 heading anchor slug。"""
    # 去除 markdown 格式
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    # 去除前导编号 (1. / 1.1. / 1．等)
    s = re.sub(r'^[\d]+[\.．]\s*', '', s)
    s = re.sub(r'^[\d]+[\.．][\d]+[\.．]?\s*', '', s)
    s = s.strip()
    # VitePress slug 规则：小写，空格和特殊字符转 -
    s = s.lower()
    s = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s


def extract_headings(body: str) -> dict[str, str]:
    """从正文提取所有 ##/### 标题，返回 {slug: heading_text}。"""
    headings = {}
    for m in re.finditer(r'^(#{2,4})\s+(.+)$', body, re.MULTILINE):
        text = m.group(2).strip()
        slug = slugify(text)
        headings[slug] = text
        # 也存一个不含编号前缀的版本
        clean = re.sub(r'^[\d]+[\.．]\s*', '', text)
        clean = re.sub(r'^[\d]+[\.．][\d]+[\.．]?\s*', '', clean)
        if clean != text:
            headings[slugify(clean)] = text
    return headings


def toc_item_to_link(line: str, headings: dict[str, str], indent: int = 0) -> str:
    """将一个 TOC 条目转为 Markdown 锚点链接。"""
    # 提取文字（去掉编号）
    text = line.strip()
    # 去掉前导编号
    display = re.sub(r'^[\d]+[\.．]\s*', '', text)
    display = re.sub(r'^[\d]+[\.．][\d]+[\.．]?\s*', '', display)
    display = display.strip()
    if not display:
        return ''

    slug = slugify(text)
    display_slug = slugify(display)

    # 尝试匹配标题
    matched = slug in headings or display_slug in headings

    prefix = '  ' * indent
    if matched:
        return f'{prefix}- [{display}](#{display_slug})'
    else:
        # 没有匹配的标题，仍然生成链接（可能是子标题格式略有不同）
        return f'{prefix}- [{display}](#{display_slug})'


def process_toc_block(text: str) -> tuple[str, bool]:
    """查找并转换 **目录** 或 ## 目录 块。"""
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return text, False

    fm = fm_match.group(0)
    body = text[fm_match.end():]

    # 提取页面标题锚点
    headings = extract_headings(body)

    # 模式1: **目录** 后跟编号列表
    toc_pattern = re.compile(
        r'^(\*\*目录\*\*)\s*\n'
        r'((?:\s*\d+[\.．].*\n?)+)',
        re.MULTILINE,
    )

    # 模式2: ## 目录 / ## **目 录** 后跟编号列表
    toc_pattern2 = re.compile(
        r'^##\s+\*{0,2}目\s*录\*{0,2}\s*\n'
        r'((?:\s*\d+[\.．].*\n?)+)',
        re.MULTILINE,
    )

    found = False

    def replace_toc(m):
        nonlocal found
        found = True
        # 获取编号列表部分
        if m.lastindex and m.lastindex >= 2:
            items_text = m.group(2)
        else:
            items_text = m.group(1)

        lines = items_text.strip().split('\n')
        linked_items = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            # 判断缩进层级
            indent = 0
            if re.match(r'\s{2,}', line) or re.match(r'\d+\.\d+\.', stripped):
                indent = 1
            item = toc_item_to_link(stripped, headings, indent)
            if item:
                linked_items.append(item)

        if not linked_items:
            return m.group(0)

        toc_content = '\n'.join(linked_items)
        return f'::: details 目录\n{toc_content}\n:::\n'

    body = toc_pattern.sub(replace_toc, body)
    body = toc_pattern2.sub(replace_toc, body)

    if not found:
        return text, False

    return fm + body, True


def main():
    files = sorted(f for f in DOCS_DIR.rglob('*.md')
                   if 'node_modules' not in str(f) and '.vitepress' not in str(f))

    count = 0
    for f in files:
        text = f.read_text(encoding='utf-8')
        new_text, changed = process_toc_block(text)
        if changed:
            f.write_text(new_text, encoding='utf-8')
            count += 1
            print(f'  {f.relative_to(DOCS_DIR)}')

    print(f'\n共处理 {count} 个文件的目录块')


if __name__ == '__main__':
    main()
