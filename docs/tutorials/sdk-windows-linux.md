---
title: Windows/Linux SDK 集成教程
description: 在 Windows 或 Linux 平台集成 AIUI SDK，实现语音交互功能
---

## 前置条件

- 已创建 AIUI 应用并获取 AppID（参考 [创建应用教程](/tutorials/create-app)）
- C/C++ 开发环境（支持 CMake）
- Windows 或 Linux 操作系统

## 你将完成的目标

通过本教程，你将学会：

1. 在 CMake 工程中导入 AIUI SDK
2. 初始化 AIUI 工作目录和日志
3. 创建 AIUIAgent 并实现事件监听
4. 发送文本和语音数据进行交互
5. 解析语义结果
6. 使用 C 接口支持多语言调用

## 第一步：下载 SDK

登录 AIUI 平台，进入应用管理页面，在「资源下载」中下载对应平台的 SDK。

## 第二步：导入 SDK

在 CMake 工程中添加 SDK 的头文件和库文件路径。可参考 SDK 包中 `aiui_sample` 的 `CMakeLists.txt`：

```cmake
include_directories(${CMAKE_CURRENT_LIST_DIR}/../../include)
link_directories(${CMAKE_CURRENT_LIST_DIR}/../../libs/${PLATFORM})
link_libraries(aiui)
```

将 SDK 包中 `aiui_sample/build/AIUI` 文件夹添加到工程中，该文件夹包含：

- `cfg/aiui.cfg` — AIUI 配置参数文件
- `vad/` — 语音识别 VAD 资源

修改 `cfg/aiui.cfg` 中的关键配置：

```text
login.appid={你的 AppID}
global.scene={你的场景名称}
```

## 第三步：初始化 AIUI

在创建 AIUIAgent 之前，完成系统初始化设置：

```cpp
// 设置 AIUI 工作目录
AIUISetting::setAIUIDir("./AIUI/");

// 设置日志级别（可选）
AIUISetting::setNetLogLevel(aiui::_none);
AIUISetting::setLogLevel(aiui::_none);

// 设置设备唯一标识（用于装机量统计）
AIUISetting::setSystemInfo(AIUI_KEY_SERIAL_NUM, "your_device_sn");
```

## 第四步：实现事件监听器

创建继承自 `IAIUIListener` 的监听器类，处理 AIUI 回调事件：

```cpp
class MyListener : public IAIUIListener
{
public:
    void onEvent(const IAIUIEvent& event) const override
    {
        switch (event.getEventType()) {
            case AIUIConstant::EVENT_STATE: {
                switch (event.getArg1()) {
                    case AIUIConstant::STATE_IDLE:
                        cout << "状态：闲置" << endl;
                        break;
                    case AIUIConstant::STATE_READY:
                        cout << "状态：就绪" << endl;
                        break;
                    case AIUIConstant::STATE_WORKING:
                        cout << "状态：工作中" << endl;
                        break;
                }
            } break;

            case AIUIConstant::EVENT_WAKEUP:
                cout << "唤醒事件: " << event.getInfo() << endl;
                break;

            case AIUIConstant::EVENT_SLEEP:
                cout << "休眠事件" << endl;
                break;

            case AIUIConstant::EVENT_VAD: {
                switch (event.getArg1()) {
                    case AIUIConstant::VAD_BOS:
                        cout << "检测到语音前端点" << endl;
                        break;
                    case AIUIConstant::VAD_EOS:
                        cout << "检测到语音后端点" << endl;
                        break;
                }
            } break;

            case AIUIConstant::EVENT_RESULT: {
                handleResult(event);
            } break;

            case AIUIConstant::EVENT_ERROR:
                cout << "错误码: " << event.getArg1() << endl;
                cout << "错误信息: " << event.getInfo() << endl;
                break;
        }
    }

private:
    void handleResult(const IAIUIEvent& event) const
    {
        Json::Value bizParamJson;
        Json::Reader reader;

        if (!reader.parse(event.getInfo(), bizParamJson, false)) {
            cout << "JSON 解析失败: " << event.getInfo() << endl;
            return;
        }

        Json::Value& data = (bizParamJson["data"])[0];
        Json::Value& params = data["params"];
        Json::Value& content = (data["content"])[0];

        string sub = params["sub"].asString();

        if (sub == "nlp" || sub == "iat" || sub == "tts") {
            Json::Value empty;
            Json::Value contentId = content.get("cnt_id", empty);
            if (contentId.empty()) return;

            string cntId = contentId.asString();
            int dataLen = 0;
            const char* buffer = event.getData()->getBinary(
                cntId.c_str(), &dataLen
            );

            if (sub == "tts") {
                Json::Value isUrl = content.get("url", empty);
                if (isUrl.asString() == "1") {
                    cout << "TTS URL: " << string(buffer, dataLen) << endl;
                }
            } else if (buffer) {
                cout << sub << ": " << string(buffer, dataLen) << endl;
            }
        }
    }
};
```

## 第五步：创建 AIUIAgent 并交互

```cpp
// 创建监听器
MyListener listener;

// 读取配置文件
string fileParam = readFileAsString("./AIUI/cfg/aiui.cfg");

// 创建 AIUIAgent
IAIUIAgent* agent = IAIUIAgent::createAgent(fileParam.c_str(), &listener);
```

### 发送唤醒消息

```cpp
IAIUIMessage* wakeupMsg = IAIUIMessage::create(AIUIConstant::CMD_WAKEUP);
agent->sendMessage(wakeupMsg);
wakeupMsg->destroy();
```

### 发送文本进行语义理解

```cpp
string text = "合肥明天天气怎么样";
Buffer* textData = Buffer::alloc(text.length());
text.copy((char*)textData->data(), text.length());

IAIUIMessage* writeMsg = IAIUIMessage::create(
    AIUIConstant::CMD_WRITE, 0, 0,
    "data_type=text,tts_res_type=url", textData
);
agent->sendMessage(writeMsg);
writeMsg->destroy();
```

::: warning 内存管理
每个 `IAIUIMessage` 使用后需要调用 `destroy()` 释放资源。`Buffer` 由 SDK 自动管理，无需手动释放。
:::

## 多语言调用（C 接口）

AIUI SDK 提供 C 接口，方便 Python、Go 等非 C++ 语言通过 FFI 调用：

```c
// 获取版本信息
const char* version = aiui_get_version();

// 创建 Agent
AIUIAgent agent = aiui_agent_create(config, callback, user_data);

// 发送消息
aiui_agent_send_message(agent, msg);

// 销毁 Agent
aiui_agent_destroy(agent);
```

::: tip 调用约定
- **Windows** 平台：函数导出基于 `__stdcall` 调用
- **Linux** 等其他平台：基于 `__cdecl` 调用
:::

## 下一步

- [Android SDK 集成教程](/tutorials/sdk-android) — 在 Android 应用中集成 AIUI
- [iOS SDK 集成教程](/tutorials/sdk-ios) — 在 iOS 应用中集成 AIUI
- [API 接入教程](/tutorials/api-integration) — 通过 WebSocket API 接入 AIUI
- [SDK 基础信息](/sdk-dev/basics/) — 了解 SDK 接口、参数和事件详情
