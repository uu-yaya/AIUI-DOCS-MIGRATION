---
title: AIUI 智能文档平台 · UI 设计规范
version: "1.0"
status: draft
author: AIUI 文档重构项目组
created: 2026-04-13
last_updated: 2026-04-13
---

# AIUI 智能文档平台 — UI 设计规范文档

> 本文档定义 AIUI 智能文档平台（基于 VitePress）的视觉设计体系、组件规范、页面布局与交互模式，确保最终产出物与科大讯飞企业形象一致，同时兼顾开发者文档的可读性与易用性。

---

## 一、设计原则

### 1.1 核心理念

**降低认知负荷，加速首次调用。** 整个设计围绕一个目标展开：让开发者从"打开文档"到"完成第一次成功 API 调用"的时间压缩至 15 分钟以内。

### 1.2 四项准则

**清晰优先（Clarity First）** — 信息层级分明，每一屏有且仅有一个核心行动点。视觉噪音最小化，代码区与说明区对比度鲜明。

**品牌统一（Brand Consistency）** — 色彩、字体、图标语言严格继承科大讯飞 / 讯飞开放平台视觉体系，文档站即品牌触点。

**可操作性（Actionable）** — 所有示例代码均可一键复制；API Playground、Webhook 测试器、鉴权计算器内嵌于文档流中，无需跳转。

**智能辅助（AI-Augmented）** — 内置 AI 智能体（OpenClaw）贯穿阅读旅程，提供上下文感知的答疑、代码生成与路径推荐。

---

## 二、品牌视觉体系

### 2.1 色彩系统

#### 2.1.1 主色（Primary）

科大讯飞品牌以"讯飞蓝"渐变为核心视觉锚点。文档平台取渐变的中间值作为主色，辅以两端色作为悬停/激活态。

| 用途 | 色名 | HEX | RGB | 应用场景 |
|------|------|-----|-----|---------|
| 主色-深 | 讯飞蓝-深 | `#0050D8` | 0, 80, 216 | 顶部导航栏背景、主按钮激活态 |
| 主色 | 讯飞蓝 | `#1A6FFF` | 26, 111, 255 | 主按钮、链接、侧边栏选中态、标签 |
| 主色-浅 | 讯飞蓝-浅 | `#4D94FF` | 77, 148, 255 | 按钮悬停态、次级高亮 |
| 主色-极浅 | 讯飞蓝-背景 | `#E8F1FF` | 232, 241, 255 | 提示框背景、选中行背景 |

#### 2.1.2 辅助色（Secondary）

| 用途 | 色名 | HEX | 应用场景 |
|------|------|-----|---------|
| 成功 | 翠绿 | `#00B578` | 成功提示、状态标签-已完成 |
| 警告 | 琥珀 | `#FF8F1F` | 警告提示、过期标记 |
| 错误 | 赤红 | `#E63F3F` | 错误提示、必填标记、错误码高亮 |
| 信息 | 天蓝 | `#37B1E6` | 信息提示、版本号标签 |

#### 2.1.3 中性色（Neutral）

| 用途 | HEX（亮色模式） | HEX（暗色模式） |
|------|----------------|----------------|
| 标题文字 | `#1A1A2E` | `#EDEDF0` |
| 正文文字 | `#333347` | `#C8C8D0` |
| 次级文字 | `#6B6B80` | `#8E8E9E` |
| 占位/禁用 | `#B0B0C0` | `#5A5A6E` |
| 分割线 | `#E5E5EC` | `#3A3A4A` |
| 页面背景 | `#FFFFFF` | `#1A1A2E` |
| 侧边栏背景 | `#F7F8FA` | `#22223A` |
| 代码块背景 | `#F5F6F8` | `#2A2A3E` |

#### 2.1.4 暗色模式

VitePress 原生支持 `appearance: 'dark'`。所有自定义 CSS 变量以 `--aiui-` 为命名空间前缀，通过 `.dark` 选择器覆盖。暗色模式下代码块保持深底浅字，正文区背景 `#1A1A2E`，与讯飞星火产品暗色风格一致。

### 2.2 字体系统

#### 2.2.1 字体栈

