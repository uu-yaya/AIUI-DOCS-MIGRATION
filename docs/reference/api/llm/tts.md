---
title: 通用大模型合成能力
description: 通用大模型链路下的 TTS（语音合成）调用方式，支持通用合成、超拟人合成和声音复刻合成
---

## 概述

本文档介绍在**通用大模型交互链路**下使用 API 协议进行主动合成服务的调用方式。所有合成请求均通过 WebSocket 交互协议发送。

支持的合成类型：

| 合成类型 | 发音人类别 | scene 取值 |
|---|---|---|
| 通用合成 | 普通发音人 | `IFLYTEK.tts` |
| 超拟人合成 | 超拟人发音人 | `IFLYTEK.hts` |
| 声音复刻合成 | 声音复刻发音人 | `IFLYTEK.tts` |

### WebSocket 连接地址

```text
wss://aiui.xf-yun.com/v2/aiint/ws
```

## 通用合成

使用**普通发音人**进行文本合成，合成文本一帧发送完毕。

### 请求示例

```json
{
    "header": {
        "sn": "device001",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.tts"        // 通用合成固定值
    },
    "parameter": {
        "tts": {
            "vcn": "x2_xiaojuan",      // 普通发音人
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
| scene | `IFLYTEK.tts` | 通用合成固定值 |
| header.status | `3` | 文本一帧发完 |
| vcn | 如 `x2_xiaojuan` | 普通发音人名称 |

## 超拟人合成

使用**超拟人发音人**进行文本合成。

> 与极速超拟人链路不同，通用大模型链路下超拟人合成的 `scene` 取值为 `IFLYTEK.hts`（非 `IFLYTEK.tts`）。

### 请求示例

```json
{
    "header": {
        "sn": "device001",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.hts"            // 超拟人合成固定值
    },
    "parameter": {
        "tts": {
            "vcn": "x4_lingxiaoqi_oral",   // 超拟人发音人
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

### 关键参数

| 参数名 | 取值 | 说明 |
|---|---|---|
| scene | `IFLYTEK.hts` | 超拟人合成固定值（注意与通用合成不同） |
| vcn | 如 `x4_lingxiaoqi_oral` | 超拟人发音人名称 |

## 声音复刻合成

使用**声音复刻创建的发音人**进行文本合成。使用前需通过 [声音复刻 API](./voice-clone.md) 注册获取 `res_id`。

### vcn 与复刻版本对应关系

| 复刻版本 | vcn 取值 |
|---|---|
| v4 | `x5_clone` |
| omni_v1 | `x6_clone` |

### 请求示例

```json
{
    "header": {
        "sn": "device001",           // 与资源注册 SN 保持一致
        "appid": "a44e0f36",         // 与资源注册 AppID 保持一致
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x5_clone",              // 声音复刻固定值
            "res_id": "fsdfwee234324",       // 声音复刻资源 ID
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

## 合成参数汇总

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| vcn | string | 是 | 发音人名称 | `x2_xiaojuan` |
| res_id | string | 否 | 声音复刻资源 ID（仅复刻合成时需要） | `fsdfwee234324` |
| speed | int | 否 | 语速，取值 0 ~ 100 | `50` |
| volume | int | 否 | 音量，取值 0 ~ 100 | `50` |
| pitch | int | 否 | 音调，取值 0 ~ 100 | `50` |
| tts.channels | int | 是 | 通道数 | `1` |
| tts.sample_rate | int | 是 | 采样率 | `16000` |
| tts.bit_depth | int | 是 | 位深 | `16` |
| tts.encoding | string | 是 | 音频格式：`raw`（PCM）、`lame`（MP3）、`speex-wb;10`、`opus` | `raw` |

## cURL 等效调用示例

```bash
# 建立 WebSocket 连接
wscat -c "wss://aiui.xf-yun.com/v2/aiint/ws?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>"

# 连接成功后发送通用合成请求
> {"header":{"sn":"device001","appid":"your_appid","stmid":"text-1","status":3,"scene":"IFLYTEK.tts"},"parameter":{"tts":{"vcn":"x2_xiaojuan","tts":{"channels":1,"sample_rate":16000,"bit_depth":16,"encoding":"raw"}}},"payload":{"text":{"compress":"raw","format":"plain","text":"5L2g5aW9","encoding":"utf8","status":3}}}
```
