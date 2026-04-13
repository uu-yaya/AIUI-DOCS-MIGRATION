---
title: SDK 接口说明
description: AIUI SDK 主要接口概述，包括 AIUISetting 系统设置和 AIUIAgent 控制接口。
---

## 概述

发送 `AIUIMessage` 控制 AIUI，通过 `AIUIListener` 接收回调事件，解析 `EVENT_RESULT` 获取识别和语义结果。

## AIUI SDK 接口概述

AIUI SDK 主要提供操作对象有：

**AIUISetting**
AIUI 系统设置类，用于设置设备唯一标识、设置日志开关、日志存放目录等。

- `setAIUIDir(String dir)` — 设置 AIUI 文件夹路径，SDK 会在该路径下保存日志等文件
- `getAIUIDir()` — 获取 AIUI 文件夹路径
- `setMscCfg(String cfg)` — 设置 msc.cfg 中的配置到 SDK
- `getMscCfg()` — 获取 MSC 配置
- `setShowLog(boolean show)` — 是否打印 AIUI 日志
- `setSystemInfo(String sn, String value)` — 设置设备装机量统计唯一标识 SN 号
- `setNetLogLevel(LogLevel level)` — 设置网络交互日志等级
- `setLogLevel(LogLevel level)` — 设置 logcat 调试日志等级
- `setSaveDataLog(boolean save)` — 设置是否保存数据日志
- `setDataLogDir(String dir)` — 设置数据日志存储路径

**AIUIAgent**
AIUI 接口控制类，用于服务初始化、各类型事件发送。

- 初始化
- 消息发送
- 销毁

## 装机量统计说明

AIUI 初始化时，要上传设备唯一标识 SN 来统计装机量：

```cpp
// 取值说明：设置设备唯一标识，保证每台设备不变。
// 调用顺序：在初始化 AIUI SDK 之前（即 createAgent 之前）

// Android 示例代码
AIUISetting.setSystemInfo(AIUIConstant.KEY_SERIAL_NUM, "xxx");

// iOS 示例代码
[IFlyAIUISetting setSystemInfo:@"sn" withVal:@"xxx"];

// Windows / Linux 示例代码
AIUISetting::setSystemInfo(AIUI_KEY_SERIAL_NUM, "xxx");
```

## 各平台接口详解

- [Android SDK 接口](./android)
- [iOS SDK 接口](./ios)
- [Windows / Linux SDK 接口](./windows-linux)

::: info 说明
iOS / Windows / Linux 中命名与 Android 中的命名类似，稍有不同，一般加前缀 `I` 表示接口。例如 `AIUIMessage` 在 Android 中为 `AIUIMessage`，在 iOS 中为 `IFlyAIUIMessage`，在 Windows / Linux 中为 `IAIUIMessage`。
:::
