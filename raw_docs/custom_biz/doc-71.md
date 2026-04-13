---
title: 技能后处理协议：标准请求
source_url: https://aiui-doc.xf-yun.com/project-1/doc-71/
---

**目录**

1. 请求类型分类
2. 请求类型说明
    2.1. IntentRequest
    2.1.1. 消息示例
    2.1.2. 参数说明
    2.1.2.1. slots 参数说明
    2.2. LaunchRequest
    2.2.1. 消息示例
    2.2.2. 参数说明
    2.3. SessionEndedRequest
    2.4. TextRequest
    2.4.1. 消息示例
    2.4.2. 参数说明

# 请求类型分类

通过AIUI链路，标准请求request中包含经过AIUI解析后的用户请求有4类，其中 他们分为：

| 请求类型 | 是否常用 | 介绍 | 技能类型 |
| --- | --- | --- | --- |
| IntentRequest | 是 | 用户的语音请求经过AIUI解析后请求你的服务器时，你将会收到这个请求。 | 私有技能 |
| LaunchRequest | 否 | 适用于开放技能，用户通过入口词“打开{技能名称}”进入你的技能时，你将会收到这个请求。 | 开放技能（进入操作） |
| SessionEndedRequest | 否 | 用户主动退出技能结束会话时，你将会收到这个请求。 | 开放技能（退出操作） |
| TextRequest | 否 | 在你的技能中，用户的语音请求未经过AIUI解析直接请求你的服务器时，你将会收到这个请求。 | iflyos链路业务 |

- 该文档中，除了`IntentRequest`外，其他均只适用于技能协议v2.1，v2.0中没有该请求。
- `IntentRequest`在v2.1中有字段更新。

