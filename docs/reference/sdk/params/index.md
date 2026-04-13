---
title: 参数配置说明
description: AIUI SDK 静态参数（aiui.cfg）和动态参数设置的完整配置说明。
---

## 概述

AIUI SDK 工作时，先通过读取配置文件（aiui.cfg）加载内置参数进行初始化工作。配置文件参数设置属于**静态参数设置**，SDK 加载后本地默认构建参数结构体，每次会话携带。当用户需要在对话过程中对业务参数进行动态修改时，AIUI SDK 也提供**动态参数设置**方式。

::: tip 温馨提示
动态参数设置仅支持交互服务业务相关参数，SDK 非业务参数不支持动态修改，例如 AppID 等信息。
:::

## AIUI 静态基础参数设置

AIUI SDK 基础参数主要分为以下模块：

- 登录参数：login
- 全局参数：global
- 交互控制参数：interact
- 业务参数：speech
- 本地 VAD（端点检测）参数：vad
- 用户自定义参数：userparams
- 音频交互参数：audioparams
- 语音识别参数：iat
- 语音合成参数：tts
- 语音唤醒：ivw
- 录音控制参数：recorder
- SDK 日志设置参数：log

### 配置文件示例

AIUI 初始化时会读取 cfg 配置，格式为 JSON：

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
    "userparams":{
        "xxxx": "xxx"
    },
    "audioparams":{
        "msc.lng": "117.16334474",
        "msc.lat":"31.82102191"
    },
    "iat":{
        "sample_rate":"16000"
    },
    "tts": {
        "engine_type": "cloud",
        "vcn": "x2_xiaojuan",
        "play_mode": "sdk",
        "buffer_time": "0",
        "stream_type": "3",
        "audio_focus": "0"
    },
    "ivw":{
        "mic_type": "mic1",
        "res_type": "path",
        "res_path": "/sdcard/AIUI/ivw/vtn/vtn.ini"
    },
    "recorder":{
        "channel_count": 1,
        "channel_filter": "0,-1"
    },
    "log": {
        "debug_log": "0",
        "save_datalog": "0",
        "datalog_path": "",
        "datalog_size": 1024,
        "raw_audio_path": ""
    }
}
```

### 配置字段说明

| 模块名称 | 模块说明 | 参数名称 | 是否必传 | 参数和取值说明 |
| --- | --- | --- | --- | --- |
| **login** | 登录参数 | appid | 是 | AIUI 应用信息 AppID |
| | | key | 否 | AIUI 应用信息 APIKey |
| | | api_secret | 否 | AIUI 应用信息 APISecret |
| **global** | 全局参数 | scene | 是 | AIUI 应用情景模式 |
| | | aiui_ver | 否 | AIUI 交互链路指定：1=传统语义链路，2=大模型语义链路，3=极速超拟人链路 |
| | | clean_dialog_history | 否 | 清除交互历史设置：auto=自动清除（默认），user=用户手动清除 |
| **interact** | 交互控制参数 | interact_timeout | 否 | 交互超时（单位：ms），唤醒后无有效交互则重新进入待唤醒状态，取值 [10000,180000)，默认 60000 |
| | | result_timeout | 否 | 结果超时（单位：ms），检测到语音后端点后无结果返回则抛出 10120 错误码，默认 5000 |
| **speech** | 业务相关参数 | data_source | 是 | 录音数据来源：sdk=SDK 内部录音，user=外部录音 |
| | | wakeup_mode | 否 | 唤醒设置：off=关闭唤醒，vtn=VTN 2.0 版本唤醒 |
| | | interact_mode | 是 | 交互模式：continuous=持续交互，oneshot=一次交互（默认） |
| | | work_mode | 否 | 工作模式：intent=默认，rec_only=只录音 |
| | | audio_source | 否 | Android 系统录音配置：1=MIC，7=VOICE_COMMUNICATION |
| | | audio_captor | 否 | 音频源设置：system=系统录音，portaudio=独立声卡（仅 Windows / Linux） |
| **vad** | 端点检测参数 | vad_enable | 是 | VAD 启用：1=开启（默认），0=关闭 |
| | | engine_type | 是 | VAD 引擎类型：meta、evad |
| | | res_type | 是 | VAD 资源类型：assets、res、path |
| | | res_path | 是 | VAD 资源文件路径 |
| | | vad_bos | 否 | VAD 前端超时时间（ms），取值 [1000,10000]，默认 5000 |
| | | vad_eos | 否 | VAD 后端超时时间（ms），取值 [0,10000]，默认 1000 |
| | | cloud_vad_eos | 否 | 云端 VAD 后端超时时间（ms） |
| | | cloud_vad_gap | 否 | 云端 VAD 分句间隔（ms） |
| | | threshold | 否 | VAD 检测阈值，取值 [0.1,0.9]，值越大越难触发 |
| | | speech_timeout | 否 | 对话超时时间（ms），默认 60000 |
| **userparams** | 用户自定义参数 | 自定义 key | 否 | 自定义 value，符合 JSON 格式即可 |
| **audioparams** | 音频透传参数 | msc.lng | 否 | 经度，示例：117.16334474 |
| | | msc.lat | 否 | 纬度，示例：31.82102191 |
| **iat** | 识别音频参数 | sample_rate | 否 | 采样率：16000 |
| **tts** | 合成和播放控制参数 | engine_type | 否 | 合成引擎：cloud=云端（默认），local=本地 |
| | | vcn | 否 | 合成发音人 |
| | | play_mode | 否 | 播放控制：sdk=SDK 托管播放（默认），user=外部自行播放 |
| | | buffer_time | 否 | 音频缓冲时长（ms），默认 0 |
| | | stream_type | 否 | 播放音频流类型，默认 3 |
| | | audio_focus | 否 | 播放时是否抢占焦点：1=抢占，0=不抢占（默认） |
| **ivw** | 语音唤醒参数 | mic_type | 否 | 唤醒依赖库，如 mic1 |
| | | res_type | 否 | 唤醒配置文件路径读取类型：path |
| | | res_path | 否 | 唤醒配置文件路径 |
| **recorder** | 音频通道参数 | channel_count | 否 | 通道数量 |
| | | channel_filter | 否 | 通道过滤参数 |
| **log** | 日志设置 | debug_log | 否 | Debug 日志开关：1=打开，0=关闭（默认） |
| | | save_datalog | 否 | 是否保存数据日志：1=打开，0=关闭（默认） |
| | | datalog_path | 否 | 数据日志保存路径，默认 /sdcard/AIUI/data/ |
| | | datalog_size | 否 | 数据日志大小限制（MB），-1=无限制（默认） |
| | | raw_audio_path | 否 | 原始音频保存路径，默认 /sdcard/AIUI/audio/ |

## AIUI 动态参数设置

动态参数设置的核心原理是通过 `CMD_SET_PARAMS` 事件改变 AIUI SDK 初始化后的内部参数结构。

::: tip 温馨提示
1. 动态参数设置后将在下一次对话才生效（当前对话已携带参数）。
2. SDK 保活期间设置的参数永久有效，SDK 销毁或覆盖更新后参数恢复默认。
3. 动态参数设置一般仅针对音频请求生效，文本请求需在构建的请求参数中直接携带。
:::

常用动态参数：

- 全局参数（global）：scene
- 音频交互参数（audioparams）：msc.lng、msc.lat
- 自定义参数（userparams）：自定义取值
- 全链路合成参数（audioparams）：vcn、speed、volume、pitch

不支持动态设置的参数：

- AIUI 应用密钥参数（login 配置项）
- 本地 VAD 模块相关参数（vad 配置项）
- TTS 播放器控制相关参数（play_mode 等）

## 动态参数设置示例

- [Android 示例](./android)
- [iOS / Windows / Linux 示例](./ios-windows-linux)
