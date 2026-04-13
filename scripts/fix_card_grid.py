#!/usr/bin/env python3
"""
scripts/fix_card_grid.py

将 nav-cards 中所有描述 ≤ 30 字的短条目区域转为 card-grid 网格布局。
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"


def process_file(filepath: Path) -> tuple[int, int]:
    """返回 (转换的区域数, 卡片数)。"""
    text = filepath.read_text(encoding='utf-8')

    # Find all <div class="nav-cards"> ... </div> blocks
    pattern = re.compile(
        r'<div class="nav-cards">\s*\n(.*?)\n\s*</div>',
        re.DOTALL,
    )

    total_regions = 0
    total_cards = 0

    def replace_block(m):
        nonlocal total_regions, total_cards
        content = m.group(1).strip()
        lines = content.split('\n')

        # Parse list items: - **[title](url)** — desc  OR  - **[title](url)**
        items = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('<'):
                continue
            item_m = re.match(
                r'^-\s+\*\*\[([^\]]+)\]\(([^)]+)\)\*\*(?:\s*—\s*(.*))?$',
                line,
            )
            if item_m:
                title = item_m.group(1)
                url = item_m.group(2)
                desc = (item_m.group(3) or '').strip()
                items.append((title, url, desc))

        if len(items) < 3:
            return m.group(0)  # keep as-is

        # Check if ALL descriptions are short (≤ 30 chars) — card grid candidate
        descs = [desc for _, _, desc in items if desc]
        if not descs or all(len(d) <= 30 for d in descs):
            # Convert to card-grid
            total_regions += 1
            total_cards += len(items)
            parts = ['<div class="card-grid">']
            for title, url, desc in items:
                parts.append('<div class="card-grid-item">')
                parts.append(f'<a href="{url}"><strong>{title}</strong></a>')
                if desc:
                    parts.append(f'<p>{desc}</p>')
                parts.append('</div>')
            parts.append('</div>')
            return '\n'.join(parts)

        return m.group(0)  # long descriptions — keep as nav-cards list

    new_text = pattern.sub(replace_block, text)

    if new_text != text:
        filepath.write_text(new_text, encoding='utf-8')

    return total_regions, total_cards


def main():
    files = sorted(f for f in DOCS_DIR.rglob('*.md')
                   if 'node_modules' not in str(f) and '.vitepress' not in str(f))

    total_files = 0
    total_regions = 0
    total_cards = 0

    for f in files:
        regions, cards = process_file(f)
        if regions:
            total_files += 1
            total_regions += regions
            total_cards += cards
            print(f'  {f.relative_to(DOCS_DIR)}: {regions} 区域, {cards} 卡片')

    print(f'\n转换文件数：{total_files}')
    print(f'卡片网格区域：{total_regions}')
    print(f'卡片总数：{total_cards}')


if __name__ == '__main__':
    main()
