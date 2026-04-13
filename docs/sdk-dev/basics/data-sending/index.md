---
title: 数据发送方式
description: AIUI SDK 音频和文本数据发送方式说明，包括录音配置和 CMD_WRITE 参数。
---

## 概述

AIUI 服务请求支持音频和文本两种数据类型。做音频请求时需确认音频来源：**托管 AIUI SDK 进行系统录音**，还是**外部实现录音后写入 AIUI SDK**。

## 确认录音方式

在 AIUI SDK 加载的配置文件（aiui.cfg）中，通过 `data_source` 指定录音来源，详见[参数配置说明](/sdk-dev/basics/params/)。

- **SDK** — 托管 SDK 内部录音（支持 Android、iOS、Windows）。用 `CMD_START_RECORD`、`CMD_STOP_RECORD` 控制录音开关。

```java
// 开启系统录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage startRecord = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params, null);
mAIUIAgent.sendMessage(startRecord);

// 停止系统录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage stopRecord = new AIUIMessage(AIUIConstant.CMD_STOP_RECORD, 0, 0, params, null);
mAIUIAgent.sendMessage(stopRecord);
```

- **user** — 开发者自己外部实现录音后送音频给 SDK，使用 `CMD_WRITE`、`CMD_STOP_WRITE` 通知数据写入和写入结束。

## 外部数据写入

通过 `CMD_WRITE` 事件向 AIUI 写入数据，支持文本和音频。请求参数字段说明：

| 参数名称 | 是否必传 | 参数和取值说明 |
| --- | --- | --- |
| data_type | 是 | 数据类型：`audio`=音频数据，`text`=文本数据 |
| sample_rate | 否 | 音频采样率，固定取值 16000（音频数据类型时必传） |
| msc.lng | 否 | GPS 经度信息，示例：117.16334474（不超过 8 位精度） |
| msc.lat | 否 | GPS 纬度信息，示例：31.82102191（不超过 8 位精度） |
| rec_user_data | 否 | 临时识别热词（仅在传统语义服务链路生效） |

## 示例代码

- [Android 示例](./android)
- [iOS / Windows / Linux 示例](./ios-windows-linux)
