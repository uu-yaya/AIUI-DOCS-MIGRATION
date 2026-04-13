#!/usr/bin/env python3
"""
scripts/build.py

读取 config/mapping.json，将 raw_docs/ 转换并输出到 docs/。

处理步骤（按顺序）：
  1. 更新 frontmatter（规范标题、去除 source_url）
  2. 删除 TOC 跳转链接块（>>>点击跳转）
  3. 展开卡片导航块（[### 标题\n\n描述](URL) → ### 标题 + 描述 + [查看详情](URL)）
  4. 重写内部文档链接（旧 URL → VitePress 路径）
  5. 术语替换（config/terminology.json，跳过代码块和 URL）
  6. 修正图片路径（/_images/ → /images/）
  7. 清理 【[...]】 双括号样式 → [...]
  8. 复制图片到 docs/public/images/
  9. 生成 docs/.vitepress/sidebar.js

用法：
    python3 scripts/build.py [--dry-run]
"""

import argparse
import json
import re
import shutil
import ssl
import urllib.request
from pathlib import Path

ROOT        = Path(__file__).parent.parent
CONFIG_DIR  = ROOT / "config"
RAW_DOCS    = ROOT / "raw_docs"
DOCS_DIR    = ROOT / "docs"
IMAGES_SRC  = RAW_DOCS / "_images"
IMAGES_DST  = DOCS_DIR / "public" / "images"
PUBLIC_DIR  = DOCS_DIR / "public"
VITEPRESS   = DOCS_DIR / ".vitepress"

ORIGIN_BASE = "https://aiui-doc.xf-yun.com"

# 匹配站内相对路径图片（含可选 title 属性）
MEDIA_IMG_RE = re.compile(r'!\[[^\]]*\]\((/media/\S+?)(?:\s|"|\))')

MAPPING_FILE     = CONFIG_DIR / "mapping.json"
TERMINOLOGY_FILE = CONFIG_DIR / "terminology.json"


# ── 正则常量 ─────────────────────────────────────────────────────────────────

# 匹配内部文档链接（带或不带标题属性，含 doc-NNN/ 后可能跟随多余子路径）
DOC_LINK_RE = re.compile(
    r'https?://aiui-doc\.xf-yun\.com/project-1/(doc-\d+)/[^\s)"]*',
)

# 匹配 TOC 跳转链接行（整行，允许行首缩进，链接文字内可含 ** 等标记）
TOC_LINE_RE = re.compile(r'^\s*\[.*?>>>点击跳转.*?\]\(#[^\)]*\)\s*$', re.MULTILINE)

# 匹配 【[text](url)】 样式
DOUBLE_BRACKET_RE = re.compile(r'【(\[[^\]]+\]\([^\)]+\))】')

# 图片路径修正：绝对路径 /_images/ 和相对路径 _images/ 统一转为 /images/
IMG_PATH_RE = re.compile(r'\(\.?/?_images/')

# 修正 ]([URL...) 形式的 markdown link（多余的 [ 在 URL 处）
_BRACKET_URL_RE = re.compile(r'\]\(\[([^)\[\]]+?)(?:\]\([^)]*\))?\s*(?:"[^"]*")?\)')

# 相对链接修正表：原始链接文本 → VitePress 路径
_REL_LINK_MAP: dict[str, str] = {
    'AIUIServiceKitSDK.md': '/hardware/legacy-evb/aiui-service-kit',
    './AIUIServiceKitSDK.md': '/hardware/legacy-evb/aiui-service-kit',
}

# 无对应目标页的相对链接：去除超链接，仅保留链接文字
_DEAD_REL_LINKS: list[re.Pattern] = [
    re.compile(r'\[([^\]]+)\]\(\./display_card(?:\.md)?\)'),
    re.compile(r'\[([^\]]+)\]\(display_card(?:\.md)?\)'),
]


# ── 术语替换（跳过代码块和 URL）──────────────────────────────────────────────

