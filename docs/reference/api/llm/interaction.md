---
title: 通用大模型交互 API
description: 通用大模型链路的 WebSocket 交互接口，支持语音和文本输入，集成语义理解与语音合成
---

## 概述

通用大模型交互 API 提供基于 WebSocket 的在线语音交互能力，适用于**通用大模型交互链路**服务场景。通过持续输入音频或文本，云端处理后返回识别、语义理解和合成结果。

- 必须符合 WebSocket 协议规范（RFC 6455）
- WebSocket 握手成功后，10 秒内未发送数据，服务端会主动断开连接
- 服务端下发错误码后，客户端应重新建立连接

## 建立连接

### 请求地址

```text
ws[s]://aiui.xf-yun.com/v2/aiint/ws
```

### 请求示例

```text
wss://aiui.xf-yun.com/v2/aiint/ws?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>
```

鉴权参数构建方式参考 [鉴权文档](./auth.md)。

### 连接成功响应

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "cid": "xxx"
    }
}
```

## 请求数据结构

请求数据由 `header`、`parameter` 和 `payload` 三部分构成。

### 完整请求示例（文本交互）

```json
{
    "header": {
        "appid": "a44e0f36",         // 应用 AppID
        "sn": "device001",           // 设备唯一标识
        "status": 3,                 // 数据状态：文本固定为 3
        "stmid": "text-1",           // 会话 ID
        "scene": "main_box"          // 情景模式
    },
    "parameter": {
        "nlp": {
            "sub_scene": "cbm_v45",  // 大模型引擎（固定值）
            "richness": "mid",       // 回复丰富度
            "new_session": true,     // 是否清除会话历史
            "nlp": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            }
        },
        "tts": {
            "vcn": "x4_lingxiaoqi_oral",  // 发音人
            "tts": {
                "encoding": "raw",
                "sample_rate": 16000,
                "channels": 1,
                "bit_depth": 16
            }
        }
    },
    "payload": {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 3,
            "text": "5L2g5aW9"      // Base64 编码的文本
        }
    }
}
```

### header 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用的 AppID | `a44e0f36` |
| sn | string | 是 | 设备（用户）唯一标识，长度不超过 32 位 | `device001` |
| status | int | 是 | 数据状态：`0`-首帧、`1`-中间帧、`2`-尾帧、`3`-一帧发完（文本固定为 3） | `3` |
| stmid | string | 是 | 会话请求 ID，长度不超过 32 位 | `text-1` |
| scene | string | 是 | AIUI 应用情景模式 | `main_box` |
| msc.lat | double | 否 | 纬度，取值 -90 ~ +90 | `19.65309164` |
| msc.lng | double | 否 | 经度，取值 -180 ~ +180 | `109.25905608` |
| os_sys | string | 否 | 应用系统类型 | `windows` |

### parameter 参数

#### IAT（语音识别）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| svad | string | 否 | 云端 VAD（端点检测）开关：`1`-开、`0`-关 | `1` |
| eos | string | 否 | 音频尾端点检测时长（毫秒） | `1000` |
| vgap | string | 否 | 会话断句时长检测（毫秒） | `800` |
| speex_size | int | 否 | speex 帧大小 | `60` |
| iat.compress | string | 是 | 识别结果压缩方式 | `raw` |
| iat.format | string | 是 | 识别结果格式 | `json` |
| iat.encoding | string | 是 | 识别结果编码 | `utf8` |

#### NLP（语义理解）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| sub_scene | string | 是 | 大模型引擎，固定值 `cbm_v45` | `cbm_v45` |
| richness | string | 否 | 回复丰富度：`concise`（简洁）、`mid`（适中）、`rich`（丰富） | `mid` |
| env | string | 否 | 设备人设，JSON 格式，含 `expand_persona` 和 `persona` 字段 | — |
| new_session | boolean | 否 | 是否清除本次会话历史 | `true` |
| sn | string | 否 | 信源激活绑定设备标识，与 header 中 `sn` 保持一致 | `device001` |
| nlp.compress | string | 否 | 语义结果压缩方式 | `raw` |
| nlp.format | string | 否 | 语义结果格式 | `json` |
| nlp.encoding | string | 否 | 语义结果编码 | `utf8` |

#### TTS（语音合成）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| vcn | string | 否 | 合成发音人，使用声音复刻时固定为 `x5_clone` | `x4_lingxiaoqi_oral` |
| res_id | string | 否 | 声音复刻资源 ID，仅 `vcn=x5_clone` 时需要 | `fsdfwee234324` |
| oral_level | string | 否 | 口语化程度：`high`、`mid`、`low` | `mid` |
| tts_res_type | string | 否 | 合成结果类型，`url` 表示返回下载链接 | `url` |
| tts.bit_depth | int | 是 | 合成音频位深 | `16` |
| tts.channels | int | 是 | 合成音频通道数 | `1` |
| tts.encoding | string | 是 | 合成音频格式：`raw`（PCM）、`lame`（MP3）、`speex-wb;10`、`opus` | `raw` |
| tts.sample_rate | int | 是 | 合成音频采样率 | `16000` |

### payload 参数

#### payload.text（文本请求）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| encoding | string | 是 | 文本编码 | `utf8` |
| compress | string | 是 | 压缩方式 | `raw` |
| format | string | 是 | 数据格式 | `plain` |
| status | int | 是 | 数据状态，文本固定为 `3` | `3` |
| text | string | 是 | Base64 编码的文本 | `5L2g5aW9` |

#### payload.audio（音频请求）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| encoding | string | 是 | 音频编码：`raw`、`lame`、`speex`、`opus`、`opus-wb`、`speex-wb`、`ico` | `raw` |
| sample_rate | int | 是 | 采样率：`8000` 或 `16000` | `16000` |
| channels | int | 是 | 通道数：`1` 或 `2` | `1` |
| bit_depth | int | 是 | 位深：`8` 或 `16` | `16` |
| status | int | 是 | 数据状态：`0`-首帧、`1`-中间帧、`2`-尾帧、`3`-一帧发完 | `0` |
| frame_size | int | 是 | 帧大小：0 ~ 1024 | `0` |
| audio | string | 是 | Base64 编码的音频数据 | — |

## 响应结果

### 响应数据类型

交互过程中会返回多种类型的结果数据：

| 数据类型 | 字段路径 | 说明 |
|---|---|---|
| IAT（语音识别） | `payload.iat` | 语音识别结果 |
| cbm_tidy | `payload.cbm_tidy` | 语义规整结果（历史改写、意图拆分） |
| cbm_meta | `payload.cbm_meta` | 补充描述信息 |
| cbm_semantic | `payload.cbm_semantic` | 聚合语义结果 |
| NLP（大模型回复） | `payload.nlp` | 最终语义结果（经大模型润色） |
| TTS（语音合成） | `payload.tts` | 合成音频结果 |

### 响应示例

#### IAT（语音识别）结果

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xxx",
        "stmid": "audio-1"
    },
    "payload": {
        "iat": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "json",
            "seq": 1,
            "status": 2,
            "text": "<base64编码的识别结果>"
        }
    }
}
```

