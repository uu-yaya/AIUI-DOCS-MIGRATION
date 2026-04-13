---
title: 声音复刻教程
description: 录入音频生成 AI 定制音色，在 AIUI 中使用复刻声音进行语音合成
---

## 前置条件

- 已创建 AIUI 应用并完成 SDK 集成（参考 [Android SDK 教程](/tutorials/sdk-android)）
- 已联系讯飞商务获取声音复刻能力授权（邮箱：aiui_support@iflytek.com）
- 准备一段符合要求的录音音频

## 你将完成的目标

通过本教程，你将学会：

1. 准备符合要求的录音音频
2. 通过 SDK 注册声音复刻资源
3. 查询和管理已注册的复刻资源
4. 使用复刻声音进行语音合成

## 音频要求

录制的音频需要满足以下规格：

| 参数 | 要求 |
|------|------|
| 时长 | 建议 20s ~ 40s |
| 文件大小 | 480KB ~ 3MB |
| 采样率 | 24000 Hz |
| 通道数 | 1（单声道） |
| 位深 | 16 bit |
| 编码格式 | PCM 裸音频 |

::: tip 录音建议
- 选择安静环境录制，避免背景噪声
- 语速适中，发音清晰
- 每个设备（SN）最多注册绑定 3 个资源 ID
:::

## 第一步：注册声音复刻资源

通过 AIUI SDK 上传音频文件，注册声音复刻资源：

```java
// 音频文件路径（需满足上述音频要求）
String audioPath = "/sdcard/voice_clone_sample.pcm";

JSONObject paramsJson = new JSONObject();
paramsJson.put(AIUIConstant.KEY_RES_PATH, audioPath);

// 发送声音注册消息
AIUIMessage regMsg = new AIUIMessage(
    AIUIConstant.CMD_VOICE_CLONE,
    AIUIConstant.VOICE_CLONE_REG,
    0,
    paramsJson.toString(),
    null
);
mAIUIAgent.sendMessage(regMsg);
```

::: warning 保存资源 ID
注册成功后返回的 `res_id` 需要客户端自行存储，丢失后无法恢复。
:::

## 第二步：处理注册回调

在 AIUIListener 中处理声音复刻相关的回调：

```java
@Override
public void onEvent(AIUIEvent event) {
    if (event.eventType == AIUIConstant.EVENT_CMD_RETURN
        && event.arg1 == AIUIConstant.CMD_VOICE_CLONE) {

        int retCode = event.arg2;
        int dtype = event.data.getInt(AIUIConstant.KEY_SYNC_DTYPE, -1);

        if (dtype == AIUIConstant.VOICE_CLONE_REG) {
            // 注册结果
            if (retCode == AIUIConstant.SUCCESS) {
                String resId = event.data.getString(AIUIConstant.KEY_RES_ID, "");
                Log.i(TAG, "注册成功，res_id=" + resId);
                // 务必保存 resId
            } else {
                Log.e(TAG, "注册失败，error=" + retCode);
            }
        } else if (dtype == AIUIConstant.VOICE_CLONE_DEL) {
            // 删除结果
            if (retCode == AIUIConstant.SUCCESS) {
                Log.i(TAG, "删除成功");
            }
        } else if (dtype == AIUIConstant.VOICE_CLONE_RES_QUERY) {
            // 查询结果
            if (retCode == AIUIConstant.SUCCESS) {
                String result = event.data.getString("result", "");
                Log.i(TAG, "查询结果: " + result);
            }
        }
    }
}
```

## 第三步：查询和删除资源

### 查询已注册资源

```java
AIUIMessage queryMsg = new AIUIMessage(
    AIUIConstant.CMD_VOICE_CLONE,
    AIUIConstant.VOICE_CLONE_RES_QUERY,
    0, "", null
);
mAIUIAgent.sendMessage(queryMsg);
```

### 删除指定资源

```java
String resId = "你的资源 ID";

JSONObject paramsJson = new JSONObject();
paramsJson.put(AIUIConstant.KEY_RES_ID, resId);

AIUIMessage delMsg = new AIUIMessage(
    AIUIConstant.CMD_VOICE_CLONE,
    AIUIConstant.VOICE_CLONE_DEL,
    0,
    paramsJson.toString(),
    null
);
mAIUIAgent.sendMessage(delMsg);
```

## 第四步：使用复刻声音合成

注册成功后，可以使用复刻声音进行 TTS（语音合成）。

### 方式一：主动合成请求

直接发送文本进行合成：

```java
String text = "您好，欢迎使用科大讯飞语音合成技术。";
byte[] textData = text.getBytes("utf-8");

String resId = "你的资源 ID";
// vcn 固定为 x5_clone，附带 res_id
String params = "vcn=x5_clone,res_id=" + resId;

AIUIMessage ttsMsg = new AIUIMessage(
    AIUIConstant.CMD_TTS,
    AIUIConstant.START,
    0,
    params,
    textData
);
mAIUIAgent.sendMessage(ttsMsg);
```

### 方式二：全链路合成（配置文件）

在 `aiui.cfg` 中直接配置声音复刻参数，所有交互回复都会使用复刻声音：

```json
{
  "tts": {
    "voice_name": "x5_clone",
    "res_id": "你的资源 ID",
    "play_mode": "sdk"
  }
}
```

### 方式三：全链路合成（动态参数）

运行时动态切换合成声音：

```java
String setParams = "{\"tts\":{"
    + "\"voice_name\":\"x5_clone\","
    + "\"res_id\":\"你的资源 ID\","
    + "\"volume\":\"50\""
    + "}}";

AIUIMessage setMsg = new AIUIMessage(
    AIUIConstant.CMD_SET_PARAMS, 0, 0, setParams, null
);
mAIUIAgent.sendMessage(setMsg);
```

## 合成结果解析

TTS 合成结果通过 `EVENT_RESULT` 回调返回，`sub` 值为 `tts`：

```java
case AIUIConstant.EVENT_RESULT: {
    JSONObject bizParam = new JSONObject(event.info);
    JSONObject data = bizParam.getJSONArray("data").getJSONObject(0);
    JSONObject params = data.getJSONObject("params");
    String sub = params.optString("sub");

    if ("tts".equals(sub)) {
        JSONObject content = data.getJSONArray("content").getJSONObject(0);
        String cntId = content.getString("cnt_id");
        byte[] audio = event.data.getByteArray(cntId); // 合成音频数据

        int dts = content.getInt("dts");
        // dts: 0=音频开始, 1=中间块, 2=音频结束, 3=独立音频（短文本）
        int percent = event.data.getInt("percent"); // 合成进度
    }
    break;
}
```

## 下一步

- [Android SDK 集成教程](/tutorials/sdk-android) — SDK 基础集成
- [API 接入教程](/tutorials/api-integration) — 通过 API 使用声音复刻
- [创建应用教程](/tutorials/create-app) — 应用创建和基础配置
