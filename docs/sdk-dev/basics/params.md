---
title: 参数配置说明
---

AIUI基础参数概述

AIUI SDK工作时，先通过读取配置文件（aiui.cfg）加载内置的参数进行初始化工作。配置文件参数设置属于**静态参数设置**，SDK加载后本地默认构建参数结构体，每次会话进行携带。当用户需要再对话过程中对业务参数进行动态修改时，AIUI SDK也提供**动态参数设置**方式。

温馨提示

动态参数设置仅支持交互服务业务相关参数设置，SDK非业务参数不支持动态修改，例如appid等信息。

## AIUI静态基础参数设置

AIUI SDK基础参数主要分为以下模块：

- 登录参数：login
- 全局参数：global
- 交互控制参数：interact
- 业务参数：speech
- 本地vad参数：VAD（端点检测）
- 用户自定义参数：userparams
- 音频交互参数：audioparams
- 语音识别参数：IAT（语音识别）
- 语音合成参数：TTS（语音合成）
- 语音唤醒：ivw
- 录音控制参数：recorder
- SDK日志设置参数：log

### 1.1. 配置文件示例

AIUI初始化时会读取cfg配置，格式是json，参数如下：

```json
{
    "login":{
        "appid": "",
        "key":"",
        "api_secret": ""
    },
    "global":{
        "scene":"main_box",
        "clean_dialog_history":"auto",
        /* 1：传统语义 、2：通用大模型、3：极速超拟人 */
        "aiui_ver": "1"
    },
    "interact":{
        "interact_timeout":"60000",
        "result_timeout":"5000"
    },
    "speech":{
        "data_source": "sdk",
        "wakeup_mode": "vtn",
        "interact_mode": "oneshot",
        "work_mode": "intent",
        "audio_source": 7
    },
    "vad":{
        "vad_enable":"1",
        "engine_type":"evad",
        "res_type":"assets",
        "res_path":"vad/evad_16k.jet",
        "vad_bos":"5000",
        "vad_eos":"1000",
        "threshold":"0.7",
        "speech_timeout":"5000"
    },
    /* 用户参数，透传到后处理(非必须)*/
    "userparams":{
        "xxxx": "xxx" //自定义键值对参数或json数据
    },
    /*音频交互参数*/
    "audioparams":{
        "msc.lng": "117.16334474",  // 经度
        "msc.lat":"31.82102191"     // 纬度
    },
    // 识别（音频输入）参数
    "iat":{
        "sample_rate":"16000"
    },
    // 合成和播报参数
    "tts": {
        "engine_type": "cloud",
        "vcn": "x2_xiaojuan",
        "play_mode": "sdk",
        "buffer_time": "0",
        "stream_type": "3",
        "audio_focus": "0"
    },
    // 唤醒参数
    "ivw":{
        "mic_type": "mic1",
        "res_type": "path",
        "res_path": "/sdcard/AIUI/ivw/vtn/vtn.ini"
    },
    // 录音参数
     "recorder":{
         "channel_count": 1,
         "channel_filter": "0,-1"
     },
    /* 日志设置
    "log": {
        "debug_log": "0",
        "save_datalog": "0",
        "datalog_path": "",
        "datalog_size": 1024,
        "raw_audio_path": ""
    }
}
```

