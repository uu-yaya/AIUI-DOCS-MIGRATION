---
title: Hello World — 传统语义链路
description: 使用传统语义交互链路快速体验 AIUI 结构化语义理解能力
category: 快速入门
source_doc_ids:
  - doc-2
  - doc-403
  - doc-769
  - doc-790
  - doc-782
last_updated: 2026-04-13
---

## 前提条件

- 已注册 [AIUI 平台账号](https://aiui.xfyun.cn/)
- 拥有老应用（2025-06-11 之前创建）

::: tip 新项目推荐
如果你正在开始新项目，建议直接使用[极速超拟人链路](./hello-world-rapid)。传统语义链路适合已有存量应用、只需结构化语义结果的场景。
:::

## 第一步：确认应用配置

1. 登录 AIUI 账号，进入 [我的应用](https://aiui.xfyun.cn/app)
2. 打开目标应用的配置页面
3. 确保**未开启大模型配置**（传统语义链路不可开启大模型）

## 第二步：配置结构化语义

传统语义链路以结构化语义理解为核心，支持以下能力：

- **商店技能**：AIUI 技能商店提供的预置技能（天气、音乐等）
- **自定义技能**：开发者在技能工作室自行创建的技能
- **语句问答**：基于关键句配置的问答对
- **关键词问答**：基于关键词匹配的问答
- **设备人设**：设备角色和回复风格设定
- **闲聊兜底**：无法命中其他技能时的兜底回复

### 添加商店技能

1. 在应用配置中点击 **添加**
2. 从技能商店选择需要的技能并保存
3. 配置完成后，在页面右侧进行模拟测试

### 创建自定义技能（可选）

1. 进入 [技能工作室](https://aiui.xfyun.cn/studio/skill)，创建技能
2. 创建意图、编写语料、配置实体和槽位
3. 构建并测试技能
4. 发布技能后，在应用中添加该技能

自定义技能的完整开发指南请参阅 [技能工作室](/custom-biz/skill-studio/)。

## 第三步：配置语音识别与合成

### 语音识别

选择识别引擎（如"通用-中文-近场"），可选配置：

- 勾选"识别结果优先阿拉伯数字"
- 上传热词文件以提升特定词汇的识别率

### 语音合成

- **主动合成（推荐）**：开发者主动调用合成接口
- **语义后合成**：语义理解后自动合成语音

## 第四步：审核与发布

1. 点击 **审核上线**，一般 24 小时内处理完成
2. 审核通过后点击 **发布**，配置将同步到线上环境

## 第五步：接入开发

### SDK 接入

**版本要求**：

- SDK 5.x 版本：直接对接
- SDK 6.x 及以上版本：`aiui.cfg` 中需配置 `aiui_ver` 参数取值为 `1`

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

详细文档请参阅 [SDK 开发接入 — 传统语义链路](/sdk-dev/classic-chain/)。

### WebSocket API 接入

传统语义链路使用**会话级短连接**：一次会话结束后即断开连接。

<!-- TODO: 补充传统语义链路 WebSocket API 的最小可用代码示例 -->

详细文档请参阅 [API 开发接入 — 传统语义链路](/api-dev/classic-chain/)。

## 服务流程

传统语义链路的完整服务流程为：

**语音识别 → 结构化语义 → 后处理 → 语音合成**

该流程顺序固定，除语音识别外的其他模块可开关。

**技能优先级**：自定义技能 > 语句问答 > 设备人设 > 商店技能 > 关键词问答 > 兜底闲聊

::: warning 全链路注意事项
开启后处理 + 语音合成全链路时，语音合成服务从后处理结果的 `answer.text` 字段中提取合成文本。后处理返回结果需满足以下格式：

```json
{"intent": {"answer": {"text": "xxxx"}}}
```
:::

## 免费额度

传统语义链路的免费授权：

| 项目 | 额度 |
|---|---|
| 日服务调用次数 | 500 次（普通版） |
| API 并发限制 | 20 QPS |
| AIUI 装机量 | 20 台 |
| 唤醒（VTN）装机量 | 20 台 |

## 下一步

- [AIUI 应用配置](/app-config/) — 详细了解应用的各项配置
- [SDK 开发接入 — 传统语义链路](/sdk-dev/classic-chain/) — 完整的 SDK 开发文档
- [API 开发接入 — 传统语义链路](/api-dev/classic-chain/) — 完整的 API 开发文档
- [技能工作室](/custom-biz/skill-studio/) — 创建自定义技能