标准请求是所有技能都需要实现的请求，这些请求中包含[请求协议\_2.1](https://aiui-doc.xf-yun.com/project-1/doc-73/)中提到的所有字段：version, session, context, request。

# 请求类型说明

## 2.1. IntentRequest

当用户命中了你的技能中定义的意图时，你将会收到请求。

### 2.1.1. 消息示例

```json
{
  "type": "IntentRequest",
  "requestId": "TbXlwz-F86pYnD0VwWbqauUDRwiNOU5i70DgS54E8wFCqpK2ku9bGYKzCGfm1mNw",
  "timestamp": "2018-09-05T02:59:45.503551Z",
  "dialogState": "STARTED",
  "query": {
      "type": "TEXT",
      "original": "下一首"
  },
 "intent": {
    "name": "string",
    "score": float,
    "confirmationStatus": "string",
    "slots": {
      "SlotName": {
        "name": "SlotName",
        "value": "周董",
        "normValue": "周杰伦",
        "moreValue": ["槽值1","槽值2"],
        "confirmationStatus": "string",
      }
    }
  }
}
```text

### 2.1.2. 参数说明

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| type | 请求类型，这里取值 `IntentRequest` | string | 是 |
| requestId | 代表请求的唯一标识符。 | string | 是 |
| timestamp | 请求时间戳，以ISO 8601格式发送 | string | 是 |
| dialogState | 当前会话状态。**取值：** `STARTED`开始，`IN_PROGRESS`进行中，`COMPLETED`完成（意图收集和确认了所有必填槽位，同时如果意图有需求也已经一并确认了） | string | 是 |
| query | 请求信息。 - type: 请求类型，取值`TEXT` - original: 用户语音经过ivs理解后生成的文本 | object | 是 |
| intent | 意图信息 | object | 是 |
| intent.name | 意图名称，你的技能中定义的意图名称 | string | 是 |
| intent.score | 意图置信度。iFLYOS语义理解之后对用户语料命中该意图的置信度。 | string | 是 |
| intent.confirmationStatus | 意图确认状态。**取值：**`NONE`未确认，`CONFIRMED`确认，`DENIED`否认。当`dialogState`为`COMPLETED`时，此处状态为`CONFIRMED`或`DENIED`。当意图不需要确认时，该字段不出现 | string | 否 |
| intent.slots | 意图中的槽位信息，以key-value结构展示，key为槽名，value为槽值。只显示解析出来的槽。IVS开放意图此项不显示；意图中未定义词槽，该字段不出现。 | array | 否 |

#### 2.1.2.1. slots 参数说明

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| [slotName].name | 槽位名称 | string | 是 |
| [slotName].value | 用户语料经过语义理解后解析出来的槽值，是用户语料中包含的词，如“周董”。 | string | 是 |
| [slotName].normValue | 用户语料经过语义理解后解析出来并规整后的槽值，指向实体主字段取值。例如匹配歌星实体，不管上面value取值是`华仔`还是`华哥`，该字段取值固定都是`刘德华` | string | 是 |
| [slotName].moreValue | 用户语料经过语义理解后解析出来的槽值，当用户语料中包含该词槽的多个槽值时，出现该字段，以数组形式展示。比如用户说“我要买苹果，香蕉和橘子”，则`value`=”苹果”,`moreValue`=[“香蕉”,”橘子”]。`moreValue`取值来源于用户语料中包含的槽值的词条名（`normValue`） | array | 否 |
| [slotName].confirmationStatus | 槽确认状态。**取值：**`NONE`未确认，`CONFIRMED`确认，`DENIED`否认。当词槽非必填时，该字段不出现。 | string | 否 |

## 2.2. LaunchRequest

### 2.2.1. 消息示例

```json
{
  "type": "LaunchRequest",
  "requestId": "f78b7d68...",
  "timestamp": "2018-08-06T16:13Z ",
}
```text

### 2.2.2. 参数说明

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| type | 请求类型，这里取值 `LaunchRequest` | String | 是 |
| requestId | 代表请求的唯一标识符。 | String | 是 |
| timestamp | 请求时间戳，以ISO 8601格式发送 | String | 是 |

## 2.3. SessionEndedRequest

用户触发了结束会话的操作时发送。

消息示例

```json
{
  "type": "SessionEndedRequest",
  "requestId": "f78b7d68...",
  "timestamp": "2018-08-06T16:13Z ",
  "reason": "ERROR",
  "error": {
    "type": "INVALID_RESPONSE",
    "message": "无效回复"
  }
}
```text

**参数说明**

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| type | 请求类型，这里取值 `SessionEndedRequest` | String | 是 |
| requestId | 代表请求的唯一标识符。 | String | 是 |
| timestamp | 请求时间戳，以ISO 8601格式发送 | String | 是 |
| reason | 结束会话的原因，**取值：** - `USER_INITIATED`：用户明确结束了会话；  - `ERROR`：错误导致会话结束；  - `EXCEEDED_MAX_REPROMPTS`：用户无输入或多次输入无法理解 | String | 是 |
| error | 当结束原因为`ERROR`时，出现该字段。包含： - type: 错误类型，**取值：**  - `INVALID_RESPONSE`，无效回复  - `DEVICE_COMMUNICATION_ERROR`，设备通讯错误  - `INTERNAL_ERROR`，内部错误 - message: 错误信息 | Object | 否 |

## 2.4. TextRequest

### 2.4.1. 消息示例

```json
{
  "type": "TextRequest",
  "requestId": "f78b7d68...",
  "timestamp": "2018-08-06T16:13Z ",
  "query": {
    "type": "TEXT",
    "original":"今天天气怎么样？"
  }
}
```

### 2.4.2. 参数说明

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| type | 请求类型，这里取值 `TextInputRequest` | String | 是 |
| requestId | 代表请求的唯一标识符。 | String | 是 |
| timestamp | 请求时间戳，以ISO 8601格式发送 | String | 是 |
| query | 请求信息。 - type:请求类型，取值`TEXT` - original:用户语音经过IVS理解后生成的文本 | String | 是 |
