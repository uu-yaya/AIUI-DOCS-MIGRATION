---
title: 消息事件说明
source_url: https://aiui-doc.xf-yun.com/project-1/doc-14/
---

消息事件概述

本章节详细介绍请求事件和回调事件对应的内部消息类型。AIUI SDK做请求发送和结果接受时，分别通过下面两个事件来进行详细区分:

**请求事件：**通过构建不同的AIUIMessage进行发送，来实现不同的消息指令请求。

[**- AIUIMessage>>>点击跳转**](#AIUIMessage)

**回调事件：**通过解析回调中AIUIEvent不同类型，可以获取AIUI SDK抛出的状态或结果。

[**- AIUIEvent>>>点击跳转**](#AIUIEvent)

## AIUIMessage

通过AIUIMessage向SDK发送指令，通过AIUIEvent获取sdk事件回调。

温馨提示

有返回值的消息类型，代表向AIUI发送该消息后，AIUI会抛出EVENT\_CMD\_RETURN事件返回结果。

|  |  |  |  |
| --- | --- | --- | --- |
| msgType（消息类型） | 取值 | 返回值 | 说明 |
| CMD\_GET\_STATE | 1 | 有 | **获取[交互状态](https://aiui-doc.xf-yun.com/project-1/doc-15/)** |
| CMD\_WRITE | 2 | 无 | **向AIUI写入数据，回调vad bos事件**   使用参考[数据写入](https://aiui-doc.xf-yun.com/project-1/doc-21/#数据写入)。 |
| CMD\_STOP\_WRITE | 3 | 无 | **停止写入数据，回调vad eos事件**   使用参考[数据写入](https://aiui-doc.xf-yun.com/project-1/doc-21/#数据写入)。 |
| CMD\_START | 5 | 无 | **启动AIUI**    AIUI停止后，使用此命令启动 |
| CMD\_STOP | 6 | 无 | **停止AIUI**    AIUI停止之后，将不响应外部输入。 |
| CMD\_WAKEUP | 7 | 无 | **唤醒消息**    手动唤醒AIUI，arg1为唤醒后拾音的波束号，默认为0。为了保障识别效果稳定性，请勿将手动唤醒用于延长交互时间。 |
| CMD\_RESET\_WAKEUP | 8 | 无 | **休眠消息**    进入待唤醒状态 |
| CMD\_SET\_PARAMS | 10 | 无 | **动态参数设置**    用params携带参数设置JSON字符串，具体格式参照aiui.cfg文件。  可动态更新参数如下  - global - speech - userparams - audioparams - tts   示例:  ``` {   "global":{      "scene":"main"    } } ```   使用参考[基础配置说明](https://aiui-doc.xf-yun.com/project-1/doc-13/#动态配置)。 |
| CMD\_SYNC | 13 | 有 | **上传个性化数据**    arg1表示上传的数据类型  data表示上传的数据内容   使用参考[用户个性化使用文档](https://aiui-doc.xf-yun.com/project-1/doc-24/)。 |
| CMD\_RESULT\_VALIDATION\_ACK | 20 | 无 | **结果确认**  收到云端结果5s内发送该指令，重置交互超时的计时。    关于交互超时的机制参看[AIUI配置](https://aiui-doc.xf-yun.com/project-1/doc-13/#配置文件示例)中interact\_timeout的解释。   使用参考[延迟休眠](https://aiui-doc.xf-yun.com/project-1/doc-21/#延迟休眠)。 |
| CMD\_CLEAN\_DIALOG\_HISTORY | 21 | 无 | **清空交互历史**   使用参考[清除历史](https://aiui-doc.xf-yun.com/project-1/doc-21/#清除历史)。 |
| CMD\_START\_RECORD | 22 | 无 | **开始录制数据（暂只支持Android系统）** |
| CMD\_STOP\_RECORD | 23 | 无 | **停止录制数据（暂只支持Android系统）** |
| CMD\_QUERY\_SYNC\_STATUS | 24 | 有 | **查询数据同步状态**    arg1表示状态查询的类型  params包含查询条件   使用参考[查询打包状态](https://aiui-doc.xf-yun.com/project-1/doc-24/#查询打包状态)。 |
| CMD\_TTS | 27 | 有 | **进行语音合成**    arg1表示控制语音合成命令  params包含合成参数   使用参考[云端TTS](https://aiui-doc.xf-yun.com/project-1/doc-23/)。 |

## AIUIEvent

通过AIUIEvent解析，获取AIUI SDK交互或其他状态信息回调结果。

|  |  |  |
| --- | --- | --- |
| eventType(事件类型) | 取值 | 说明 |
| EVENT\_RESULT | 1 | **结果事件**    解析参考[结果解析](https://aiui-doc.xf-yun.com/project-1/doc-16/)。 |
| EVENT\_ERROR | 2 | **出错事件**    arg1是错误码，info上错误描述信息。  错误码附录[错误码](https://aiui-doc.xf-yun.com/project-1/doc-42/)说明。 |
| EVENT\_STATE | 3 | **服务状态事件**    详细见[SDK状态说明](https://aiui-doc.xf-yun.com/project-1/doc-15/)。 |
| EVENT\_WAKEUP | 4 | **唤醒事件**    arg1字段取值：  0 （语音唤醒）  1 （发送CMD\_WAKEUP手动唤醒）。  info字段为唤醒结果JSON字符串。 |
| EVENT\_SLEEP | 5 | **休眠事件**    arg1字段取值：  0 （交互超时,自动休眠）  1 (发送CMD\_RESET\_WAKEUP，手动休眠)。 |
| EVENT\_VAD | 6 | **VAD事件**    arg1取值:0(vad 开始说话)、1(音量)、2(vad 结束说话)、3（没说话超时）。  当arg1取值为1时，arg2为音量大小。 |
| EVENT\_CMD\_RETURN | 8 | **某条CMD命令对应的返回事件**    对于除CMD\_GET\_STATE外的有返回的命令，都会返回该事件，  用arg1标识对应的CMD命令，arg2为返回值，0表示成功，info字段为描述信息。 |
| EVENT\_PRE\_SLEEP | 10 | **准备休眠事件**    若10s内不交互，则休眠。 |
| EVENT\_START\_RECORD | 11 | **通知外部录音开始，用户可以开始说话** |
| EVENT\_STOP\_RECORD | 12 | **通知外部录音停止** |
| EVENT\_CONNECTED\_TO\_SERVER | 13 | **与服务端建立连接** |
| EVENT\_SERVER\_DISCONNECTED | 14 | **与服务端断开连接** |
| EVENT\_TTS | 15 | **语音合成事件**    合成状态以及合成进度，使用参考[云端TTS](https://aiui-doc.xf-yun.com/project-1/doc-23/)。 |
