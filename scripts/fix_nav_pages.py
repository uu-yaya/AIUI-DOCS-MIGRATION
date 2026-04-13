#!/usr/bin/env python3
"""
scripts/fix_nav_pages.py

1. 删除残留 emoji 行
2. 将 ### [title](link) + desc 格式转为紧凑列表 + nav-cards 容器
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

# 宽泛的 emoji / 装饰符号行
EMOJI_LINE_RE = re.compile(
    r'^\s*[\U0001F300-\U0001FAFF\u2600-\u27BF\u2700-\u27BF'
    r'♨♩♪♫♬♭♮♯✦✧✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋'
    r'▼▽△▲◆◇●○♦♠♣♤♧☆★※⚠⚡◉⬟⬡⬢♻⚙⛓✓☼]+\s*$'
)


def clean_emoji_lines(text: str) -> tuple[str, int]:
    """删除 frontmatter 后的孤立 emoji 行。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, 0
    fm = m.group(0)
    body = text[m.end():]
    lines = body.split('\n')
    new_lines = []
    count = 0
    for line in lines:
        if EMOJI_LINE_RE.match(line):
            count += 1
            continue
        new_lines.append(line)
    if count:
        return fm + '\n'.join(new_lines), count
    return text, 0


def convert_nav_links(text: str) -> tuple[str, bool]:
    """将 ### [title](link) + desc 转为 - **[title](link)** — desc 列表。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, False

    fm = m.group(0)
    body = text[m.end():]

    # Count ### [title](link) patterns
    nav_links = re.findall(r'^###\s+\[.+\]\(.+\)', body, re.MULTILINE)
    if len(nav_links) < 3:
        return text, False

    lines = body.split('\n')
    new_lines = []
    i = 0
    in_nav_section = False
    nav_items = []

    def flush_nav():
        nonlocal nav_items
        if nav_items:
            new_lines.append('<div class="nav-cards">')
            new_lines.append('')
            for item in nav_items:
                new_lines.append(item)
            new_lines.append('')
            new_lines.append('</div>')
            nav_items = []

    while i < len(lines):
        line = lines[i]

        # Check for ### [title](link) pattern
        nav_m = re.match(r'^###\s+(\[.+\]\(.+\))\s*$', line)
        if nav_m:
            link_part = nav_m.group(1)
            in_nav_section = True

            # Look ahead for description (next non-empty line that's not another ### or ##)
            desc = ''
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                # Is it a description? (not a heading, not a link pattern, not a div)
                if (next_line
                    and not next_line.startswith('#')
                    and not next_line.startswith('[')
                    and not next_line.startswith('<')
                    and not next_line.startswith('---')
                    and not next_line.startswith(':::')
                    and not re.match(r'^-\s+\*\*\[', next_line)):
                    desc = next_line
                    i = j + 1  # skip desc line
                else:
                    i += 1
            else:
                i += 1

            if desc:
                nav_items.append(f'- **{link_part}** — {desc}')
            else:
                nav_items.append(f'- **{link_part}**')
            continue

        # Check for ## heading (section divider) — flush and keep
        if re.match(r'^##\s+', line) and not re.match(r'^###', line):
            flush_nav()
            in_nav_section = False
            new_lines.append(line)
            i += 1
            continue

        # Non-nav line
        if in_nav_section and line.strip() == '':
            i += 1
            continue  # skip blank lines between nav items

        flush_nav()
        in_nav_section = False
        new_lines.append(line)
        i += 1

    flush_nav()

    return fm + '\n'.join(new_lines), True


def main():
    files = sorted(f for f in DOCS_DIR.rglob('*.md')
                   if 'node_modules' not in str(f) and '.vitepress' not in str(f))

    emoji_count = 0
    nav_count = 0

    for f in files:
        text = f.read_text(encoding='utf-8')
        changed = False

        # Step 1: clean emoji
        text, n_emoji = clean_emoji_lines(text)
        if n_emoji:
            emoji_count += 1
            changed = True

        # Step 2: convert nav links
        text, converted = convert_nav_links(text)
        if converted:
            nav_count += 1
            changed = True
            print(f'  nav: {f.relative_to(DOCS_DIR)}')

        if changed:
            f.write_text(text, encoding='utf-8')

    print(f'\n清理 emoji 行：{emoji_count} 个文件')
    print(f'转换导航链接：{nav_count} 个文件')


if __name__ == '__main__':
    main()