```css
:root {
  /* 正文 */
  --aiui-font-body: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
                     "Helvetica Neue", Arial, sans-serif;
  /* 代码 */
  --aiui-font-code: "JetBrains Mono", "Fira Code", "Source Code Pro",
                     Menlo, Monaco, Consolas, monospace;
  /* 品牌标题（可选，用于 Hero 区域） */
  --aiui-font-brand: "FZLanTingHei-M-GBK", var(--aiui-font-body);
}
```

品牌标题字体为"方正兰亭中黑"（FZLanTingHei-M-GBK），与科大讯飞品牌规范一致。若客户端未安装该字体，回退至 PingFang SC。

#### 2.2.2 字号层级

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| Display | Hero 标题 | 36px / 2.25rem | 1.2 | 700 |
| H1 | 页面标题 | 28px / 1.75rem | 1.3 | 700 |
| H2 | 章节标题 | 22px / 1.375rem | 1.4 | 600 |
| H3 | 子标题 | 18px / 1.125rem | 1.5 | 600 |
| H4 | 段落标题 | 16px / 1rem | 1.5 | 600 |
| Body | 正文 | 15px / 0.9375rem | 1.75 | 400 |
| Small | 辅助说明 | 13px / 0.8125rem | 1.6 | 400 |
| Code | 行内代码 | 14px / 0.875rem | 1.6 | 400 |

### 2.3 间距与栅格

**基准单位**：`4px`。所有间距为 4 的整数倍。

| Token | 值 | 用途 |
|-------|-----|------|
| `--space-xs` | 4px | 行内元素间距 |
| `--space-sm` | 8px | 紧凑列表项间距 |
| `--space-md` | 16px | 段落间距、卡片内边距 |
| `--space-lg` | 24px | 章节间距 |
| `--space-xl` | 32px | 页面区块间距 |
| `--space-2xl` | 48px | Hero / Footer 区域留白 |

**内容最大宽度**：`768px`（VitePress 默认）。代码块允许溢出至 `920px` 并水平滚动。

### 2.4 圆角与阴影

| 元素 | 圆角 | 阴影 |
|------|------|------|
| 按钮 | 6px | 无 |
| 卡片 | 8px | `0 1px 3px rgba(0,0,0,0.08)` |
| 弹窗/面板 | 12px | `0 8px 24px rgba(0,0,0,0.12)` |
| 代码块 | 8px | 无 |
| 提示框 | 8px | 无 |
| AI 智能体浮窗 | 16px | `0 12px 40px rgba(26,111,255,0.15)` |

### 2.5 图标系统

采用 **Lucide Icons**（MIT 协议），风格为 24×24 / stroke-width 1.75 的线性图标，与讯飞开放平台技术文档风格统一。特殊图标（如 AIUI Logo、链路图标）使用定制 SVG。

图标颜色跟随文字颜色（`currentColor`），交互态跟随主色。

---

## 三、全局布局

### 3.1 页面骨架

```
┌─────────────────────────────────────────────────────────┐
│  Top Nav Bar (固定, 高度 64px)                            │
│  [Logo] [快速开始] [教程] [参考] [硬件] [FAQ] [🔍] [☀/🌙] │
├──────────┬──────────────────────────────┬───────────────┤
│ Sidebar  │  Main Content               │  Right TOC    │
│ (260px)  │  (max 768px, 居中)           │  (220px)      │
│          │                              │               │
│ 可折叠   │  Breadcrumb                  │  当前页目录   │
│ 树形导航 │  H1 标题                      │  H2/H3 锚点  │
│          │  正文/代码/交互组件            │               │
│          │                              │               │
│          │  Prev / Next 导航             │               │
├──────────┴──────────────────────────────┴───────────────┤
│  Footer (站点信息、版权、社群链接)                         │
├─────────────────────────────────────────────────────────┤
│  AI Agent 浮窗 (右下角, 可展开/收起)                      │
└─────────────────────────────────────────────────────────┘
```

### 3.2 响应式断点

| 断点 | 宽度 | 布局变化 |
|------|------|---------|
| Desktop | ≥ 1280px | 三栏（Sidebar + Content + TOC） |
| Tablet | 960–1279px | 两栏（Sidebar 可折叠 + Content），TOC 移入 hamburger |
| Mobile | < 960px | 单栏，Sidebar 和 TOC 均折叠到 hamburger 菜单 |

### 3.3 顶部导航栏

