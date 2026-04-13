---
title: 参数配置 - Android 示例
description: AIUI Android SDK 动态参数设置示例代码。
---

> 参数说明请参见[参数配置说明](./)

## Android 动态参数设置示例

```java
// 1. 情景模式动态设置
String setParams = "{\"global\":{\"scene\":\"main\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0, 0, setParams, null);
mAIUIAgent.sendMessage(setMsg);

// 2. 经纬度参数动态设置
// 注意经纬度取值：精确位数不要超过8位
String gpsParams = "{\"audioparams\":{\"msc.lng\":\"117.16334474\",\"msc.lat\":\"31.82102191\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0, 0, gpsParams, null);
mAgent.sendMessage(setMsg);

// 3. 自定义参数动态设置
String userParams = "{\"userparams\":{\"k1\":\"v1\",\"k2\":\"v2\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0, 0, userParams, null);
mAgent.sendMessage(setMsg);

// 4. 云端合成发音人参数动态设置（全链路合成时指定）
String ttsParams = "{\"audioparams\":{\"vcn\":\"xxx\",\"speed\":\"50\",\"volume\":\"50\",\"pitch\":\"50\"}}";
AIUIMessage setMsg = new AIUIMessage(AIUIConstant.CMD_SET_PARAMS, 0, 0, ttsParams, null);
mAIUIAgent.sendMessage(setMsg);
```
