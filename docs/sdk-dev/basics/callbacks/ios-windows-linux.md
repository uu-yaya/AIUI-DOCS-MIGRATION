---
title: 回调解析 - iOS / Windows / Linux
description: AIUI iOS / Windows / Linux SDK 交互结果解析示例代码。
---

> 回调概述请参见[回调解析说明](./)

## 交互结果解析

`EVENT_RESULT` 的 data 中包含的结果数据需根据 info 描述信息获取。iOS / Windows / Linux 平台使用 C++ 接口：

```cpp
using namespace VA;
Json::Value bizParamJson;
Json::Reader reader;

if (!reader.parse(event.getInfo(), bizParamJson, false)) {
    NSLog(@"parse error!, getinfo=%s", event.getInfo());
}

Json::Value data = (bizParamJson["data"])[0];
Json::Value params = data["params"];
Json::Value content = (data["content"])[0];
std::string sub = params["sub"].asString();

if (sub == "iat") {
    Json::Value empty;
    Json::Value contentId = content.get("cnt_id", empty);

    if (contentId.empty()) {
        NSLog(@"Content Id is empty");
        break;
    }
    std::string cnt_id = contentId.asString();
    Buffer *buffer = event.getData()->getBinary(cnt_id.c_str());

    if (NULL != buffer) {
        const char *resultStr = (char *) buffer->data();
        if (resultStr == NULL) {
            return;
        }
        NSLog(@"resultStr=%s", resultStr);
    }
}
```

::: info 说明
其他事件（唤醒、VAD、状态、播放器、报错等）的回调结构与 [Android 事件解析](./android)相同，仅 API 调用方式不同（使用 `IAIUIEvent` 的 `getEventType()`、`getArg1()` 等 C++ 接口）。
:::
