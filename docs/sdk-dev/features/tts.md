---
title: 语音合成
---

概述

语音合成是以指定文本生成音频的能力。AIUI服务链路支持两种合成方案：

**- 全链路合成托管（语义后合成）

- 主动发送文本合成**

如需了解AIUI平台支持的发音人列表，可以查看
[发音人列表](/sdk-dev/voice-list)详细了解。

温馨提示

语义后合成开启后会对所有交互请求的相关信息进行处理，无法指定相关对话做干预。如果开发者需要端侧结合业务处理结果做播报，建议关闭语义后合成，使用主动合成方式。

## 合成调用

### 1.1. 语义后合成

语义后合成指的是在AIUI应用下开启语音合成，单次交互过程中，AIUI服务链路根据配置，将技能结果或应用后处理结果或大模型结果获取的文本内容送入合成引擎直接合成。

**使用方式**：
AIUI应用下开启语音合成配置需要发音人后即可。详见语音合成配置或回复角色配置。

|  |
| --- |
| 语义后合成开关 |
| Image 1 Image 3 |

### 1.2. 主动合成

### 概述

主动合成是SDK端构建需要的合成文本后直接发送文本合成请求，根据使用合成合成引擎不同分为：

#### 1.2.1. 在线主动合成

**发音人激活**
主动合成方式需要端侧在请求参数中指定发音人名称，故使用的发音人要先确认以激活授权。
AIUI平台提供很多免费发音人，详见[发音人列表](/sdk-dev/voice-list "发音人列表")说明。免费发音人激活方式：

- 登录到AIUI应用配置页面
- 开启语义后合成模块
- 选择需要的免费发音人，配置后即可激活发音人
- 激活发音人后按照业务需要是否保留语义后合成模块开关

**接口调用**

### 注意：

一次请求最多合成2000字

```java
// 获取待合成文本
String ttsStr = "我是要合成的文本";
// 转为二进制数据
byte[] ttsData = ttsStr.getBytes("utf-8");
// 构建合成参数，一般包含发音人、语速、音调、音量
StringBuffer params = new StringBuffer();
// 发音人，发音人列表：/sdk-dev/voice-list
params.append("vcn=x2_xiaojuan");
// 语速，取值范围[0,100]
params.append(",speed=50");
// 音调，取值范围[0,100]
params.append(",pitch=50");
// 音量，取值范围[0,100]
params.append(",volume=50");

//开始合成
AIUIMessage startTTS = new AIUIMessage(AIUIConstant.CMD_TTS,AIUIConstant.START, 0, params.toString(), ttsData);
mAIUIAgent.sendMessage(startTTS);

//取消合成
AIUIMessage cancelTTS = new AIUIMessage(AIUIConstant.CMD_TTS,AIUIConstant.CANCEL, 0, params.toString(), ttsData);
mAIUIAgent.sendMessage(cancelTTS);

//暂停播放
AIUIMessage pauseTTS = new AIUIMessage(AIUIConstant.CMD_TTS,AIUIConstant.PAUSE, 0, params.toString(), ttsData);
mAIUIAgent.sendMessage(pauseTTS);

//恢复播放
AIUIMessage resumeTTS = new AIUIMessage(AIUIConstant.CMD_TTS,AIUIConstant.RESUME, 0, params.toString(), ttsData);
mAIUIAgent.sendMessage(resumeTTS);
```

#### 1.2.2. 离线主动合成

#### 1.2.2.1. 获取SDK

AIUI平台应用下下载的通用SDK开发包，默认仅支持在线语音交互能力【唤醒除外】，需要支持离线合成SDK，需要联系讯飞商务申请，申请方式有：

- 方式1：邮件联系[技术支持](mailto:aiui_support@iflytek.com)说明需求，并提供有效信息
  - 公司名称
  - 联系人方式
  - 产品需求描述
  - AIUI应用appid信息
- 方式2：添加AIUI QQ交流群（575396706）联系讯飞技术同事咨询。

获取支持离线合成能力SDK后，AIUI输出的资源包中，一般包含两部分：

- 开启了离线能力的SDK原始库
- 绑定appid的离线合成引擎资源（xtts\_common.jet）、离线发音人资源(例如 xtts\_xiaoxue.jet)

#### 1.2.2.2. 参数配置

`aiui.cfg`中增加离线合成相关配置，多个发音人用 `;` 分割。

