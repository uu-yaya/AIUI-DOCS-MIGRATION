---
title: 流式合成
---

## 前言

`流式合成`即使用特定发音人将合成文本进行分帧发送，常用于大模型流式输出的文本合成实现。现阶段支持流式合成方式的发音人类型有：

- **`极速超拟人`**
   在极速超拟人交互链路下，所有极速超拟人都免费开放开发者使用。各极速超拟人发音人见[发音人列表](/sdk-dev/voice-list "发音人列表")说明。
- **`声音复刻`**
   声音复刻能力需要先进行资源创建，具体接口调用详见[声音复刻](/sdk-dev/ultra-chain/voice-clone "声音复刻")说明。

温馨提示

1、极速超拟人交互链路下，**普通发音人** 和 **超拟人发音人** 合成调用方式一样，调用方式见[3.3.4 语音合成](/sdk-dev/features/tts)文档说明。

2、AIUI平台支持的发音人及分类详见[3.8 发音人列表](/sdk-dev/voice-list)说明。

## 调用说明

### 确认参数

**类型1**：使用极速超拟人发音人

- vcn：**x5\_lingxiaoyue\_flow** // 聆小玥
- scene：**IFLYTEK.TTS（语音合成）** // 固定取值

**类型2**：使用声音复刻发音人

- vcn：**x5\_clone** // 固定取值
- res\_id：**fsdfwee234324** // 创建的资源id
- scene：**IFLYTEK.TTS（语音合成）** // 固定取值

### 构建请求

温馨提示

1、背景说明：AIUI SDK进行流式合成时，当发送的文本内容为空，此请求SDK会忽略。

2、现象处理：使用大模型回复文本直接进行流式合成时，注意尾帧结果为空异常判断，为空时建议使用单个标点符号进行替换

- 请求代码示例（Android）：

**`特别说明`** ：集成Android SDK做流式合成发送，还要在非首帧携带 cancel\_last=false 参数，否则SDK内部出现合成打断。

```java
/**
 * 流式合成。
 * @param text 待合成文本
 * @param cancel_last 是否合成打断（true：打断，false：不打断），该参数仅限 Android SDK使用
 * @param vcn 发音人 （当使用声音时固定取值为 x5_clone ，并携带 res_id 参数）
 * @param data_status 流状态，首帧取值：0（开始），中间帧取值：1（继续），尾帧取值：2（结束）
 * @param tag 自定义标签（非必选）
 */
void startStreamTTS(String text, String vcn, int data_status, String tag) {
    try {
        // 在输入参数中设置tag，则对应结果中也将携带该tag，可用于关联输入输出
        if（0 == data_status）{
            String params = "vcn=" + vcn + ",data_status=" + data_status + ",tag=" + tag;
        }else{
        // Android sdk非首帧，流式合成携带不打断参数
            String params = "cancel_last=false,vcn=" + vcn + ",data_status=" + data_status + ",tag=" + tag;
        }

        byte[] textData = text.getBytes("utf-8");

        AIUIMessage ttsMessage = new AIUIMessage(AIUIConstant.CMD_TTS,
            AIUIConstant.START, 0, params, textData);
        mAIUIAgent.sendMessage(ttsMessage);
    } catch (UnsupportedEncodingException e) {
        e.printStackTrace();
    }
}

/**
 * 一次完整示例。
 */
void example() {
    // 待合成分段文本
    String[] reqList = {"好嘞，","音量已经","调到一半","啦。"};

    // 极速超拟人
    String vcn = "x5_lingxiaoyue_flow";

    // 声音复刻发音人
    // String vcn = "x5_clone";
    // String res_id = "fsdfwee234324";

    int mode;
    String ttsText = null;
    for(int i=0 ; i < reqList.length ; i++){
        if (i == 0) {    // 首帧
            mode = 0;
        }else if ( i == (reqList.length-1)) { // 尾帧
            mode = 2;
        } else {    // 中间帧
            mode = 1;
        }
        // 合成文本
        ttsText = reqList[i];
        // 结束帧合成文本非空判断，使用任意标点替换一下
        if(2==mode && ttsText.isEmpty()){
            ttsText = "。";
        }
        startStreamTTS(ttsText, vcn, mode, "");
    }
}
```

## 结果解析

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
