---
title: 回调解析 - Android
description: AIUI Android SDK 全部事件回调的解析示例代码。
---

> 回调概述请参见[回调解析说明](./)

## 服务链接

`EVENT_CONNECTED_TO_SERVER` 事件属于 AIUI SDK 与云服务链接建立成功的回调。可用于在传统语义链路下获取 SDK 链接建立成功的 `uid` 信息：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CONNECTED_TO_SERVER:{
                String uid = event.data.getString("uid");
                Log.i(TAG, "已连接服务器" + uid);
                break;
            }
        }
    }
};
```

## 语音唤醒

`EVENT_WAKEUP` 事件属于 AIUI SDK 唤醒事件的回调，支持两种类型：

- 通过 `CMD_WAKEUP` 手动唤醒 — `event.arg1 = 1`，`event.info` 为空
- 通过语音唤醒 — `event.arg1 = 0`，`event.info` 有返回值

```json
{
    "angle": 0,
    "beam": 0,
    "ivw_result": {
        "angle": 0,
        "beam": 0,
        "end_ms": 3430,
        "keyword": "xiao3 fei1 xiao3 fei1",
        "physical": 0,
        "power": 0,
        "score": 1054,
        "start_ms": 2730
    },
    "type": 0
}
```

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_WAKEUP:{
                String info = event.info;
                Log.i(TAG, "on EVENT_WAKEUP: " + info);
                if(info != null && !info.isEmpty()){
                    JSONObject jsInfo = new JSONObject(info);
                    String ivwResult = jsInfo.getString("ivw_result");
                    JSONObject ivwInfo = new JSONObject(ivwResult);
                    String keyword = ivwInfo.getString("keyword");
                    Log.i("本次唤醒为：" + keyword);
                }
                break;
            }
        }
    }
};
```

## 语音交互结果

`EVENT_RESULT` 事件属于 AIUI SDK 交互结果回调。离线引擎或在线服务返回的结果都通过该回调事件抛出。

解析 `event.info` 获取结果格式：

```json
{
    "data": [
        {
            "content": [{ "cnt_id": "0", "dte": "utf8" }],
            "params": { "sub": "iat" }
        }
    ]
}
```

`sub` 字段确定结果类型：

::: tip 温馨提示
1. 注意传统语义链路下 `nlp` 与大模型相关链路下 `cbm_semantic` 和 `nlp` 结果的区别。
2. 合成 TTS 不区分在线和离线。
:::

| 交互场景 | sub 取值 | 结果介绍 |
| --- | --- | --- |
| **离线交互** | esr_pgs | 离线听写流式结果 |
| | esr_iat | 离线听写结果 |
| | esr_fsa | 离线命令词结果 |
| | tts | 合成结果 |
| **在线-传统语义链路** | iat | 语音识别结果 |
| | nlp | 传统语义技能结果 |
| | tpp | 应用后处理结果 |
| | tts | 合成结果 |
| | itrans | 翻译结果 |
| **在线-通用大模型链路** | iat | 语音识别结果 |
| | cbm_tidy | 语义规整结果 |
| | cbm_semantic | 传统语义技能结果 |
| | cbm_tool_pk | 意图落域结果 |
| | cbm_knowledge | 知识溯源结果 |
| | nlp | 大模型回复结果 |
| | tpp | 应用后处理结果 |
| | tts | 合成结果 |
| **在线-极速超拟人链路** | event | 事件结果（VAD 事件 Bos/Eos，结束交互事件 Silence） |
| | iat | 语音识别结果 |
| | cbm_tidy | 语义规整结果 |
| | cbm_semantic | 传统语义技能结果 |
| | cbm_tool_pk | 意图落域结果 |
| | cbm_knowledge | 知识溯源结果 |
| | cbm_plugin | 智能体结果 |
| | nlp | 大模型回复结果 |
| | tpp | 应用后处理结果 |
| | tts | 合成结果 |

::: warning 注意
合成 TTS 结果解析后是音频数据流，不能和其他结果混合处理（JSON 转义会直接报错）。
:::

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_RESULT: {
                JSONObject data = new JSONObject(event.info).getJSONArray("data").getJSONObject(0);
                String sub = data.getJSONObject("params").optString("sub");
                JSONObject content = data.getJSONArray("content").getJSONObject(0);

                if (content.has("cnt_id") && !"tts".equals(sub)) {
                    String cnt_id = content.getString("cnt_id");
                    String cntStr = new String(event.data.getByteArray(cnt_id), "utf-8");
                    JSONObject cntJson = new JSONObject(cntStr);
                    // 业务处理……
                }

                if ("tts".equals(sub)) {
                    int dts = content.getInt("dts");
                    String cnt_id = content.getString("cnt_id");
                    byte[] audio = event.data.getByteArray(cnt_id);
                    // 播放音频……
                }
            }
        }
    }
};
```

## VAD 端点检测结果

`EVENT_VAD` 事件属于 AIUI SDK 本地 VAD 模块结果回调，提供音频会话前后端点检测信息和识别音频音量信息。

::: tip 温馨提示
音频音量信息是 SDK 内部做的数据映射回调，取值范围为 [0,30]。
:::

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_VAD: {
                switch (event.arg1) {
                    case AIUIConstant.VAD_BOS:
                        // 发现前端点
                        break;
                    case AIUIConstant.VAD_VOL:
                        // 交互音频音量回调
                        int audioVol = event.arg2;
                        break;
                    case AIUIConstant.VAD_EOS:
                        // 发现尾端点
                        break;
                    case AIUIConstant.VAD_BOS_TIMEOUT:
                        // 音频无有效信息
                        break;
                }
            } break;
        }
    }
};
```