**高度**：64px，背景 `#FFFFFF`（亮）/ `#1A1A2E`（暗），底部 1px 分割线。

**左侧**：AIUI Logo（SVG，高度 32px） + 文字"AIUI 文档"，字号 18px，字重 600，颜色 `--aiui-primary`。Logo 与科大讯飞官网保持一致的蓝色渐变。

**中间**：一级导航项（快速开始 / 教程 / API 参考 / SDK 参考 / 硬件 / FAQ），悬停下划线动画（2px 高，`--aiui-primary`）。

**右侧**：搜索图标（点击展开全屏搜索浮层）、亮暗模式切换、GitHub 仓库链接（可选）。

### 3.4 侧边栏

**宽度**：260px 固定，左侧紧贴。

**分组**：按信息架构分为可折叠的章节组。每组有 16px 字号标题（字重 600）和 14px 的子项列表。

**选中态**：左侧 3px 实色竖条（`--aiui-primary`）+ 背景 `--aiui-primary-bg` + 文字变为 `--aiui-primary`。

**折叠/展开**：带旋转箭头动画（Lucide `chevron-right`），展开时箭头旋转 90°。

**滚动**：侧边栏独立滚动，当前选中项自动滚入视野。

### 3.5 右侧目录（TOC）

**宽度**：220px，标题 "本页目录"，字号 13px，字重 600。

**锚点项**：H2 不缩进，H3 缩进 12px。字号 13px，颜色 `--aiui-text-secondary`。

**活跃态**：左侧 2px 蓝条 + 文字变为 `--aiui-primary`，随滚动自动高亮。

---

## 四、核心页面设计

### 4.1 首页（Landing / Hero）

首页不同于普通文档页，需传递品牌价值与快速引导。

**Hero 区域**：高度 480px（Desktop），渐变背景从 `#0050D8` → `#1A6FFF` → `#4D94FF` 斜向渐变（与讯飞开放平台首页风格呼应）。白色文字居中排列：主标题 "AIUI 智能文档平台"（36px, 700），副标题 "让 AI 交互开发从这里开始"（18px, 400），下方两个按钮——"快速开始"（主按钮，白底蓝字）和"API 参考"（幽灵按钮，白边白字）。

**链路选择卡片区**：Hero 下方，三列等宽卡片（移动端堆叠），分别对应三大链路——"传统语义链路"、"通用大模型链路"、"极速超拟人链路"。每张卡片包含图标（Lucide）、标题、一句话描述、"开始接入"链接。鼠标悬停上移 4px + 阴影加深。

**数据统计条**：水平排列 4 个数字指标——"163+ 篇文档"、"5 个 SDK"、"23 种方言支持"、"10,000+ 年免费调用"，字号 28px / 700，下方 13px 说明文字。

**快速指引网格**：2×3 网格，每个入口有图标 + 标题 + 描述。包含：Hello World、SDK 下载、WebSocket API、技能商店、Webhook 配置、错误码查询。

### 4.2 快速开始页

**决策树引导**：页面顶部嵌入交互式链路选择器，三步决策——

第一步：你的产品形态是什么？（带屏设备 / 纯语音设备 / 服务端/Web）。第二步：你需要大模型能力吗？（是 / 否）。第三步：推荐链路卡片 + "开始 Hello World"按钮。

每步为一个水平步骤条，选中后下方区域滑入动画展示下一步。

**Hello World 代码区**：左右分栏。左侧为步骤说明（编号圆圈 + 描述），右侧为对应代码块。代码块顶部 Tab 切换（Android / iOS / Linux / WebSocket），一键复制按钮在代码块右上角。步骤不超过 10 步。

### 4.3 教程页

标准文档布局（三栏）。页面顶部显示面包屑和预估阅读时间。正文中穿插 "Tip"、"Warning"、"Info" 提示框（VitePress 自定义容器）。代码示例紧跟说明段落，带语言标签和复制按钮。

### 4.4 API 参考页

**接口卡片**：每个接口一个卡片区域，包含方法标签（GET 绿色 / POST 蓝色 / WebSocket 紫色）+ 路径 + 描述。

**参数表格**：固定表头，列为"参数名 / 类型 / 必填 / 默认值 / 描述"。必填列用红色圆点标记。表格支持行悬停高亮。

