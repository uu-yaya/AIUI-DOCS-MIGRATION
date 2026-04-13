---
title: 数据发送 - iOS / Windows / Linux 示例
description: AIUI iOS / Windows / Linux SDK 外部数据写入示例代码。
---

> 参数说明请参见[数据发送方式概述](./)

## iOS / Windows / Linux 数据发送示例

```cpp
// 写入音频
char audio[length];
Buffer* buffer = Buffer::alloc(length);
memcpy(buffer->data, audio, length);
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_WRITE, 0, 0, "data_type=audio,sample_rate=16000", buffer);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 写入文本
string text = "确定预定";
Buffer* textData = Buffer::alloc(text.length());
text.copy((char*) textData->data(), text.length());
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_WRITE, 0, 0, "data_type=text", textData);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 停止写入
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_STOP_WRITE, 0, 0, "data_type=audio,sample_rate=16000", buffer);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();
```