#### NLP（大模型回复）结果

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xxx",
        "stmid": "text-1"
    },
    "payload": {
        "nlp": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "json",
            "seq": 0,
            "status": 0,
            "text": "<base64编码的语义结果>"
        }
    }
}
```

NLP 结果流式下发，Base64 解码后为逐段文本。

#### TTS（语音合成）结果

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xxx"
    },
    "payload": {
        "tts": {
            "audio": "<base64编码的合成音频>",
            "bit_depth": 16,
            "channels": 1,
            "encoding": "raw",
            "sample_rate": 16000,
            "seq": 1,
            "status": 0
        }
    }
}
```

#### 错误响应

```json
{
    "header": {
        "code": 10110,
        "message": "server licence error",
        "sid": "xxx",
        "status": 2
    }
}
```

### header 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| code | int | 服务错误码，`0` 表示成功 | `0` |
| sid | string | 会话 SID | `xxx` |
| status | int | 会话状态 | `0` |
| stmid | string | 会话 ID | `text-1` |
| message | string | 返回消息描述 | `success` |

### payload 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| payload.$sub | object | 数据部分，`$sub` 为具体类型 | — |
| payload.$sub.text | string | Base64 编码的数据内容（合成结果使用 `audio` 字段） | — |
| payload.$sub.status | int | 数据状态：`0`-首帧、`1`-中间帧、`2`-末帧 | `0` |
| payload.$sub.encoding | string | 数据编码格式 | `utf8` |
| payload.$sub.seq | int | 数据段编号 | `1` |
| payload.$sub.format | string | 数据格式 | `json` |
| payload.$sub.compress | string | 数据压缩方法 | `raw` |

## 断开连接

客户端主动断开 WebSocket 连接即可结束会话。服务端在以下情况会主动断开连接：

- 握手成功后 10 秒内未发送数据
- 发生服务端错误

## cURL 等效调用示例

由于本接口使用 WebSocket 协议，以下使用 `wscat` 演示：

```bash
# 建立 WebSocket 连接
wscat -c "wss://aiui.xf-yun.com/v2/aiint/ws?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>"

# 连接成功后发送文本请求
> {"header":{"appid":"your_appid","sn":"device001","status":3,"stmid":"text-1","scene":"main_box"},"parameter":{"nlp":{"sub_scene":"cbm_v45","nlp":{"encoding":"utf8","compress":"raw","format":"json"}},"tts":{"vcn":"x4_lingxiaoqi_oral","tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"text":{"encoding":"utf8","compress":"raw","format":"plain","status":3,"text":"5L2g5aW9"}}}
```
