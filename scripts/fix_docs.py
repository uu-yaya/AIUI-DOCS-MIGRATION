#!/usr/bin/env python3
"""
scripts/fix_docs.py

对 docs/ 目录下所有 .md 文件执行 12 项清洗修复。
每项修复完成后打印统计，最后生成 validation_report.json。

用法：
    python3 scripts/fix_docs.py
"""

import json
import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
CONFIG   = ROOT / "config"

# ── 工具函数 ──────────────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)
FENCE_RE = re.compile(
    r'(`{3,})[^\n]*\n.*?\n\1'
    r'|'
    r'(~{3,})[^\n]*\n.*?\n\2',
    re.DOTALL,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    """返回 (frontmatter含分隔线, body)。"""
    m = FRONTMATTER_RE.match(text)
    if m:
        return m.group(0), text[m.end():]
    return '', text


def protect_code_blocks(text: str):
    """返回 (segments, is_code) 交替列表，偶数索引为普通文本。"""
    parts = []
    last = 0
    for m in FENCE_RE.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts


def reassemble(segments):
    return ''.join(s for s, _ in segments)


# ── 收集文件 ──────────────────────────────────────────────────────────────────

def collect_md_files() -> list[Path]:
    files = sorted(DOCS_DIR.rglob('*.md'))
    # 排除 node_modules 等
    return [f for f in files if 'node_modules' not in str(f)]


# ── 修复 1：断裂的加粗标记 ─────────────────────────────────────────────────────

# Pattern: **- text  (bold opening wrapping a list-like item)
# or multiline ** ... ** wrapping list items
_BOLD_LIST_SINGLE_RE = re.compile(r'^\*\*-\s+(.+?)\*\*\s*$', re.MULTILINE)
_BOLD_LIST_OPEN_RE = re.compile(r'^\*\*-\s+(.+)$', re.MULTILINE)


def fix_broken_bold(text: str) -> tuple[str, int]:
    """修复 **- ... 和跨行 **...**  包裹列表项的情况。"""
    fm, body = split_frontmatter(text)
    count = 0

    # 保护代码块
    segs = protect_code_blocks(body)
    new_segs = []
    for seg, is_code in segs:
        if is_code:
            new_segs.append((seg, True))
            continue

        # Case 1: **- text** on single line → - **text**
        def repl_single(m):
            nonlocal count
            inner = m.group(1).rstrip('*').strip()
            # 如果 inner 以 ** 结尾（已经关闭的粗体），去掉
            count += 1
            return f'- **{inner}**'
        seg = _BOLD_LIST_SINGLE_RE.sub(repl_single, seg)

        # Case 2: **- text (no closing ** on same line)
        # Find pairs: **- line1\n...\n...**
        lines = seg.split('\n')
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check for **- pattern (opening bold wrapping list)
            m = re.match(r'^(\*\*)-\s+(.*)$', line)
            if m and not line.rstrip().endswith('**'):
                # Find closing **
                collected = [m.group(2)]
                j = i + 1
                found_close = False
                while j < len(lines):
                    l = lines[j]
                    if l.rstrip().endswith('**'):
                        collected.append(l.rstrip()[:-2].strip())
                        found_close = True
                        j += 1
                        break
                    collected.append(l)
                    j += 1
                if found_close:
                    count += 1
                    # Convert to list items
                    for c in collected:
                        c = c.strip()
                        if c.startswith('- '):
                            result.append(c)
                        elif c.startswith('-- '):
                            result.append(f'  - {c[3:]}')
                        elif c:
                            result.append(f'- {c}')
                    i = j
                    continue
            result.append(line)
            i += 1
        seg = '\n'.join(result)
        new_segs.append((seg, False))

    return fm + reassemble(new_segs), count


# ── 修复 2：缺少左方括号的链接 ─────────────────────────────────────────────────

# text](/path) 但没有 [ 在 text 前面
# 匹配：非 [ 字符后紧跟 ](path)
_MISSING_LBRACKET_RE = re.compile(
    r'(?<!\[)'             # 前面不是 [
    r'(?<!\!)'             # 前面不是 !（排除图片）
    r'([\u4e00-\u9fffA-Za-z0-9）\)].{0,60}?)'  # 链接文本（以中文/英文/数字开头）
    r'\]\((/[^)]+)\)'      # ](path)
)

# 更精准：只在行首或标点后匹配
_MISSING_LBRACKET_RE2 = re.compile(
    r'(?:^|(?<=\s)|(?<=。)|(?<=，)|(?<=：))([^\[\]\n]{2,60}?)\]\((/[^)]+)\)',
    re.MULTILINE,
)


def fix_missing_left_bracket(text: str) -> tuple[str, int]:
    fm, body = split_frontmatter(text)
    count = 0
    segs = protect_code_blocks(body)
    new_segs = []
    for seg, is_code in segs:
        if is_code:
            new_segs.append((seg, True))
            continue
        # Scan for ] followed by ( that doesn't have matching [
        lines = seg.split('\n')
        new_lines = []
        for line in lines:
            # Find all ]( in line, check if [ exists before each
            new_line = line
            # Find pattern: text](url) where text doesn't have [
            # Walk backwards from each ]( to find if there's a matching [
            positions = []
            idx = 0
            while True:
                pos = new_line.find('](', idx)
                if pos < 0:
                    break
                # Check backwards for [
                bracket_pos = new_line.rfind('[', idx, pos)
                img_bracket = new_line.rfind('![', idx, pos)
                if bracket_pos < 0 and pos > 0:
                    # No [ found - this is a broken link
                    # Find the closing )
                    close = new_line.find(')', pos + 2)
                    if close > 0:
                        url = new_line[pos+2:close]
                        if url.startswith('/') or url.startswith('http'):
                            # Find text start: go back from pos to find where text starts
                            # Use beginning of line or after whitespace/punctuation
                            text_start = pos
                            for k in range(pos - 1, -1, -1):
                                if new_line[k] in ' \t|':
                                    text_start = k + 1
                                    break
                                if k == 0:
                                    text_start = 0
                            link_text = new_line[text_start:pos]
                            if link_text and len(link_text) > 1:
                                # 【附件】... pattern
                                if '【' in link_text and not link_text.startswith('['):
                                    old = new_line[text_start:close+1]
                                    new = f'[{link_text}]({url})'
                                    new_line = new_line[:text_start] + new + new_line[close+1:]
                                    count += 1
                                    break  # re-scan after modification
                idx = pos + 1
            new_lines.append(new_line)
        seg = '\n'.join(new_lines)
        new_segs.append((seg, False))
    return fm + reassemble(new_segs), count


# ── 修复 3 & 4：纯文本 "目录" 块 & TOC 块 ─────────────────────────────────────

_TOC_BLOCK_RE = re.compile(
    r'^目录\s*\n',
    re.MULTILINE,
)


def fix_toc_blocks(text: str) -> tuple[str, int]:
    """删除 frontmatter 之后开头的纯文本"目录"行。"""
    fm, body = split_frontmatter(text)
    count = 0
    # 只在 body 开头匹配
    body_stripped = body.lstrip('\n')
    if body_stripped.startswith('目录\n') or body_stripped.startswith('目录\r\n'):
        body_stripped = re.sub(r'^目录\s*\n', '', body_stripped, count=1)
        count += 1
    if count:
        return fm + '\n' + body_stripped, count
    return text, 0


# ── 修复 5：列表项伪装成标题 ─────────────────────────────────────────────────────
# 暂时跳过——误判风险高，需要上下文分析


def fix_list_as_heading(text: str) -> tuple[str, int]:
    """暂不自动处理，返回 0。"""
    return text, 0


# ── 修复 6：多余空行和分隔线 ──────────────────────────────────────────────────

def fix_extra_whitespace(text: str) -> tuple[str, int, int]:
    """压缩多余空行、重复分隔线。返回 (text, 压缩空行数, 删除分隔线数)。"""
    fm, body = split_frontmatter(text)
    blank_count = 0
    hr_count = 0

    # 如果没匹配到 frontmatter，不要动（文件可能整体是 frontmatter，如首页）
    if not fm:
        return text, 0, 0

    # 删除 body 开头的 ---（frontmatter 后紧跟的分隔线）
    body2 = body.lstrip('\n')
    while body2.startswith('---\n') or body2.startswith('---\r\n'):
        body2 = re.sub(r'^---\s*\n', '', body2, count=1)
        hr_count += 1

    # 压缩 3+ 空行 → 2 空行
    new_body, n = re.subn(r'\n{3,}', '\n\n', body2)
    blank_count += n

    # 连续多条 --- → 只保留 1 条
    new_body, n2 = re.subn(r'(---\s*\n){2,}', '---\n', new_body)
    hr_count += n2

    # 文件末尾：去除多余空行，保留单个换行
    new_body = new_body.rstrip() + '\n'

    return fm + new_body, blank_count, hr_count


# ── 修复 7：图片路径双斜杠 ──────────────────────────────────────────────────────

_DOUBLE_SLASH_RE = re.compile(r'(/media/\d{6})//')
_IMG_NULL_TITLE_RE = re.compile(r'(\!\[[^\]]*\]\([^)]+)\s+"null"\)')


def fix_image_paths(text: str) -> tuple[str, int]:
    """修复 /media/YYYYMM//file → /media/YYYYMM/file，去掉 "null" title。"""
    count = 0

    def repl_dblslash(m):
        nonlocal count
        count += 1
        return m.group(1) + '/'
    text = _DOUBLE_SLASH_RE.sub(repl_dblslash, text)

    # 去掉图片的 "null" title 属性
    text = _IMG_NULL_TITLE_RE.sub(r'\1)', text)

    return text, count


# ── 修复 8：[### 标题塞进链接 ──────────────────────────────────────────────────
# 已由 build.py 的 expand_card_links() 完全处理，此处仅做验证扫描

_HEADING_IN_LINK_RE = re.compile(r'\[#{1,4}\s')


def fix_heading_in_links(text: str) -> tuple[str, int]:
    """扫描 [### heading](url) 模式。若仍存在则展开。"""
    fm, body = split_frontmatter(text)
    count = 0
    segs = protect_code_blocks(body)
    new_segs = []
    for seg, is_code in segs:
        if is_code:
            new_segs.append((seg, True))
            continue
        # 单行 [### Title](url)
        def repl_single(m):
            nonlocal count
            hashes = m.group(1)
            title = m.group(2).strip()
            url = m.group(3).strip()
            count += 1
            return f'{hashes} {title}\n\n[查看详情]({url})'
        seg = re.sub(
            r'\[(#{1,4})\s+([^\]\n]+)\]\(([^)]+)\)',
            repl_single,
            seg,
        )
        # 多行 [### Title\n\nDesc](url)
        def repl_multi(m):
            nonlocal count
            hashes = m.group(1)
            title = m.group(2).strip()
            desc = m.group(3).strip()
            url = m.group(4).strip()
            count += 1
            return f'{hashes} {title}\n\n{desc}\n\n[查看详情]({url})'
        seg = re.sub(
            r'\[(#{1,4})\s+([^\n\]]+)\n\n([^\]\[]+?)\]\(([^)]+)\)',
            repl_multi,
            seg,
            flags=re.DOTALL,
        )
        new_segs.append((seg, False))
    return fm + reassemble(new_segs), count


# ── 修复 9：补全不完整列表项 / 裸链接索引页转卡片导航 ──────────────────────────

# 匹配索引页中的裸链接行: [标题](url)  或 [标题](url "title attr")
_BARE_LINK_LINE_RE = re.compile(
    r'^\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)\s*$',
    re.MULTILINE,
)


def generate_empty_index_nav(filepath: Path, entries: list[dict]) -> tuple[str, int]:
    """为空的 section index 页面自动生成子页面卡片导航。"""
    text = filepath.read_text(encoding='utf-8')
    fm, body = split_frontmatter(text)
    if body.strip():
        return text, 0  # 非空页面不处理

    rel = str(filepath.relative_to(DOCS_DIR))
    # 当前目录的前缀
    dir_prefix = 'docs/' + str(filepath.parent.relative_to(DOCS_DIR)) + '/'

    # 找到该目录下的直接子页面
    children = []
    for e in entries:
        tp = e['target_path']
        if not tp.startswith(dir_prefix):
            continue
        # 排除自身
        if tp == 'docs/' + rel:
            continue
        # 只取直接子项（子目录的 index 或同级文件）
        remainder = tp[len(dir_prefix):]
        # 直接子文件（如 device-persona.md）
        if '/' not in remainder:
            children.append(e)
        # 子目录的 index（如 skill-studio/index.md）
        elif remainder.count('/') == 1 and remainder.endswith('/index.md'):
            children.append(e)

    if not children:
        return text, 0

    cards = []
    for e in children:
        vp_path = '/' + e['target_path'].removeprefix('docs/').removesuffix('.md')
        if vp_path.endswith('/index'):
            vp_path = vp_path.removesuffix('/index') + '/'
        cards.append(f'### {e["nav_title"]}\n\n[查看详情]({vp_path})')

    new_body = '\n\n'.join(cards) + '\n'
    return fm + new_body, len(cards)


def fix_bare_link_indexes(text: str, mapping_titles: dict[str, str]) -> tuple[str, int]:
    """将索引页中的裸链接列表转为 ### 标题 + [查看详情](url) 卡片导航。"""
    fm, body = split_frontmatter(text)
    count = 0

    matches = list(_BARE_LINK_LINE_RE.finditer(body))
    if not matches:
        return text, 0

    # 只处理连续裸链接行占主体的页面
    link_chars = sum(len(m.group(0)) for m in matches)
    body_stripped = body.strip()
    if not body_stripped or link_chars < len(body_stripped) * 0.5:
        return text, 0

    new_body = body
    # 从后往前替换，以免偏移
    for m in reversed(matches):
        title = m.group(1).strip()
        url = m.group(2).strip()
        # 尝试从 mapping 找描述
        desc = mapping_titles.get(title, '')
        card = f'### {title}\n\n{desc}\n\n[查看详情]({url})'
        new_body = new_body[:m.start()] + card + '\n' + new_body[m.end():]
        count += 1

    return fm + new_body, count

# ── 修复 10：清理 **-- 混合符号 ────────────────────────────────────────────────

_BOLD_DASHES_RE = re.compile(r'^\*\*--\s+(.+?)$', re.MULTILINE)
_JUST_DASHES_RE = re.compile(r'^--\s+', re.MULTILINE)


def fix_bold_dashes(text: str) -> tuple[str, int]:
    """修复 **-- text... 和 -- text 模式。"""
    fm, body = split_frontmatter(text)
    count = 0
    segs = protect_code_blocks(body)
    new_segs = []
    for seg, is_code in segs:
        if is_code:
            new_segs.append((seg, True))
            continue

        lines = seg.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # **-- text  (possibly with closing ** on later line)
            m = re.match(r'^\*\*--\s+(.+?)(\*\*)?$', line)
            if m:
                inner = m.group(1).strip()
                has_close = m.group(2) is not None
                if has_close:
                    # Self-closing: **-- text** → - text
                    inner = inner.rstrip('*').strip()
                new_lines.append(f'  - {inner}')
                count += 1
                i += 1
                continue

            # Indented -- text (sub-list style, often inside ** block)
            m2 = re.match(r'^(\s+)--\s+(.+?)(\*\*)?$', line)
            if m2:
                indent = m2.group(1)
                inner = m2.group(2).strip()
                has_close = m2.group(3) is not None
                if has_close:
                    inner = inner.rstrip('*').strip()
                new_lines.append(f'  - {inner}')
                count += 1
                i += 1
                continue

            # Standalone -- text at line start (not in code, not ---)
            m3 = re.match(r'^--\s+(.+?)(\*\*)?$', line)
            if m3 and not line.startswith('---'):
                inner = m3.group(1).strip()
                has_close = m3.group(2) is not None
                if has_close:
                    inner = inner.rstrip('*').strip()
                new_lines.append(f'  - {inner}')
                count += 1
                i += 1
                continue

            new_lines.append(line)
            i += 1

        seg = '\n'.join(new_lines)
        new_segs.append((seg, False))

    return fm + reassemble(new_segs), count


# ── 修复 11：标记空页面/内容极少的页面 ─────────────────────────────────────────

def check_incomplete_pages(files: list[Path]) -> list[dict]:
    """扫描正文少于 50 字的页面，在 frontmatter 添加 status: incomplete。"""
    incomplete = []
    for f in files:
        text = f.read_text(encoding='utf-8')
        fm, body = split_frontmatter(text)

        # 跳过 VitePress home 布局页面和带卡片导航的 section index 页
        if 'layout: home' in fm:
            continue
        rel = str(f.relative_to(DOCS_DIR))
        # 有 [查看详情] 链接的导航页视为导航枢纽，不标记
        if '[查看详情]' in body:
            continue

        # 去除标题行
        body_clean = re.sub(r'^#+\s.*$', '', body, flags=re.MULTILINE)
        # 去除图片、链接标记、空白
        body_clean = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body_clean)
        body_clean = re.sub(r'\[[^\]]*\]\([^)]*\)', '', body_clean)
        body_clean = re.sub(r'[#*\-_|`>\s]', '', body_clean)

        char_count = len(body_clean)
        if char_count < 50:
            incomplete.append({
                'file': rel,
                'char_count': char_count,
            })
            # 添加 status: incomplete 到 frontmatter
            if fm and 'status:' not in fm:
                if fm.endswith('---\n'):
                    new_fm = fm[:-4] + 'status: incomplete\n---\n'
                    f.write_text(new_fm + body, encoding='utf-8')
        else:
            # 移除之前可能错误添加的 status: incomplete
            if fm and 'status: incomplete' in fm:
                new_fm = fm.replace('status: incomplete\n', '')
                f.write_text(new_fm + body, encoding='utf-8')

    return incomplete


