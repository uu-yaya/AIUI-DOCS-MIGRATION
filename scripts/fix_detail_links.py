#!/usr/bin/env python3
"""
scripts/fix_detail_links.py

将 "### 标题 + 描述 + [查看详情](link)" 模式转为 "### [标题](link) + 描述"。
"""

import json
import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

# 匹配 [查看详情] 或 [阅读详情]（可能前有 emoji）
DETAIL_LINK_RE = re.compile(
    r'^(?:👉\s*)?\[(?:查看详情|阅读详情)\]\(([^)]+)\)\s*$'
)


def process_file(filepath: Path) -> tuple[int, int, list[tuple[int, str]]]:
    """返回 (模式A数, 模式B数, 孤立链接列表)。"""
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')
    new_lines = []
    count_a = 0  # 标题+描述+详情
    count_b = 0  # 标题+详情
    orphans = []

    i = 0
    while i < len(lines):
        line = lines[i]
        detail_m = DETAIL_LINK_RE.match(line.strip())

        if not detail_m:
            new_lines.append(line)
            i += 1
            continue

        # Found a [查看详情] / [阅读详情] line
        link = detail_m.group(1)

        # Look backwards for the heading and optional description
        # Skip trailing blank lines above
        j = len(new_lines) - 1
        while j >= 0 and new_lines[j].strip() == '':
            j -= 1

        if j < 0:
            orphans.append((i + 1, line.strip()))
            new_lines.append(line)
            i += 1
            continue

        # Check if line at j is a heading
        heading_m = re.match(r'^(#{2,4})\s+(.+)$', new_lines[j])

        if heading_m:
            # 模式 B：标题 + [详情]（无描述）
            hashes = heading_m.group(1)
            title = heading_m.group(2).strip()
            new_lines[j] = f'{hashes} [{title}]({link})'
            # Remove blank lines between heading and detail link
            while len(new_lines) > j + 1 and new_lines[-1].strip() == '':
                new_lines.pop()
            count_b += 1
            i += 1
            continue

        # Line at j is not a heading — check if it's description text
        # and the heading is further up
        desc_line = new_lines[j]
        # Go further up past this description line
        k = j - 1
        while k >= 0 and new_lines[k].strip() == '':
            k -= 1

        if k >= 0:
            heading_m2 = re.match(r'^(#{2,4})\s+(.+)$', new_lines[k])
            if heading_m2:
                # 模式 A：标题 + 描述 + [详情]
                hashes = heading_m2.group(1)
                title = heading_m2.group(2).strip()

                # Collect all description lines between heading and detail link
                desc_start = k + 1
                # Skip blank lines after heading
                while desc_start <= j and new_lines[desc_start].strip() == '':
                    desc_start += 1
                desc_lines = []
                for d in range(desc_start, j + 1):
                    if new_lines[d].strip():
                        desc_lines.append(new_lines[d])

                # Rebuild: heading with link, blank, description
                new_lines[k] = f'{hashes} [{title}]({link})'
                # Remove everything from k+1 to end of new_lines
                del new_lines[k + 1:]
                # Add blank + description
                if desc_lines:
                    new_lines.append('')
                    new_lines.extend(desc_lines)

                count_a += 1
                i += 1
                continue

        # No heading found above — orphan
        orphans.append((i + 1, line.strip()))
        new_lines.append(line)
        i += 1

    if count_a or count_b:
        filepath.write_text('\n'.join(new_lines), encoding='utf-8')

    return count_a, count_b, orphans


def main():
    files = sorted(f for f in DOCS_DIR.rglob('*.md')
                   if 'node_modules' not in str(f) and '.vitepress' not in str(f))

    total_a = 0
    total_b = 0
    all_orphans = []

    for f in files:
        a, b, orphans = process_file(f)
        total_a += a
        total_b += b
        rel = str(f.relative_to(DOCS_DIR))
        for line_no, text in orphans:
            all_orphans.append({'file': rel, 'line': line_no, 'text': text})

    print(f"扫描文件数：{len(files)}")
    print(f"模式 A（标题+描述+详情）替换：{total_a}")
    print(f"模式 B（标题+详情）替换：{total_b}")
    print(f"孤立链接数：{len(all_orphans)}")

    if all_orphans:
        print("\n孤立链接：")
        for o in all_orphans:
            print(f"  {o['file']}:{o['line']}: {o['text']}")
        orphan_path = ROOT / 'orphan_links.json'
        orphan_path.write_text(
            json.dumps(all_orphans, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )

    # Update validation_report.json
    report_path = ROOT / 'validation_report.json'
    report = {}
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding='utf-8'))
    report['detail_link_fixes'] = {
        'pattern_a': total_a,
        'pattern_b': total_b,
        'orphans': len(all_orphans),
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print("\n已更新 validation_report.json")


if __name__ == '__main__':
    main()