### 1.2. 配置字段说明

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **模块名称** | | **模块说明** | | |
| **模块名称** | **模块说明** | **参数名称** | **是否必传** | **参数和取值说明** |
| **login** | 登录参数 | AppID | 是 | AIUI应用信息appid |
| key | 否 | AIUI应用信息appKey |
| API\_secret | 否 | AIUI应用信息apiSecret |
| **global** | 全局参数 | scene | 是 | AIUI应用情景模式 |
| aiui\_ver | 否 | **AIUI交互链路指定** 1：传统语义链路 2：大模型语义链路（6.6.xxx及以上版本支持） 3：极速超拟人链路（6.8.xxx及以上版本支持） |
| clean\_dialog\_history | 否 | **清除交互历史设置** auto：自动清除历史（默认模式） user：用户手动清除历史 |
| **interact** | 交互控制参数 | interact\_timeout | 否 | **交互超时(单位：ms)** 即唤醒之后，如果在这段时间内无有效交互则重新进入待唤醒状态， 取值：[10000,180000)。 默认为1min。 |
| result\_timeout | 否 | **结果超时(单位：ms)** 即检测到语音后端点后一段时间内无结果返回则抛出10120错误码。 默认值：5000。 |
| **speech** | 业务相关参数 | data\_source | 是 | **录音数据来源配置** SDK：sdk内部录音 user： 外部录音 |
| wakeup\_mode | 否 | **唤醒设置** off：关闭唤醒 vtn：vtn2.0版本唤醒开关 |
| interact\_mode | 是 | **交互模式设置** continuous：持续交互，对于语音即“一次唤醒，多次交互” Oneshot（单轮交互）：（默认模式）一次交互，对于语音即“一次唤醒，一次交互” |
| work\_mode | 否 | **SDK工作模式设置** intent：默认取值，SDK进行音频数据上传获取交互意图 rec\_only：只录音，开发者仅需要语音唤醒时可配 |
| audio\_source | 否 | **系统录音设置：Android系统配置** 1：对应安卓的AudioSource取值为MIC 7：（安卓的AudioSource取值为VOICE\_COMMUNICATION（带回声消除，但某些机型不支持） |
| audio\_captor | 否 | **音频源设置** system：系统录音 portaudio：设备具有独立声卡时配置成portaudio，仅支持windows/linux平台 |
| **VAD（端点检测）** | 音频端点检测参数 | VAD（端点检测）\_enable | 是 | **VAD启用设置** 1：(默认参数)开启vad 0：关闭vad |
| engine\_type | 是 | **VAD引擎类型** 取值有 meta、evad，注意该参数与实际加载的vad资源要对应 |
| res\_type | 是 | **VAD资源类型** 使用模型vad时必须设置，取值说明如下 assets：assets资源（apk工程的assets文件） res：res资源（apk工程的res文件） path：path资源（sdcard文件） |
| res\_path | 是 | **VAD资源文件路径** 使用模型vad时必须设置。 |
| VAD（端点检测）\_bos | 否 | **VAD前端超时时间** 单位：毫秒 取值范围：[1000,10000] 默认值： "5000" |
| VAD（端点检测）\_eos | 否 | **VAD后端超时时间** 单位：毫秒 取值范围：[0,10000] 默认值："1000" |
| cloud\_vad\_eos | 否 | **云端VAD后端超时时间** 单位：毫秒 示例 "3000" |
| cloud\_vad\_gap | 否 | **云端VAD分句间隔** 单位：毫秒 示例 "400" |
| threshold | 否 | **VAD检测阈值** 控制VAD模块检测程度的，取值范围[0.1,0.9]， 值越大越难触发vad |
| speech\_timeout | 否 | **对话超时时间** VAD（端点检测）\_bos开始说话时计时，超过设置的时间自动结束对话并回调vad\_eos，单位：毫秒，示例 "500"（默认值60000） |
| **userparams** | 用户自定义参数 | 用户自定义key | 否 | **用户自定义value** 无固定取值限制，开发者自定义健值对符合json格式即可 |
| **audioparams** | 音频透传参数 | msc.lng | 否 | **经度** 示例：117.16334474（不超过8位精度） |
| msc.lat | 否 | **纬度** 示例：31.82102191（不超过8位精度） |
| **IAT（语音识别）** | 识别音频参数 | sample\_rate | 否 | **采样率** 16000 |
| **TTS（语音合成）** | 合成和播放控制参数 | engine\_type | 否 | **主动合成引擎模型** cloud：云端合成，默认取值 local：本地合成 |
| res\_type | 否 | **离线资源加载方式，离线合成时必须配置** assets：android程序assets目录 path：外部绝对路径 |
| res\_path | 否 | **离线资源路径，离线合成时必须配置** 注意资源构建方式为,每个资源用分号隔开，可一次加载多个离线发音人资源：引擎资源;发音人;发音人…… xtts/xtts\_common.jet;xtts/xtts\_xiaoxue.jet;xtts/xtts\_xiaofeng.jet |
| vcn | 否 | **合成发音人** 在线发音人按照云端发音人传如：x2\_xiaojuan 离线发音人按照实际资源名称传如：xiaoxue |
| play\_mode | 否 | **播放控制** SDK：内部SDK托管播放（默认取值) user：外部自行播放 |
| buffer\_time | 否 | **音频缓冲时长** 当缓冲音频大于该值时才开始播放，默认值：0ms |
| stream\_type | 否 | **播放音频流类型** 取值参考AudioManager类，默认值：3 |
| audio\_focus | 否 | **播放音频时是否抢占焦点** 1：抢占焦点 0：不抢占焦点（默认值） |
| **ivw** | 语音唤醒参数 | mic\_type | 否 | **唤醒依赖库** mic1：代表托管AIUI SDK加载单麦唤醒库libvtn\_mic1.so(取值xxx，代表SDK加载 libvtn\_xxx.so), |
| res\_type | 否 | **唤醒配置文件路径读取类型** path：path资源（sdcard文件） |
| res\_path | 否 | **唤醒配置文件路劲** /sdcard/AIUI/ivw/vtn/vtn.ini |
|
| **recorder** | 音频通道参数 用唤醒时必传 | channel\_count | 否 | **通道数量** 1：单唤醒不接麦克风阵列时一般为1 |
| channel\_filter | 否 | **通道过滤参数** 0,-1：单唤醒固定取值2通道音频（从原始数据中取相应的通道组成新阵列数据：非负数字代表原始音频的通道号，-1代表填充一个全0通道） |
| **log** | 日志设置 | debug\_log | 否 | **Debug日志开关** 取值：1（打开），0（关闭），默认值：0。 日志打开时会向logcat打印调试日志。 |
| save\_datalog | 否 | **是否保存数据日志** 取值：1（打开），0（关闭），默认值：0。 打开之后会将所有上传到云端的音频和云端返回的结果保存到本地，保存的路径位于/sdcard/AIUI/data/，每一次唤醒后的交互音频都保存在此目录下wakeXX开始的文件夹下。 |
| datalog\_path | 否 | **数据日志的保存路径** 当不设置或者为空值时，使用默认值：“/sdcard/AIUI/data/”。 |
| datalog\_size | 否 | **数据日志的大小限制（单位：MB）** 取值：[-1，+∞) 默认值：-1（表示无大小限制）。 注意：设置成-1可能会造成SD卡被日志写满，从而导致AIUI性能下降，影响体验效果。 |
| raw\_audio\_path | 否 | **原始音频保存路径** 当不设置或者为空值时，使用默认值：“/sdcard/AIUI/audio/”。 |
|

