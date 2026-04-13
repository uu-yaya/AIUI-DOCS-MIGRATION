---
title: 回调解析说明
description: AIUI SDK 回调方式和事件解析概述，包括各类回调事件类型说明。
---

## 概述

AIUI 回调解析是 SDK 使用中的重要部分，包含回调方式和事件解析两个核心内容。

## AIUI SDK 回调方式

AIUI SDK 交互中所有结果都是通过初始化时传入的回调对象 `AIUIListener` 进行数据抛出，端侧做 `AIUIEvent` 事件解析，监听各项结果输出即可。

开发者常见可处理的结果回调事件类型（`event.eventType`）：

| 事件类型 | 说明 |
| --- | --- |
| EVENT_CONNECTED_TO_SERVER | 服务链接成功 |
| EVENT_WAKEUP | 唤醒结果 |
| EVENT_RESULT | 语音交互结果 |
| EVENT_VAD | VAD（端点检测）状态 |
| EVENT_STATE | SDK 状态 |
| EVENT_TTS | 托管 SDK 播放器状态 |
| EVENT_CMD_RETURN | 个性化数据使用 |
| EVENT_ERROR | SDK 报错 |

## 事件解析示例

- [Android 事件解析](./android) — 完整的 Android 平台事件回调解析示例
- [iOS / Windows / Linux 事件解析](./ios-windows-linux) — iOS / Windows / Linux 平台交互结果解析示例
