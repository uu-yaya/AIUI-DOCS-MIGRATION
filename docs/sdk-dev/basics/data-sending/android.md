---
title: 数据发送 - Android 示例
description: AIUI Android SDK 外部数据写入示例代码。
---

> 参数说明请参见[数据发送方式概述](./)

## Android 数据发送示例

::: tip 温馨提示
1. 外部音频数据写入请求中，发送停止写入命令（`CMD_STOP_WRITE`）后代表本次会话结束。
2. 文本数据请求要一次发送完成，多次发送算多次请求。文本数据请求不需要发送停止写入命令。
:::

```java
/*
 * 外部音频数据写入
 */
// 第一步：获取音频流（外部录音或音频文件读取）
byte[] audio = xxx;
// 第二步：循环构建 CMD_WRITE 事件，发送获取的音频流
String params = "data_type=audio,sample_rate=16000";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, audio);
mAIUIAgent.sendMessage(msg);

/*
 * 停止音频数据写入
 */
// 第三步：当外部录音停止或音频文件读取完成后，发送停止写入命令
String params = "data_type=audio,sample_rate=16000";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_STOP_WRITE, 0, 0, params, null);
mAIUIAgent.sendMessage(msg);

/*
 * 文本数据写入
 */
// 第一步：获取需要请求的文本，转成字节流
byte[] content = "确定预定".getBytes();
// 第二步：构建 CMD_WRITE 事件，直接发送
String params = "data_type=text";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, content);
mAIUIAgent.sendMessage(msg);
```

## 使用 tag 对应多个文本请求

同时写入多个文本时，用 tag 将结果与请求一一对应：

```java
// 写入文本
byte[] content = "你好".getBytes();
String params = "data_type=text";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, "tag=write_data_1", content);
mAIUIAgent.sendMessage(msg);

// 结果回调
private void processResult(AIUIEvent event) {
    String tag = event.data.getString("tag");
}
```
