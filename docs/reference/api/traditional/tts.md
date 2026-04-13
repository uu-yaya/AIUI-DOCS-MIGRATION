---
title: 传统语义合成能力
description: 传统语义链路下的 TTS（语音合成）调用方式，仅支持普通发音人
---

## 概述

本文档介绍在**传统语义交互链路**下使用 API 协议进行合成服务的调用方式。

> 传统语义链路仅支持**普通发音人**，不支持超拟人、极速超拟人和声音复刻发音人。如需使用高级合成能力，请使用 [通用大模型链路](../llm/tts.md) 或 [极速超拟人链路](../rapid/tts.md)。

### WebSocket 连接地址

```text
ws[s]://wsapi.xfyun.cn/v1/aiui
```

## 合成请求

### 确认参数

- 发音人（vcn）：仅支持普通发音人，如 `x2_xiaojuan`
- 情景模式（scene）：固定为 `IFLYTEK.tts`
- 数据类型（data_type）：固定为 `text`

### param 参数示例

```json
{
    "auth_id": "d3b6d50a9f8194b623b5e2d4e298c9d6",
    "data_type": "text",
    "scene": "IFLYTEK.tts",       // 合成请求固定值
    "vcn": "x2_xiaojuan",         // 普通发音人
    "volume": "50",
    "tts_aue": "raw"              // 音频格式：raw 或 lame（MP3）
}
```

### 合成参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| scene | string | 是 | 固定为 `IFLYTEK.tts` | `IFLYTEK.tts` |
| data_type | string | 是 | 固定为 `text` | `text` |
| vcn | string | 是 | 普通发音人名称 | `x2_xiaojuan` |
| speed | string | 否 | 语速，0 ~ 100 | `50` |
| volume | string | 否 | 音量，0 ~ 100 | `50` |
| pitch | string | 否 | 音调，0 ~ 100 | `50` |
| tts_aue | string | 否 | 音频格式：`raw`（PCM）或 `lame`（MP3） | `raw` |

### 数据发送

合成请求文本一次发送，发送后立即发送 `--end--` 标记结束。

## 在对话中使用合成

在对话交互中同时获取语义结果和合成音频，需要在 param 中设置 `context` 字段启用 TTS（语音合成）：

### param 参数示例

```json
{
    "auth_id": "d3b6d50a9f8194b623b5e2d4e298c9d6",
    "data_type": "text",
    "scene": "main_box",
    "result_level": "plain",
    "close_delay": "200",
    "vcn": "x2_xiaojuan",
    "tts_aue": "raw",
    "tts_res_type": "url",
    "context": "{\"sdk_support\":[\"iat\",\"nlp\",\"tts\"]}"
}
```

> `context` 中的 `sdk_support` 数组列出需要的服务类型，添加 `tts` 即可启用合成。

## 合成响应

合成结果通过 `sub=tts` 类型返回，`content` 字段为 Base64 编码的音频数据。

### 响应示例

```json
{
    "action": "result",
    "code": "0",
    "data": {
        "sub": "tts",
        "auth_id": "xxx",
        "content": "<base64编码的音频>",
        "result_id": 0,
        "json_args": {
            "cancel": "0",
            "dte": "raw",
            "dts": 1,
            "frame_id": 59,
            "text_percent": 50
        },
        "is_last": false,
        "is_finish": false
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

### json_args 字段

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| dte | string | 音频编码格式 | `raw` |
| dts | int | 数据状态：`0`-开始、`1`-中间、`2`-结束、`3`-短音频结束 | `1` |
| frame_id | int | 音频段 ID | `59` |
| text_percent | int | 合成进度百分比 | `50` |
| cancel | string | 是否已取消 | `0` |

## cURL 等效调用示例

```bash
APPID="your_appid"
API_KEY="your_apikey"
CURTIME=$(date +%s)

# 合成 param
PARAM=$(echo -n '{"auth_id":"test_user","data_type":"text","scene":"IFLYTEK.tts","vcn":"x2_xiaojuan","tts_aue":"raw"}' | base64)

# 计算 checksum
CHECKSUM=$(echo -n "${API_KEY}${CURTIME}${PARAM}" | md5sum | awk '{print $1}')

# 建立 WebSocket 连接
wscat -c "ws://wsapi.xfyun.cn/v1/aiui?appid=${APPID}&checksum=${CHECKSUM}&param=${PARAM}&curtime=${CURTIME}&signtype=md5"

# 连接成功后发送待合成文本
> 今天天气真好
> --end--
```
