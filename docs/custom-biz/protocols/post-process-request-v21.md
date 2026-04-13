---
title: 技能后处理协议：Request v2.1
---

::: info 概述
自定义技能开发包括以下步骤：

- 处理AIUI发送的不同类型的请求
- 在返回完整回复前选择性地发送一些信息给用户，比如告诉用户系统正在处理中
- 对用户的请求返回合适的回复
:::

## 请求校验

请求校验可以保障数据安全。

- 每一个AIUI发送的请求均包含一个application\_ID，你需要检查这个ID是否和你的技能ID相同；
- 所有发送给技能的请求Header都包含`Signature`字段（[校验步骤](/custom-biz/protocols/post-process-verify)）

当请求不符合以上两点，你应该返回`HTTP CODE: 400`.

## HTTP头

```http
POST / HTTP/1.1
Content-Type : application/json;charset=UTF-8
Host : your.application.endpoint
Content-Length :
Accept : application/json
Accept-Charset : utf-8
Signature: xxxxxxxxxxxxxxx
```

## Body示例

```json
{
  "version": "2.1",
  "session": {
    "new": true,
    "sessionId": "f78b7d68...",
    "attributes": {
      "key": "String value"
    }
  },
  "context": {
    "Custom":{
      "iflytek_data":{
        "user_data": "xxxxxx",
        "device_request_id": "xxxxx"
      },
      "custom_data": {
        "key": "value"
      }
    },
    "System": {
      "device": {
        "deviceId": "f78b7d68...",
        "supportedInterfaces": {
          "AudioPlayer": {},//音频播放器
          "TemplateRuntime": {},//屏幕模板渲染
          "PlaybackController": {},//音频播放控制
        },
        "location":{
          "lng": float,
          "lat": float
        },
        "platform": {
          "name" : "android",
          "version": "8.0.1"
        },
        "kidMode": {
          "enable": true
        }
      },
      "application": {
        "applicationId": "f78b7d68..."
      },
      "user": {
        "userId": "f78b7d68...",
        "accessToken": "23bf653f..."
      }
    },
    "AudioPlayer": {
      "playerActivity": "PLAYING",
      "token": "audioplayer-token",
      "offsetInMilliseconds": 0
    }
  },
  "request": {}
}
```

正文参数说明

所有请求都包含顶层的*version*、*session*、*context*和*request*对象。

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| version | 请求的版本, 其值定义为: “2.1 “ | String | 是 |
| session | 用户的会话信息，仅包含在标准请求中。[查看详细](#session) | Object | 否 |
| context | 设备端状态。[查看详细](#context) | Object | 是 |
| request | 经过AIUI解析的用户请求。 | Object | 是 |

### session参数说明

session表示用户会话信息，一次session过程从用户调起技能到结束，表示用户与技能的一次会话。会话结束方式：技能返回结束，用户明确结束，或用户输入错误导致结束。

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| new | 一个布尔值, 指示这是否为新会话。新会话返回true，已有会话的返回false 。 | boolean | 是 |
| sessionId | 活动会话的唯一标识符。sessionId 对于用户和会话的多个后续请求是一致的。如果用户的会话结束, 则为同一用户的后续请求提供一个新的唯一 sessionId 值。 | String | 是 |
| attributes | 用于保存上下文信息，由开发者自定义上传。对于新会话已从新设置为 true 的新会话, 属性映射为空。 拦截器可在response中的sessionAttributes中设置属性，在同一会话的下一次请求中在此字段中回传。 | map | 是 |

### context参数说明

在向服务发送请求时, `context`对象提供了有关 IVS 服务和设备当前状态的信息。对于在会话上下文 (CanFulfillIntentRequest、LaunchRequest 和 IntentRequest) 中发送的请求, `context`对象将复制会话对象中可用的用户和应用程序信息。

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| Custom | 设备传输给技能使用的自定义信息 | Object | 否 |
| Custom.iflytek\_data | 讯飞的自定义数据，应用开发者可以把要传输给技能的自定义数据放到这个字段中。 | Object | 否 |
| Custom.iflytek\_data. user\_data | 自定义用户数据，相当于v2.0协议中的`userparams` | String | 否 |
| Custom.iflytek\_data. device\_request\_id | 设备请求时生成的request\_id，只有拦截器技能会收到这个字段 | String | 否 |
| Custom.custom\_data | 自定义数据，其中的key-value由设备厂商自行定义 | Object | 否 |
| System | 与技能交互的设备的信息 | Object | 是 |
| System.application | 技能信息。包含： - applicationId | Object | 是 |
| System.device | 设备信息。包含： - deviceId：设备唯一标识符。 - suportedInterfaces：设备支持的接口列表。**取值：**`AudioPlayer: {}`、`PlaybackController{}`、`TemplateRuntime{}`。 - location：设备的地理位置。包含：lng：经度，lat：纬度 - kidMode：设备当前是否处于儿童模式 | Object | 是 |
| System.user | 用户信息。包含： - userId：提出请求的用户的唯一标识符。不超过255个字符。这个userId是在用户启用技能时自动生成的。禁用和重新启用技能会说呢过程新的标识符。 - accessToken：第三方（拦截器服务）的授权token。 | Object | 是 |
| AudioPlayer | 音频播放器当前状态 | Object | 是 |
| AudioPlayer.token | 音频资源的标识符。该字段只发送给最近一次播放音频的技能方。 | String | 否 |
| AudioPlayer. offsetInMilliseconds | 播放进度。该字段只发送给最近一次播放音频的技能方。 | Long | 否 |
| AudioPlayer. playerActivity | 音频播放器状态。**取值** : IDLE，PAUSED，PLAYING，BUFFER\_UNDERRUN，FINISHED，STOPPED | String | 是 |

### request参数说明

request中包含经过AIUI解析后的用户请求。他们分为：

- 标准请求
  - `LaunchRequest`: 用户通过入口词“打开`{技能名称}`”进入你的技能时，你将会收到这个请求。
  - `TextRequest`: 在你的技能中，用户的语音请求未经过AIUI解析直接请求你的服务器时，你将会收到这个请求。
  - `IntentRequest`: 用户的语音请求经过AIUI解析后请求你的服务器时，你将会收到这个请求。
  - `SessionEndedRequest`: 用户主动退出技能结束会话时，你将会收到这个请求。
