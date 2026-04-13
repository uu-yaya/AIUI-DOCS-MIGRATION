---
title: Hello World — 极速超拟人链路
description: 使用极速超拟人交互链路快速创建你的第一个 AIUI 应用
category: 快速入门
source_doc_ids:
  - doc-2
  - doc-769
  - doc-792
  - doc-784
last_updated: 2026-04-13
---

## 前提条件

- 已注册 [AIUI 平台账号](https://aiui.xfyun.cn/)
- 2025 年 6 月 12 日后创建的新应用（默认使用极速超拟人链路）

## 第一步：创建应用

1. 登录 AIUI 账号，进入 [我的应用](https://aiui.xfyun.cn/app)
2. 点击 **创建应用** 并填写应用名称等基本信息
3. 新应用自动绑定极速超拟人交互链路，无需额外配置

::: tip 新应用特点
新应用的语义和大模型配置在服务链路中固定开启，不支持手动开关。你可以在基础配置中选配识别引擎、兜底大模型和回复角色。
:::

## 第二步：配置应用

### 选配大模型

在应用配置中，选择兜底大模型。极速超拟人链路支持讯飞星火大模型，也支持兼容 OpenAI API 协议的三方大模型。

<!-- TODO: 补充极速超拟人链路的大模型选配截图和具体配置步骤 -->

### 配置结构化语义（可选）

如果你的应用需要结构化语义能力（如自定义技能、商店技能），可以在应用配置中进行设置：

1. 点击 **添加** 技能
2. 开启需要的技能并保存
3. 配置完成后，可在页面右侧进行模拟测试

### 配置发音人

- **主动合成（推荐）**：开发者主动调用合成接口，支持云端 TTS（默认）和离线 TTS
- **语义后合成**：语义理解后系统自动合成语音。开启后所有技能回复都会自动合成

### 配置语音识别

在应用配置中选择识别引擎（如"通用-中文-近场"），可选开启以下功能：

- **阿拉伯数字优先**：手机号等数字优先输出阿拉伯格式
- **热词**：提升特定词汇的识别率（下载热词模板，每行一个词语，上传后约 20 分钟生效）

## 第三步：审核与发布

1. 点击 **审核上线**，一般 24 小时内处理完成
2. 审核通过后，点击 **发布**，填写发布信息
3. 发布后，测试情景模式的配置将同步到线上环境

## 第四步：接入开发

极速超拟人链路支持 SDK 和 WebSocket API 两种接入方式。

### SDK 接入

**版本要求**：SDK 6.8.x 及以上版本，`aiui.cfg` 中需配置 `aiui_ver` 参数取值为 `3`。

1. 下载 SDK：在应用的 **接入配置** 页面下载最新版 AIUI SDK
2. 导入 SDK 到工程中
3. 修改 `aiui.cfg` 配置文件：

```text
login.appid={你的 AppID}
global.scene={你的场景名称}
```

4. 创建 `AIUIAgent` 并监听事件回调

**Android 示例**：

```java
// 创建 AIUIAgent
AIUIAgent mAIUIAgent = AIUIAgent.createAgent(context, getAIUIParams(), mAIUIListener);

// 发送唤醒消息
if (AIUIConstant.STATE_WORKING != mAIUIState) {
    AIUIMessage wakeupMsg = new AIUIMessage(AIUIConstant.CMD_WAKEUP, 0, 0, "", null);
    mAIUIAgent.sendMessage(wakeupMsg);
}

// 开始录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage writeMsg = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params, null);
mAIUIAgent.sendMessage(writeMsg);
```

详细 SDK 开发文档请参阅 [SDK 开发接入 — 极速超拟人链路](/sdk-dev/ultra-chain/)。

### WebSocket API 接入

极速超拟人链路使用**长连接交互协议**，支持一次连接进行长时间多次对话。

<!-- TODO: 补充极速超拟人链路 WebSocket API 的最小可用代码示例 -->

详细 API 开发文档请参阅 [API 开发接入 — 极速超拟人链路](/api-dev/ultra-chain/)。

## 第五步：验证结果

在 `AIUIListener`（或对应平台的监听器）的 `EVENT_RESULT` 回调中，解析语义结果：

```java
case AIUIConstant.EVENT_RESULT: {
    JSONObject bizParamJson = new JSONObject(event.info);
    JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
    JSONObject params = data.getJSONObject("params");
    JSONObject content = data.getJSONArray("content").getJSONObject(0);

    if (content.has("cnt_id")) {
        String cnt_id = content.getString("cnt_id");
        JSONObject cntJson = new JSONObject(
            new String(event.data.getByteArray(cnt_id), "utf-8"));
        String sub = params.optString("sub");
        if ("nlp".equals(sub)) {
            String resultStr = cntJson.optString("intent");
            Log.i(TAG, resultStr);
        }
    }
}
```

## 免费额度

极速超拟人链路的免费授权：

| 项目 | 额度 |
|---|---|
| 服务调用次数 | 10,000 次（有效期 1 年，从应用创建时计算） |
| API 并发路数 | 3 路 |
| AIUI 装机量 | 20 台 |
| 唤醒（VTN）装机量 | 20 台 |

如需提升授权额度，请参阅 [联系我们](/faq/contact)。

## 下一步

- [AIUI 应用配置](/app-config/) — 详细了解应用的各项配置
- [SDK 开发接入 — 极速超拟人链路](/sdk-dev/ultra-chain/) — 完整的 SDK 开发文档
- [API 开发接入 — 极速超拟人链路](/api-dev/ultra-chain/) — 完整的 API 开发文档
- [技能工作室](/custom-biz/skill-studio/) — 创建自定义技能
