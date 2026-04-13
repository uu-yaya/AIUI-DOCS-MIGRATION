# AIUI 文档中心

> 科大讯飞 AIUI 开放平台技术文档站，基于 [VitePress](https://vitepress.dev) 构建。

## 项目简介

本项目将 AIUI 原文档站 [aiui-doc.xf-yun.com](https://aiui-doc.xf-yun.com) 的全部内容迁移至 VitePress，重点在于信息架构重组、格式统一化和开发者体验改善。

## 迁移做了什么

### 信息架构重组

原站按编号平铺所有文档（1.x、2.x、3.x...），没有区分入门引导、操作教程和 API 参考。新站将内容重新组织为递进式结构：快速开始 → 开发教程 → 开发接入 → 参考文档 → 故障排查。

### 内容拆分与归类

- **SDK 文档**：原站将 Android、iOS、Windows、Linux 的接口、参数、回调混在同一页面。新站按操作系统拆分为独立页面，开发者只看自己平台的内容。
- **API 文档**：原站 API 文档零散分布且仅部分覆盖。新站按极速超拟人（rapid）、通用大模型（llm）、传统语义（traditional）三条链路各自独立归类，明确标注鉴权方式、WebSocket 地址、协议格式等差异。
- **FAQ**：原站按来源分为 3 篇独立文章。新站按症状重组为 8 个分类（连接与网络、语音识别、语音合成、交互模式、评估板、动态实体、SDK 集成、平台功能），统一「症状 → 原因 → 解决步骤」格式。
- **法律条款**：原站分散在不同位置。新站集中到 `/legal/` 目录，导航栏有独立入口。

### 新增整合内容

以下内容原站没有独立页面，是从原站各处信息整合而成：

- **选择接入路径**：三条链路的对比选择指南，帮助开发者判断该用哪条链路
- **Hello World 教程**：三条链路各一篇快速体验，将原站分散的配置步骤串联为完整流程
- **开发教程**（12 篇）：从创建应用到高级功能的步骤式教程，技术细节来自原站，新增了统一的教程框架（前置条件、目标、步骤、下一步）
- **大模型链路 API 文档**：原站没有独立的 llm 链路文档，基于 rapid 链路结构和原站零散的 llm 参数说明整合而成
- **错误码汇总**：原站错误码分散在各文档中，整合为集中索引页
- **发音人列表**：70+ 发音人汇总索引，原站无集中列表
- **术语表**：从原站各处提取术语定义（AIUI、AppID、APIKey、WebSocket、SDK 等）整合为统一页面

### 格式统一化

所有 244 篇文档统一执行了以下规范：

- frontmatter 包含 title 和 description
- 正文从 `##` 开始，不使用 `#`
- 中英文之间加空格
- 术语写法统一（AIUI、AppID、APIKey、WebSocket、SDK、TTS、VAD）
- 代码块标注语言
- 提示信息使用 VitePress 容器语法（`::: tip`、`::: warning`、`::: danger`）
- 参数表格统一为「参数名 / 类型 / 必填 / 说明 / 示例」格式

## 文档结构

新站目录（总计 244 篇 Markdown 文档）：

- `docs/getting-started/` — 快速开始（5 页）
  - `introduction.md` — AIUI 平台介绍
  - `choose-your-path.md` — 选择接入路径（三条链路对比）
  - `hello-world-rapid.md` — 极速超拟人快速体验
  - `hello-world-llm.md` — 大模型链路快速体验
  - `hello-world-traditional.md` — 传统语义链路快速体验

- `docs/tutorials/` — 开发教程（12 页）
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
  - `basics/interfaces/` — 按平台拆分（index, android, ios, windows-linux）
  - `basics/params/` — 按平台拆分（index, android, ios-windows-linux）
  - `basics/callbacks/` — 按平台拆分（index, android, ios-windows-linux）
  - `basics/data-sending/` — 按平台拆分（index, android, ios-windows-linux）
  - `ultra-chain/` — 极速超拟人链路 SDK
  - `llm-chain/` — 大模型链路 SDK
  - `classic-chain/` — 传统语义链路 SDK
  - `features/` — SDK 功能特性

- `docs/api-dev/` — API 开发接入（18 页）
  - `ultra-chain/` — 极速超拟人链路（6 篇）
  - `llm-chain/` — 通用大模型链路（5 篇）
  - `classic-chain/` — 传统语义链路（4 篇）

- `docs/reference/` — 参考文档（54 页）
  - `app-config/` — 应用配置参考
  - `sdk/` — SDK 参考（按平台拆分）
  - `protocols/` — 协议文档
  - `error-codes.md` — 错误码汇总
  - `tts-voices.md` — 发音人列表

- `docs/custom-biz/` — 自定义业务（36 页）

- `docs/hardware/` — 硬件模组（37 页）

- `docs/faq/` — 常见问题（5 页）

- `docs/troubleshooting/` — 故障排查（1 页，按症状分 8 类）

- `docs/legal/` — 法律条款（12 页）

- `docs/glossary.md` — 术语表

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