## AIUI动态参数设置概述

动态参数设置核心原理就是改变AIUI SDK初始化后默认加载生成的内部参数结构相关参数取值。AIUI SDK提供固定事件（CMD\_SET\_PARAMS）来进行参数更新。
开发者在对话过程中，如果遇到相关业务处理需要更新参数可以参考下面示例进行处理。

温馨提示

1、如有动态参数设置不明确或需要更多动态参数设置，可以咨询AIUI平台技术同事。

2、由于SDK交互再首帧携带参数，如果本次对话已经进行中，动态参数设置后将在下一次对话才生效。

3、动态参数设置以后，在SDK保活期间，设置的参数将永久有效。SDK销毁或覆盖更新，参数才会回复默认或切换为新设置参数。

4、动态参数设置一般仅针对音频请求生效，文本请求需要再构建的请求参数中直接携带需要的参数。

在基础参数中，动态参数设置常用在一下参数更新中：

- 全局参数相关（global）：scene
- 语音交互相关（audioparams）：msc.lng、msc.lat
- 自定义参数相关（userparams）：自定义取值
- 全链路合成相关（audioparams）：vcn、speed（语速）、volume（音量）、pitch（语调）

不是所有参数都支持动态设置，常见如AIUI SDK启动加载的本地参数就不支持，如：

- AIUI应用秘钥参数（login配置项）
- 本地vad模块相关参数（vad配置项）
- tts播放器控制相关参数：play\_mode 等

### 2.1. **Android 示例代码**

```java
// 1. 情景模式动态设置
String setParams = "{\"global\":{\"scene\":\"main\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, setParams, null);
mAIUIAgent.sendMessage(setMsg);

// 2. 经纬度参数动态设置
// 注意经纬度取值：精确位数不要超过8位
String gpsParams = "{\"audioparams\":{\"msc.lng\":\"117.16334474\",\"msc.lat\":\"31.82102191\"}}"
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, gpsParams, null);
mAgent.sendMessage(setMsg);

// 3. 自定义参数动态设置
String userParams = "{\"userparams\":{\"k1\":\"v1\",\"k2\":\"v2\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, userParams, null);
mAgent.sendMessage(setMsg);

// 4. 云端合成发音人参数动态设置（全链路合成时指定）
String ttsParams = "{\"audioparams\":{\"vcn\":\"xxx\",\"speed\":\"50\",\"volume\":\"50\",\"pitch\":\"50\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0 , 0, ttsParams, null);
mAIUIAgent.sendMessage(setMsg);
```

### 2.2. **iOS/Linux/Windows 示例代码**

```cpp
// 1.情景模式动态设置
const char* setParams = "{\"global\":{\"scene\":\"main\"}}";
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, setParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 2. 经纬度参数动态设置
// 注意经纬度取值：精确位数不要超过8位
const char* gpsParams = "{\"audioparams\":{\"msc.lng\":\"117.16334474\",\"msc.lat\":\"31.82102191\"}}"
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, gpsParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 3. 自定义参数动态设置
const char* userParams = "{\"userparams\":{\"k1\":\"v1\",\"k2\":\"v2\"}}";
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, userParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 4. 云端合成发音人参数动态设置（全链路合成时指定）
const char* ttsParams = "{\"audioparams\":{\"vcn\":\"xxx\",\"speed\":\"50\",\"volume\":\"50\",\"pitch\":\"50\"}}";
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, ttsParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();
```
