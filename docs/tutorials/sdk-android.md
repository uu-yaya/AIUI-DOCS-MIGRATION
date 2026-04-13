---
title: Android SDK 集成教程
description: 在 Android 应用中集成 AIUI SDK，实现语音交互功能
---

## 前置条件

- 已创建 AIUI 应用并获取 AppID（参考 [创建应用教程](/tutorials/create-app)）
- Android Studio 开发环境
- Android 设备或模拟器（需要录音权限）

## 你将完成的目标

通过本教程，你将学会：

1. 在 Android 工程中导入 AIUI SDK
2. 配置 AIUI 参数（AppID、场景等）
3. 创建 AIUIAgent 并监听事件
4. 实现语音输入和语义理解
5. 解析交互结果

## 第一步：下载 SDK

1. 登录 AIUI 平台，进入应用管理页面
2. 点击「资源下载」，下载最新版 Android SDK

SDK 压缩包包含以下关键内容：

```text
libs/
├── AIUI.jar          # SDK 核心库
└── libaiui.so        # 原生库
assets/
└── cfg/
    └── aiui.cfg      # AIUI 配置文件
res/
└── vad/              # VAD（端点检测）资源
```

## 第二步：导入 SDK

1. 在 Android Studio 中创建或打开工程
2. 将 `libs/libaiui.so` 和 `libs/AIUI.jar` 拷贝至工程的 `libs` 目录
3. 将 `assets/cfg` 文件夹拷贝至工程的 `assets` 目录
4. 将 `res/vad` 文件夹拷贝至工程的 `res` 目录

在 `app/build.gradle` 中添加依赖和 JNI 目录配置：

```groovy
android {
    // ...
    sourceSets {
        main {
            jniLibs.srcDirs = ['libs']
        }
    }
}

dependencies {
    implementation files('libs/AIUI.jar')
}
```

### 混淆配置（可选）

如果开启了代码混淆，在 `proguard-rules.pro` 中添加：

```text
-dontoptimize
-keep class com.iflytek.**{*;}
-keepattributes Signature
```

## 第三步：修改 AIUI 配置

打开 `assets/cfg/aiui.cfg`，修改以下关键配置项：

```text
login.appid={你的 AppID}
global.scene={你的场景名称}
```

::: tip 场景名称说明
- 测试阶段使用沙盒场景：`main_box`
- 发布后使用线上场景：`main`
:::

## 第四步：设置设备标识

在初始化 AIUI SDK 之前，设置设备唯一标识（用于装机量计量）：

```java
// 在 createAgent 之前调用
// 传入设备唯一标识，确保每台设备值不变
AIUISetting.setSystemInfo(AIUIConstant.KEY_SERIAL_NUM, "your_device_sn");
```

## 第五步：创建 AIUIAgent

`AIUIAgent` 是与 AIUI 服务交互的核心对象。创建时需要传入三个参数：

```java
// 读取 aiui.cfg 配置文件内容
String aiuiConfig = readFileAsString("aiui.cfg");

// 创建 AIUIAgent
AIUIAgent mAIUIAgent = AIUIAgent.createAgent(context, aiuiConfig, mAIUIListener);
```

定义事件监听器来接收 AIUI 的各种回调：

```java
private int mAIUIState = AIUIConstant.STATE_IDLE;

private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_WAKEUP:
                // 唤醒事件
                Log.i(TAG, "AIUI 已唤醒");
                break;

            case AIUIConstant.EVENT_RESULT:
                // 结果事件（听写、语义、离线语法）
                handleResult(event);
                break;

            case AIUIConstant.EVENT_SLEEP:
                // 休眠事件
                Log.i(TAG, "AIUI 已休眠");
                break;

            case AIUIConstant.EVENT_STATE:
                // 状态变更事件
                mAIUIState = event.arg1;
                if (AIUIConstant.STATE_IDLE == mAIUIState) {
                    Log.i(TAG, "状态：闲置，AIUI 未开启");
                } else if (AIUIConstant.STATE_READY == mAIUIState) {
                    Log.i(TAG, "状态：就绪，等待唤醒");
                } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                    Log.i(TAG, "状态：工作中，可进行交互");
                }
                break;

            case AIUIConstant.EVENT_ERROR:
                // 错误事件
                Log.e(TAG, "错误码: " + event.arg1 + "，信息: " + event.info);
                break;
        }
    }
};
```

## 第六步：发起语音交互

先发送唤醒消息让 AIUI 进入工作状态，再开启录音：

```java
// 1. 发送唤醒消息（只有工作状态才能接收语音输入）
if (AIUIConstant.STATE_WORKING != mAIUIState) {
    AIUIMessage wakeupMsg = new AIUIMessage(AIUIConstant.CMD_WAKEUP, 0, 0, "", null);
    mAIUIAgent.sendMessage(wakeupMsg);
}

// 2. 开启 AIUI 内部录音机
String params = "sample_rate=16000,data_type=audio";
AIUIMessage startRecordMsg = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params, null);
mAIUIAgent.sendMessage(startRecordMsg);
```

::: warning 录音权限
如果出现错误码 20006，请检查应用是否已获取 `RECORD_AUDIO` 权限。在 AndroidManifest.xml 中添加：
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
```
:::

## 第七步：解析交互结果

在 `EVENT_RESULT` 回调中解析语义结果：

```java
private void handleResult(AIUIEvent event) {
    try {
        JSONObject bizParamJson = new JSONObject(event.info);
        JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
        JSONObject params = data.getJSONObject("params");
        JSONObject content = data.getJSONArray("content").getJSONObject(0);

        if (content.has("cnt_id")) {
            String cntId = content.getString("cnt_id");
            String resultStr = new String(
                event.data.getByteArray(cntId), "utf-8"
            );

            String sub = params.optString("sub");

            if ("nlp".equals(sub)) {
                // NLP（语义理解）结果
                JSONObject cntJson = new JSONObject(resultStr);
                String intentResult = cntJson.optString("intent");
                Log.i(TAG, "语义结果: " + intentResult);
            } else if ("iat".equals(sub)) {
                // IAT（语音识别）结果
                Log.i(TAG, "识别结果: " + resultStr);
            } else if ("tts".equals(sub)) {
                // TTS（语音合成）结果
                Log.i(TAG, "合成数据已返回");
            }
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

### AIUI 事件类型汇总

| 事件 | 常量 | 说明 |
|------|------|------|
| 唤醒 | `EVENT_WAKEUP` | AIUI 被唤醒 |
| 结果 | `EVENT_RESULT` | 收到交互结果 |
| 休眠 | `EVENT_SLEEP` | AIUI 进入休眠 |
| 状态 | `EVENT_STATE` | 状态变更 |
| 错误 | `EVENT_ERROR` | 发生错误 |
| VAD | `EVENT_VAD` | 检测到语音前端点/后端点 |
| 开始录音 | `EVENT_START_RECORD` | 录音开始 |
| 停止录音 | `EVENT_STOP_RECORD` | 录音结束 |

## 下一步

- [iOS SDK 集成教程](/tutorials/sdk-ios) — 在 iOS 应用中集成 AIUI
- [Windows/Linux SDK 集成教程](/tutorials/sdk-windows-linux) — 在桌面平台集成 AIUI
- [SDK 基础信息](/sdk-dev/basics/) — 了解 SDK 接口、参数和事件详情
- [错误码列表](/sdk-dev/error-codes) — 查看完整的错误码说明
