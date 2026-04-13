---
title: 消息事件说明
description: AIUI SDK 请求事件（AIUIMessage）和回调事件（AIUIEvent）的消息类型详解
---

## 概述

本章节详细介绍请求事件和回调事件对应的内部消息类型。AIUI SDK 做请求发送和结果接受时，分别通过下面两个事件来进行详细区分：

**请求事件：** 通过构建不同的 AIUIMessage 进行发送，来实现不同的消息指令请求。

**回调事件：** 通过解析回调中 AIUIEvent 不同类型，可以获取 AIUI SDK 抛出的状态或结果。

## AIUIMessage

通过 AIUIMessage 向 SDK 发送指令，通过 AIUIEvent 获取 SDK 事件回调。

:::tip 提示
有返回值的消息类型，代表向 AIUI 发送该消息后，AIUI 会抛出 EVENT_CMD_RETURN 事件返回结果。
:::

| msgType（消息类型） | 取值 | 返回值 | 说明 |
| --- | --- | --- | --- |
| CMD_GET_STATE | 1 | 有 | **获取[交互状态](/reference/sdk/states)** |
| CMD_WRITE | 2 | 无 | **向 AIUI 写入数据，回调 VAD bos 事件。** 使用参考[数据写入](/sdk-dev/basics/data-sending/)。 |
| CMD_STOP_WRITE | 3 | 无 | **停止写入数据，回调 VAD eos 事件。** 使用参考[数据写入](/sdk-dev/basics/data-sending/)。 |
| CMD_START | 5 | 无 | **启动 AIUI。** AIUI 停止后，使用此命令启动。 |
| CMD_STOP | 6 | 无 | **停止 AIUI。** AIUI 停止之后，将不响应外部输入。 |
| CMD_WAKEUP | 7 | 无 | **唤醒消息。** 手动唤醒 AIUI，arg1 为唤醒后拾音的波束号，默认为 0。为了保障识别效果稳定性，请勿将手动唤醒用于延长交互时间。 |
| CMD_RESET_WAKEUP | 8 | 无 | **休眠消息。** 进入待唤醒状态。 |
| CMD_SET_PARAMS | 10 | 无 | **动态参数设置。** 用 params 携带参数设置 JSON 字符串，具体格式参照 aiui.cfg 文件。可动态更新参数如下：global、speech、userparams、audioparams、TTS（语音合成）。示例见下方。使用参考[基础配置说明](/sdk-dev/basics/params/)。 |
| CMD_SYNC | 13 | 有 | **上传个性化数据。** arg1 表示上传的数据类型，data 表示上传的数据内容。使用参考[用户个性化使用文档](/sdk-dev/features/personalization)。 |
| CMD_RESULT_VALIDATION_ACK | 20 | 无 | **结果确认。** 收到云端结果 5s 内发送该指令，重置交互超时的计时。关于交互超时的机制参看 [AIUI 配置](/sdk-dev/basics/params/)中 interact_timeout 的解释。使用参考[延迟休眠](/sdk-dev/basics/data-sending/)。 |
| CMD_CLEAN_DIALOG_HISTORY | 21 | 无 | **清空交互历史。** 使用参考[清除历史](/sdk-dev/basics/data-sending/)。 |
| CMD_START_RECORD | 22 | 无 | **开始录制数据（暂只支持 Android 系统）。** |
| CMD_STOP_RECORD | 23 | 无 | **停止录制数据（暂只支持 Android 系统）。** |
| CMD_QUERY_SYNC_STATUS | 24 | 有 | **查询数据同步状态。** arg1 表示状态查询的类型，params 包含查询条件。使用参考[查询打包状态](/sdk-dev/features/personalization)。 |
| CMD_TTS | 27 | 有 | **进行语音合成。** arg1 表示控制 TTS（语音合成）命令，params 包含合成参数。使用参考[云端 TTS](/sdk-dev/features/tts)。 |

CMD_SET_PARAMS 示例：

```json
{
  "global": {
    "scene": "main"
  }
}
```

## AIUIEvent

通过 AIUIEvent 解析，获取 AIUI SDK 交互或其他状态信息回调结果。

| eventType（事件类型） | 取值 | 说明 |
| --- | --- | --- |
| EVENT_RESULT | 1 | **结果事件。** 解析参考[结果解析](/sdk-dev/basics/callbacks/)。 |
| EVENT_ERROR | 2 | **出错事件。** arg1 是错误码，info 是错误描述信息。错误码附录[错误码](/sdk-dev/error-codes)说明。 |
| EVENT_STATE | 3 | **服务状态事件。** 详见 [SDK 状态说明](/reference/sdk/states)。 |
| EVENT_WAKEUP | 4 | **唤醒事件。** arg1 字段取值：0（语音唤醒）、1（发送 CMD_WAKEUP 手动唤醒）。info 字段为唤醒结果 JSON 字符串。 |
| EVENT_SLEEP | 5 | **休眠事件。** arg1 字段取值：0（交互超时，自动休眠）、1（发送 CMD_RESET_WAKEUP，手动休眠）。 |
| EVENT_VAD | 6 | **VAD（端点检测）事件。** arg1 取值：0（VAD 开始说话）、1（音量）、2（VAD 结束说话）、3（没说话超时）。当 arg1 取值为 1 时，arg2 为音量大小。 |
| EVENT_CMD_RETURN | 8 | **某条 CMD 命令对应的返回事件。** 对于除 CMD_GET_STATE 外的有返回的命令，都会返回该事件，用 arg1 标识对应的 CMD 命令，arg2 为返回值，0 表示成功，info 字段为描述信息。 |
| EVENT_PRE_SLEEP | 10 | **准备休眠事件。** 若 10s 内不交互，则休眠。 |
| EVENT_START_RECORD | 11 | **通知外部录音开始，用户可以开始说话。** |
| EVENT_STOP_RECORD | 12 | **通知外部录音停止。** |
| EVENT_CONNECTED_TO_SERVER | 13 | **与服务端建立连接。** |
| EVENT_SERVER_DISCONNECTED | 14 | **与服务端断开连接。** |
| EVENT_TTS | 15 | **TTS（语音合成）事件。** 合成状态以及合成进度，使用参考[云端 TTS](/sdk-dev/features/tts)。 |
