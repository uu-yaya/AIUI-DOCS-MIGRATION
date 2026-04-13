---
title: AIUI 类型消息事件
---

::: info 概述
多模态模组内置集成AIUI SDK，除了支持AIUI SDK的[通用消息](/sdk-dev/basics/events)控制指令外，还增加了部分多模态交互相关的控制指令:
:::

## AIUI控制消息

通过AIUIMessage向SDK发送指令，通过AIUIEvent获取sdk事件回调。

温馨提示

有返回值的消息类型，代表向AIUI发送该消息后，AIUI会抛出EVENT\_CMD\_RETURN事件返回结果。

|  |  |  |  |
| --- | --- | --- | --- |
| msgType（消息类型） | 取值 | 返回值 | 说明 |
| CMD\_SET\_INTERACT\_MODE | 1008 | 无 | **设置唤醒降噪模式**   arg1表示类型：   0:使用人脸唤醒+唇形降噪；   1:使用语音唤醒+声学降噪 |
| CMD\_SET\_WAKEUP\_MODE | 1009 | 无 | **设置唤醒模式**   arg1表示类型：   0:使用人脸唤醒   1:使用语音唤醒 |
| CMD\_REGISTER\_FACE | 1011 | 有 | **注册单个人脸信息（多人多模态版本）**   info字段指定data数据类型及注册人脸信息：   data\_type=raw\_jpeg,extend\_info=base64(自定义人员信息)   data字段：base64编码之后的jpeg图片数据 |
| CMD\_DELETE\_REGISTER\_FACE | 1012 | 有 | **删除已注册人脸**    **info**字段指定需要删除的人脸id：face\_ids=xx 多个id使用&分隔 |
| CMD\_GET\_ALL\_REGISTER\_FACE | 1013 | 有 | **获取所有已注册的人脸信息** |

## 本地人脸识别功能

机器人超脑版本V1.3及以上版本默认开启本地人脸识别功能

1. 人脸注册、删除、查询列表功能，通过AIUI消息事件管理
2. 人脸检测结果在[视频传输协议](/hardware/rk3588-mm/video-protocol)中进行接收
