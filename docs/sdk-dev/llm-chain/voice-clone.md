---
title: 声音复刻
---

::: info 概述
声音复刻是录入一段音频生成AI定制音色的能力。
:::

## 集成开发

温馨提示

1、声音复刻能力使用前需先联系讯飞商务获取授权或发送邮件到 aiui\_support@iflytek.com 提交申请。

2、每个设备（SN）最多注册绑定3个资源id。

### 资源管理

AIUI SDK提供了声音复刻资源管理能力，开发者可以直接进行声音复刻资源相关操作，包括：

- 复刻资源注册
- 复刻资源查询
- 复刻资源删除

#### 资源注册

::: warning 注意
使用时客户端需要自行存储res\_id，避免丢失
:::

- 加载音频文件注册，音频要求：

  > 时长: 建议20s~40s
  >  文件大小范围：[480KB, 3MB]
  >  采样率: 24000
  >  通道数: 1
  >  位深: 16
  >  编码格式: 裸音频pcm
- 接口调用方式如下（Android示例）：

```java
// 注册音频保存的路径
// 注意音频文件格式和参数要求
String path = "";

JSONObject paramsJson = new JSONObject();
paramsJson.put(AIUIConstant.KEY_RES_PATH, path);
// 构建注册事件
AIUIMessage regVoice = new AIUIMessage(AIUIConstant.CMD_VOICE_CLONE,AIUIConstant.VOICE_CLONE_REG, 0, paramsJson.toString(), null);

mAIUIAgent.sendMessage(regVoice);
```

#### 1.1.2. 资源查询

查询当前设备所注册的所有资源id

- Android示例：

```java
// 构建资源查询事件
AIUIMessage queryVoice = new AIUIMessage(AIUIConstant.CMD_VOICE_CLONE,
    AIUIConstant.VOICE_CLONE_RES_QUERY, 0, "", null);
mAIUIAgent.sendMessage(queryVoice);
```

#### 1.1.3. 资源删除

根据指定注册的资源id进行删除。

- Android示例：

```java
// 注册好的资源id
String mCurResId = "resID";

JSONObject paramsJson = new JSONObject();
paramsJson.put(AIUIConstant.KEY_RES_ID, mCurResId);
// 构建资源删除事件
AIUIMessage delVoice = new AIUIMessage(AIUIConstant.CMD_VOICE_CLONE,
        AIUIConstant.VOICE_CLONE_DEL, 0, paramsJson.toString(), null);
mAIUIAgent.sendMessage(delVoice);
```

#### 结果回调解析

- 回调结果处理（Android示例）:

```java
/**
 * AIUI 回调
 */
private final AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent aiuiEvent) {
        switch (aiuiEvent.eventType) {
            // 声音复刻：资源注册、资源查询和资源删除回调
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (aiuiEvent.arg1 == AIUIConstant.CMD_VOICE_CLONE) {
                    int retCode = aiuiEvent.arg2;
                    int dtype = aiuiEvent.data.getInt(AIUIConstant.KEY_SYNC_DTYPE, -1);
                    if (dtype == AIUIConstant.VOICE_CLONE_REG) {
                        // 声音注册结果
                        if (retCode == AIUIConstant.SUCCESS) {
                            String resId = aiuiEvent.data.getString(AIUIConstant.KEY_RES_ID, "");
                            showTip("注册成功，res_id=" + resId);
                        } else {
                            showTip("注册失败，error=" + retCode);
                        }
                    } else if (dtype == AIUIConstant.VOICE_CLONE_DEL) {
                        // 声音删除结果
                        if (retCode == AIUIConstant.SUCCESS) {
                            showTip("删除成功");
                        } else {
                            showTip("删除失败，error=" + retCode);
                        }
                    }else if (dtype == AIUIConstant.VOICE_CLONE_RES_QUERY) {
                        // 已注册声音查询结果
                        if (retCode == AIUIConstant.SUCCESS) {
                            String result = aiuiEvent.data.getString("result", "");
                            try {
                                JSONObject resultJson = new JSONObject(result);
                                if (!resultJson.isNull("data")) {
                                    JSONArray dataArray = resultJson.getJSONArray("data");
                                    if (dataArray != null) {
                                        showTip("查询结果：\n" + dataArray);
                                    } else {
                                        showTip("资源id为空");
                                    }
                                } else {
                                    showTip("没有注册资源");
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        } else {
                            showTip("查询失败，error=" + retCode + "，" + getErrorDes(retCode));
                        }
                    }
                }
            }
        }
    }
};
```

### 能力使用

#### 主动合成请求

