#!/usr/bin/env python3
"""
AIUI 文档清洗脚本
对 raw_docs/ 下所有 .md 文件执行：
1. 图片本地化（下载到 raw_docs/_images/，替换路径）
2. 去除 CMS 噪音（页脚、导航、视频错误提示）
3. 标题层级归一化（提升层级、去除数字编号前缀、去除 emoji）
4. 格式清理（压缩空行、去行尾空格、代码块语言推断）

用法：
    python3 scripts/clean.py [--dry-run]   # --dry-run 只打印，不写文件
"""

import argparse
import hashlib
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DOCS = ROOT / "raw_docs"
IMAGES_DIR = RAW_DOCS / "_images"

# ── 正则常量 ─────────────────────────────────────────────────────────────────

# 图片链接（含可能的 title 属性，如 "null"）
IMG_RE = re.compile(
    r'!\[([^\]]*)\]\('
    r'(https?://[^\)\s"]+)'          # URL（不含空格和引号）
    r'(?:\s+"[^"]*")?'               # 可选 title 属性
    r'\)'
)

# CMS 噪音行（匹配整行）
CMS_NOISE_RE = re.compile(
    r'^.*?('
    r'admin\s+\d{4}年\d+月'          # "admin 2026年2月9日" 风格的页脚
    r'|视频加载失败'
    r'|请检查链接'
    r'|\[上一篇\]'
    r'|\[下一篇\]'
    r'|上一篇[:：【\[]'
    r'|下一篇[:：【\[]'
    r').*$',
    re.IGNORECASE
)

# 标题行
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$')

# 数字编号前缀（匹配行首的 "1.1.1、" "2.3 " "1、" 等）
NUM_PREFIX_RE = re.compile(
    r'^'
    r'(?:'
    r'\d+(?:\.\d+)*\s*[、，．:：]\s*'   # 1、 1.1、 2.3.1：  等（含中文标点）
    r'|\d+(?:\.\d+)+\s+'               # 1.1  2.3.1  （多级，空格分隔）
    r'|\d+\.\s+'                       # 1.  （只有一级 + 点 + 空格）
    r')'
)

# emoji：涵盖主要表情符号区块
EMOJI_RE = re.compile(
    r'[\U0001F300-\U0001FFFF'
    r'\U00002600-\U000026FF'
    r'\U00002700-\U000027BF'
    r'\U0001F900-\U0001F9FF'
    r'\u200d\ufe0f]+'
)

# 代码块围栏
CODE_FENCE_OPEN_RE = re.compile(r'^(```|~~~)(\w*)$')
CODE_FENCE_CLOSE_RE = re.compile(r'^(```|~~~)\s*$')

# ── 语言推断 ─────────────────────────────────────────────────────────────────

