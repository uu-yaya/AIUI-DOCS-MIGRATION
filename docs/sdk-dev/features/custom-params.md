---
title: 自定义参数
---

::: info 概述
自定义参数是系统中用于个性化配置的重要组成部分，以下是关于自定义参数的详细说明：
:::

## 能力概述

在AIUI服务使用过程中，客户侧需要结合端侧上报的自定义数据+AIUI服务结果做业务处理。这时候就需要AIUI支持端侧自定义参数上传。

自定义参数上报，云端服务常见使用的服务模块有：

- 自定义技能的技能后处理
- 应用后处理

知识说明

1、技能后处理是自定义技能的业务补充，仅在当前技能中生效。只有当对话触发该技能，才会执行。

2、应用后处理是和 识别、语义技能、合成 等平级的能力模块，业务配置后每次对话都会触发。

## 参数上传和使用

自定义参数取值内容没有任何限制，只要在满足的json格式下开发者端侧上报与云端协定好解析格式即可。

### 2.1. 静态参数配置

在AIUI配置参数文件aiui.cfg，可以直接配置userparams来指定设备端需要携带的自定义参数:

```text
/* 用户参数，透传到后处理(非必须)*/
"userparams":{
    "k1": "v1", //满足json格式的自定义数据，取值无限制要求
    "k2": "v2"
    ……
},
```

示例：

```text
/* 用户参数，透传到后处理(非必须)*/
"userparams":{
    "deviceId": "abcd12345"
},
```

### 2.2. 动态参数配置

使用`CMD_SET_PARAMS`进行参数更新，更新后默认参数是在当前对话的下一次对话开始生效。
示例代码如下:

```java
String setParams = "{\"userparams\":{\"k1\":\"v1\",\"k2\":\"v2\"}}";
AIUIMessage setMsg = new AIUIMessage(CMD_SET_PARAMS, 0 , 0, setParams, "");
mAgent.sendMessage(setMsg);
```

## 云端数据处理

### 3.1. 自定义技能后处理

在技能后处理中，可以通过 Custom.iflytek\_data.user\_data 字段取值来获取端侧上传的自定义参数。详见技能后处理Request\_v2.1协议文档。

![](/media/202508/2025-08-25_144513_1077030.9314517508412556.png)

解析代码示例：

```javascript
AIUI.create("v2.1", function(aiui, err) {
  var requestObject = aiui.getRequest().getObject();
  // 获取自定义数据
  var customData = requestObject.context.Custom.iflytek_data.user_data;
  aiui.commit();
 })
```

### 3.2. 应用后处理

AIUI服务在做应用后处理服务转发时，转发数据结构体直接有`UserParams`参数字段指定自定义参数，开发者服务直接按照协议文档解析即可。详见应用后处理配置文档。

![](/media/202508/2025-08-25_145213_3605160.1510763737100994.png)