# 匹配需要保护的片段：围栏代码块 / 行内代码 / 链接 URL 部分
_PROTECT_RE = re.compile(
    r'(`{3,}[^\n]*\n.*?\n`{3,})'   # 围栏代码块（```...```）
    r'|(~{3,}[^\n]*\n.*?\n~{3,})'  # 围栏代码块（~~~...~~~）
    r'|(`[^`\n]+`)'                 # 行内代码
    r'|(\]\([^\)]*\))',             # 链接 URL 部分 ](...)
    re.DOTALL,
)


def apply_terminology(text: str, mappings: list[dict]) -> str:
    """
    对文本中的非代码、非 URL 部分应用术语替换。
    用正则分段：奇数索引为保护片段（不替换），偶数索引为普通文本。
    """
    parts = _PROTECT_RE.split(text)
    result = []
    for i, part in enumerate(parts):
        if part is None:
            continue
        # split() 奇数位置是捕获组匹配的片段（受保护）
        if i % 5 != 0:   # 4 个捕获组 → 每 5 个元素一组，位置 1-4 为保护
            result.append(part)
        else:
            for m in mappings:
                src = m["from"]
                dst = m["to"]
                if m.get("caseSensitive") is False:
                    part = re.sub(
                        r'(?<!\w)' + re.escape(src) + r'(?!\w)',
                        dst,
                        part,
                        flags=re.IGNORECASE,
                    )
                else:
                    part = part.replace(src, dst)
            result.append(part)
    return ''.join(result)