# ── 修复 12：移除无链接的纯文本 TOC ────────────────────────────────────────────
# (已在修复 3/4 中处理 "目录" 行)


# ── 主流程 ───────────────────────────────────────────────────────────────────

def main():
    files = collect_md_files()
    print(f"扫描到 {len(files)} 个 .md 文件\n")

    # 加载 mapping 用于修复 9
    mapping = json.loads((CONFIG / 'mapping.json').read_text(encoding='utf-8'))
    mapping_titles: dict[str, str] = {}
    for e in mapping['entries']:
        # nav_title → 简短描述（暂用空字符串，因为 mapping 中没有描述字段）
        mapping_titles[e['nav_title']] = ''
        mapping_titles[e['title']] = ''

    stats = {
        'fix1_broken_bold': {'files': 0, 'fixes': 0},
        'fix2_missing_bracket': {'files': 0, 'fixes': 0},
        'fix3_toc_blocks': {'files': 0, 'fixes': 0},
        'fix6_extra_whitespace': {'files': 0, 'blank_lines': 0, 'hr_removed': 0},
        'fix7_image_paths': {'files': 0, 'fixes': 0},
        'fix8_heading_in_link': {'files': 0, 'fixes': 0},
        'fix9_bare_link_index': {'files': 0, 'fixes': 0},
        'fix10_bold_dashes': {'files': 0, 'fixes': 0},
        'fix11_incomplete_pages': {'count': 0, 'pages': []},
    }

    for f in files:
        text = f.read_text(encoding='utf-8')
        original = text
        changed = False

        # 修复 10：**-- 混合符号（在修复 1 之前，因为修复 1 也处理 **- ）
        text, n10 = fix_bold_dashes(text)
        if n10:
            stats['fix10_bold_dashes']['files'] += 1
            stats['fix10_bold_dashes']['fixes'] += n10
            changed = True

        # 修复 1：断裂的加粗标记
        text, n1 = fix_broken_bold(text)
        if n1:
            stats['fix1_broken_bold']['files'] += 1
            stats['fix1_broken_bold']['fixes'] += n1
            changed = True

        # 修复 2：缺少左方括号
        text, n2 = fix_missing_left_bracket(text)
        if n2:
            stats['fix2_missing_bracket']['files'] += 1
            stats['fix2_missing_bracket']['fixes'] += n2
            changed = True

        # 修复 3/4/12：TOC 块
        text, n3 = fix_toc_blocks(text)
        if n3:
            stats['fix3_toc_blocks']['files'] += 1
            stats['fix3_toc_blocks']['fixes'] += n3
            changed = True

        # 修复 8：[### 标题塞进链接（验证+补漏）
        text, n8 = fix_heading_in_links(text)
        if n8:
            stats['fix8_heading_in_link']['files'] += 1
            stats['fix8_heading_in_link']['fixes'] += n8
            changed = True

        # 修复 9：裸链接索引页 → 卡片导航
        text, n9 = fix_bare_link_indexes(text, mapping_titles)
        if n9:
            stats['fix9_bare_link_index']['files'] += 1
            stats['fix9_bare_link_index']['fixes'] += n9
            changed = True

        # 修复 7：图片路径双斜杠
        text, n7 = fix_image_paths(text)
        if n7:
            stats['fix7_image_paths']['files'] += 1
            stats['fix7_image_paths']['fixes'] += n7
            changed = True

        # 修复 6：多余空行和分隔线（最后执行）
        text, nb, nh = fix_extra_whitespace(text)
        if nb or nh:
            stats['fix6_extra_whitespace']['files'] += 1
            stats['fix6_extra_whitespace']['blank_lines'] += nb
            stats['fix6_extra_whitespace']['hr_removed'] += nh
            changed = True

        if changed:
            f.write_text(text, encoding='utf-8')

    # 修复 9b：为空的 section index 页面自动生成导航
    entries = mapping['entries']
    for f in files:
        rel = str(f.relative_to(DOCS_DIR))
        if rel.endswith('/index.md') and rel != 'index.md':
            new_text, n9b = generate_empty_index_nav(f, entries)
            if n9b:
                f.write_text(new_text, encoding='utf-8')
                stats['fix9_bare_link_index']['files'] += 1
                stats['fix9_bare_link_index']['fixes'] += n9b

    # 修复 11：标记空页面
    # 重新读取修复后的文件
    files = collect_md_files()
    incomplete = check_incomplete_pages(files)
    stats['fix11_incomplete_pages']['count'] = len(incomplete)
    stats['fix11_incomplete_pages']['pages'] = incomplete

    # 输出 incomplete_pages.json
    incomplete_path = ROOT / 'incomplete_pages.json'
    incomplete_path.write_text(
        json.dumps(incomplete, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )

    # 打印统计
    print("=" * 60)
    print("修复统计")
    print("=" * 60)
    print(f"修复 1  断裂加粗标记：{stats['fix1_broken_bold']['files']} 文件，"
          f"{stats['fix1_broken_bold']['fixes']} 处")
    print(f"修复 2  缺少左方括号：{stats['fix2_missing_bracket']['files']} 文件，"
          f"{stats['fix2_missing_bracket']['fixes']} 处")
    print(f"修复 3  TOC 块移除 ：{stats['fix3_toc_blocks']['files']} 文件，"
          f"{stats['fix3_toc_blocks']['fixes']} 处")
    print(f"修复 6  多余空行/HR ：{stats['fix6_extra_whitespace']['files']} 文件，"
          f"空行 {stats['fix6_extra_whitespace']['blank_lines']}，"
          f"分隔线 {stats['fix6_extra_whitespace']['hr_removed']}")
    print(f"修复 7  图片双斜杠  ：{stats['fix7_image_paths']['files']} 文件，"
          f"{stats['fix7_image_paths']['fixes']} 处")
    print(f"修复 8  标题塞进链接：{stats['fix8_heading_in_link']['files']} 文件，"
          f"{stats['fix8_heading_in_link']['fixes']} 处")
    print(f"修复 9  裸链接→卡片：{stats['fix9_bare_link_index']['files']} 文件，"
          f"{stats['fix9_bare_link_index']['fixes']} 处")
    print(f"修复 10 **-- 混合  ：{stats['fix10_bold_dashes']['files']} 文件，"
          f"{stats['fix10_bold_dashes']['fixes']} 处")
    print(f"修复 11 不完整页面  ：{stats['fix11_incomplete_pages']['count']} 页")
    print()

    # 生成 validation_report.json
    report = {
        'total_files_scanned': len(files),
        'fixes': stats,
    }
    report_path = ROOT / 'validation_report.json'
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f"已生成 validation_report.json")
    print(f"已生成 incomplete_pages.json")


if __name__ == '__main__':
    main()
