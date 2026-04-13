# AIUI 文档迁移项目规则

## 项目目标

将科大讯飞 AIUI 平台旧文档站（https://aiui-doc.xf-yun.com/）的全部内容迁移为 VitePress 格式的 Markdown 文档。

## Markdown 写作规范

- 标题统一使用 ATX 风格（`#` 开头），禁止使用 Setext 风格（`===` / `---` 下划线）
- 正文从 `##`（h2）开始；`#`（h1）由 VitePress 从 frontmatter `title` 字段自动生成，正文中不重复出现 h1
- 所有代码块必须标注语言，例如 ` ```json `、` ```bash `、` ```java `
- 中英文之间加空格，例如：`调用 WebSocket API 建立连接`
- 不使用 emoji 作为章节标记或装饰

## frontmatter 规范

每个文档文件开头必须包含以下 frontmatter：

```yaml
---
title: 文档标题
description: 一句话描述（可选）
---
```

## 术语规范

统一术语见 `config/terminology.json`，写作时必须使用规范形式：

| 原始写法 | 规范写法 |
|---|---|
| AlUI | AIUI |
| appid | AppID |
| appkey | APIKey |
| apisecret | APISecret |
| websocket / Websocket | WebSocket |
| sdk | SDK |
| api | API |
| tts | TTS（语音合成） |
| iat | IAT（语音识别） |
| nlp | NLP（语义理解） |
| vad | VAD（端点检测） |
| continues | Continuous（全双工） |
| oneshot | Oneshot（单轮交互） |

## 目录结构

```
raw_docs/          # 爬取的原始 Markdown（不可手动编辑）
raw_docs/_images/  # 下载的原始图片
docs/              # VitePress 目标文档（最终输出）
scripts/           # 工具脚本（爬取、清洗、转换）
config/            # 配置文件（术语表、URL 列表等）
```

## 工作流程

1. `scripts/` 中的爬取脚本将原始内容存入 `raw_docs/`
2. 清洗脚本读取 `raw_docs/`，按新信息架构重组后输出到 `docs/`
3. `docs/` 内容为最终 VitePress 文档，可直接构建发布

## 其他约定

- 图片统一存放于 `docs/public/images/`，Markdown 中以 `/images/xxx.png` 形式引用
- 脚本使用 Node.js（ESM）编写，运行环境 Node 18+
- 配置文件使用 JSON 格式，UTF-8 编码