```java
"tts":{
    // 使用xtts
    "ent": "xtts",
    // 离线引擎
    "engine_type": "local",
    // 资源类型
    "res_type": "assets",
    //配置发音人
    "res_path": "xtts/xtts_common.jet;xtts/xtts_xiaoxue.jet"
},
```

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **模块名称** | | **模块说明** | | |
| **模块名称** | **模块说明** | **参数名称** | **是否必传** | **参数和取值说明** |
| **TTS（语音合成）** | 合成参数 | ent | 是 | **合成引擎类型** 固定取值 xtts |
| engine\_type | 是 | **合成服务类型** cloud：在线合成 local：离线合成 |
| res\_type | 是 | **离线合成资源加载方式** assets：assets资源路径（apk工程的assets文件） path：path资源路径（sdcard文件） |
| res\_path | 是 | **离线合成资源文件路径** 先配置合成引擎资源，在配置合成发音人资源（可多个），每个资源用；隔开 例：xtts/xtts\_common.jet;xtts/xiaoxue.jet;xtts/xiaofeng.jet |

#### 1.2.2.3. 接口调用

与在线主动合成调用方式一致，重点需要注意离线发音人资源名称取值不要弄错

温馨提示

离线发音人资源名称在讯飞提供的资源文件中会表明，如 xtts\_xiaoxue.jet 对应的发音人即 xiaoxue。

```java
// 获取待合成文本
String ttsStr = "我是要合成的文本";
// 转为二进制数据
byte[] ttsData = ttsStr.getBytes("utf-8");
// 构建合成参数，一般包含发音人、语速、音调、音量
StringBuffer params = new StringBuffer();
// 离线发音人
params.append("vcn=xiaoxue");

//离线主动合成
AIUIMessage startTTS = new AIUIMessage(AIUIConstant.CMD_TTS,AIUIConstant.START, 0, params.toString(), ttsData);
mAIUIAgent.sendMessage(startTTS);
```

## 结果解析

AIUI SDK在EVENT\_RESULT回调抛出合成音频和缓存进度，默认合成音频格式为`16k 16bit pcm`，Android 示例如下：

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

## 播放处理

### 3.1. 播放处理参数配置

AIUI SDK通过配置参数`tts`下的`play_mode`配置项来指定合成音频播报处理方式：

- `sdk` 代表托管AIUI SDK调用系统播放器进行合成音频播报
- `user` 代表SDK不进行合成音频处理，开发者外部自行处理合成音频数据

aiui.cfg配置示例：

```json
{
    "tts": {
        // 播放模式：sdk（sdk播放，默认，只支持安卓），user（开发者自己播放）
        "play_mode": "sdk",
        // 音频缓冲时长：缓冲音频大于buffer_time才播放，默认0ms
        "buffer_time": "0",
        // 音频类型，取值参考AudioManager类，默认值:3
        "stream_type": "3",
        // 播放是否抢占焦点：1（抢占), 0（不抢占，默认）
        "audio_focus": "0"
    }
}
```

### 3.2. 托管系统播报时播放状态

当配置播放模式`play_mode`取值为`sdk`时，`Android`端系统回调状态信息如下：

```java
private AIUIListener mAIUIListener = new AIUIListener() {

    @Override
    public void onEvent(AIUIEvent event) {

            case AIUIConstant.EVENT_TTS: {
                switch (event.arg1) {
                    case AIUIConstant.TTS_SPEAK_BEGIN:
                        showTip("开始播放");
                        break;

                    case AIUIConstant.TTS_SPEAK_PROGRESS:
                        showTip("缓冲进度为" + mTtsBufferProgress +
                                ", 播放进度为" + event.data.getInt("percent"));     // 播放进度
                        break;

                    case AIUIConstant.TTS_SPEAK_PAUSED:
                        showTip("暂停播放");
                        break;

                    case AIUIConstant.TTS_SPEAK_RESUMED:
                        showTip("恢复播放");
                        break;

                    case AIUIConstant.TTS_SPEAK_COMPLETED:
                        showTip("播放完成");
                        break;

                    default:
                        break;
                }
            } break;

            default:
                break;
        }
    }
};
```

## 过滤合成标记

部分技能结果的回复语文本中包含`[n1]`、`[k1]`等TTS发音辅助标识，可参考以下方法进行过滤消除。

```java
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class TTSUtil {
    static String REPLACE_NULL = "";
    static String REGEX_TTS_ASSIST_TAG = "\\[[a-z]\\d\\]";
    public static void main(String[] args) {
        System.out.println(removeTTSAssistTag("The [a1] dog says meow."));
    }
    public static String removeTTSAssistTag(String text){

        Pattern regex = Pattern.compile(REGEX_TTS_ASSIST_TAG);
        Matcher input =  regex.matcher(text);
        text =  input.replaceAll(REPLACE_NULL);
        return text;
    }
}
```
