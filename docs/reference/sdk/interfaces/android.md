---
title: Android SDK 接口
description: AIUI Android SDK 接口详解，包括 AIUIAgent、AIUIListener、AIUIEvent 和 AIUIMessage。
---

> 通用接口概述请参见[接口说明概述](./)

## AIUIAgent

`AIUIAgent` 是控制 AIUI 的接口类：

```java
// 创建
static AIUIAgent createAgent(Context context, String cfg, AIUIListener listener)

// 发送消息
void sendMessage(AIUIMessage message)

// 销毁
void destroy()
```

## AIUIListener

`AIUIListener` 是 AIUI 事件监听器：

```java
interface AIUIListener
{
    void onEvent(AIUIEvent event);
}
```

## AIUIEvent

`AIUIListener` 中监听的事件类型是 `AIUIEvent`，定义如下：

```java
class AIUIEvent
{
    int eventType; // 事件类型
    int arg1;      // 参数1
    int arg2;      // 参数2
    String info;
    Bundle data;
}
```

`eventType` 定义参照 [AIUIEvent](/reference/sdk/events)。

## AIUIMessage

`AIUIMessage` 是向 AIUI 发送的消息：

```java
class AIUIMessage
{
    int msgType;   // 消息类型
    int arg1;      // 参数1，默认空值 0
    int arg2;      // 参数2，默认空值 0
    String params; // 默认空值 null
    byte[] data;   // 默认空值 null
}
```

`msgType` 详见 [AIUIMessage](/reference/sdk/events)。
