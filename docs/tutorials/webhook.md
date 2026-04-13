---
title: 技能后处理与 Webhook 开发
description: 为自定义技能添加业务逻辑，支持云函数和 Webhook 两种方式
---

## 前置条件

- 已创建自定义技能并配置好意图和语料（参考 [自定义技能开发](/tutorials/custom-skill)）
- 了解基本的 HTTP 请求和 JSON 数据格式
- 如使用 Webhook 方式，需要一台可公网访问的服务器

## 你将完成的目标

通过本教程，你将学会：

1. 理解技能后处理的工作原理
2. 使用云函数实现简单的业务逻辑
3. 使用 Webhook 对接自有服务器
4. 处理填槽对话和多轮交互
5. 实现请求校验保障安全

## 技能后处理概述

技能后处理允许你在 AIUI 完成语义理解后，添加自定义业务逻辑。每次用户请求都会触发后处理流程：

1. 用户发起语音/文本请求
2. AIUI 完成语义理解，生成结构化结果（Request JSON）
3. 后处理接收结果并执行业务逻辑
4. 返回处理结果（Response JSON）给客户端

AIUI 支持两种后处理方式：

| 方式 | 优势 | 限制 |
|------|------|------|
| 云函数 | 无需服务器，在线编辑，即时生效 | Node.js v9.10.1 环境，1000ms 超时 |
| Webhook | 完全自主控制，支持复杂业务 | 需公网服务器，网络延迟增加耗时 |

## 方式一：云函数开发

### 基础模板

云函数使用 v2.1 协议。以下是最基础的模板，实现填槽对话托管和自定义回复：

```javascript
AIUI.create("v2.1", function(aiui, err) {
  // 获取请求对象
  var requestObject = aiui.getRequest().getObject();
  console.log(requestObject);

  // 获取 response 对象
  var response = aiui.getResponse();

  // 获取填槽对话状态
  var dialogState = requestObject.request.dialogState;

  if (dialogState != null && dialogState != "COMPLETED") {
    // 填槽对话未完成，托管给系统管理
    response.addDelegateDirective();
  } else {
    // 填槽对话完成，回复用户
    response.setOutputSpeech("这里修改成你想要的回复");
  }

  // 提交响应
  aiui.commit();
});
```

### 获取槽位值并构建回复

当需要使用用户填入的槽位信息时，通过 `getSlotValue` 获取：

```javascript
AIUI.create("v2.1", function(aiui, err) {
  var requestObject = aiui.getRequest().getObject();
  var response = aiui.getResponse();
  var dialogState = requestObject.request.dialogState;

  if (dialogState != null && dialogState != "COMPLETED") {
    response.addDelegateDirective();
  } else {
    // 获取已填充的槽位值
    var updatedIntent = aiui.getUpdatedIntent();
    var company = updatedIntent.getSlotValue("company");
    var number = updatedIntent.getSlotValue("number");

    var answer = "你的" + company + "快递，单号是：" + number + "，已经到达合肥市";
    response.setOutputSpeech(answer);
  }

  aiui.commit();
});
```

### 根据意图返回不同回复

当技能包含多个意图时，可根据意图名称分别处理：

```javascript
AIUI.create("v2.1", function(aiui, err) {
  var requestObject = aiui.getRequest().getObject();
  var response = aiui.getResponse();
  var intentName = requestObject.request.intents[0].name;
  var dialogState = requestObject.request.dialogState;

  console.log("本次意图来自: " + intentName);

  if (dialogState != null && dialogState != "COMPLETED") {
    response.addDelegateDirective();
  } else if (intentName === "query_express") {
    response.setOutputSpeech("正在为你查询快递信息");
  } else if (intentName === "cancel_order") {
    response.setOutputSpeech("订单已取消");
  } else {
    response.setOutputSpeech("抱歉，我不太理解你的意思");
  }

  aiui.commit();
});
```

::: warning 云函数注意事项
- 整体处理耗时不能超过 **1000ms**，超时后技能将退出
- 避免编写死循环等阻塞事件循环的代码
- 异步操作（如 HTTP 调用）需设置合理超时
- 危险代码会导致技能被下线
:::

