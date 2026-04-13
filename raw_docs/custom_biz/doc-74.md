---
title: 技能后处理协议：Response_v2.1协议
source_url: https://aiui-doc.xf-yun.com/project-1/doc-74/
---

### 注意：

协议v2.1比v2.0协议，存在字段增删，和支持取值的增加。

在你处理完技能发送的请求后，你需要给用户发送回复。回复可以是：

- 技能请求处理完成回复用户TTS
- 播放一些和技能相关的提示音

## HTTP头

```
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Content-Length:
```

## body示例

```json
{
  "version": "2.1",
  "sessionAttributes": {
    "key": "value"
  },
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "Plain text String to speak"
    },
    "reprompt": {
      "outputSpeech": {
        "type": "PlainText",
        "text": "Plain text String to speak"
      }
    },
    "card": {
      "type": "Standard",
        "title": {
          "size":"LARGE|SMALL",
          "text":"20~32℃"
      },
        "content":"2018-08-27 | 广州",
        "imageUrl":"https://carfu.com/resources/card-images/race-car-small.png",
        "link": {
          "url":"example.iflyos.cn/",
          "text":"点击查看"
      }
    },
     "directives": [
    {
      "type": "AudioPlayer.Play",
      "playBehavior": "ENQUEUE",
      "audioItem": {
        "stream": {
          "type": "AUDIOH",
          "url": "https://example.com/audiofile.mp3",
          "token": "S0wiXQZ1rVBkov...",
          "expectedPreviousToken": "f78b7d68...",
          "offsetInMilliseconds": 0
        },
        "metadata": {
          "title": "《十年》",
          "subtitle": "陈奕迅",
          "art": {
            "sources": [
              {
                "url": "https://example.com/brie-album-art.png"
              }
            ]
          }
        }
      }
    }
  ],
    "expectSpeech": true,
    "shouldEndSession": true
  }
}
```text

响应正文参数说明

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| version | 版本，取值2.1 | String | 是 |
| sessionAttributes | 需要放入下一次请求的`session{attributes{}}`中回传至技能的属性。包含key， value | Object | 否 |
| response | 返回内容。 | Object | 是 |

### 标准响应中的对象

| 参数 | 描述 | 类型 | 必须出现 |
| --- | --- | --- | --- |
| outputSpeech | 操作返回的语音文本 - type: 输出语音类型，**取值：**`PlainText`，纯文本 - text: 文本内容，type取值为`PlainText`时需要出现该字段。 | Object | 否 |
| reprompt | 若该技能回复需要打开录音收听用户的语音回复，当用户在8秒内没有说话时，设备将推送该语音文本，用于再次提示用户输入。 推送后设备再打开录音8s。若用户依旧没有说话，则会话结束。 - type: 输出语音类型，**取值：**`PlainText`，纯文本 - text: 文本内容，type取值为`PlainText`时需要出现该字段。 | Object | 否 |
| card | 用于向设备的关联APP推送消息。支持三种卡片类型：Simple、Standard、List。 - [点击查看详情](./display_card.md) | Object | 否 |
| directives | 一组指令，用于指定使用特定接口进行设备级别的操作。目前支持以下指令： - AudioPlayer指令  - Playback指令  - Dialog指令 - Display指令 | Array | 否 |
| expectSpeech | 该返回是否需要设备打开麦克风进行追问。true代表要追问，默认取值为false | Boolean | 否 |
| shouldEndSession | 该返回是否为会话的终点。true表示会话在响应后结束；false表示会话保持活动状态。如果未提供，则默认为true。我们约定：若回复中包含`AudioPlayer`，且技能没有过多交互，此处取值必须为`true` | Boolean | 否 |

### 针对不同请求的响应

| request | response格式 |
| --- | --- |
| [LaunchRequest](https://aiui-doc.xf-yun.com/project-1/doc-71/) | 标准响应中的所有内容的均可根据业务需求选择包含 |
| [TextRequest](https://aiui-doc.xf-yun.com/project-1/doc-71/) | 标准响应中的所有内容的均可根据业务需求选择包含 |
| [IntentRequest](https://aiui-doc.xf-yun.com/project-1/doc-71/) | 标准响应中的所有内容的均可根据业务需求选择包含 |
| [SessionEndedRequest](https://aiui-doc.xf-yun.com/project-1/doc-71/) | - 若`reason`为`USER_INITIATED`，可以回复。回复内容中只能包括`outputSpeech`，且`ShouldEndSession`取值必须为`true`。  - 若`reason`为`ERROR`，不可回复。 |
