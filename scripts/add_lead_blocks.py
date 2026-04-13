#!/usr/bin/env python3
"""
scripts/add_lead_blocks.py

为 docs/ 下 .md 文件的页面导语添加 VitePress ::: info 概述 容器。
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

# 导语前可能出现的纯文字小标题（非 # 标题）
INTRO_LABELS = {'背景介绍', '概述', '简介', '说明', '概要', '前言',
                '背景', '温馨提示', '智能体介绍'}
# 加上带"概述"后缀的标题（如 "星火大模型配置概述"）
INTRO_SUFFIX_RE = re.compile(r'^.{2,15}(?:概述|简介|说明|介绍)\s*$')


def collect_md_files() -> list[Path]:
    files = sorted(DOCS_DIR.rglob('*.md'))
    return [f for f in files
            if 'node_modules' not in str(f)
            and '.vitepress' not in str(f)]


def process_file(filepath: Path) -> tuple[bool, str]:
    """处理单个文件。返回 (是否修改, 文件描述)。"""
    text = filepath.read_text(encoding='utf-8')

    # 跳过首页（layout: home）
    if 'layout: home' in text[:200]:
        return False, ''

    # 跳过已有 ::: info 的文件
    if '::: info' in text:
        return False, ''

    # 分离 frontmatter
    m = FRONTMATTER_RE.match(text)
    if not m:
        return False, ''

    fm = m.group(0)
    body = text[m.end():]

    # 找到第一个 ## 标题的位置
    h2_match = re.search(r'^## ', body, re.MULTILINE)
    if not h2_match:
        return False, ''

    before_h2 = body[:h2_match.start()]

    # 提取导语：frontmatter 到第一个 ## 之间的内容
    # 跳过空白
    lead = before_h2.strip()
    if not lead:
        return False, ''

    # 跳过代码块
    if lead.startswith('```') or lead.startswith('~~~'):
        return False, ''

    # 跳过已有容器
    if lead.startswith(':::'):
        return False, ''

    # 跳过 ### 标题开头（卡片导航页）
    if lead.startswith('#'):
        return False, ''

    # 跳过 **目录** 或纯目录块
    if lead.startswith('**目录**') or lead == '目录':
        return False, ''

    # 分行处理：检测并移除纯文字小标题
    lines = lead.split('\n')
    first_line = lines[0].strip()

    # 检查第一行是否是导语标签
    label_removed = False
    if first_line in INTRO_LABELS or INTRO_SUFFIX_RE.match(first_line):
        lines = lines[1:]
        label_removed = True
        lead = '\n'.join(lines).strip()

    if not lead:
        return False, ''

    # 字数检查（去除 markdown 标记后）
    clean = re.sub(r'[*`\[\]()#\-_|>]', '', lead)
    clean = re.sub(r'\s+', '', clean)
    if len(clean) < 20:
        return False, ''

    # 构建 ::: info 容器
    container = f'::: info 概述\n{lead}\n:::'

    # 重组文件
    after_h2 = body[h2_match.start():]
    new_body = f'\n{container}\n\n{after_h2}'
    new_text = fm + new_body

    filepath.write_text(new_text, encoding='utf-8')
    rel = str(filepath.relative_to(DOCS_DIR))
    return True, rel


def main():
    files = collect_md_files()
    print(f"扫描 {len(files)} 个 .md 文件\n")

    modified = []
    for f in files:
        changed, rel = process_file(f)
        if changed:
            modified.append(rel)

    print(f"处理完成：{len(modified)} 个文件添加了导语容器\n")

    if modified:
        print("修改文件列表：")
        for m in modified:
            print(f"  {m}")

    print(f"\n总计：{len(files)} 扫描，{len(modified)} 修改")


if __name__ == '__main__':
    main()
