---
title: Hello World — 通用大模型链路
description: 使用通用大模型交互链路为老应用接入大模型语义能力
category: 快速入门
source_doc_ids:
  - doc-2
  - doc-403
  - doc-769
  - doc-791
  - doc-783
last_updated: 2026-04-13
---

## 前提条件

- 已注册 [AIUI 平台账号](https://aiui.xfyun.cn/)
- 拥有 2022-06-01 至 2025-06-11 期间创建的老应用（支持大模型开关）
- 应用信息中包含 AppID、APIKey 和 APISecret

::: tip 新项目推荐
如果你正在开始新项目，建议直接使用[极速超拟人链路](./hello-world-rapid)，功能更完整且持续更新。
:::

## 第一步：开启大模型配置

1. 登录 AIUI 账号，进入 [我的应用](https://aiui.xfyun.cn/app)
2. 打开目标应用的配置页面
3. 在语义模型配置中**开启大模型**开关

开启大模型配置后，应用服务将指向通用大模型链路。

::: warning 注意
老应用一旦进行过传统语义链路授权，关闭大模型后再开启可能会提示授权限制。建议一个应用固定选用一种服务链路。
:::

## 第二步：选配大模型

在应用配置中选择"讯飞星火交互大模型 V2"或其他可用版本。

<!-- TODO: 补充通用大模型链路的模型选配详细步骤和截图说明 -->

## 第三步：配置其他能力（可选）

### 结构化语义

通用大模型链路在大模型基础上支持级联多种能力：语义规整、意图落域、知识分类、智能体、文档问答、联网搜索、兜底大模型等。

你可以根据需求在应用配置中开启相应的结构化语义技能。

### 语音合成

- **主动合成（推荐）**：开发者主动调用合成接口
- **语义后合成**：语义理解后自动合成语音

### 语音识别

选择识别引擎并配置热词以提升识别率。

## 第四步：审核与发布

1. 点击 **审核上线**，一般 24 小时内处理完成
2. 审核通过后点击 **发布**，配置将同步到线上环境

## 第五步：接入开发

通用大模型链路支持 SDK 和 WebSocket API 两种接入方式。

### SDK 接入

**版本要求**：SDK 6.x 及以上版本，`aiui.cfg` 中需配置 `aiui_ver` 参数取值为 `2`。

> 5.x 版本不支持通用大模型链路。

1. 下载 SDK 并导入工程
2. 修改 `aiui.cfg` 配置：

```text
login.appid={你的 AppID}
global.scene={你的场景名称}
```

3. 创建 `AIUIAgent` 并开始交互：

```java
// 创建 AIUIAgent
AIUIAgent mAIUIAgent = AIUIAgent.createAgent(context, getAIUIParams(), mAIUIListener);

// 发送唤醒消息
AIUIMessage wakeupMsg = new AIUIMessage(AIUIConstant.CMD_WAKEUP, 0, 0, "", null);
mAIUIAgent.sendMessage(wakeupMsg);

// 开始录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage writeMsg = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params, null);
mAIUIAgent.sendMessage(writeMsg);
```

详细文档请参阅 [SDK 开发接入 — 通用大模型链路](/sdk-dev/llm-chain/)。

### WebSocket API 接入

通用大模型链路使用**长连接交互协议**，支持一次连接进行长时间多次对话。

<!-- TODO: 补充通用大模型链路 WebSocket API 的最小可用代码示例 -->

详细文档请参阅 [API 开发接入 — 通用大模型链路](/api-dev/llm-chain/)。

## 免费额度

通用大模型链路的免费授权：

| 项目 | 额度 |
|---|---|
| 日服务调用次数 | 500 次（大模型版） |
| API 并发限制 | 20 QPS |
| AIUI 装机量 | 20 台 |
| 唤醒（VTN）装机量 | 20 台 |

::: warning 装机量说明
AIUI 和唤醒装机量不区分服务链路，两者共同消耗。建议一个应用固定使用一种服务链路。
:::

## 下一步

- [AIUI 应用配置](/app-config/) — 详细了解应用的各项配置
- [SDK 开发接入 — 通用大模型链路](/sdk-dev/llm-chain/) — 完整的 SDK 开发文档
- [API 开发接入 — 通用大模型链路](/api-dev/llm-chain/) — 完整的 API 开发文档
- [星火大模型配置](/app-config/spark-llm) — 大模型参数详细说明