# ── Frontmatter 处理 ─────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def update_frontmatter(text: str, new_title: str) -> str:
    """替换 title 字段、去除 source_url，保留其他字段。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return f'---\ntitle: {new_title}\n---\n\n' + text

    fm_body = m.group(1)
    # 替换 title
    fm_body = re.sub(r'^title:.*$', f'title: {new_title}', fm_body, flags=re.MULTILINE)
    # 去除 source_url
    fm_body = re.sub(r'^source_url:.*\n?', '', fm_body, flags=re.MULTILINE)
    # 清理尾部空行
    fm_body = fm_body.strip()

    new_fm = f'---\n{fm_body}\n---\n'
    return new_fm + text[m.end():]


# ── 内部链接重写 ──────────────────────────────────────────────────────────────

def build_url_map(entries: list[dict]) -> dict[str, str]:
    """doc-XXX → VitePress 绝对路径（不含 .md 后缀）"""
    url_map = {}
    for e in entries:
        target = e["target_path"]           # e.g. docs/sdk-dev/basics/index.md
        # 去掉 docs/ 前缀和 .md 后缀
        vp_path = '/' + target.removeprefix('docs/').removesuffix('.md')
        # index.md → 目录路径
        if vp_path.endswith('/index'):
            vp_path = vp_path.removesuffix('/index') + '/'
        url_map[e["doc_id"]] = vp_path
    return url_map


def fix_malformed_bracket_links(text: str) -> str:
    """修正 ]([URL) 形式：原始 CMS 生成了多余的 [ 在 URL 处，提取实际 URL。"""
    return _BRACKET_URL_RE.sub(lambda m: f']({m.group(1)})', text)


def fix_relative_links(text: str) -> str:
    """将已知的相对链接（非 aiui-doc URL）替换为对应的 VitePress 路径；
    无目标页的链接降级为纯文字。"""
    for raw_href, vp_path in _REL_LINK_MAP.items():
        text = text.replace(f']({raw_href})', f']({vp_path})')
    for pat in _DEAD_REL_LINKS:
        text = pat.sub(r'\1', text)
    return text


def rewrite_doc_links(text: str, url_map: dict[str, str]) -> str:
    def replacer(m):
        doc_id  = m.group(1)
        vp_path = url_map.get(doc_id)
        if vp_path:
            return vp_path
        # 未知 doc_id：保留原 URL
        return m.group(0)

    return DOC_LINK_RE.sub(replacer, text)


# ── 各项清洗步骤 ──────────────────────────────────────────────────────────────

_CARD_LINK_RE = re.compile(
    r'\[###\s+[^\n]+\n+[^\[]*?>>>点击跳转\]\(#[^\)]*\)\n?',
    re.DOTALL,
)


def remove_toc_jumps(text: str) -> str:
    """
    删除两种 TOC 导航构件：
    1. 单行跳转链接：[..>>>点击跳转](#anchor)
    2. 多行卡片链接：[### 标题\n\n描述\n\n>>>点击跳转](#anchor)
    """
    text = TOC_LINE_RE.sub('', text)
    text = _CARD_LINK_RE.sub('', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


# 匹配卡片导航块：[### 标题\n\n描述文字](URL)
# 标题：到行尾；描述：到 ](，不跨越另一个 [
_CARD_NAV_RE = re.compile(
    r'\[###\s+([^\n\]]+)\n\n([^\]\[]+?)\]\(([^)]+)\)',
    re.DOTALL,
)


def expand_card_links(text: str) -> int:
    """
    将 [### 标题\\n\\n描述](URL) 展开为普通 Markdown：
        ### 标题

        描述

        [查看详情](URL)

    返回替换次数。
    """
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        heading = m.group(1).strip()
        desc    = m.group(2).strip()
        url     = m.group(3).strip()
        count  += 1
        return f'### {heading}\n\n{desc}\n\n[查看详情]({url})'

    return _CARD_NAV_RE.sub(replacer, text), count


# 相对路径图片（如 ./images/xxx.png），无法从服务器获取
_REL_IMG_RE = re.compile(
    r'(!\[[^\]]*\])\(\./images/([^\)\s"]+?)(?:\s+"[^"]*")?\)',
)


def fix_image_paths(text: str) -> str:
    # 1. /_images/ → /images/
    text = IMG_PATH_RE.sub('(/images/', text)
    # 2. ./images/xxx → placeholder（本地 SDK 包内图片，服务器不存在）
    text = _REL_IMG_RE.sub(
        r'\1(/images/placeholder.svg "原图：./images/\2")',
        text,
    )
    return text


def clean_double_brackets(text: str) -> str:
    """【[text](url)】 → [text](url)"""
    return DOUBLE_BRACKET_RE.sub(r'\1', text)


_FENCE_LINE_RE = re.compile(r'^(`{3,}|~{3,})(\S.*)?$')


def normalize_closing_fences(text: str) -> str:
    """
    修正 clean.py 误将关闭围栏标注了语言标签的问题。

    CommonMark 规范：关闭围栏不能含 info string（即不能是 ```lang）。
    当 clean.py 的 annotate_code_blocks 对一个关闭 ``` 追加了语言名称时，
    该行被 markdown-it 视为嵌套开启，导致代码块永不关闭，
    块后的 <Tag> 被 Vue 编译器当作 HTML 元素，引发构建报错。

    本函数在状态机中追踪围栏开闭状态：
    - 若在围栏内发现同类型/同长度且带 info string 的围栏行，
      视其为关闭围栏并去掉 info string。
    """
    lines = text.split('\n')
    result = []
    in_fence = False
    fence_char = ''
    fence_len = 0

    for line in lines:
        m = _FENCE_LINE_RE.match(line)
        if m:
            chars = m.group(1)
            c = chars[0]
            n = len(chars)
            info = (m.group(2) or '').strip()

            if not in_fence:
                # 开启围栏
                in_fence = True
                fence_char = c
                fence_len = n
                result.append(line)
            elif c == fence_char and n >= fence_len:
                # 关闭位置
                if info:
                    # info string 不合法 → 剥掉，只保留围栏字符
                    result.append(chars)
                else:
                    result.append(line)
                in_fence = False
            else:
                # 围栏内的其他内容
                result.append(line)
        else:
            result.append(line)

    return '\n'.join(result)


# ── 侧边栏生成 ───────────────────────────────────────────────────────────────

def build_sidebar(entries: list[dict], url_map: dict[str, str]) -> dict:
    """
    生成 VitePress sidebar 配置对象（Python dict，稍后序列化为 JS）。

    结构：
        {
          '/platform-service/': [ { text, items: [...] } ],
          ...
        }
    每个 entry 按 sidebar_group 分组；同一 section 内的多个 group 作为
    collapsed: false 的子项目组。
    """
    # section 前缀 → section 标题
    SECTION_META = {
        'platform-service': 'AIUI 平台服务',
        'app-config':       'AIUI 应用配置',
        'sdk-dev':          'AIUI SDK 开发',
        'api-dev':          'AIUI API 开发',
        'custom-biz':       '自定义业务',
        'hardware':         '硬件模组',
        'faq':              '常见问题',
        'legal':            '服务条款',
    }

    # 按 section 归组
    from collections import defaultdict, OrderedDict
    sections: dict[str, list] = defaultdict(list)

    # "联系方式"放在顶部导航栏，不出现在 FAQ 侧边栏
    # "法律条款"通过顶部导航 + index 页导航，不生成侧边栏
    SIDEBAR_EXCLUDE = {'/faq/contact'}
    SIDEBAR_SKIP_SECTIONS = {'legal'}

    for e in entries:
        vp_path = url_map[e["doc_id"]]
        if vp_path in SIDEBAR_EXCLUDE:
            continue
        # 推断 section（第一段路径）
        parts = vp_path.strip('/').split('/')
        section_key = parts[0]
        if section_key in SIDEBAR_SKIP_SECTIONS:
            continue
        sections[section_key].append({
            "text":    e["nav_title"],
            "link":    vp_path,
            "group":   e["sidebar_group"],
        })

    sidebar = {}
    for section_key, items in sections.items():
        prefix = f'/{section_key}/'

        # 按 group 再分组（保持第一次出现的顺序）
        groups: OrderedDict[str, list] = OrderedDict()
        for item in items:
            g = item["group"]
            if g not in groups:
                groups[g] = []
            groups[g].append({"text": item["text"], "link": item["link"]})

        section_title = SECTION_META.get(section_key, section_key)

        if len(groups) == 1:
            # 单 group：直接平铺
            only_group = list(groups.values())[0]
            sidebar[prefix] = [{"text": section_title, "items": only_group}]
        else:
            # 多 group：每个 group 一个 collapsed=false 子分组
            group_nodes = []
            for g_name, g_items in groups.items():
                group_nodes.append({
                    "text":      g_name,
                    "collapsed": False,
                    "items":     g_items,
                })
            sidebar[prefix] = group_nodes

    return sidebar


def sidebar_to_js(sidebar: dict) -> str:
    """将 sidebar dict 序列化为可读的 JS export。"""
    lines = ["// 自动生成，勿手动编辑（由 scripts/build.py 生成）",
             "export default {"]

    def render_items(items, indent):
        parts = []
        for item in items:
            if "items" in item:
                # group node
                inner = render_items(item["items"], indent + '  ')
                collapsed = str(item.get("collapsed", False)).lower()
                parts.append(
                    f'{indent}  {{\n'
                    f'{indent}    text: {json.dumps(item["text"], ensure_ascii=False)},\n'
                    f'{indent}    collapsed: {collapsed},\n'
                    f'{indent}    items: [\n{inner}\n{indent}    ],\n'
                    f'{indent}  }}'
                )
            else:
                parts.append(
                    f'{indent}  {{ text: {json.dumps(item["text"], ensure_ascii=False)}, '
                    f'link: {json.dumps(item["link"], ensure_ascii=False)} }}'
                )
        return ',\n'.join(parts)

    for prefix, groups in sidebar.items():
        lines.append(f'  {json.dumps(prefix, ensure_ascii=False)}: [')
        for group in groups:
            if "items" in group:
                inner = render_items(group["items"], '    ')
                collapsed_line = ''
                if "collapsed" in group:
                    collapsed_line = (
                        f'      collapsed: {str(group["collapsed"]).lower()},\n'
                    )
                lines.append(
                    f'    {{\n'
                    f'      text: {json.dumps(group["text"], ensure_ascii=False)},\n'
                    f'{collapsed_line}'
                    f'      items: [\n{inner}\n'
                    f'      ],\n'
                    f'    }},'
                )
            else:
                lines.append(
                    f'    {{ text: {json.dumps(group["text"], ensure_ascii=False)}, '
                    f'link: {json.dumps(group["link"], ensure_ascii=False)} }},'
                )
        lines.append('  ],')

    lines.append('}')
    return '\n'.join(lines) + '\n'


# ── 主流程 ───────────────────────────────────────────────────────────────────

def run(dry_run: bool) -> None:
    # 读取配置
    mapping     = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
    terminology = json.loads(TERMINOLOGY_FILE.read_text(encoding='utf-8'))
    entries     = mapping["entries"]
    term_maps   = terminology["mappings"]

    url_map = build_url_map(entries)

    # ── 1a. 复制 raw_docs/_images/ → docs/public/images/ ─────────────────────
    if not dry_run:
        IMAGES_DST.mkdir(parents=True, exist_ok=True)
    img_copied = 0
    for src_img in IMAGES_SRC.iterdir():
        if src_img.is_file():
            dst_img = IMAGES_DST / src_img.name
            if not dry_run and not dst_img.exists():
                shutil.copy2(src_img, dst_img)
                img_copied += 1
    print(f"图片（本地）：{'[dry]' if dry_run else ''}复制 {img_copied} 张到 docs/public/images/")

    # ── 1b. 下载站内 /media/... 图片 → docs/public/media/ ────────────────────
    # 先收集所有文档中的 /media/ 路径（在 raw_docs 阶段扫描，目标路径还未写入）
    media_paths: set[str] = set()
    for entry in entries:
        raw_path = ROOT / entry["raw_path"]
        if raw_path.exists():
            for m in MEDIA_IMG_RE.finditer(raw_path.read_text(encoding='utf-8')):
                media_paths.add(m.group(1).rstrip('"'))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {"User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )}
    media_ok = media_skip = media_fail = 0
    for path in sorted(media_paths):
        dst = PUBLIC_DIR / path.lstrip("/")
        if dst.exists():
            media_skip += 1
            continue
        if dry_run:
            print(f"  [dry] 待下载 {path}")
            media_ok += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        url = ORIGIN_BASE + path
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                dst.write_bytes(resp.read())
            media_ok += 1
        except Exception as e:
            print(f"  [media FAIL] {path}  ({e})")
            media_fail += 1
    label = '[dry]' if dry_run else ''
    print(f"图片（/media/）：{label}下载 {media_ok}，跳过 {media_skip}，失败 {media_fail}")

    # ── 2. 转换每篇文档 ───────────────────────────────────────────────────────
    ok = 0
    for entry in entries:
        raw_path    = ROOT / entry["raw_path"]
        target_path = ROOT / entry["target_path"]
        title       = entry["title"]

        if not raw_path.exists():
            print(f"  [SKIP] {entry['doc_id']}: raw 文件不存在")
            continue

        text = raw_path.read_text(encoding='utf-8')

        # 按顺序应用变换
        text = update_frontmatter(text, title)
        text = remove_toc_jumps(text)
        text, _n = expand_card_links(text)   # [### 标题\n\n描述](URL) → 展开
        text = rewrite_doc_links(text, url_map)
        text = fix_malformed_bracket_links(text)
        text = fix_relative_links(text)
        text = apply_terminology(text, term_maps)
        text = fix_image_paths(text)
        text = clean_double_brackets(text)
        text = normalize_closing_fences(text)  # 修正误标语言标签的关闭围栏
        # 最终折叠多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        if not text.endswith('\n'):
            text += '\n'

        if not dry_run:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(text, encoding='utf-8')
        ok += 1

    print(f"文档：{'[dry]' if dry_run else ''}转换 {ok} 篇 → docs/")

    # ── 3. 生成侧边栏配置 ──────────────────────────────────────────────────────
    sidebar     = build_sidebar(entries, url_map)
    sidebar_js  = sidebar_to_js(sidebar)

    if not dry_run:
        VITEPRESS.mkdir(parents=True, exist_ok=True)
        sidebar_file = VITEPRESS / "sidebar.js"
        sidebar_file.write_text(sidebar_js, encoding='utf-8')
        print(f"侧边栏：生成 docs/.vitepress/sidebar.js")
    else:
        # dry-run 时只打印前 40 行预览
        preview = '\n'.join(sidebar_js.splitlines()[:40])
        print(f"\n[dry] sidebar.js 预览：\n{preview}\n...")

    print(f"\n完成：{ok} 篇文档{'（dry-run，未写入）' if dry_run else '已写入 docs/'}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='构建 VitePress 文档目录')
    parser.add_argument('--dry-run', action='store_true', help='只打印，不写入文件')
    args = parser.parse_args()
    run(dry_run=args.dry_run)
