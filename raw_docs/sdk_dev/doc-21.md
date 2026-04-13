---
title: 数据发送方式
source_url: https://aiui-doc.xf-yun.com/project-1/doc-21/
---

概述

AIUI服务请求支持音频和文本两种数据类型。本文档主要就SDK选用不同数据请求做详细说明:

做音频请求时，需要先确认音频来源：确认是**托管AIUI SDK进行系统录音调用获取录音数据**，还是**客户侧外部实现录音获取音频数据流写入AIUI SDK。**

[**- 确认录音方式>>>点击跳转**](#确认录音方式)
[**- 外部数据写入>>>点击跳转**](#外部数据写入)

## 确认录音方式

开发者根据实际设备录音方式，选择对应的数据发送方式，通过配置文件参数直接体验。

在AIUI SDK加载的配置文件（aiui.cfg）中，通过`data_source`可以指定AIUI录音来源，详见[参数配置说明](https://aiui-doc-admin.xf-yun.com/project-1/doc-13/ "参数配置说明")。

- **sdk**：
  托管sdk内部录音（支持Android、IOS、Windows）。用`CMD_START_RECORD、CMD_STOP_RECORD`控制录音开关，录音开始抛出 `EVENT_START_RECORD`事件，录音结束抛出`EVENT_STOP_RECORD`事件

```java
// 开启系统录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage startRecord = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params,null);
mAIUIAgent.sendMessage(startRecord);

// 停止系统录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage stopRecord = new AIUIMessage(AIUIConstant.CMD_STOP_RECORD, 0, 0, params,null);
mAIUIAgent.sendMessage(stopRecord);
```java

- **user**：
  开发者自己外部实现录音后送音频给sdk，使用`CMD_WRITE、CMD_STOP_WRITE`通知AIUI数据写入和写入结束

## 外部数据写入

通过`CMD_WRITE`事件向AIUI写入数据，支持文本和音频，请求参数字段说明如下：

|  |  |  |
| --- | --- | --- |
| **参数名称** | **是否必传** | **参数和取值说明** |
| **data\_type** | 是 | **数据类型** 音频数据取值：audio 文本数据请求：text |
| **sample\_rate** | 否 | **音频采样率** 固定取值：16000 音频数据类型时必传 |
| **msc.lng** | 否 | **GPS经度信息** 取值示例：117.16334474（不超过8位精度） |
| **msc.lat** | 否 | **GPS纬度信息** 取值示例：31.82102191（不超过8位精度） |
| **rec\_user\_data** | 否 | **临时识别热词** 取值示例：rec\_user\_data=”{“recHotWords”: “播报内容|地图显示|路径优先”, “sceneInfo”: {}}” 注意：该参数仅在传统语义服务链路生效 |

### Android 示例代码

温馨提示

1、外部音频数据写入请求中，发送停止写入命令（CMD\_STOP\_WRITE）后代表本次会话结束

2、文本数据请求要一次发送完成，多次发送算多次请求。另外文本数据请求不需要发送停止写入命令

```java
/*
*    外部音频数据写入
*/
// 第一步：获取音频流（外部录音 或 音频文件读取）
byte[] audio = xxx;
// 第二步：循环构建CMD_WRITE事件，发送获取的音频流
String params = "data_type=audio,sample_rate=16000";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, audio);
mAIUIAgent.sendMessage(msg);

/*
*    停止音频数据写入
*/
// 第三步：当外部录音停止或音频文件读取完成后，发送停止写入命令
String params = "data_type=audio,sample_rate=16000";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_STOP_WRITE, 0, 0, params, null);
mAIUIAgent.sendMessage(msg);

/*
*    文本数据写入
*/
// 第一步：获取需要请求的文本，转成字节流
byte[] content= "确定预定".getBytes();
// 第二步：构建CMD_WRITE事件，直接发送。
String params = "data_type=text";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, content);
mAIUIAgent.sendMessage(msg);
```java

### iOS/Linux/Windows 示例代码

```cpp
//写入音频
char audio[length] ;
Buffer* buffer = Buffer::alloc(length);
memcpy(buffer->data, audio, length);
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_WRITE, 0, 0, "data_type=audio,sample_rate=16000", buffer);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

//写入文本
string text ="确定预定";
Buffer* textData = Buffer::alloc(text.length());
text.copy((char*) textData->data(), text.length());
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_WRITE, 0, 0, "data_type=text", textData);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

//停止写入
IAIUIMessage* writeMsg=IAIUIMessage::create(AIUIConstant::CMD_STOP_WRITE, 0, 0, "data_type=audio,sample_rate=16000", buffer);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();
```java

同时写入多个文本，用tag将结果与请求一一对应。示例：

```java
//写入文本
byte[] content= "你好".getBytes();
String params = "data_type=text";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, "tag=write_data_1", content);
mAIUIAgent.sendMessage(msg);

//结果回调
private void processResult(AIUIEvent event) {
    String tag = event.data.getString("tag");
}
```