**响应示例**：JSON 代码块，带语法高亮。可折叠（默认展开成功示例，错误示例折叠）。

**内嵌 Playground**：每个接口下方可展开"在线试一试"面板——左侧填写参数，右侧实时显示请求和响应。发送按钮使用主色。

### 4.5 错误码页

全表检索模式：顶部搜索框（输入错误码或关键字即时过滤），下方为三列表格（错误码 / 描述 / 解决方案），支持排序。错误码单元格使用 `monospace` 字体，颜色 `--aiui-error`。

---

## 五、组件设计规范

### 5.1 按钮

| 类型 | 背景 | 文字 | 边框 | 悬停态 | 用途 |
|------|------|------|------|--------|------|
| Primary | `#1A6FFF` | `#FFFFFF` | 无 | `#0050D8` | 主要行动（提交、开始、发送） |
| Secondary | `#FFFFFF` | `#1A6FFF` | 1px `#1A6FFF` | 背景 `#E8F1FF` | 次要行动（取消、查看更多） |
| Ghost | 透明 | `#333347` | 1px `#E5E5EC` | 背景 `#F7F8FA` | 辅助操作（复制、折叠） |
| Danger | `#E63F3F` | `#FFFFFF` | 无 | `#CC3636` | 危险操作（删除） |
| Text | 透明 | `#1A6FFF` | 无 | 下划线 | 文字链接式按钮 |

所有按钮高度 36px（小号 28px），内边距水平 16px，字号 14px，圆角 6px。禁用态 opacity 0.4。

### 5.2 提示框（Custom Containers）

VitePress 原生支持 `:::tip`、`:::warning`、`:::danger`、`:::info`。自定义颜色如下：

| 类型 | 左边框色 | 背景色 | 图标 | 标题色 |
|------|---------|--------|------|--------|
| tip | `#00B578` | `#F0FFF5` | Lucide `lightbulb` | `#00B578` |
| warning | `#FF8F1F` | `#FFFBE8` | Lucide `alert-triangle` | `#FF8F1F` |
| danger | `#E63F3F` | `#FFF0F0` | Lucide `alert-circle` | `#E63F3F` |
| info | `#37B1E6` | `#EDF8FF` | Lucide `info` | `#37B1E6` |
| details | `#6B6B80` | `#F7F8FA` | Lucide `chevron-right` | `#333347` |

暗色模式下背景透明度降至 10%，边框保持原色。

### 5.3 代码块

**背景**：`#F5F6F8`（亮）/ `#2A2A3E`（暗）。圆角 8px，内边距 16px。

**语言标签**：右上角，字号 12px，颜色 `--aiui-text-tertiary`，如 `java`、`python`、`json`。

**复制按钮**：右上角，Lucide `clipboard`，点击后变为 `check` + "已复制" 持续 2 秒。

**行号**：默认隐藏，超过 10 行时显示。行号颜色 `--aiui-text-placeholder`。

**高亮行**：通过 `// [!code highlight]` 标记，背景 `rgba(26,111,255,0.08)`，左边框 2px `--aiui-primary`。

**代码组（Tab 切换）**：支持 `code-group`，Tab 栏背景 `#EEEFF2`（亮）/ `#333347`（暗），选中 Tab 底部 2px 主色下划线。

### 5.4 表格

**表头**：背景 `#F7F8FA`（亮）/ `#2A2A3E`（暗），字重 600，字号 14px。

**行悬停**：背景 `#FAFBFC`（亮）/ `#2E2E42`（暗）。

**边框**：仅水平线，颜色 `--aiui-border`。

**单元格内边距**：12px 16px。

**响应式**：移动端表格水平滚动，不折行。

### 5.5 搜索

**触发方式**：点击顶部搜索图标 或 键盘快捷键 `Cmd/Ctrl + K`。

**浮层**：全屏半透明遮罩 + 居中卡片（max-width 640px），顶部输入框自动聚焦。

**结果列表**：按分类分组（快速开始、教程、API、SDK、FAQ），每条显示标题 + 路径 + 摘要片段（关键词高亮）。

**技术方案**：优先使用 VitePress 内置 MiniSearch，备选接入 Algolia DocSearch。

---

## 六、交互工具组件

### 6.1 API Playground