def guess_lang(code: str) -> str:
    """从代码内容推断编程语言，返回语言标识符（可能为空字符串）。"""
    s = code.strip()
    if not s:
        return ''

    first = s.splitlines()[0].strip()

    # JSON：以 { 或 [ 开头，且含 "key": 模式
    if (s.startswith('{') or s.startswith('[')) and re.search(r'"[\w\-]+"[\s]*:', s):
        return 'json'

    # Java：关键字 / import / 注解
    if re.search(
        r'\b(public|private|protected)\s+\w'
        r'|import\s+\w+\.\w+'
        r'|@(Override|NonNull|Nullable|Test|Autowired)'
        r'|\bvoid\s+\w+\s*\('
        r'|\bString\s+\w+\s*[=;(]',
        s
    ):
        return 'java'

    # XML / HTML
    if re.match(r'\s*<[a-zA-Z?!]', s) and '>' in s:
        if re.search(r'<(manifest|application|uses-permission|activity|config|project)', s, re.IGNORECASE):
            return 'xml'
        if re.search(r'<(html|div|span|head|body|script|style|meta)', s, re.IGNORECASE):
            return 'html'
        return 'xml'

    # Shell / Bash
    if re.search(
        r'^(adb\s|apt\s|apt-get\s|npm\s|pip\s|pip3\s|gradle\s|make\s|cmake\s'
        r'|curl\s|wget\s|export\s|cd\s|ls\s|echo\s|mkdir\s|rm\s|cp\s|mv\s'
        r'|chmod\s|chown\s|sudo\s|tar\s|git\s|ssh\s|scp\s|\.\/)',
        s, re.MULTILINE
    ) or s.startswith('#!/bin/') or s.startswith('#!/usr/'):
        return 'bash'

    # Python
    if re.search(
        r'^(def |class |import |from .+ import |async def |if __name__)',
        s, re.MULTILINE
    ) or 'print(' in s:
        return 'python'

    # C / C++
    if re.search(r'#include|std::|::|->|nullptr|sizeof\(|typedef\s+struct', s):
        return 'cpp'

    # Gradle / Groovy
    if re.search(
        r'\bandroid\s*\{'
        r'|\bcompileSdkVersion\b'
        r'|\bimplementation\s+[\'"]com\.'
        r'|\bdependencies\s*\{'
        r'|\bapply\s+plugin:',
        s
    ):
        return 'groovy'

    # Objective-C
    if re.search(r'@interface|@implementation|@property|\[.*\s+\w+\]|\- \(', s):
        return 'objc'

    # Kotlin
    if re.search(r'\bfun\s+\w+\s*\(|val\s+\w+\s*=|var\s+\w+\s*:|object\s+\w+', s):
        return 'kotlin'

    # TypeScript / JavaScript
    if re.search(
        r'\bconst\s+\w+\s*=\s*(async\s+)?(\(|function|async)'
        r'|\bfunction\s+\w+\s*\('
        r'|\binterface\s+\w+\s*\{'
        r'|\btype\s+\w+\s*='
        r'|=>\s*\{',
        s
    ):
        return 'typescript' if 'interface ' in s or ': string' in s or ': number' in s else 'javascript'

    # JavaScript（较宽松匹配：回调函数、链式调用、var/let/const）
    if re.search(
        r'\bfunction\s*\('
        r'|\bvar\s+\w+\s*='
        r'|\blet\s+\w+\s*='
        r'|\.\w+\s*\(\s*function'
        r'|\bcallback\s*\('
        r'|\.then\s*\('
        r'|\.catch\s*\(',
        s
    ):
        return 'javascript'

    # Properties / ini 配置
    if re.match(r'^\[.+\]\s*$', first) or (
        re.match(r'^\w[\w.]+\s*=\s*\S', s) and '{' not in s
    ):
        return 'ini'

    # HTTP 请求行（如 "GET /api/... HTTP/1.1"）
    if re.match(r'^(GET|POST|PUT|DELETE|PATCH|HEAD)\s+\S+\s+HTTP', s):
        return 'http'

    # 纯 URL 或参数串
    if re.match(r'^(https?|ws[s]?)://', s) or re.match(r'^\w+=\w+&', s):
        return 'text'

    # 看起来是 Markdown/纯文本被误放入代码块
    if re.match(r'^[>#\*\-]', s) or re.search(r'[\u4e00-\u9fff]', first):
        return 'text'

    return ''


# ── 图片处理 ─────────────────────────────────────────────────────────────────

# 忽略 SSL 证书（站点使用自签名证书）
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

def download_image(url: str, dry_run: bool = False) -> str | None:
    """
    下载图片到 IMAGES_DIR，文件名为 URL 的 MD5 前12位 + 原扩展名。
    返回本地相对路径（相对于 raw_docs/），失败返回 None。
    """
    # 提取扩展名
    clean_url = url.split('?')[0]
    suffix = Path(clean_url).suffix.lower() or '.png'
    if len(suffix) > 6:   # 异常扩展名 fallback
        suffix = '.png'

    key = hashlib.md5(url.encode()).hexdigest()[:12]
    filename = f"{key}{suffix}"
    local_path = IMAGES_DIR / filename
    rel_path = f"_images/{filename}"

    if local_path.exists():
        return rel_path          # 已下载，直接复用

    if dry_run:
        return rel_path          # dry-run 不实际下载

    try:
        # 对 URL 中的非 ASCII 字符（如中文路径）做百分比编码
        parsed = urllib.parse.urlsplit(url)
        safe_path = urllib.parse.quote(parsed.path, safe='/:@!$&\'()*+,;=')
        encoded_url = urllib.parse.urlunsplit(parsed._replace(path=safe_path))

        req = urllib.request.Request(
            encoded_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; docs-crawler/1.0)"},
        )
        with urllib.request.urlopen(req, context=_SSL_CTX, timeout=20) as resp:
            data = resp.read()
        local_path.write_bytes(data)
        return rel_path
    except (urllib.error.URLError, OSError, UnicodeEncodeError) as e:
        print(f"    [image download failed] {url[:70]} → {e}")
        return None


