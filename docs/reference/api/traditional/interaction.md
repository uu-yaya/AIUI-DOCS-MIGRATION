---
title: 传统语义交互 API
description: 传统语义链路的 WebSocket 交互接口，支持语音识别、语义理解、合成和翻译能力
---

## 概述

传统语义交互 API 提供基于 WebSocket 的在线语音交互能力，适用于**传统语义交互链路**。支持语音识别、语义理解、语音合成和翻译等功能。

- 必须符合 WebSocket 协议规范（RFC 6455）
- 握手超时 60 秒，无数据超过 10 秒自动断开
- 单次会话音频不超过 60 秒，不超过 2MB，不超过 3000 帧

## 建立连接

### 请求地址

```text
ws[s]://wsapi.xfyun.cn/v1/aiui
```

### 请求示例

```text
ws://wsapi.xfyun.cn/v1/aiui?appid=xxx&checksum=xxx&param=xxx&curtime=xxx&signtype=md5
```

鉴权参数构建方式参考 [鉴权文档](./auth.md)。

### 连接成功响应

```json
{
    "action": "started",
    "code": "0",
    "data": "",
    "desc": "success",
    "sid": "awa00000001@ch27f00e2d00fe430100"
}
```

## param 业务参数

`param` 是 Base64 编码的 JSON 字符串，包含以下配置分类。

### 通用配置参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| scene | string | 是 | 情景模式 | `main_box` |
| auth_id | string | 是 | 用户唯一标识，32 位 | `d3b6d50a9f8194b...` |
| data_type | string | 是 | 数据类型：`text` 或 `audio` | `audio` |
| interact_mode | string | 否 | 交互模式：`continuous` 或 `oneshot` | `continuous` |
| close_delay | string | 否 | 关闭延迟（0 ~ 200 毫秒） | `200` |
| sn | string | 否 | 设备序列号 | `device001` |

### 语义参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| lat | string | 否 | 纬度 | `19.653` |
| lng | string | 否 | 经度 | `109.259` |
| topn | string | 否 | 多候选 | — |
| pers_param | string | 否 | 动态实体范围 JSON | `{"appid":"xxx"}` |
| clean_dialog_history | string | 否 | 清除对话历史：`user` 或 `auto` | `user` |

### 识别参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| aue | string | 否 | 音频编码：`raw`、`speex`、`speex-wb`、`opus`、`opus-wb` | `raw` |
| sample_rate | string | 否 | 采样率：`16000`（默认）或 `8000` | `16000` |
| speex_size | string | 否 | speex 帧大小 | `60` |
| result_level | string | 否 | 结果级别：`plain`（默认）或 `complete` | `plain` |
| vad_info | string | 否 | 云端 VAD（端点检测）：`end` | `end` |
| cloud_vad_eos | string | 否 | 端点静音时长（毫秒） | `1000` |
| vrto | string | 否 | 无效交互等待时间（毫秒） | `5000` |

### 合成参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| vcn | string | 是 | 发音人 | `x_xiaoyan` |
| speed | string | 否 | 语速，0 ~ 100 | `50` |
| volume | string | 否 | 音量，0 ~ 100 | `50` |
| pitch | string | 否 | 音调，0 ~ 100 | `50` |
| ent | string | 否 | 引擎类型 | `xtts` |
| tts_aue | string | 否 | 合成音频格式：`raw` 或 `lame`（MP3） | `raw` |
| tts_res_type | string | 否 | 合成结果类型：`url` 或 `url_v2` | `url` |

### 语义后合成参数

需要在 param 中设置 `context` 字段以启用合成：

```json
{
    "context": "{\"sdk_support\":[\"tts\"]}"
}
```

### 翻译参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| from | string | 是 | 源语言：`cn`、`en` | `cn` |
| to | string | 是 | 目标语言：`cn`、`en`、`ug`、`ja`、`ko`、`fr`、`es`、`ru` | `en` |

## 数据上传

### 音频数据

音频数据逐帧发送（二进制），发送完毕后发送字符串 `--end--` 标记结束。

- 建议每帧 1280 字节（采样率 16000 时）
- 发送间隔建议 40ms
- 使用 speex 编码时，上传字节数必须是 `speex_size` 的整数倍

### 文本数据

文本数据一次发送完毕，发送后立即发送 `--end--` 标记。

