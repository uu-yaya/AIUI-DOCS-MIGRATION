---
title: Windows / Linux SDK 接口
description: AIUI Windows / Linux SDK 接口详解，包括 IAIUIAgent、IAIUIListener、IAIUIEvent 和 IAIUIMessage。
---

> 通用接口概述请参见[接口说明概述](./)

## IAIUIAgent

用于与 AIUI SDK 交互的接口类为 `IAIUIAgent`：

```cpp
class IAIUIAgent
{
public:
    AIUIEXPORT virtual ~IAIUIAgent();

    /**
     * 创建 Agent 单例对象，AIUI 开始工作。
     * 注：该方法总是返回非空对象，非空并不代表创建过程中无错误发生。
     *
     * @param params 参数设置
     * @param listener 事件监听器
     * @return AIUIAgent 单例对象指针
     */
    AIUIEXPORT static IAIUIAgent* createAgent(const char* params, IAIUIListener* listener);

    /**
     * 发送消息给 AIUI，消息中可以包含命令、参数和数据。
     *
     * @param msg AIUI 消息
     */
    virtual void sendMessage(IAIUIMessage* message) = 0;

    /**
     * 销毁 AIUIAgent。
     */
    virtual void destroy() = 0;
};
```

cfg 内容参见 [AIUI 配置文件](/reference/sdk/params/)。

## IAIUIListener

创建 `IAIUIAgent` 时传递的参数 `IAIUIListener` 是用于接收 AIUI SDK 抛出事件的监听器：

```cpp
class AIUIListener
{
public:
    AIUIEXPORT virtual ~AIUIListener();

    /**
     * 事件回调，SDK 所有输出都通过 event 抛出。
     *
     * @param event AIUI 事件
     */
    virtual void onEvent(const IAIUIEvent& event) const = 0;
};

typedef AIUIListener IAIUIListener;
```

## IAIUIEvent

`IAIUIListener` 中监听的抛出事件类型是 `IAIUIEvent`，定义如下：

```cpp
class IAIUIEvent
{
public:
    AIUIEXPORT virtual ~IAIUIEvent();

    /** 获取事件类型 */
    virtual int getEventType() = 0;

    /** 获取扩展参数1 */
    virtual int getArg1() = 0;

    /** 获取扩展参数2 */
    virtual int getArg2() = 0;

    /** 获取描述信息。返回的指针不可外部 delete 或 free。 */
    virtual const char* getInfo() = 0;

    /** 获取附带数据。返回的内存不可外部 delete 或 free。 */
    virtual IDataBundle* getData() = 0;
};
```

不同 `IAIUIEvent` 有不同 `eventType`，详见 [AIUIEvent](/reference/sdk/events)。

## IAIUIMessage

`IAIUIAgent` 中 `sendMessage` 方法用于向 AIUI 发送消息。消息类型是 `IAIUIMessage`，定义如下：

```cpp
class IAIUIMessage
{
public:
    AIUIEXPORT virtual ~IAIUIMessage();

    /**
     * 创建消息对象。
     *
     * @param msgType 消息类型
     * @param arg1 扩展参数1
     * @param arg2 扩展参数2
     * @param params 业务参数
     * @param data 附带数据，Message 在 SDK 内部处理后会自动释放
     * @return IAIUIMessage 对象指针
     */
    AIUIEXPORT static IAIUIMessage* create(
        int msgType,
        int arg1 = 0,
        int arg2 = 0,
        const char* params = "",
        Buffer* data = 0);

    virtual int getMsgType() = 0;
    virtual int getArg1() = 0;
    virtual int getArg2() = 0;
    virtual const char* getParams() = 0;
    virtual Buffer* getData() = 0;
    virtual void releaseData() = 0;
    virtual void destroy() = 0;
};
```

不同 `IAIUIMessage` 有不同 `msgType`，详见 [AIUIMessage](/reference/sdk/events)。
