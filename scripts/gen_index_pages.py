#!/usr/bin/env python3
"""
scripts/gen_index_pages.py

为 7 个空的 section index 页面生成分类导航内容。
从子文档的 frontmatter title 和正文前 80 字提取描述。
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

# ── 目录配置 ──────────────────────────────────────────────────────────────────

INDEX_CONFIG = {
    "custom-biz": {
        "title": "自定义业务",
        "description": "AIUI 平台自定义业务开发指南",
        "intro": (
            "自定义业务模块提供技能工作室、问答库和设备人设等能力，"
            "帮助开发者快速构建领域专属的语音交互体验。"
            "通过技能工作室可以创建自定义技能、配置意图与实体，"
            "问答库则支持语句问答、关键词问答和文档问答等多种形式。"
        ),
    },
    "custom-biz/protocols": {
        "title": "协议规范",
        "description": "AIUI 技能交互协议与后处理接口规范",
        "intro": (
            "本节汇总了 AIUI 技能工作室涉及的各类协议规范，"
            "包括语义协议字段定义、技能后处理请求与响应格式、"
            "请求校验机制及资源限制说明，"
            "是技能后处理开发的核心参考文档。"
        ),
    },
    "custom-biz/qa-library": {
        "title": "问答库",
        "description": "AIUI 问答库开发指南",
        "intro": (
            "问答库是技能工作室提供的轻量级问答配置能力，"
            "支持语句问答、关键词问答和文档问答三种模式。"
            "开发者无需编写代码，通过平台配置即可实现常见场景的问答交互。"
        ),
    },
    "custom-biz/skill-studio/development": {
        "title": "技能开发",
        "description": "AIUI 技能工作室开发流程指南",
        "intro": (
            "技能开发流程涵盖从创建技能、配置意图与语料、"
            "到测试验证和审核发布的完整链路。"
            "本节还提供了技能后处理开发和批量导入导出等进阶功能说明。"
        ),
    },
    "faq": {
        "title": "常见问题",
        "description": "AIUI 平台常见问题与解决方案",
        "intro": (
            "本节汇总了 AIUI 平台使用中的常见问题及解决方案，"
            "涵盖 AIUI 服务、评估板硬件和动态实体等方面。"
            "如遇到开发问题，可优先在此查阅。"
        ),
    },
    "hardware": {
        "title": "硬件模组",
        "description": "AIUI 配套硬件模组产品文档",
        "intro": (
            "AIUI 提供多种配套硬件模组，覆盖降噪板、评估板、多模态套件、"
            "离线语音模块和 USB 声卡等产品形态。"
            "每款硬件均附带产品白皮书、使用手册和开发指南，"
            "方便开发者快速完成硬件集成与调试。"
        ),
    },
    "legal": {
        "title": "法律与协议",
        "description": "AIUI 平台及相关产品法律文件",
        "intro": (
            "本节包含 AIUI 开放平台、AIUI SDK 及相关产品的服务协议、"
            "隐私政策、合规使用说明和开源软件许可等法律文件。"
            "接入 AIUI 服务前，请仔细阅读相关条款。"
        ),
    },
}


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def extract_title(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).split('\n'):
            if line.startswith('title:'):
                return line.split(':', 1)[1].strip().strip('"').strip("'")
    return ''


def extract_body_desc(text: str, max_chars: int = 80) -> str:
    """提取正文前 max_chars 个有效字符作为描述。"""
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text

    # 去掉标题行、目录行、图片、空行
    lines = body.split('\n')
    clean = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            continue
        if stripped.startswith('**目录**') or stripped == '目录':
            continue
        if stripped.startswith('!['):
            continue
        if stripped.startswith('[查看详情]') or stripped.startswith('[阅读详情]'):
            continue
        if re.match(r'^\d+[\.\、]', stripped):
            continue  # 目录编号行
        # 装饰符号和 emoji
        if re.match(r'^[▼♦♫✪⚙🛠🔊✧]', stripped):
            continue
        if stripped.startswith('- ') or stripped.startswith('> '):
            continue  # 列表项和引用块
        if stripped.startswith('status:'):
            continue
        if re.match(r'^\d+[\.．]', stripped) and len(stripped) < 30:
            continue  # 短编号行（目录项）
        # 跳过代码行
        if stripped.startswith('```') or '=' in stripped[:10]:
            continue
        # 去掉 markdown 格式标记
        text_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
        text_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_clean)
        text_clean = re.sub(r'`([^`]+)`', r'\1', text_clean)
        # 去掉前导装饰符号
        text_clean = re.sub(r'^[▼♦♫✪⚙🛠🔊✧\s]+', '', text_clean)
        if text_clean and len(text_clean) > 5:
            clean.append(text_clean)
        if sum(len(c) for c in clean) >= max_chars:
            break

    if not clean:
        return ''

    desc = clean[0][:max_chars]
    # 截断到最后一个句号、逗号或分号
    for sep in ['。', '，', '；', '、', ',', '.']:
        pos = desc.rfind(sep)
        if pos > max_chars // 3:
            desc = desc[:pos + 1]
            break

    return desc


def collect_children(index_dir: Path, dir_key: str) -> list[dict]:
    """收集 index 目录下的直接子文档和子目录 index。"""
    children = []

    for f in sorted(index_dir.iterdir()):
        if f.name == 'index.md':
            continue
        if f.is_file() and f.suffix == '.md':
            text = f.read_text(encoding='utf-8')
            title = extract_title(text)
            desc = extract_body_desc(text)
            rel = f.stem
            link = f'/{dir_key}/{rel}'
            children.append({'title': title or f.stem, 'desc': desc, 'link': link})
        elif f.is_dir():
            sub_index = f / 'index.md'
            if sub_index.exists():
                text = sub_index.read_text(encoding='utf-8')
                title = extract_title(text)
                # 子目录描述：优先从第一个内容子文件提取
                desc = ''
                for sf in sorted(f.iterdir()):
                    if sf.is_file() and sf.suffix == '.md' and sf.name != 'index.md':
                        desc = extract_body_desc(sf.read_text(encoding='utf-8'))
                        if desc:
                            break
                rel = f.name
                link = f'/{dir_key}/{rel}/'
                children.append({'title': title or f.name, 'desc': desc, 'link': link})

    return children


# ── 主流程 ──────────────────────────────────────────────────────────────────

def main():
    for dir_key, cfg in INDEX_CONFIG.items():
        index_path = DOCS_DIR / dir_key / 'index.md'
        if not index_path.exists():
            print(f"  [SKIP] {index_path} 不存在")
            continue

        index_dir = index_path.parent
        children = collect_children(index_dir, dir_key)

        # 构建页面内容
        lines = [
            '---',
            f'title: {cfg["title"]}',
            f'description: {cfg["description"]}',
            '---',
            '',
            f'## {cfg["title"]}',
            '',
            cfg["intro"],
            '',
            '## 本节内容',
            '',
        ]

        for child in children:
            lines.append(f'### {child["title"]}')
            lines.append('')
            desc = child['desc']
            # 过滤掉代码或过短的无效描述
            if desc and len(desc) > 10 and not any(c in desc for c in ['()', '{}', '=', ';']):
                lines.append(desc)
                lines.append('')
            lines.append(f'[阅读详情]({child["link"]})')
            lines.append('')

        content = '\n'.join(lines)
        index_path.write_text(content, encoding='utf-8')

        char_count = len(content)
        child_count = len(children)
        print(f"  {dir_key}/index.md: {char_count} 字符, {child_count} 个子项")

    print(f"\n完成：7 个 index 页面已生成")


if __name__ == '__main__':
    main()