## 响应结果

### 响应结构

```json
{
    "action": "result",         // 动作：started / result / error / vad
    "code": "0",                // 返回码
    "data": {},                 // 结果数据
    "desc": "success",          // 描述
    "sid": "awa00000001@ch..."  // 会话 ID
}
```

### data 字段说明

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| sub | string | 业务类型：`iat`、`nlp`、`tpp`、`itrans`、`tts` | `nlp` |
| auth_id | string | 用户 ID 回传 | — |
| is_last | boolean | 该业务类型最后一条结果 | `true` |
| is_finish | boolean | 本次会话最后一条结果 | `true` |
| result_id | int | 结果序号 | `1` |

### IAT（语音识别）结果

#### 简洁模式（result_level=plain）

```json
{
    "action": "result",
    "code": "0",
    "data": {
        "sub": "iat",
        "auth_id": "xxx",
        "text": "今天星期几",
        "result_id": 1,
        "is_last": true,
        "is_finish": true
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

#### 完整模式（result_level=complete）

```json
{
    "action": "result",
    "code": "0",
    "data": {
        "sub": "iat",
        "auth_id": "xxx",
        "text": {
            "sn": 1,
            "ls": false,
            "bg": 0,
            "ed": 0,
            "ws": [
                {"bg": 0, "cw": [{"sc": 0, "w": "今天"}]},
                {"bg": 0, "cw": [{"sc": 0, "w": "星期几"}]}
            ]
        },
        "result_id": 1,
        "is_last": true,
        "is_finish": true
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

### NLP（语义理解）结果

```json
{
    "action": "result",
    "code": "0",
    "data": {
        "sub": "nlp",
        "auth_id": "xxx",
        "intent": {
            "answer": {
                "text": "今天是3月1日",
                "type": "T"
            },
            "operation": "ANSWER",
            "rc": 0,
            "service": "datetime",
            "text": "今天星期几"
        },
        "result_id": 1,
        "is_last": true,
        "is_finish": true
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

### TTS（语音合成）结果

```json
{
    "action": "result",
    "code": "0",
    "data": {
        "sub": "tts",
        "auth_id": "xxx",
        "content": "<base64编码的音频数据>",
        "result_id": 0,
        "json_args": {
            "cancel": "0",
            "dte": "raw",          // 音频编码格式
            "dts": 1,              // 0-开始 1-中间 2-结束 3-短音频结束
            "frame_id": 59,        // 音频段 ID
            "text_percent": 11     // 合成进度百分比
        },
        "is_last": true,
        "is_finish": true
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

### TTS json_args 字段

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| dte | string | 合成音频编码格式 | `raw` |
| dts | int | 数据状态：`0`-开始、`1`-中间、`2`-结束、`3`-短音频结束 | `1` |
| frame_id | int | 音频段 ID | `59` |
| text_percent | int | 合成进度百分比 | `11` |
| cancel | string | 是否已取消 | `0` |
| text_end | int | 已合成文本的结束位置（UTF-16） | `220` |

### VAD（端点检测）事件

```json
{
    "action": "vad",
    "code": "0",
    "data": {
        "vad_info": "end"
    },
    "desc": "success",
    "sid": "awa00000001@ch..."
}
```

### 错误响应

```json
{
    "action": "error",
    "code": "10205",
    "data": "",
    "desc": "websocket read error|read dispatch data error: i/o timeout",
    "sid": "awa00000003@ch..."
}
```

## cURL 等效调用示例

```bash
APPID="your_appid"
API_KEY="your_apikey"
CURTIME=$(date +%s)

# 文本交互 param
PARAM=$(echo -n '{"auth_id":"test_user","data_type":"text","scene":"main_box","result_level":"plain","context":"{\"sdk_support\":[\"iat\",\"nlp\",\"tts\"]}"}' | base64)

# 计算 checksum
CHECKSUM=$(echo -n "${API_KEY}${CURTIME}${PARAM}" | md5sum | awk '{print $1}')

# 建立 WebSocket 连接
wscat -c "ws://wsapi.xfyun.cn/v1/aiui?appid=${APPID}&checksum=${CHECKSUM}&param=${PARAM}&curtime=${CURTIME}&signtype=md5"

# 连接成功后发送文本
> 今天天气怎么样
> --end--
```