## SDK 状态

`EVENT_STATE` 事件属于 AIUI SDK 状态结果回调，可基于该事件判断请求数据是否会被处理：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_STATE: {
                int mAIUIState = event.arg1;
                if (AIUIConstant.STATE_IDLE == mAIUIState) {
                    // 闲置状态，AIUI 未开启
                } else if (AIUIConstant.STATE_READY == mAIUIState) {
                    // AIUI 已就绪，等待唤醒
                } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                    // AIUI 工作中，可进行交互
                }
            } break;
        }
    }
};
```

## 播放器状态

`EVENT_TTS` 事件属于 AIUI SDK 托管合成结果系统播放的播放器状态回调：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_TTS: {
                switch (event.arg1) {
                    case AIUIConstant.TTS_SPEAK_BEGIN:
                        Log.i(TAG, "开始播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_PAUSED:
                        Log.i(TAG, "暂停播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_RESUMED:
                        Log.i(TAG, "恢复播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_COMPLETED:
                        Log.i(TAG, "播放完成");
                        break;
                    case AIUIConstant.TTS_SPEAK_PROGRESS:
                        Log.i(TAG, "播放进度" + event.data.getInt("percent"));
                        break;
                }
            } break;
        }
    }
};
```

## 数据执行

`EVENT_CMD_RETURN` 事件属于 AIUI SDK 数据执行相关处理的回调，常用于**个性化数据使用**和**离线语法操作**。

### 个性化数据 - 传统语义交互链路

个性化数据主要分为数据上传和数据打包查询操作：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (AIUIConstant.CMD_SYNC == event.arg1) {
                    int dtype = event.data.getInt("sync_dtype", -1);
                    int retCode = event.arg2;

                    switch (dtype) {
                        case AIUIConstant.SYNC_DATA_SCHEMA: {
                            if (AIUIConstant.SUCCESS == retCode) {
                                mSyncSid = event.data.getString("sid");
                            } else {
                                mSyncSid = "";
                            }
                        } break;
                    }
                } else if (AIUIConstant.CMD_QUERY_SYNC_STATUS == event.arg1) {
                    int syncType = event.data.getInt("sync_dtype", -1);
                    if (AIUIConstant.SYNC_DATA_QUERY == syncType) {
                        String result = event.data.getString("result");
                    }
                }
            } break;
        }
    }
};
```

### 个性化数据 - 通用大模型和极速超拟人交互链路

个性化数据主要分为数据上传、数据下载和数据删除操作：

```java
private static String mSyncSid = null;
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (AIUIConstant.CMD_SYNC == event.arg1) {
                    int dtype = event.data.getInt("sync_dtype", -1);
                    int retCode = event.arg2;
                    if (AIUIConstant.SUCCESS == retCode) {
                        mSyncSid = event.data.getString("sid");
                        String tag = event.data.getString("tag");
                        switch (dtype) {
                            case AIUIConstant.SYNC_DATA_UPLOAD:
                                Log.e("个性化数据上传成功，tag=" + tag);
                                break;
                            case AIUIConstant.SYNC_DATA_DOWNLOAD:
                                String base64 = event.data.getString("text", "");
                                String content = new String(Base64.decode(base64, Base64.DEFAULT));
                                Log.e("个性化数据下载成功，内容为: \n" + content);
                                break;
                            case AIUIConstant.SYNC_DATA_DELETE:
                                Log.e("个性化数据删除成功，tag=" + tag);
                                break;
                        }
                    } else {
                        mSyncSid = "";
                    }
                }
            } break;
        }
    }
};
```

### 离线语法操作

当 SDK 进行离线语法操作（构建语法或更新离线槽位取值）时，可监听回调获取执行结果：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (AIUIConstant.CMD_SYNC == event.arg1) {
                    int dtype = event.data.getInt("sync_dtype", -1);
                    int retCode = event.arg2;

                    switch (dtype) {
                        case AIUIConstant.CMD_BUILD_GRAMMAR:
                            if (retCode == 0) {
                                Log.e(TAG, "build grammar success");
                            } else {
                                Log.e(TAG, "build grammar failed");
                            }
                            break;
                        case AIUIConstant.CMD_UPDATE_LOCAL_LEXICON: {
                            Log.d("UPDATE_LOCAL_LEXICON", "arg1 " + event.arg1 + " ret " + event.arg2 + " info " + event.info);
                        }
                    }
                }
            } break;
        }
    }
};
```

## SDK 报错

`EVENT_ERROR` 事件属于 AIUI SDK 错误信息结果回调。获取错误码后按照[错误码列表](/reference/error-codes)描述进行处理：

```java
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_ERROR: {
                int errCode = event.arg1;
                String errInfo = event.info;
                Log.i("EVENT_ERROR", "错误码：" + errCode + "，错误信息：" + errInfo);
            } break;
        }
    }
};
```
