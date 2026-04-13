---
title: SDK接口说明
source_url: https://aiui-doc.xf-yun.com/project-1/doc-12/
---

目录

发送“AIUIMessage”控制AIUI，通过“AIUIListener”接收回调事件，解析“EVENT\_RESULT”获取识别和语义结果。

[**- AIUI SDK接口概述>>>点击跳转**](#AIUI SDK接口概述)

[**- 各平台下SDK接口详解>>>点击跳转**](#各平台下SDK接口详解)

[-装机量统计说明>>>点击跳转](#装机量统计说明)

[-Android SDK接口>>>点击跳转](#Android SDK接口)

[-iOS SDK接口>>>点击跳转](#iOS SDK接口)

[-Windows/Linux SDK接口>>>点击跳转](#Windows/Linux SDK接口)

## AIUI SDK接口概述

AIUI SDK主要提供操作对象有：
**AIUISetting**
AIUI系统设置类，用于设置设备唯一标识、设置日志开关、日志存放目录等。

- setAIUIDir(String dir)，设置AIUI文件夹路径，SDK会在该路径下保存日志等文件；
- getAIUIDir()，获取AIUI文件夹路径
- setMscCfg(String cfg)，设置msc.cfg中的配置到SDK
- getMscCfg()，获取msc配置
- setShowLog(boolean show)，是否打印AIUI日志
- setSystemInfo(String sn，String value)，设置设备装机量统计唯一标识SN号；
- setNetLogLevel(LogLevel level)，设置网络交互日志（打印到aiui.log文件）等级，只会打印高于该等级的日志
- setLogLevel(LogLevel level)，设置logcat调试日志等级，只会打印高于该等级的日志
- setSaveDataLog(boolean save)，设置是否保存数据日志，设置为true时，输入（音频、文本等）和云端返回的结果都将保存
- setDataLogDir(String dir)，设置数据日志存储路径

**AIUIAgent**
AIUI接口控制类，用户服务初始化、各类型事件发送。

- 初始化
- 消息发送
- 销毁

## 各平台下SDK接口详解

### 2.1. 装机量统计说明

AIUI初始化时，要上传设备唯一标识SN来统计装机量

```cpp
// 取值说明：设置设备唯一标识，保证每台设备不变。
// 调用顺序：在初始化AIUI SDK之前（即createAgent之前）

// android 示例代码
AIUISetting.setSystemInfo(AIUIConstant.KEY_SERIAL_NUM, "xxx")；

// ios 示例代码
 [IFlyAIUISetting setSystemInfo:@"sn" withVal:@"xxx"];

// windows|Linux 示例代码
AIUISetting::setSystemInfo(AIUI_KEY_SERIAL_NUM, "xxx");
```java

### 2.2. Android SDK接口

**AIUIAgent**

`AIUIAgent`是控制AIUI的接口类

```java
//创建
static AIUIAgent createAgent(Context context, String cfg, AIUIListener listener)

//发送消息
void sendMessage(AIUIMessage message)

//销毁
void destroy()
```java

**AIUIListener**

`AIUIListener`是AIUI事件监听器。

```java
interface AIUIListener
{
    void onEvent(AIUIEvent event);
}
```java

**AIUIEvent**

`AIUIEvent`监听的事件的类型是`AIUIEvent`。`AIUIEvent`定义如下：

```java
class AIUIEvent
{
    int eventType; //事件类型
    int arg1;      //参数1
    int arg2;      //参数2
    String info;
    Bundle data;
}
```

`eventType`定义参照[AIUIEvent](https://aiui-doc.xf-yun.com/project-1/doc-14/)

**AIUIMessage**

`AIUIMessage`是向AIUI发送的消息：

```java
class AIUIMessage
{
    int msgType;   //消息类型
    int arg1;      //参数1 默认空值0
    int arg2;      //参数2 默认空值0
    String params; //默认空值 null
    byte[] data;   //默认空值 null
}
```objc

`msgType`详见[AIUIMessage](https://aiui-doc.xf-yun.com/project-1/doc-14/)。

### 2.3. iOS SDK接口

与AIUI交互的接口类为`IFlyAIUIAgent`：

```objc
@interface IFlyAIUIAgent : NSObject
-(instancetype) initWithParams:(NSString*) cfgParams withListener:(id) listener;
/*!
    * 创建AIUIAgent
    *  @param cfgParams cfg文件内容
    *  @return YES:设置成功；NO:设置失败
    */
+ (instancetype) createAgent:(NSString *) cfgParams withListener:(id) listener;

/*!
    * 发送AIUI消息
    *  @param msg 消息实例
    */
- (void) sendMessage:(IFlyAIUIMessage *)msg;

/*!
    * 销毁
    */
- (void) destroy;

/*!
    * 设置GPS定位信息。
    *  @param lng 经度值
    *  @param lat 纬度值
    */
- (void) setGPSwithLng:(NSNumber *)lng andLat:(NSNumber *)lat;

@end
```text

cfg内容参见[AIUI配置文件](https://aiui-doc.xf-yun.com/project-1/doc-13/)。

**IFlyAIUIListener**

实现IFlyAIUIListener协议类的接口，用于获取结果回调。接口如下所示：

```
@protocol IFlyAIUIListener <NSObject>

@required
/*!
    * 事件回调<br>
    * SDK所有输出都通过event抛出。
    *
    @param event AIUI事件，具体参见IFlyAIUIEvent。
    */
- (void) onEvent:(IFlyAIUIEvent *) event ;

@end
```objc

**IFlyAIUIEvent**

`IFlyAIUIListener`中监听的抛出事件的类型是`IFlyAIUIEvent`。`IFlyAIUIEvent`定义如下：

```objc
/*!
    * AIUI事件类，业务结果、SDK内部状态变化等输出信息都通过事件抛出。
    */
@interface IFlyAIUIEvent : NSObject

/**
    * 事件类型。
    */
@property (nonatomic, assign) int eventType;

/**
    * 扩展参数1。
    */
@property (nonatomic, assign) int arg1;

/**
    * 扩展参数2。
    */
@property (nonatomic, assign) int arg2;

/**
    * 描述信息。
    */
@property (nonatomic, copy) NSString *info;

/**
    * 附带数据。
    */
@property (nonatomic, strong) NSDictionary *data;

@end
```objc

**IFlyAIUIMessage**

IFlyAIUIAgent中`sendMessage`方法用于向AIUI发送消息。消息类型是`IFlyAIUIMessage`。`IFlyAIUIMessage`定义如下：

```objc
/*!
    * AIUI消息类，发送消息控制SDK。
    */
@interface IFlyAIUIMessage : NSObject

/**
    * 消息类型。
    */
@property (nonatomic, assign) int msgType;

/**
    * 扩展参数1。
    */
@property (nonatomic, assign) int arg1;

/**
    * 扩展参数2。
    */
@property (nonatomic, assign) int arg2;

/**
    * 业务参数。
    */
@property (nonatomic, copy) NSString *params;

/**
    * 附带数据。
    */
@property (nonatomic, strong) NSData *data;

/**
    * 附加参数，一般用于控件层。
    */
@property (nonatomic, strong) NSDictionary *dic;

@end
```

### 2.4. Windows/Linux SDK接口

**IAIUIAgent**

用于与AIUI SDK交互的接口类为`IAIUIAgent`。`IAIUIAgent`提供如下接口：

```java
/**
    * AIUI代理类，单例对象，应用通过代理与AIUI交互。
    */
class IAIUIAgent
{
public:
    AIUIEXPORT virtual ~IAIUIAgent();

    /**
        * 创建Agent单例对象，AIUI开始工作。
        * 注：该方法总是返回非空对象，非空并不代表创建过程中无错误发生。
        *
        * @param params 参数设置
        * @param listener 事件监听器
        * @return AIUIAgent单例对象指针
        */
    AIUIEXPORT static IAIUIAgent* createAgent(const char* params, IAIUIListener* listener);

    /**
        * 发送消息给AIUI，消息中可以包含命令、参数和数据，具体格式参见IAIUIMessage。
        *
        * @param msg AIUI消息
        * message 如果指定了非空的Buffer *data， 在Message在内部处理后会自动release()这部分data;
        * 而不能外部去释放掉。
        */
    virtual void sendMessage(IAIUIMessage* message) = 0;

    /**
        * 销毁AIUIAgent。
        */
    virtual void destroy() = 0;
};
```java

cfg内容参见[AIUI配置文件](https://aiui-doc.xf-yun.com/project-1/doc-13/)

**IAIUIListener**

创建`IAIUIAgent`时传递的参数`IAIUIListener`是用于接受AIUI SDK抛出事件的监听器。`IAIUIListener`定义如下：

```java
/**
    * AIUI事件监听接口。SDK所有输出都通过回调onEvent方法抛出。
    */
class AIUIListener
{
public:
    AIUIEXPORT virtual ~AIUIListener();

    /**
        * 事件回调，SDK所有输出都通过event抛出。
        *
        * @param event AIUI事件
        */
    virtual void onEvent(const IAIUIEvent& event) const = 0;
};

typedef AIUIListener IAIUIListener;
```java

**IAIUIEvent**

`IAIUIListener`中监听的抛出事件的类型是`IAIUIEvent`。`IAIUIEvent`定义如下：

```python
/**
    * AIUI事件类。业务结果、SDK内部状态变化等输出信息都通过事件抛出。SDK通过回调抛出事件后会
    * 立即释放事件中的内存对象，若要在别处使用到这些内存对象，开发者需要在回调中做拷贝。
    */
class IAIUIEvent
{
public:
    AIUIEXPORT virtual ~IAIUIEvent();

    /**
        * 获取事件类型。取值参见AIUIConstant中EVENT_开头的常量定义。
        */
    virtual int getEventType() = 0;

    /**
        * 获取扩展参数1。
        */
    virtual int getArg1() = 0;

    /**
        * 获取扩展参数2。
        */
    virtual int getArg2() = 0;

    /**
        * 获取描述信息。返回的指针不可外部delete或者free。
        */
    virtual const char* getInfo() = 0;

    /**
        * 获取附带数据。返回的内存不可外部delete或者free。
        */
    virtual IDataBundle* getData() = 0;
};
```java

不同`IAIUIEvent`有不同`eventType`。不同`eventType`其余字段有不同的定义，详见[AIUIEvent](https://aiui-doc.xf-yun.com/project-1/doc-14/)

**IAIUIMessage**

IAIUIAgent中`sendMessage`方法用于向AIUIService发送AIUI消息。消息类型是`IAIUIMessage`，定义：

```java
/**
    * AIUI消息类。发送消息控制SDK。
    */
class IAIUIMessage
{
public:
    AIUIEXPORT virtual ~IAIUIMessage();

    /**
        * 创建消息对象。
        *
    * @param msgType 消息类型，参见AIUIConstant中CMD_开头的常量定义
        * @param arg1 扩展参数1
        * @param arg2 扩展参数2
        * @param params 业务参数，传入后内部会做拷贝
    * @param data 附带数据，Message在SDK内部处理后会自动释放, 不需要外部释放。
    *
        * @return IAIUIMessage 对象指针
        */
    AIUIEXPORT static IAIUIMessage*  create(
        int msgType ,
        int arg1 = 0,
        int arg2 = 0,
        const char* params = "",
        Buffer* data = 0);

    /**
        * 获取消息类型。类型取值参见AIUIConstant中CMD_开头的常量定义。
        */
    virtual int getMsgType() = 0;

    /**
        * 获取扩展参数1。
        */
    virtual int getArg1() = 0;

    /**
        * 获取扩展参数2。
        */
    virtual int getArg2() = 0;

    /**
        * 获取业务参数。
        */
    virtual const char* getParams() = 0;

    /**
        * 获取附带数据。
        */
    virtual Buffer* getData() = 0;

    /**
        * 释放附带数据
        */
    virtual void releaseData() = 0;

    /**
        * 销毁消息对象本身。注意：不会释放Buffer* data。
        */
    virtual void destroy() = 0;
};
```

不同`IAIUIMessage`有不同的`msgType`。不同`msgType`时，其他参数有不同定义，详见[AIUIMessage](https://aiui-doc.xf-yun.com/project-1/doc-14/)

### 注意：

iOS/Windows/Linux中命名与android中的命名类似，稍有不同，一般加前缀“I”表示接口，如，“AIUIMessage”在android中为AIUIMessage,在iOS中为IAIUIMessage。