# ── 各清洗步骤 ────────────────────────────────────────────────────────────────

def localize_images(text: str, dry_run: bool) -> tuple[str, int]:
    """替换文中所有远程图片 URL 为本地路径，返回 (新文本, 下载数)。"""
    downloaded = 0

    def replace(m: re.Match) -> str:
        nonlocal downloaded
        alt, url = m.group(1), m.group(2)
        local = download_image(url, dry_run)
        if local:
            downloaded += 1
            return f"![{alt}]({local})"
        return m.group(0)   # 下载失败保留原始

    new_text = IMG_RE.sub(replace, text)
    return new_text, downloaded


def remove_cms_noise(text: str) -> str:
    """删除 CMS 系统注入的噪音行（页脚、导航、视频提示等）。"""
    lines = text.splitlines()
    cleaned = [line for line in lines if not CMS_NOISE_RE.match(line)]
    return '\n'.join(cleaned)


def normalize_headings(text: str) -> tuple[str, int]:
    """
    1. 计算文档最浅标题层级；如果 > 2，整体上移至从 h2 开始。
    2. 去掉标题中的数字编号前缀（1.1.1、→ 去掉）。
    3. 去掉标题中的 emoji。
    返回 (新文本, 提升的层级数)。
    """
    lines = text.splitlines()

    # 收集所有标题层级（跳过代码块内容）
    in_code = False
    levels = []
    for line in lines:
        if CODE_FENCE_OPEN_RE.match(line) or CODE_FENCE_CLOSE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            levels.append(len(m.group(1)))

    # 计算需要提升的层数（目标最浅层级 = 2）
    promote = 0
    if levels:
        min_level = min(levels)
        if min_level > 2:
            promote = min_level - 2

    # 重写标题行
    new_lines = []
    in_code = False
    for line in lines:
        if CODE_FENCE_OPEN_RE.match(line) or CODE_FENCE_CLOSE_RE.match(line):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue

        m = HEADING_RE.match(line)
        if m:
            hashes, title = m.group(1), m.group(2)
            new_level = max(1, len(hashes) - promote)
            title = NUM_PREFIX_RE.sub('', title).strip()   # 去数字前缀
            title = EMOJI_RE.sub('', title).strip()        # 去 emoji
            new_lines.append(f"{'#' * new_level} {title}")
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), promote


def annotate_code_blocks(text: str) -> tuple[str, int]:
    """
    为无语言标注的代码块推断语言并补全标注。
    返回 (新文本, 补全数量)。
    """
    lines = text.splitlines()
    new_lines = []
    i = 0
    annotated = 0

    while i < len(lines):
        line = lines[i]
        m = CODE_FENCE_OPEN_RE.match(line)

        if m and not m.group(2):          # 无语言标注的开围栏
            fence_char = m.group(1)
            # 收集代码块内容（直到同类型关闭围栏）
            code_lines = []
            j = i + 1
            while j < len(lines):
                if lines[j].startswith(fence_char) and CODE_FENCE_CLOSE_RE.match(lines[j]):
                    break
                code_lines.append(lines[j])
                j += 1

            lang = guess_lang('\n'.join(code_lines))
            new_lines.append(f"{fence_char}{lang}")
            new_lines.extend(code_lines)
            # 写入关闭围栏
            if j < len(lines):
                new_lines.append(lines[j])
                i = j + 1
            else:
                i = j
            if lang:
                annotated += 1
        else:
            new_lines.append(line)
            i += 1

    return '\n'.join(new_lines), annotated