**布局**：嵌入文档页内，可折叠面板。展开后左右分栏——左侧为参数表单（标签+输入框/下拉框/开关），右侧为请求预览（curl 命令）和响应结果（JSON 高亮）。

**发送按钮**：主色，点击后显示 loading 动画（讯飞蓝脉冲圆圈），响应后自动滚动到结果区。

**鉴权**：用户输入 AppID / APIKey / APISecret，前端使用 JavaScript 计算签名，密钥不离开浏览器。顶部有安全提示条："你的密钥仅在本地浏览器中使用，不会发送至我们的服务器。"

### 6.2 Webhook 测试器

**功能**：一键生成临时 Webhook URL（有效期 24 小时），用户配置到 AIUI 控制台后，本页面实时显示接收到的 Webhook 请求内容。

**UI**：上方为生成的 URL（带复制按钮），下方为请求日志列表——每条显示时间戳、HTTP Method、Headers（可折叠）、Body（JSON 高亮）。新请求到达时顶部出现蓝色脉冲动画。

### 6.3 鉴权签名计算器

**功能**：用户输入 AppID、APIKey、APISecret、当前时间戳，自动生成完整的鉴权 URL 或 Header 值。

**UI**：表单式布局，输入框 + "生成"按钮 + 结果展示区（带复制按钮）。结果区分步展示：原始字符串 → HMAC-SHA256 签名 → Base64 编码 → 最终拼接结果，每步可展开查看中间值。

### 6.4 链路选择决策树

**功能**：引导用户通过 3 个问题选择最适合的 AIUI 接入链路。

**UI**：水平步骤条（3 步），每步显示问题 + 选项卡片。选中后自动前进到下一步，带滑入动画。最终步展示推荐结果卡片（链路名 + 特点摘要 + "查看接入文档"按钮）。支持"重新选择"回退。

---

## 七、AI 智能体（OpenClaw Agent）

### 7.1 入口

**浮窗按钮**：右下角固定定位，距底部 24px、距右侧 24px。圆形按钮，直径 56px，背景渐变 `#0050D8` → `#1A6FFF`，图标为讯飞星火风格的 AI 图标（白色 SVG）。悬停时轻微放大（scale 1.05）+ 阴影增强。

**展开面板**：点击后向上展开为 400px × 560px 的聊天面板（移动端全屏）。面板圆角 16px，阴影 `0 12px 40px rgba(26,111,255,0.15)`。

### 7.2 面板结构

```
┌─────────────────────────┐
│  AIUI 智能助手    [—] [×]│  ← 标题栏 + 最小化/关闭
├─────────────────────────┤
│                         │
│  对话消息区域             │  ← 滚动区域
│  (AI 气泡左对齐-蓝底白字  │
│   用户气泡右对齐-灰底黑字) │
│                         │
├─────────────────────────┤
│  快捷操作标签              │  ← 可横向滚动的 chip
│  [生成代码] [解释错误码]    │
│  [推荐链路] [Webhook帮助]  │
├─────────────────────────┤
│  [📎] 输入框        [发送] │  ← 输入区
└─────────────────────────┘
```

### 7.3 消息样式

**AI 消息**：左对齐，头像为 AIUI 图标（24×24），气泡背景 `#E8F1FF`（亮）/ `#2A2A3E`（暗），文字 `--aiui-text-primary`。支持 Markdown 渲染（代码块、列表、链接）。打字机效果逐字输出。

**用户消息**：右对齐，气泡背景 `#F0F0F5`（亮）/ `#3A3A4A`（暗）。

**工具调用**：AI 调用工具时显示状态卡片——"正在生成鉴权签名…" / "正在查询错误码 10407…"，带 loading 动画，完成后展开结果。

### 7.4 快捷操作

面板底部固定一排 Chip 标签（水平滚动），根据用户当前浏览的文档页面动态生成。例如浏览 SDK 页面时显示"生成初始化代码"、"查看常见报错"；浏览 API 页面时显示"测试此接口"、"生成 curl 命令"。

### 7.5 行为感知

智能体根据用户行为自动触发提示：

**停留感知** — 用户在某页面停留超过 3 分钟未滚动，浮窗弹出气泡："需要帮助吗？我可以解释这个配置项。"

**错误感知** — 用户在 Playground 中得到错误响应，智能体自动弹出："检测到错误码 {code}，点击查看解决方案。"

