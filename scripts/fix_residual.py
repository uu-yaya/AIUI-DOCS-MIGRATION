#!/usr/bin/env python3
"""
scripts/fix_residual.py

修复 docs/ 下 4 类残留问题：
  A. 断裂的 Markdown 链接（缺少左方括号 [）
  B. 残留特殊装饰符号行（▼ ♦ ♫ ✪ ✧ ✦ ⚠ ♠ 等）
  C. 图片 "null" title 属性
  D. h1 标题（# xxx）→ h2（## xxx），CLAUDE.md 规定正文从 h2 开始
"""

import json
import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)
FENCE_RE = re.compile(
    r'(`{3,})[^\n]*\n.*?\n\1'
    r'|'
    r'(~{3,})[^\n]*\n.*?\n\2',
    re.DOTALL,
)


def collect_md_files() -> list[Path]:
    return sorted(f for f in DOCS_DIR.rglob('*.md') if 'node_modules' not in str(f))


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FRONTMATTER_RE.match(text)
    if m:
        return m.group(0), text[m.end():]
    return '', text


def get_code_ranges(text: str) -> list[tuple[int, int]]:
    """返回所有代码块的 (start, end) 范围。"""
    ranges = []
    for m in FENCE_RE.finditer(text):
        ranges.append((m.start(), m.end()))
    # 也保护行内代码
    for m in re.finditer(r'`[^`\n]+`', text):
        ranges.append((m.start(), m.end()))
    return ranges


def in_code(pos: int, ranges: list[tuple[int, int]]) -> bool:
    for s, e in ranges:
        if s <= pos < e:
            return True
    return False


# ═══════════════════════════════════════════════════════════════════════════
# 修复 A：断裂的 Markdown 链接（缺少 [）
# ═══════════════════════════════════════════════════════════════════════════

# 匹配：中文/英文文字紧接 ](url)，前面没有 [
_BROKEN_LINK_RE = re.compile(
    r'(?<!\[)'                                    # 前面不是 [
    r'(?<!\!)'                                    # 前面不是 !
    r'([\u4e00-\u9fffA-Za-z]'                     # 以中文或字母开头
    r'[\u4e00-\u9fffA-Za-z0-9_、，。：（）\-\s]*?' # 链接文字
    r')'
    r'\]\((/[^)\s]+)\)'                           # ](/path)
)


def fix_broken_links(text: str) -> tuple[str, int, list[str]]:
    fm, body = split_frontmatter(text)
    count = 0
    details = []

    # Pattern 1: ## Heading\n\nDescription](/url) — broken card links missing [
    _BROKEN_CARD_RE = re.compile(
        r'^(#{2,4})\s+([^\n]+)\n\n([^\n\[]+?)\]\((/[^)]+)\)',
        re.MULTILINE,
    )
    def repl_card(m):
        nonlocal count
        hashes = m.group(1)
        heading = m.group(2).strip()
        desc = m.group(3).strip()
        url = m.group(4)
        count += 1
        details.append(f"  {heading} + {desc}]({url}) → card nav")
        return f'### {heading}\n\n{desc}\n\n[查看详情]({url})'
    body = _BROKEN_CARD_RE.sub(repl_card, body)

    # Pattern 2: inline text](/url) missing [
    code_ranges = get_code_ranges(body)
    matches = list(_BROKEN_LINK_RE.finditer(body))
    new_body = body
    for m in reversed(matches):
        if in_code(m.start(), code_ranges):
            continue
        link_text = m.group(1).strip()
        url = m.group(2)

        before = new_body[:m.start()]
        line_start = before.rfind('\n') + 1
        line_prefix = before[line_start:]

        last_open = line_prefix.rfind('[')
        if last_open >= 0:
            between = line_prefix[last_open + 1:]
            if ']' not in between:
                continue

        if '|' in line_prefix and line_prefix.count('[') > 0:
            continue

        old = new_body[m.start():m.end()]
        new = f'[{link_text}]({url})'
        new_body = new_body[:m.start()] + new + new_body[m.end():]
        count += 1
        details.append(f"  {link_text}]({url}) → [{link_text}]({url})")

    return fm + new_body, count, details


# ═══════════════════════════════════════════════════════════════════════════
# 修复 B：残留特殊装饰符号
# ═══════════════════════════════════════════════════════════════════════════

_DECO_LINE_RE = re.compile(
    r'^\s*\[?[△▽▲▼♠♣♤♧☆★※⚠⚡✦✧◆◇●○♦♫✪⚙🛠🔊]\]?\s*$'
)


