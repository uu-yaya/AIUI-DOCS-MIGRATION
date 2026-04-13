---
title: 极速超拟人合成能力
description: 极速超拟人链路下的 TTS（语音合成）调用方式，支持通用、超拟人、声音复刻和流式合成
---

## 概述

本文档介绍在**极速超拟人交互链路**下使用 API 协议进行主动合成服务的调用方式。所有合成请求均通过 WebSocket 交互协议发送。

支持的合成类型：

| 合成类型 | 发音人类别 | 文本发送方式 |
|---|---|---|
| 通用合成 | 普通发音人 | 一帧发送 |
| 超拟人合成 | 超拟人发音人 | 一帧发送 |
| 声音复刻合成 | 声音复刻发音人 | 一帧发送 / 分帧发送 |
| 极速超拟人合成 | 极速超拟人发音人 | 一帧发送 / 分帧发送 |
| 流式合成 | 极速超拟人 / 声音复刻 | 分帧发送 |

> 流式合成能力仅支持**极速超拟人发音人**和**声音复刻发音人**。

## 通用合成

使用**普通发音人**进行文本合成，合成文本一帧发送完毕。

普通发音人除部分免费外，其他需联系讯飞商务授权。

### 请求示例

```json
{
    "header": {
        "sn": "device001",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "interact_mode": "oneshot",    // 文本请求固定 oneshot
        "status": 3,
        "scene": "IFLYTEK.tts"        // 合成请求固定值
    },
    "parameter": {
        "tts": {
            "vcn": "x2_xiaojuan",      // 普通发音人
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",  // Base64 编码的待合成文本
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

### 关键参数

| 参数名 | 取值 | 说明 |
|---|---|---|
| scene | `IFLYTEK.tts` | 合成请求固定值 |
| interact_mode | `oneshot` | 文本请求固定值 |
| header.status | `2` 或 `3` | 与 `payload.text.status` 保持一致 |
| vcn | 如 `x2_xiaojuan` | 普通发音人名称 |

## 超拟人合成

使用**超拟人发音人**进行文本合成，合成文本一帧发送完毕。极速超拟人链路下所有超拟人发音人免费开放。

### 请求示例

```json
{
    "header": {
        "sn": "device001",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "interact_mode": "oneshot",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x4_lingxiaoqi_oral",  // 超拟人发音人
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

## 声音复刻合成

使用**声音复刻创建的发音人**进行文本合成。支持一帧发送和分帧发送（流式合成）。

使用前需通过 [声音复刻 API](./voice-clone.md) 注册获取 `res_id`。

### vcn 与复刻版本对应关系

| 复刻版本 | vcn 取值 |
|---|---|
| v4 | `x5_clone` |
| omni_v1 | `x6_clone` |

### 请求示例（一帧发送）

```json
{
    "header": {
        "sn": "device001",           // 与资源注册 SN 保持一致
        "appid": "a44e0f36",         // 与资源注册 AppID 保持一致
        "stmid": "text-1",
        "interact_mode": "oneshot",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x5_clone",              // 声音复刻固定值
            "res_id": "fsdfwee234324",       // 声音复刻资源 ID
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

## 极速超拟人合成

使用**极速超拟人发音人**进行文本合成。支持一帧发送和分帧发送（流式合成）。极速超拟人链路下所有极速超拟人发音人免费开放。

### 请求示例（一帧发送）

```json
{
    "header": {
        "sn": "device001",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "interact_mode": "oneshot",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x5_lingxiaoyue_flow",  // 极速超拟人发音人
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

## 流式合成

使用极速超拟人发音人或声音复刻发音人对合成文本进行分帧发送，常用于大模型流式输出的文本合成场景。

### 协议要点

- `header.status` 和 `payload.text.status` 保持一致：首帧 `0`，中间帧 `1`，尾帧 `2`
- 与交互协议中间帧可省略参数不同，**流式合成每一帧都需要携带 `parameter`**
- `stmid` 在整个流式合成过程中保持不变

### 数据流示例

假设合成文本分段为：`"好嘞，"` `"音量已经"` `"调到一半"` `"啦。"`

```text
建立 WebSocket 连接

# 首帧 (header.status=0, payload.text.status=0)
{
  "header": {"appid":"6bd8c032","sn":"device001","stmid":"text-1",
    "interact_mode":"oneshot","status":0,"scene":"IFLYTEK.tts"},
  "parameter": {"tts":{"vcn":"x5_lingxiaoyue_flow","volume":100,
    "tts":{"sample_rate":16000,"channels":1,"encoding":"lame","bit_depth":16},
    "pitch":50,"speed":50}},
  "payload": {"text":{"format":"plain","text":"5aW95Zie77yM",
    "encoding":"utf8","status":0}}
}

# 中间帧 (header.status=1, payload.text.status=1)
{
  "header": {"appid":"6bd8c032","sn":"device001","stmid":"text-1",
    "interact_mode":"oneshot","status":1,"scene":"IFLYTEK.tts"},
  "parameter": {"tts":{...}},  // 每帧必须携带完整 parameter
  "payload": {"text":{"format":"plain","text":"6Z+z6YeP5bey57uP",
    "encoding":"utf8","status":1}}
}

# 尾帧 (header.status=2, payload.text.status=2)
{
  "header": {"appid":"6bd8c032","sn":"device001","stmid":"text-1",
    "interact_mode":"oneshot","status":2,"scene":"IFLYTEK.tts"},
  "parameter": {"tts":{...}},
  "payload": {"text":{"format":"plain","text":"5ZWm44CC",
    "encoding":"utf8","status":2}}
}
```

## 合成参数汇总

所有合成类型共用以下 TTS（语音合成）参数：

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| vcn | string | 是 | 发音人名称 | `x5_lingxiaoyue_flow` |
| res_id | string | 否 | 声音复刻资源 ID（仅复刻合成时需要） | `fsdfwee234324` |
| speed | int | 否 | 语速，取值 0 ~ 100 | `50` |
| volume | int | 否 | 音量，取值 0 ~ 100 | `50` |
| pitch | int | 否 | 音调，取值 0 ~ 100 | `50` |
| tts.channels | int | 是 | 通道数 | `1` |
| tts.sample_rate | int | 是 | 采样率：`8000` 或 `16000` | `16000` |
| tts.bit_depth | int | 是 | 位深 | `16` |
| tts.encoding | string | 是 | 音频格式：`raw`（PCM）、`lame`（MP3）、`opus`（8k）、`opus-wb`（16k） | `raw` |

## cURL 等效调用示例

由于合成请求通过 WebSocket 协议发送，以下使用 `wscat` 演示文本合成调用：

```bash
# 建立 WebSocket 连接
wscat -c "wss://aiui.xf-yun.com/v3/aiint/sos?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>"

# 连接成功后发送合成请求（通用合成示例）
> {"header":{"sn":"device001","appid":"your_appid","stmid":"text-1","interact_mode":"oneshot","status":3,"scene":"IFLYTEK.tts"},"parameter":{"tts":{"vcn":"x2_xiaojuan","speed":50,"volume":50,"pitch":50,"tts":{"channels":1,"sample_rate":16000,"bit_depth":16,"encoding":"raw"}}},"payload":{"text":{"compress":"raw","format":"plain","text":"5L2g5aW9","encoding":"utf8","status":3}}}
```