## 方式二：Webhook 开发

Webhook 将请求转发到你的自有服务器，适合需要访问数据库、调用第三方 API 等复杂场景。

### 配置步骤

1. 在技能配置中选择 Webhook 方式
2. 填写你的服务器 URL 地址（需支持公网访问）
3. AIUI 会先发送 GET 请求验证服务器

### 服务器验证（GET 请求）

AIUI 会发送 GET 请求到你的 URL，请求参数包括：

| 参数 | 说明 |
|------|------|
| `signature` | 加密签名，由 token + timestamp + rand 生成 |
| `timestamp` | 时间戳 |
| `rand` | 随机数 |

验证流程：

1. 将 `token`、`timestamp`、`rand` 三个值按字典序排序
2. 拼接成一个字符串后进行 SHA1 加密
3. 将加密结果与 `signature` 对比验证
4. 验证通过后，将 `token` 的 SHA1 加密值放在响应 body 中返回

Java 示例：

```java
Map<String, String[]> parameterMap = request.getParameterMap();
String rand = parameterMap.get("rand")[0];
String timestamp = parameterMap.get("timestamp")[0];
String signature = parameterMap.get("signature")[0];

// 字典序排序
ArrayList<String> signList = new ArrayList<>();
signList.add(aiuiToken);
signList.add(rand);
signList.add(timestamp);
Collections.sort(signList);

// 拼接并校验
String sign = StringUtils
    .strip(signList.toString(), "[]")
    .replace(" ", "")
    .replace(",", "");

if (StringUtils.compare(signature, DigestUtils.sha1Hex(sign)) != 0) {
    return "authentication failed";
} else {
    return DigestUtils.sha1Hex(aiuiToken);
}
```

### 接收消息（POST 请求）

验证通过后，AIUI 会将交互结果通过 POST 请求发送到你的 URL。

请求格式：

```http
POST /your-endpoint HTTP/1.1
Content-Type: application/json
```

消息体结构：

```json
{
  "MsgId": "1234567",
  "CreateTime": 1348831860,
  "AppId": "12345678",
  "UserId": "d123455",
  "SessionParams": "Base64 编码的会话参数",
  "UserParams": "Base64 编码的用户自定义参数",
  "FromSub": "kc",
  "Msg": {}
}
```

关键字段说明：

| 字段 | 类型 | 说明 |
|------|------|------|
| `MsgId` | String | 消息唯一标识，用于排重 |
| `CreateTime` | Integer | 消息创建时间戳 |
| `FromSub` | String | 上游业务类型：`iat`（听写）或 `kc`（语义） |
| `UserParams` | String | 客户端上传的自定义参数，Base64 编码 |
| `Msg` | Object | 消息内容 |

::: tip 消息排重
使用 `MsgId` + `CreateTime` 组合进行排重，避免重复处理同一消息。
:::

### 响应格式

Webhook 使用 v2.1 协议返回响应：

```json
{
  "version": "2.1",
  "sessionAttributes": {
    "key": "value"
  },
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "查询结果：你的快递已到达合肥"
    },
    "expectSpeech": false,
    "shouldEndSession": true
  }
}
```

## 应用后处理配置

除了技能级别的后处理，AIUI 还支持 **应用级别** 的后处理配置，可在应用配置页面设置：

1. 填写云服务地址（支持备用地址）
2. 配置超时时间和重试次数（最大时长 x 尝试次数 <= 9000ms）
3. 可选开启消息加密（AES CBC 模式，128bit 密钥）

::: warning 超时限制
请求超时最大时长由尝试次数决定：**最大时长 x 尝试次数 <= 9000ms**。例如设置 3 次重试，则每次超时上限为 3000ms。
:::

## 下一步

- [问答库开发](/tutorials/qa-library) — 创建知识问答库
- [智能体开发](/tutorials/agent-dev) — 开发更复杂的智能体
- [API 接入教程](/tutorials/api-integration) — 通过 WebSocket API 接入 AIUI