根据资源成功后的资源id，进行主动文本合成请求。

温馨提示

通用交互大模型链路下，声音复刻主动合成**仅支持文本一帧发送**，如需流式合成，需要升级协议到极速超拟人交互链路。

声音复刻合成参数示例：

> vcn：**x5\_clone**
> res\_id：**fsdfwee234324**
> scene：**IFLYTEK.TTS（语音合成）**

- 合成请求示例（Android）：

```java
// 合成文本
String text = "您好,欢迎使用科大讯飞语音合成技术。";
byte[] textData = text.getBytes("utf-8");

// 注册好的资源id
String mCurResId = "fsdfwee234324";

// 声音复刻vcn固定x5_clone，附带res_id
String params = "vcn=x5_clone,res_id=" + mCurResId;

AIUIMessage startTTS = new AIUIMessage(AIUIConstant.CMD_TTS, AIUIConstant.START, 0,params,textData);
mAIUIAgent.sendMessage(startTTS);
```

#### 全链路合成

全链路合成使用创建的审核复刻资源，集成方式有两种：
声音复刻合成参数示例：

> vcn：**x5\_clone**
> res\_id：**fsdfwee234324**
> scene：**IFLYTEK.TTS（语音合成）**

- 在 aiui.cfg 中直接配置参数资源

```text
    // 合成参数
    // "vcn" 发音人
    // "res_id" 声音复刻资源id，仅在 vcn=x5_clone时生效
    // "play_mode" 播放模式，取值："sdk"（SDK内部播放，默认），"user"（由开发者自己播放）
    "tts":{
        "voice_name": "x5_clone",
        "res_id":"fsdfwee234324",
        "play_mode": "sdk"
    },
```

- 通过动态参数设置指定需要的合成资源

  温馨提示

  1、使用tts参数动态设置后，不区分音频和文本请求，全部生效

  2、注意发音人参数key传值区别（vcn 或 voice\_name），与aiui.cfg下tts配置项保持一致，如aiui.cfg配置文件没有传值，则任选。

```java
================================================================
    场景1：传值voice_name
================================================================
// aiui.cfg 配置文件
"tts":{
    "voice_name": "x5_lingxiaoyue_flow",
    "play_mode": "sdk"
},

// 全链路合成动态参数设置
String setParams = "{\"tts\":{\"voice_name\":\"x5_clone\",\"res_id\":\"fsdfwee234324\",\"volume\":\"50\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, setParams, null);
mAIUIAgent.sendMessage(setMsg);

================================================================
    场景2：传值vcn
================================================================
// aiui.cfg 配置文件
"tts":{
    "vcn": "x5_lingxiaoyue_flow",
    "play_mode": "sdk"
},

// 全链路合成动态参数设置
String setParams = "{\"tts\":{\"vcn\":\"x5_clone\",\"res_id\":\"fsdfwee234324\",\"volume\":\"50\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, setParams, null);
mAIUIAgent.sendMessage(setMsg);
```

#### 结果解析

AIUI SDK所有类型合成结果处理方式一致，Android 示例如下：

```java
private AIUIListener mAIUIListener = new AIUIListener() {

    @Override
    public void onEvent(AIUIEvent event) {

            case AIUIConstant.EVENT_RESULT: {
                try {
                    JSONObject bizParamJson = new JSONObject(event.info);
                    JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
                    JSONObject params = data.getJSONObject("params");
                    JSONObject content = data.getJSONArray("content").getJSONObject(0);

                    String sub = params.optString("sub");
                    if ("tts".equals(sub)) {
                        if (content.has("cnt_id")) {
                            String sid = event.data.getString("sid");
                            String cnt_id = content.getString("cnt_id");
                            byte[] audio = event.data.getByteArray(cnt_id); //合成音频数据
                            /**
                            *
                            * dts：音频块进度信息，取值：
                            * - 0（音频开始）
                            * - 1（音频中间块，可出现多次）
                            * - 2（音频结束)
                            * - 3（独立音频,合成短文本时出现）
                            *
                            * 举例说明：
                            * 常规合成dts顺序：
                            *   0 1 1 1 ... 2
                            * 短文本合成dts顺序:
                            *   3
                            **/
                            int dts = content.getInt("dts");
                            int frameId = content.getInt("frame_id");// 音频段id，取值：1,2,3,...

                            int percent = event.data.getInt("percent"); //合成进度

                            boolean isCancel = "1".equals(content.getString("cancel"));  //合成过程中是否被取消
                        }
                    }
                } catch (Throwable e) {
                    e.printStackTrace();
                }
            } break；
            default:
                break;
        }
    }
};
```
