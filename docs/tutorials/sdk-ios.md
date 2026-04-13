---
title: iOS SDK 集成教程
description: 在 iOS 应用中集成 AIUI SDK，实现语音交互功能
---

## 前置条件

- 已创建 AIUI 应用并获取 AppID（参考 [创建应用教程](/tutorials/create-app)）
- Xcode 开发环境
- iOS 真机设备（录音功能需真机测试）

## 你将完成的目标

通过本教程，你将学会：

1. 在 Xcode 工程中导入 AIUI SDK
2. 配置系统库依赖和权限
3. 初始化 AIUI 并创建 AIUIAgent
4. 实现语音输入和结果回调

## 第一步：下载 SDK

登录 AIUI 平台，进入应用管理页面，在「资源下载」中下载最新版 iOS SDK。

## 第二步：导入 SDK

### 添加 Framework

将 SDK 压缩包中的 `iflyAIUI.framework` 添加到 Xcode 工程中。

配置 Framework 搜索路径：依次点击 **TARGETS → Build Settings → Framework Search Paths**，确保路径指向 `iflyAIUI.framework` 所在目录。

### 添加配置文件和资源

将 SDK Demo 中的 `resource` 文件夹添加到工程中，包含：

- AIUI 配置参数文件（`aiui.cfg`）
- 语音识别 VAD 资源

### 添加系统库依赖

AIUI SDK 使用 C++ 和 Objective-C 混编，需要添加以下系统库：

- `libicucore.tbd`
- `libc++.tbd`
- `libz.tbd`

在 **TARGETS → Build Phases → Link Binary With Libraries** 中添加。

### 关闭 Bitcode

AIUI SDK 暂不支持 Bitcode。在 **TARGETS → Build Settings** 中搜索 `Bitcode`，设置 **Enable Bitcode** 为 `NO`。

## 第三步：配置隐私权限

在 `Info.plist` 中添加 AIUI SDK 所需的隐私权限：

```xml
<key>NSMicrophoneUsageDescription</key>
<string>AIUI 需要使用麦克风进行语音识别</string>
<key>NSLocationUsageDescription</key>
<string>AIUI 需要获取位置信息</string>
<key>NSLocationAlwaysUsageDescription</key>
<string>AIUI 需要获取位置信息</string>
<key>NSContactsUsageDescription</key>
<string>AIUI 需要访问通讯录</string>
```

## 第四步：初始化工作目录

在 `AppDelegate` 中（或在创建 AIUIAgent 之前的任意位置）初始化 AIUI 工作目录：

```objc
- (BOOL)application:(UIApplication *)application
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    NSArray *paths = NSSearchPathForDirectoriesInDomains(
        NSCachesDirectory, NSUserDomainMask, YES
    );
    NSString *cachePath = [paths objectAtIndex:0];
    cachePath = [cachePath stringByAppendingString:@"/"];

    [IFlyAIUISetting setSaveDataLog:NO];
    [IFlyAIUISetting setLogLevel:LV_INFO];
    [IFlyAIUISetting setAIUIDir:cachePath];
    [IFlyAIUISetting setMscDir:cachePath];

    return YES;
}
```

## 第五步：创建 AIUIAgent

`IFlyAIUIAgent` 是与 AIUI 服务交互的核心对象。创建时需要传入配置文件内容和事件监听代理：

```objc
@interface ViewController () <IFlyAIUIListener>
@property (nonatomic, strong) IFlyAIUIAgent *aiuiAgent;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    // 读取 aiui.cfg 配置文件
    NSString *cfgFilePath = [[NSBundle mainBundle]
        pathForResource:@"aiui" ofType:@"cfg"];
    NSString *cfg = [NSString stringWithContentsOfFile:cfgFilePath
        encoding:NSUTF8StringEncoding error:nil];

    // 创建 AIUIAgent
    _aiuiAgent = [IFlyAIUIAgent createAgent:cfg withListener:self];
}

@end
```

::: tip 配置文件
修改 `aiui.cfg` 中的 `login.appid` 为你的 AppID，`global.scene` 为对应的场景名称。
:::

## 第六步：发起语音交互

发送唤醒消息使 AIUI 进入工作状态，然后开启录音：

```objc
// 发送唤醒消息
IFlyAIUIMessage *wakeupMsg = [[IFlyAIUIMessage alloc] init];
wakeupMsg.msgType = CMD_WAKEUP;
[_aiuiAgent sendMessage:wakeupMsg];

// 发送开始录音消息
IFlyAIUIMessage *recordMsg = [[IFlyAIUIMessage alloc] init];
recordMsg.msgType = CMD_START_RECORD;
[_aiuiAgent sendMessage:recordMsg];
```

## 第七步：实现结果回调

实现 `IFlyAIUIListener` 协议，在 `onEvent:` 方法中接收各种事件：

```objc
- (void)onEvent:(IFlyAIUIEvent *)event {
    switch (event.eventType) {
        case EVENT_CONNECTED_TO_SERVER:
            NSLog(@"服务器连接成功");
            break;

        case EVENT_SERVER_DISCONNECTED:
            NSLog(@"服务器连接断开");
            break;

        case EVENT_START_RECORD:
            NSLog(@"开始录音");
            break;

        case EVENT_STOP_RECORD:
            NSLog(@"停止录音");
            break;

        case EVENT_STATE:
            switch (event.arg1) {
                case STATE_IDLE:
                    NSLog(@"状态：闲置");
                    break;
                case STATE_READY:
                    NSLog(@"状态：就绪");
                    break;
                case STATE_WORKING:
                    NSLog(@"状态：工作中");
                    break;
            }
            break;

        case EVENT_RESULT:
            [self handleResult:event];
            break;

        case EVENT_ERROR:
            NSLog(@"错误码: %d, 信息: %@", event.arg1, event.info);
            break;
    }
}
```

### 解析语义结果

```objc
- (void)handleResult:(IFlyAIUIEvent *)event {
    NSError *error;
    NSDictionary *bizParam = [NSJSONSerialization
        JSONObjectWithData:[event.info dataUsingEncoding:NSUTF8StringEncoding]
        options:0 error:&error];

    if (error) return;

    NSArray *dataArray = bizParam[@"data"];
    if (dataArray.count == 0) return;

    NSDictionary *data = dataArray[0];
    NSDictionary *params = data[@"params"];
    NSArray *contentArray = data[@"content"];
    if (contentArray.count == 0) return;

    NSDictionary *content = contentArray[0];
    NSString *sub = params[@"sub"];
    NSString *cntId = content[@"cnt_id"];

    if (cntId && [sub isEqualToString:@"nlp"]) {
        // 获取语义结果
        NSData *resultData = [event.data objectForKey:cntId];
        NSString *resultStr = [[NSString alloc]
            initWithData:resultData encoding:NSUTF8StringEncoding];
        NSLog(@"语义结果: %@", resultStr);
    }
}
```

## 下一步

- [Android SDK 集成教程](/tutorials/sdk-android) — 在 Android 应用中集成 AIUI
- [Windows/Linux SDK 集成教程](/tutorials/sdk-windows-linux) — 在桌面平台集成 AIUI
- [SDK 基础信息](/sdk-dev/basics/) — 了解 SDK 接口、参数和事件详情