**路径感知** — 新用户首次访问，浮窗自动展开并显示欢迎语："你好！我是 AIUI 智能助手。你想做什么？" + 三个选项卡片。

---

## 八、自定义 VitePress 主题变量

以下 CSS 变量写入 `docs/.vitepress/theme/style.css`：

```css
:root {
  /* ===== 品牌色 ===== */
  --vp-c-brand-1: #1A6FFF;
  --vp-c-brand-2: #4D94FF;
  --vp-c-brand-3: #0050D8;
  --vp-c-brand-soft: #E8F1FF;

  /* ===== 按钮 ===== */
  --vp-button-brand-bg: #1A6FFF;
  --vp-button-brand-hover-bg: #0050D8;
  --vp-button-brand-active-bg: #003DA8;
  --vp-button-brand-text: #FFFFFF;

  /* ===== 侧边栏 ===== */
  --vp-sidebar-width: 260px;

  /* ===== 首页 Hero ===== */
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: linear-gradient(135deg, #0050D8 0%, #1A6FFF 50%, #4D94FF 100%);
  --vp-home-hero-image-background-image: linear-gradient(135deg, #E8F1FF 0%, #FFFFFF 100%);
  --vp-home-hero-image-filter: blur(56px);

  /* ===== 自定义 ===== */
  --aiui-success: #00B578;
  --aiui-warning: #FF8F1F;
  --aiui-error: #E63F3F;
  --aiui-info: #37B1E6;
}

.dark {
  --vp-c-brand-1: #4D94FF;
  --vp-c-brand-2: #1A6FFF;
  --vp-c-brand-3: #80B3FF;
  --vp-c-brand-soft: rgba(26, 111, 255, 0.12);
}

/* ===== 侧边栏选中态 ===== */
.VPSidebarItem.is-active > .item > .link {
  border-left: 3px solid var(--vp-c-brand-1);
  background-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

/* ===== 代码块 ===== */
div[class*="language-"] {
  border-radius: 8px;
}

/* ===== AI Agent 浮窗 ===== */
.aiui-agent-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0050D8, #1A6FFF);
  box-shadow: 0 4px 16px rgba(26, 111, 255, 0.3);
  cursor: pointer;
  z-index: 1000;
  transition: transform 0.2s, box-shadow 0.2s;
}
.aiui-agent-fab:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 24px rgba(26, 111, 255, 0.4);
}
```

---

## 九、图标与品牌资产清单

| 资产 | 格式 | 尺寸 | 存放路径 | 说明 |
|------|------|------|---------|------|
| AIUI Logo（横版） | SVG | 高度 32px | `/public/logo.svg` | 顶部导航栏使用 |
| AIUI Logo（图标） | SVG | 24×24 | `/public/logo-icon.svg` | Favicon、AI 助手头像 |
| Favicon | ICO + PNG | 32×32, 16×16 | `/public/favicon.ico` | 浏览器标签图标 |
| OG Image | PNG | 1200×630 | `/public/og-image.png` | 社交分享卡片 |
| 占位图 | SVG | 自适应 | `/public/images/placeholder.svg` | 缺失图片占位 |
| Hero 背景 | SVG/CSS | 全宽 | CSS 渐变 | 首页 Hero 背景 |
| 链路图标 ×3 | SVG | 48×48 | `/public/icons/chain-*.svg` | 三大链路选择卡片 |

---

## 十、动效规范

**基础过渡**：`transition: all 0.2s ease`，适用于按钮悬停、侧边栏展开、链接颜色变化。

**页面切换**：VitePress 默认 View Transition，无需额外配置。

**AI Agent 展开**：`transform: translateY(0)` + `opacity: 1`，时长 300ms，缓动 `cubic-bezier(0.34, 1.56, 0.64, 1)`（轻微弹性）。

**代码块复制反馈**：图标从 `clipboard` 切换为 `check`，持续 2000ms 后恢复，使用 `fade` 动画。

**链路选择决策树**：步骤间切换使用 `slide-left` 动画，时长 250ms。

**通知气泡**：AI Agent 浮窗上方弹出气泡，`slideUp + fadeIn`，时长 300ms。

**减少动效**：尊重 `prefers-reduced-motion: reduce`，此时所有动画改为即时切换。

---

## 十一、无障碍（Accessibility）

