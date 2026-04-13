---
title: iOS SDK 接口
description: AIUI iOS SDK 接口详解，包括 IFlyAIUIAgent、IFlyAIUIListener、IFlyAIUIEvent 和 IFlyAIUIMessage。
---

> 通用接口概述请参见[接口说明概述](./)

## IFlyAIUIAgent

与 AIUI 交互的接口类为 `IFlyAIUIAgent`：

```objc
@interface IFlyAIUIAgent : NSObject
-(instancetype) initWithParams:(NSString*) cfgParams withListener:(id) listener;

/**
 * 创建 AIUIAgent
 * @param cfgParams cfg 文件内容
 * @return YES: 设置成功；NO: 设置失败
 */
+ (instancetype) createAgent:(NSString *) cfgParams withListener:(id) listener;

/**
 * 发送 AIUI 消息
 * @param msg 消息实例
 */
- (void) sendMessage:(IFlyAIUIMessage *)msg;

/**
 * 销毁
 */
- (void) destroy;

/**
 * 设置 GPS 定位信息
 * @param lng 经度值
 * @param lat 纬度值
 */
- (void) setGPSwithLng:(NSNumber *)lng andLat:(NSNumber *)lat;

@end
```

cfg 内容参见 [AIUI 配置文件](/reference/sdk/params/)。

## IFlyAIUIListener

实现 `IFlyAIUIListener` 协议类的接口，用于获取结果回调：

```objc
@protocol IFlyAIUIListener <NSObject>

@required
/**
 * 事件回调
 * SDK 所有输出都通过 event 抛出。
 * @param event AIUI 事件，具体参见 IFlyAIUIEvent。
 */
- (void) onEvent:(IFlyAIUIEvent *) event;

@end
```

## IFlyAIUIEvent

`IFlyAIUIListener` 中监听的抛出事件类型是 `IFlyAIUIEvent`，定义如下：

```objc
@interface IFlyAIUIEvent : NSObject

/** 事件类型 */
@property (nonatomic, assign) int eventType;

/** 扩展参数1 */
@property (nonatomic, assign) int arg1;

/** 扩展参数2 */
@property (nonatomic, assign) int arg2;

/** 描述信息 */
@property (nonatomic, copy) NSString *info;

/** 附带数据 */
@property (nonatomic, strong) NSDictionary *data;

@end
```

## IFlyAIUIMessage

`IFlyAIUIAgent` 中 `sendMessage` 方法用于向 AIUI 发送消息。消息类型是 `IFlyAIUIMessage`，定义如下：

```objc
@interface IFlyAIUIMessage : NSObject

/** 消息类型 */
@property (nonatomic, assign) int msgType;

/** 扩展参数1 */
@property (nonatomic, assign) int arg1;

/** 扩展参数2 */
@property (nonatomic, assign) int arg2;

/** 业务参数 */
@property (nonatomic, copy) NSString *params;

/** 附带数据 */
@property (nonatomic, strong) NSData *data;

/** 附加参数，一般用于控件层 */
@property (nonatomic, strong) NSDictionary *dic;

@end
```
