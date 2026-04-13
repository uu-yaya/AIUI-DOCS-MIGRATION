---
title: 参数配置 - iOS / Windows / Linux 示例
description: AIUI iOS / Windows / Linux SDK 动态参数设置示例代码。
---

> 参数说明请参见[参数配置说明](./)

## iOS / Windows / Linux 动态参数设置示例

```cpp
// 1. 情景模式动态设置
const char* setParams = "{\"global\":{\"scene\":\"main\"}}";
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, setParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 2. 经纬度参数动态设置
// 注意经纬度取值：精确位数不要超过8位
const char* gpsParams = "{\"audioparams\":{\"msc.lng\":\"117.16334474\",\"msc.lat\":\"31.82102191\"}}";
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, gpsParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 3. 自定义参数动态设置
const char* userParams = "{\"userparams\":{\"k1\":\"v1\",\"k2\":\"v2\"}}";
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, userParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();

// 4. 云端合成发音人参数动态设置（全链路合成时指定）
const char* ttsParams = "{\"audioparams\":{\"vcn\":\"xxx\",\"speed\":\"50\",\"volume\":\"50\",\"pitch\":\"50\"}}";
IAIUIMessage* writeMsg = IAIUIMessage::create(AIUIConstant::CMD_SET_PARAMS, 0, 0, ttsParams, NULL);
m_angent->sendMessage(writeMsg);
writeMsg->destroy();
```