所有交互元素具备 `:focus-visible` 样式（2px 蓝色外框），键盘可达。颜色对比度符合 WCAG 2.1 AA 标准（正文文字与背景对比度 ≥ 4.5:1，大文字 ≥ 3:1）。图片均有 `alt` 文本。AI Agent 面板支持 `Esc` 关闭、`Tab` 在输入框与发送按钮间切换。代码块复制按钮具备 `aria-label="复制代码"`。

---

## 十二、实施指南

### 12.1 技术栈

VitePress 最新稳定版（≥ 1.6）构建静态站点，Vue 3 单文件组件开发自定义组件（Playground、Webhook 测试器、AI Agent 面板），CSS 变量 + PostCSS 管理主题，Lucide Vue 引入图标，部署至 CDN（Cloudflare Pages 或讯飞内部 OSS）。

### 12.2 文件结构

```
docs/
├── .vitepress/
│   ├── config.ts              # VitePress 配置
│   ├── theme/
│   │   ├── index.ts           # 自定义主题入口
│   │   ├── style.css          # 全局样式 + CSS 变量
│   │   ├── components/
│   │   │   ├── AiAgent.vue        # AI 智能体面板
│   │   │   ├── ApiPlayground.vue  # API 在线试用
│   │   │   ├── WebhookTester.vue  # Webhook 测试器
│   │   │   ├── AuthCalc.vue       # 鉴权计算器
│   │   │   ├── ChainSelector.vue  # 链路选择决策树
│   │   │   └── ErrorSearch.vue    # 错误码搜索
│   │   └── layouts/
│   │       └── home.vue       # 首页自定义 Layout
│   └── sidebar.ts             # 侧边栏配置
├── public/
│   ├── logo.svg
│   ├── logo-icon.svg
│   ├── favicon.ico
│   ├── og-image.png
│   ├── images/
│   │   └── placeholder.svg
│   └── icons/
│       ├── chain-traditional.svg
│       ├── chain-llm.svg
│       └── chain-rapid.svg
├── getting-started/
├── tutorials/
├── api-dev/
├── sdk-dev/
├── custom-biz/
├── hardware/
├── faq/
└── legal/
```

### 12.3 交付检查清单

在提交设计评审前，确认以下各项均已完成：

色彩变量已写入 `style.css` 且亮暗模式均生效。字体栈已配置，方正兰亭中黑字体文件已上传或确认回退正确。首页 Hero 渐变与按钮在 3 种断点下表现正常。侧边栏选中态样式正确。代码块复制按钮功能正常。AI Agent 浮窗可展开/收起/发送消息。所有 Lucide 图标正确渲染。`prefers-reduced-motion` 下动画已禁用。Lighthouse Accessibility 评分 ≥ 90。`npm run docs:build` 零错误。

---

## 附录 A：色彩快速参考

```
讯飞蓝-深    #0050D8  ████████
讯飞蓝       #1A6FFF  ████████
讯飞蓝-浅    #4D94FF  ████████
讯飞蓝-背景  #E8F1FF  ████████
翠绿-成功    #00B578  ████████
琥珀-警告    #FF8F1F  ████████
赤红-错误    #E63F3F  ████████
天蓝-信息    #37B1E6  ████████
标题文字     #1A1A2E  ████████
正文文字     #333347  ████████
页面背景     #FFFFFF  ████████
暗色背景     #1A1A2E  ████████
```

## 附录 B：组件状态速查

| 组件 | Default | Hover | Active | Focus | Disabled |
|------|---------|-------|--------|-------|----------|
| Primary Btn | bg `#1A6FFF` | bg `#0050D8` | bg `#003DA8` | ring `#4D94FF` | opacity 0.4 |
| Link | color `#1A6FFF` | underline | color `#0050D8` | ring | color `#B0B0C0` |
| Sidebar Item | bg transparent | bg `#F0F1F5` | bg `#E8F1FF` + 左蓝条 | ring | — |
| Input | border `#E5E5EC` | border `#B0B0C0` | border `#1A6FFF` | ring + border blue | bg `#F7F8FA` |
| Code Copy | icon `clipboard` | bg `#E5E5EC` | icon `check` | ring | — |

---

*本文档版本 1.0，由 AIUI 文档重构项目组维护。如有修订需求请在项目仓库提交 Issue。*
