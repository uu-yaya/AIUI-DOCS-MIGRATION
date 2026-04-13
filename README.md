# AIUI 文档中心

> 科大讯飞 AIUI 开放平台技术文档站，基于 [VitePress](https://vitepress.dev) 构建。

## 项目简介

本项目将 AIUI 原文档站 [aiui-doc.xf-yun.com](https://aiui-doc.xf-yun.com) 的全部内容迁移至 VitePress，并在信息架构、内容完整性和开发者体验上做了系统性重构。

## 与原文档的结构对比

### 原文档结构

原站按单一层级平铺所有文档，没有区分入门引导和参考手册，SDK 文档将多个操作系统的内容混合在同一页面，FAQ 按来源分为三篇独立文章，API 文档仅部分覆盖传统链路和极速链路。

原站目录：

- 1.x AIUI 介绍 / 快速体验（混合在一起）
- 2.x 应用配置（平铺）
- 3.x SDK 接入（Android/iOS/Windows/Linux 混在同一页面）
- 4.x WebSocket API（仅部分链路）
- 5.x 自定义业务
- 6.x 硬件模组
- 常见问题（3 篇独立 FAQ）
- 法律条款（分散在不同位置）

### 新文档结构

新站目录（总计 244 篇 Markdown 文档）：

- `docs/getting-started/` — 🆕 快速开始（5 页）
  - `introduction.md` — AIUI 平台介绍
  - `choose-your-path.md` — 选择接入路径（三条链路对比）
  - `hello-world-rapid.md` — 极速超拟人快速体验
  - `hello-world-llm.md` — 大模型链路快速体验
  - `hello-world-traditional.md` — 传统语义链路快速体验

- `docs/tutorials/` — 🆕 开发教程（12 页）
  - `create-app.md` — 创建第一个 AIUI 应用
  - `custom-skill.md` — 自定义技能开发
  - `webhook.md` — 技能后处理与 Webhook
  - `qa-library.md` — 问答库开发
  - `sdk-android.md` — Android SDK 集成
  - `sdk-ios.md` — iOS SDK 集成
  - `sdk-windows-linux.md` — Windows/Linux SDK 集成
  - `api-integration.md` — WebSocket API 接入
  - `third-party-llm.md` — 三方大模型配置
  - `voice-clone.md` — 声音复刻
  - `agent-dev.md` — 智能体开发
  - `new-features.md` — 极速超拟人新特性

- `docs/platform-service/` — 平台服务（6 页）

- `docs/app-config/` — 应用配置（16 页）

- `docs/sdk-dev/` — SDK 开发接入（42 页）
  - `basics/interfaces/` — 🆕 按平台拆分（index, android, ios, windows-linux）
  - `basics/params/` — 🆕 按平台拆分（index, android, ios-windows-linux）
  - `basics/callbacks/` — 🆕 按平台拆分（index, android, ios-windows-linux）
  - `basics/data-sending/` — 🆕 按平台拆分（index, android, ios-windows-linux）
  - `ultra-chain/` — 极速超拟人链路 SDK
  - `llm-chain/` — 大模型链路 SDK
  - `classic-chain/` — 传统语义链路 SDK
  - `features/` — SDK 功能特性

- `docs/api-dev/` — API 开发接入（18 页）
  - `ultra-chain/` — 极速超拟人链路（6 篇：auth, interact-api, personalization-api, voice-clone-api, tts-usage, voiceprint-api）
  - `llm-chain/` — 🆕 通用大模型链路（5 篇：auth, interact-api, personalization-api, voice-clone-api, tts-usage）
  - `classic-chain/` — 传统语义链路（4 篇：interact-api, personalization-api, tts-usage）

- `docs/reference/` — 🆕 参考文档（54 页）
  - `app-config/` — 应用配置参考
  - `sdk/` — SDK 参考（按平台拆分）
  - `protocols/` — 协议文档
  - `error-codes.md` — 🆕 错误码汇总
  - `tts-voices.md` — 🆕 发音人列表（70+）

- `docs/custom-biz/` — 自定义业务（36 页）

- `docs/hardware/` — 硬件模组（37 页）

- `docs/faq/` — 常见问题（5 页）

- `docs/troubleshooting/` — 🆕 故障排查（1 页，按症状分 8 类）

- `docs/legal/` — 法律条款（12 页）

- `docs/glossary.md` — 🆕 术语表

## 主要改进

### 新增内容

- **快速开始**（5 页）：按三条链路分别提供 Hello World 教程，原站没有独立的入门引导
- **开发教程**（12 页）：端到端步骤式教程，覆盖从创建应用到高级功能，原站无此体系
- **大模型链路 API**（5 页）：llm/ 链路完整 API 文档，原站缺失
- **错误码汇总**（1 页）：集中索引页，原站分散在各文档中
- **发音人列表**（1 页）：70+ 发音人汇总，原站无集中列表
- **术语表**（1 页）：统一术语定义（AIUI、AppID、APIKey、WebSocket 等）
- **故障排查**（1 页）：将 3 篇 FAQ 按症状重组为 8 分类，统一「症状→原因→解决步骤」格式

### 结构优化

- **SDK 文档**：原站 Android/iOS/Windows/Linux 混在同一页面 → 新站按操作系统拆分为独立页面
- **API 文档**：原站仅部分覆盖 → 新站 rapid/llm/traditional 三条链路各自完整覆盖
- **FAQ**：原站 3 篇独立文章按来源分 → 新站按症状分 8 类，格式统一
- **法律条款**：原站分散在不同位置 → 新站集中到 /legal/ 目录，导航栏有独立入口
- **信息架构**：原站单层平铺 → 新站入门→教程→参考→排错递进式结构

### 格式规范化

所有文档统一执行了以下规范：

- frontmatter 包含 title 和 description
- 正文从 `##` 开始，不使用 `#`
- 中英文之间加空格
- 术语统一（AIUI、AppID、APIKey、WebSocket、SDK、TTS、VAD 等）
- 代码块标注语言
- 提示信息使用 VitePress 容器语法（`::: tip`、`::: warning`、`::: danger`）
- 参数表格统一格式（参数名 / 类型 / 必填 / 说明 / 示例）

## 导航栏结构

- 快速开始
- 开发教程
- 开发接入 ▾（SDK 开发、API 开发、参考文档）
- 平台配置 ▾（平台服务、应用配置、自定义业务）
- 硬件模组
- 帮助 ▾（常见问题、故障排查、联系方式）
- 法律条款

## 技术栈

- **静态站点生成**：VitePress（基于 Vue 3 + Vite）
- **内容格式**：Markdown + VitePress 扩展语法
- **搜索**：VitePress 内置本地搜索

## 本地开发

### 环境要求

- Node.js ≥ 18
- npm ≥ 9

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run docs:dev
```
浏览器访问 http://localhost:5173。

### 构建

```bash
npm run docs:build
```

### 预览构建结果

```bash
npm run docs:preview
```

### 源站对照
- /platform-service/ ← doc-770, doc-401, doc-403, doc-402
- /app-config/ ← doc-769, doc-774, doc-90 等
- /sdk-dev/ ← doc-2, doc-796 等
- /api-dev/ultra-chain/ ← doc-792, doc-784 等
- /api-dev/llm-chain/ ← doc-791, doc-783 等
- /api-dev/classic-chain/ ← doc-790, doc-782 等
- /custom-biz/ ← doc-44, doc-57, doc-58 等
- /hardware/ ← doc-110, doc-816 等
- /faq/ ← doc-80, doc-81, doc-82
- /legal/ ← 原站法律条款页面

### 许可证
Copyright © 2024 科大讯飞股份有限公司。保留所有权利。