def fix_decorative_symbols(text: str) -> tuple[str, int]:
    fm, body = split_frontmatter(text)
    lines = body.split('\n')
    new_lines = []
    count = 0
    for line in lines:
        if _DECO_LINE_RE.match(line):
            count += 1
            continue  # 删除该行
        # 行内的独立符号：行首的装饰符号后跟换行或空格
        cleaned = re.sub(r'^[△▽▲▼♠♣♤♧☆★※⚠⚡✦✧◆◇●○♦♫✪⚙🛠🔊]\s*', '', line)
        if cleaned != line:
            count += 1
            line = cleaned
        new_lines.append(line)
    return fm + '\n'.join(new_lines), count


# ═══════════════════════════════════════════════════════════════════════════
# 修复 C：图片 "null" title 属性
# ═══════════════════════════════════════════════════════════════════════════

_NULL_TITLE_RE = re.compile(r'(\!\[[^\]]*\]\([^")\s]+)\s+"null"\)')


def fix_null_titles(text: str) -> tuple[str, int]:
    count = 0
    def repl(m):
        nonlocal count
        count += 1
        return m.group(1) + ')'
    text = _NULL_TITLE_RE.sub(repl, text)
    return text, count


# ═══════════════════════════════════════════════════════════════════════════
# 修复 D：h1 标题 → h2（正文不应出现 h1）
# ═══════════════════════════════════════════════════════════════════════════

def fix_h1_to_h2(text: str) -> tuple[str, int]:
    fm, body = split_frontmatter(text)
    lines = body.split('\n')
    count = 0
    new_lines = []

    # 用行级状态跟踪围栏代码块
    in_fence = False
    fence_char = ''
    fence_len = 0

    for line in lines:
        # 检测围栏开关
        fence_m = re.match(r'^(`{3,}|~{3,})', line)
        if fence_m:
            chars = fence_m.group(1)
            c = chars[0]
            n = len(chars)
            if not in_fence:
                in_fence = True
                fence_char = c
                fence_len = n
            elif c == fence_char and n >= fence_len:
                in_fence = False

        if in_fence:
            new_lines.append(line)
            continue

        m = re.match(r'^# (.+)$', line)
        if m:
            heading = m.group(1)
            clean_heading = heading.strip().strip('*').strip()
            if clean_heading in ('目录', '目 录'):
                count += 1
                continue  # 删除目录行
            new_lines.append(f'## {heading}')
            count += 1
        else:
            new_lines.append(line)

    return fm + '\n'.join(new_lines), count


# ═══════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════

def main():
    files = collect_md_files()
    print(f"扫描 {len(files)} 个 .md 文件\n")

    stats = {
        'A_broken_links': {'files': 0, 'fixes': 0},
        'B_decorative_symbols': {'files': 0, 'fixes': 0},
        'C_null_titles': {'files': 0, 'fixes': 0},
        'D_h1_to_h2': {'files': 0, 'fixes': 0},
    }

    all_link_details = []

    for f in files:
        text = f.read_text(encoding='utf-8')
        changed = False

        # A: 断裂链接
        text, nA, details = fix_broken_links(text)
        if nA:
            stats['A_broken_links']['files'] += 1
            stats['A_broken_links']['fixes'] += nA
            all_link_details.extend(
                [f"  {f.relative_to(DOCS_DIR)}: {d}" for d in details]
            )
            changed = True

        # B: 装饰符号
        text, nB = fix_decorative_symbols(text)
        if nB:
            stats['B_decorative_symbols']['files'] += 1
            stats['B_decorative_symbols']['fixes'] += nB
            changed = True

        # C: null title
        text, nC = fix_null_titles(text)
        if nC:
            stats['C_null_titles']['files'] += 1
            stats['C_null_titles']['fixes'] += nC
            changed = True

        # D: h1 → h2
        text, nD = fix_h1_to_h2(text)
        if nD:
            stats['D_h1_to_h2']['files'] += 1
            stats['D_h1_to_h2']['fixes'] += nD
            changed = True

        if changed:
            f.write_text(text, encoding='utf-8')

    # 打印统计
    print("=" * 60)
    print("修复统计")
    print("=" * 60)
    print(f"A  断裂链接（补 [）：{stats['A_broken_links']['files']} 文件，"
          f"{stats['A_broken_links']['fixes']} 处")
    if all_link_details:
        for d in all_link_details:
            print(d)
    print(f"B  装饰符号删除  ：{stats['B_decorative_symbols']['files']} 文件，"
          f"{stats['B_decorative_symbols']['fixes']} 处")
    print(f"C  图片 null title：{stats['C_null_titles']['files']} 文件，"
          f"{stats['C_null_titles']['fixes']} 处")
    print(f"D  h1 → h2 降级 ：{stats['D_h1_to_h2']['files']} 文件，"
          f"{stats['D_h1_to_h2']['fixes']} 处")
    print()

    # 更新 validation_report.json
    report_path = ROOT / 'validation_report.json'
    report = {}
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding='utf-8'))
    report['residual_fixes'] = stats
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print("已更新 validation_report.json")


if __name__ == '__main__':
    main()