def clean_format(text: str) -> str:
    """压缩多余空行（>2 → 2），去行尾空格，确保文件末尾只有一个换行。"""
    # 去行尾空格
    lines = [line.rstrip() for line in text.splitlines()]
    text = '\n'.join(lines)
    # 压缩连续 3+ 个空行为 2 个
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def clean_frontmatter_title(text: str) -> str:
    """清理 frontmatter 中 title 字段的数字前缀和 emoji。"""
    def replace_title(m: re.Match) -> str:
        title = m.group(1)
        title = NUM_PREFIX_RE.sub('', title).strip()
        title = EMOJI_RE.sub('', title).strip()
        return f"title: {title}"

    return re.sub(r'^title:\s*(.+)$', replace_title, text, flags=re.MULTILINE)


# ── 主流程 ────────────────────────────────────────────────────────────────────

def clean_file(path: Path, dry_run: bool) -> dict:
    """清洗单个文件，返回统计信息字典。"""
    original = path.read_text(encoding='utf-8')
    text = original

    stats = {
        'file': str(path.relative_to(ROOT)),
        'images_downloaded': 0,
        'heading_promote': 0,
        'code_annotated': 0,
        'changed': False,
    }

    # 1. 图片本地化
    text, n_imgs = localize_images(text, dry_run)
    stats['images_downloaded'] = n_imgs

    # 2. CMS 噪音清理
    text = remove_cms_noise(text)

    # 3. 标题层级归一化
    text, promote = normalize_headings(text)
    stats['heading_promote'] = promote

    # 4. 代码块语言推断
    text, n_code = annotate_code_blocks(text)
    stats['code_annotated'] = n_code

    # 5. frontmatter title 清理
    text = clean_frontmatter_title(text)

    # 6. 格式清理（最后执行）
    text = clean_format(text)

    stats['changed'] = text != original

    if not dry_run and stats['changed']:
        path.write_text(text, encoding='utf-8')

    return stats


def run(dry_run: bool) -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(RAW_DOCS.rglob('*.md'))
    # 跳过 manifest
    md_files = [f for f in md_files if f.name != 'manifest.json']

    total_files = len(md_files)
    changed_files = 0
    total_imgs = 0
    total_code = 0
    promote_files = 0

    print(f"清洗 {total_files} 个文件（dry_run={dry_run}）\n")

    for i, path in enumerate(md_files, 1):
        stats = clean_file(path, dry_run)
        rel = stats['file']

        parts = []
        if stats['images_downloaded']:
            parts.append(f"img×{stats['images_downloaded']}")
        if stats['heading_promote']:
            parts.append(f"promote+{stats['heading_promote']}")
        if stats['code_annotated']:
            parts.append(f"code×{stats['code_annotated']}")
        if not stats['changed']:
            parts.append('no change')

        summary = '  '.join(parts) if parts else ''
        print(f"[{i:3d}/{total_files}] {rel}  {summary}")

        if stats['changed']:
            changed_files += 1
        total_imgs += stats['images_downloaded']
        total_code += stats['code_annotated']
        if stats['heading_promote']:
            promote_files += 1

    # 统计已下载图片文件数
    actual_imgs = len(list(IMAGES_DIR.glob('*')))

    print(f"\n{'='*55}")
    print(f"处理文件  : {total_files} 个（{changed_files} 个有变更）")
    print(f"下载图片  : {total_imgs} 次（_images/ 目录共 {actual_imgs} 个文件）")
    print(f"标题提升  : {promote_files} 篇文档")
    print(f"代码块标注: {total_code} 个")
    if dry_run:
        print("\n[DRY RUN] 未写入任何文件")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AIUI 文档清洗脚本")
    parser.add_argument('--dry-run', action='store_true', help='只打印统计，不写文件')
    args = parser.parse_args()
    run(dry_run=args.dry_run)
