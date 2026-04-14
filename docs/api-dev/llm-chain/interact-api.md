---
title: 交互 API
---

::: info 概述
交互API概述涵盖了与系统进行数据交互的完整流程，包括连接建立、请求发送、结果处理及相关补充说明。
:::

## 服务介绍

本协议接口仅适用于`通用大模型交互链路`服务场景，提供在线语音交互能力。
[WebSocket DEMO](https://gitee.com/iflytek-aiui/AIUILiteDemo "WebSocket DEMO")

### 说明

星火交互认知大模型支持按台授权，联系讯飞商务或邮件咨询[aiui\_support@iflytek.com](mailto:aiui_support@iflytek.com)。

## 接口说明

本协议基于websocket协议，交互过程含3个阶段：建立连接、交互、断开。

::: warning 注意
单次会话后超过60s未发送数据，云端主动断开链接
:::

## 建立连接

WebSocket 握手阶段用于设置参数和鉴权，参数在url 中指定，握手请求和参数必须符合 WebSocket 协议。

### 请求地址

> ws[s]://aiui.xf-yun.com/v2/aiint/ws

### 请求示例

> ws[s]://aiui.xf-yun.com/v2/aiint/ws?host=xxx&date=xxx&authorization=xxx
>  需 url encode

具体鉴权参数构建见[鉴权文档](/api-dev/llm-chain/auth "鉴权文档")说明。

## 交互请求

WebSocket连接后进入通信阶段，此时客户端主动操作有：上传数据或断开连接，被动操作有：接收结果和错误信息

### 请求数据结构

> 请求数据格式由header，parameter 和 payload 构成。详细结构见[**【附录】**](#附录)说明

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "xxx",
        "stmid": "text-1",
        "status": 3,
        "scene": "main_box",
        "msc.lat": 19.65309164062,
        "msc.lng": 109.259056086,
        "os_sys": "windows"
    },
    "parameter": {
        "nlp": {
            "nlp": {
                "compress": "raw",
                "format": "json",
                "encoding": "utf8"
            },
            "sub_scene": "cbm_v45",
            "new_session": true
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5L2g5aW95ZWK",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

> 数据请求协议字段说明

| 参数 | 类型 | 必须 | 说明 | 备注 |
| --- | --- | --- | --- | --- |
| header | object | 是 | 协议头部 | 协议头部，⽤于描述平台特性的参数 |
| parameter | object | 是 | AI能⼒参数 | 特性参数，⽤于控制 AI 引擎特性的开关 |
| parameter.IAT（语音识别） | object | 否 | 识别参数 | 识别引擎控制参数设置，如vad信息 |
| parameter.NLP（语义理解） | object | 否 | 语义参数 | 语义结果格式控制、历史清理等参数设置 |
| parameter.TTS（语音合成） | object | 否 | 合成参数 | 合成参数设置，如发音人、合成音频类型等 |
| payload | object | 是 | 输⼊数据段 | 数据段，携带请求的数据 |
| payload.text | object | 否 | ⽂本输⼊ | 请求⽂本数据输⼊,文本请求时必传 |
| payload.audio | object | 否 | 语⾳输⼊ | 请求语⾳数据输入，音频请求时必传 |
| payload.cbm\_semantic | object | 否 | 结构化语义 | 透传参数：个性化、自定义参数设置 |
| payload.cbm\_reply | object | 否 | 可控对话回复 | 大模型回复设置：风格化回复 |
| payload.cbm\_semantic\_tpp | object | 否 | 应用后处理 | 透传参数：自定义参数设置 |
| payload.cbm\_knowledge | object | 否 | 知识检索 | 知识检索设置：文档问答标签检索和阈值设置 |

#### header 数据参数详细说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | 是 | AIUI应用信息中的appid取值 | a44e0f36 |
| sn | string | 是 | 设备(用户)唯一标识，长度不超过32位。 | 1234567890 |
| status | int | 是 | 取值范围 0 1 2 3；（0-首帧、1-中间帧、2-尾帧、3-数据一帧发送完毕，文本请求固定为3） | 3 |
| stmid | string | 是 | 会话请求id,用于标记不同会话，每次请求需要更新不同取值。长度不超过32位。 | audio-1、text-1 |
| scene | string | 是 | AIUI应用情景模式 | main、main\_box |
| msc.lat | double | 否 | 纬度，取值范围 -90 ~ +90，最长8位精度 | 19.65309164 |
| msc.lng | double | 否 | 经度，取值范围 -180 ~ +180，最长8位精度 | 109.25905608 |
| os\_sys | string | 否 | 应用系统类型 | windows |

#### parameter 数据参数详细说明

> IAT（语音识别） 识别参数

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| svad | string | 否 | 云端vad开关：1(打开)，0(关闭) | 1 |
| eos | string | 否 | 云端音频尾端点时长检测设置 | 1000 |
| vgap | string | 否 | 云端识别引擎会话断句时长检测设置 | 800 |
| speex\_size | int | 否 | speex音频帧大小，speex音频必传。详见附录speex\_size与speex库[**【压缩等级关系表】**](#speex压缩关系等级表) | 70 |
| IAT（语音识别）.compress | string | 是 | 识别结果类型 | 固定取值： raw |
| IAT（语音识别）.format | string | 是 | 识别结果格式 | 固定取值：json |
| IAT（语音识别）.encoding | string | 是 | 识别编码格式 | 固定取值：utf8 |

> NLP（语义理解） 语义参数

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| sub\_scene | string | 是 | 大模型引擎 | 固定取值：cbm\_v45 |
| richness | string | 否 | 回复丰富度： concise（简洁）、mid（中等）、rich（丰富）[默认取值，包含markdown标签] | concise |
| env | string | 否 | 设备人设:结构固定，其中expand\_persona取值代表是否支持大模型自定义扩展人设信息 ，persona取值为自定义人设的问题和答案。详细可见附录请求示例请求参数构建写法 | {"human":{"expand\_persona":true,"persona":"{\"父亲|爸爸\":\"科大讯飞\",\"姓名|名字|称呼\":\"小飞\"}"}} |
| new\_session | boolean | 否 | 是否清除本次会话历史 | true |
| sn | string | 否 | 信源激活绑定设备标识，与header中sn取值保持一致 | 1234567890 |
| NLP（语义理解）.compress | string | 否 | 预留字段：nlp结果类型 | 固定取值：raw |
| NLP（语义理解）.format | string | 否 | 预留字段：nlp结果格式 | 固定取值：json |
| NLP（语义理解）.encoding | string | 否 | 预留字段：nlp编码格式 | 固定取值：utf8 |

> TTS（语音合成） 合成参数
> 合成url下发仅支持在主动文本合成方式（即在发送文本数据时指定 header.scene 取值固定为 IFLYTEK.TTS（语音合成）），全链路合成结果下发仅支持音频流

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| vcn | string | 否 | 发音人取值  使用声音复刻时固定取值为： x5\_clone | x2\_xiaojuan |
| res\_id | string | 否 | 声音复刻资源id。 注意：仅在使用声音复刻（vcn=x5\_clone） 时需要携带本参数 | kps77sqew4k |
| oral\_level | string | 否 | 超拟人合成口语化等级（仅在超拟人合成调用中生效）  高:high, 中:mid, 低:low。默认mid | 默认取值: mid |
| TTS（语音合成）\_res\_type | string | 否 | 合成下发url链接 | 固定取值：url |
| TTS（语音合成）.bit\_depth | int | 是 | 音频位数 | 16 |
| TTS（语音合成）.channels | int | 是 | 音频通道数 | 1 |
| TTS（语音合成）.encoding | string | 是 | 音频格式：raw、speex-wb;10、lame、opus | raw |
| TTS（语音合成）.sample\_rate | int | 是 | 音频采样率 | 16000 |

#### payload 数据参数详细说明

payload项提供交互数据类型说明及对应参数设置，现阶段主要有：文本、音频两种请求，具体参数设置如下。

> payload.text 设置 (文本请求参数和内容)

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 编码格式，默认 utf8 | utf8 |
| compress | string | 是 | 压缩格式：默认 raw | raw |
| format | string | 是 | 内容格式：默认 plain | plain |
| status | int | 是 | 数据帧状态 | 固定取值：3 |
| text | string | 是 | 文本数据：需经base64编码 | 5L2g5aW95ZWK |

> payload.audio 设置 (音频请求参数和内容)

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 音频编码（取值：lame，speex，opus，opus-wb，speex-wb， raw，ico） | raw |
| sample\_rate | int | 是 | 采样率（取值 ：8000、16000） | 16000 |
| channels | int | 是 | 通道数（取值 ：1、2） | 1 |
| bit\_depth | int | 是 | 位数（取值 ：8、16） | 16 |
| status | int | 是 | 数据状态：首帧 0、中间帧 1、尾帧2，一帧传完 3 | 0 |
| frame\_size | int | 是 | 帧大小（取值： 0~1024） | 0 |
| audio | string | 是 | 音频数据：需经base64编码 |  |

> payload.cbm\_semantic 设置（透传参数设置）

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 内容编码：固定 utf8 | utf8 |
| compress | string | 是 | 内容压缩格式：固定 raw | raw |
| format | string | 是 | 内容格式：固定 json | plain |
| status | int | 是 | 数据帧发送帧状态，固定取值 3 | 3 |
| text | string | 是 | 支持pers\_param、userparam等参数设置：结果需经base64编码 | eyJ1c2VycGFyYW1zIjoiZXlKclpYa2lPaUoyWVd4MVpTSjkiLCJwZXJzX3BhcmFtIjoie1widWlkXCI6XCIxMjM0NTY3ODkwXCJ9In0= |

> payload.cbm\_semantic\_tpp 设置（自定义参数透传设置）

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 内容编码：固定 utf8 | utf8 |
| compress | string | 是 | 内容压缩格式：固定 raw | raw |
| format | string | 是 | 内容格式：固定 json | plain |
| status | int | 是 | 数据帧发送帧状态，固定取值 3 | 3 |
| text | string | 是 | UserParam参数设置：注意UserParams参数key的大小写，以及需要三次base64编码 | ZXlKVmMyVnlVR0Z5WVcxeklqb2laWGxLY2xwWWEybFBhVW95V1ZkNE1WcFRTamtpZlE9PQ== |

> payload.cbm\_reply 设置（风格化设置）

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 内容编码：固定 utf8 | utf8 |
| compress | string | 是 | 内容压缩格式：固定 raw | raw |
| format | string | 是 | 内容格式：固定 json | json |
| status | int | 是 | 数据帧发送帧状态，固定取值 3 | 3 |
| text | string | 是 | 风格化回复设置：base64编码 | W3sidHlwZSI6IumjjuagvOWMluaOp+WItiIsInZhbHVlIjoi55So5byg6aOe57KX54q355qE5Y+j5ZC76K+J6K+0In1d |

> payload.cbm\_knowledge 设置（文档问答指定文档标签搜索）

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 内容编码：固定 utf8 | utf8 |
| compress | string | 是 | 内容压缩格式：固定 raw | raw |
| format | string | 是 | 内容格式：固定 json | json |
| status | int | 是 | 数据帧发送帧状态，固定取值 3 | 3 |
| text | string | 是 | 文档问答标签：base64编码 | eyJ0YWdzIjp7Im11c3QiOlsi56eR5oqA5oql56ysMeeJiCJdfX0= |

## 结果说明

### 连接建立成功

> 连接成功消息示例如下：cid表示会话ID，后续会话都会关联该ID

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "cid": "xxx"
    }
}
```

### 数据交互 - 会话开始

> 初始消息格式示例：

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "cid": "xxx",
        "sid": "xxx",
        "stmid": "text-1",
        "status": 0
    }
}
```

### 数据交互 - 会话中间结果

说明：下面所有结果中 text 字段取值都要解析base64才能获取明文内容

> 会话中间结果：识别结果(IAT（语音识别）) 示例如下：

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "audio-1",
        "sid": "xxx",
        "cid": "xxx",
        "status": 1
    },
    "payload": {
        "iat": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 1,
            "seq": 1,        // 结果序号，从1开始计数，1、2、3……
            "text": "eyJ0ZXh0Ijp7ImJnIjowLCJlZCI6MCwibHMiOmZhbHNlLCJzbiI6MSwid3MiOlt7ImJnIjowLCJjdyI6W3sic2MiOjAsInciOiLku4rlpKkifV19LHsiYmciOjAsImN3IjpbeyJzYyI6MCwidyI6IuaYn+acnyJ9XX0seyJiZyI6MCwiY3ciOlt7InNjIjowLCJ3Ijoi5YegIn1dfV19fQ=="
         // {"text":{"bg":0,"ed":0,"ls":false,"sn":1,"ws":[{"bg":0,"cw":[{"sc":0,"w":"今天"}]},{"bg":0,"cw":[{"sc":0,"w":"星期"}]},{"bg":0,"cw":[{"sc":0,"w":"几"}]}]}}
        }
    }
}
```

> 会话中间结果：语义规整结果(cbm\_tidy) 示例：

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "text-1",
        "sid": "xxx",
        "cid": "xxx",
        "status": 1
    },
    "payload": {
        "cbm_tidy": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "plain",
            "seq": 0,
            "status": 2,
            "text": "eyJxdWVyeSI6IuWQiOiCpeS7iuWkqeeahOWkqeawlOaAjuS5iOagt+aYjuWkqeeahOWRoiIsImludGVudCI6W3siaW5kZXgiOjAsInZhbHVlIjoi5ZCI6IKl5LuK5aSp55qE5aSp5rCU5oCO5LmI5qC3In0seyJpbmRleCI6MSwidmFsdWUiOiLlkIjogqXmmI7lpKnnmoTlpKnmsJTmgI7kuYjmoLcifV19"
// {"query":"合肥今天天气？明天呢？","intent":[{"index":0,"value":"合肥今天天气"},{"index":1,"value":"合肥明天天气"}]}
        }
    }
}
```

> 会话中间结果：聚合语义结果(cbm\_semantic) 示例：

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "audio-1",
        "sid": "xxx",
        "cid": "xxx",
        "status": 1
    },
    "payload": {
        "cbm_meta": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "plain",
            "seq": 0,
            "status": 3,
            "text": "eyJjYm0tc2VtYW50aWMiOnsiaW50ZW50IjowfX0="
        },
        "cbm_semantic": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "plain",
            "seq": 0,
            "status": 3,
            "text": "eyJhbnN3ZXIiOnsidGV4dCI6IuaYr+aYn+acn+Wbm+OAgiIsInR5cGUiOiJUIn0sImFycmF5X2luZGV4IjowLCJjYXRlZ29yeSI6IklGTFlURUsuZGF0ZXRpbWVQcm8iLCJkYXRhIjp7fSwiZGVtYW5kX3NlbWFudGljIjp7ImRhdGV0aW1lIjoi5LuK5aSpIiwib3BlcmF0aW9uIjoiV0hBVFdFRUsiLCJzZXJ2aWNlIjoiZGF0ZXRpbWVQcm8ifSwiZGlhbG9nX3N0YXQiOiJEYXRhVmFsaWQiLCJvcGVyYXRpb24iOiJXSEFUV0VFSyIsIm9yaWdfc2VtYW50aWMiOnsic2xvdHMiOnsiZGF0ZXRpbWUiOiLku4rlpKkiLCJvcGVyYXRpb24iOiJXSEFUV0VFSyJ9fSwicmMiOjAsInNhdmVfaGlzdG9yeSI6dHJ1ZSwic2NvcmUiOjEsInNlYXJjaF9zZW1hbnRpYyI6eyJkYXRldGltZSI6IuS7iuWkqSIsIm9wZXJhdGlvbiI6IldIQVRXRUVLIiwic2VydmljZSI6ImRhdGV0aW1lUHJvIn0sInNlbWFudGljIjp7InNsb3RzIjp7ImRhdGV0aW1lIjp7ImRhdGUiOiIyMDIzLTA4LTI0IiwiZGF0ZU9yaWciOiLku4rlpKkiLCJ0eXBlIjoiRFRfQkFTSUMifSwib3BlcmF0aW9uIjoiV0hBVFdFRUsifX0sInNlcnZpY2UiOiJkYXRldGltZVBybyIsInNob3VsZGVuZHNlc3Npb24iOiJ0cnVlIiwic2lkIjoid2d3MDAwYzU5NTBAZHgxOGEyNmZmOWZkOTc4MjQ1MzIiLCJzdGF0ZSI6eyJmZzo6ZGF0ZXRpbWVQcm86OmRlZmF1bHQ6OmRlZmF1bHQiOnsic3RhdGUiOiJkZWZhdWx0In19LCJ0ZXh0Ijoi5LuK5aSp5pif5pyf5YegIiwidXNlZF9zdGF0ZSI6eyJzdGF0ZSI6ImRlZmF1bHQiLCJzdGF0ZV9rZXkiOiJmZzo6ZGF0ZXRpbWVQcm86OmRlZmF1bHQ6OmRlZmF1bHQifSwidXVpZCI6IndndzAwMGM1OTUwQGR4MThhMjZmZjlmZDk3ODI0NTMyIiwidmVyc2lvbiI6IjMyMi4wIn0="
            // {"answer":{"text":"是星期四。","type":"T"},"array_index":0,"category":"IFLYTEK.datetimePro","data":{},"demand_semantic":{"datetime":"今天","operation":"WHATWEEK","service":"datetimePro"},"dialog_stat":"DataValid","operation":"WHATWEEK","orig_semantic":{"slots":{"datetime":"今天","operation":"WHATWEEK"}},"rc":0,"save_history":true,"score":1,"search_semantic":{"datetime":"今天","operation":"WHATWEEK","service":"datetimePro"},"semantic":{"slots":{"datetime":{"date":"2023-08-24","dateOrig":"今天","type":"DT_BASIC"},"operation":"WHATWEEK"}},"service":"datetimePro","shouldendsession":"true","sid":"wgw000c5950@dx18a26ff9fd97824532","state":{"fg::datetimePro::default::default":{"state":"default"}},"text":"今天星期几","used_state":{"state":"default","state_key":"fg::datetimePro::default::default"},"uuid":"wgw000c5950@dx18a26ff9fd97824532","version":"322.0"}
        }
    }
}
```

> 会话中间结果：最终语义结果（NLP（语义理解）） 示例：

::: warning 注意
大模型语义结果根据结果序列做拼接操作时，当请求改写结果有多个，需要根据 payload.cbm\_meta.text.NLP（语义理解） 中 intent 字段取值来做结果标识区分（0代表第一个改写请求响应内容，1为第二个……）
:::

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "audio-1",
        "sid": "xxx",
        "cid": "xxx",
        "status": 1
    },
    "payload": {
        "cbm_meta": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "plain",
            "seq": 0,
            "status": 1,
            "text": "eyJubHAiOnsiaW50ZW50IjowLCJubHBfb3JpZ2luIjoiY2JtX3NlbWFudGljIn19"
            // {"nlp":{"intent":0,"nlp_origin":"cbm_semantic"}}
        },
        "nlp": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "plain",
            "seq": 2,            // 结果序号，从 0 开始，0、1、2、3……
            "status": 1,        // 结果帧类型：0-首帧、1-中间帧、2-尾帧
            "text": "56Wd5oKo5bqm6L+H5LiA5Liq"    // 祝您度过一个
        }
    }
}
```

> 会话中间结果：合成结果（TTS（语音合成））示例：

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "text-1",
        "sid": "xxx",
        "cid": "xxx",
        "status": 2
    },
    "payload": {
        "tts": {
            "encoding": "opus",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
            "frame_size": 0,
            "status": 2,
            "seq": 1,
            "audio": "aHR0cHM6Ly9haXVpLm9wZW5zcGVlY2guY24vdHRzL2Rvd25sb2FkL1lYQndhV1E5WVRRMFpUQm1NellzYzJsa1BYZG5kekF3TUdOak9UZzRRR1I0TVRoaE1tRTJZbVV6WmpFM09ESTBOVE15TEhKcFpEMHgubXAz"
            // 当请求携带参数 tts_res_type：url 时下发url，否则下发音频数据流
        }
    }
}
```

### 下发结果类型说明

| 结果字段 | 类型 | 解析需要 | 结果说明 | 备注 |
| --- | --- | --- | --- | --- |
| payload.IAT（语音识别） | object | 是 | 识别结果 | 解析结果时注意是否开启了流式识别（text解析后查看是否 pgs 参数存在） |
| payload.cbm\_tidy | object | 是 | 语义规整结果 | 当请求包含有多个意图时会进行意图拆分，后续服务按照实际拆分的结果执行请求。如请求“合肥今天天气如何明天的呢” |
| payload.cbm\_meta | object | 是 | 附加描述信息 | 对下列payload的平级结果做信息补充说明， |
| payload.cbm\_semantic | object | 是 | 聚合语义结果 | AIUI通用技能结构化结果 |
| payload.NLP（语义理解） | object | 是 | 最终语义结果 | 解析文本做拼接处理 |
| payload.TTS（语音合成） | object | 是 | 合成结果 | 解析音频流做拼接，或获取url |

> 当payload.cbm\_semantic.text结构化数据结果中rc值为4或payload.cbm\_meta.text补充说明中untrusted取值为true，说明技能未命中或结果可信度不够，应当舍弃payload.cbm\_semantic中的结构化结果，直接采用payload.nlp中大模型结果
> 具体业务参考[大模型使用问答库手册](https://aiui-doc.xf-yun.com/project-1/doc-359/)中落域判断。

## 断开连接

> 断开连接机制
> 1、请求参数报错，云端直接断开连接
> 2、正常会话建立连接，可以一直请求。当某此会话后超过60s无交互云端会报错连接超时，然后断开连接
> 3、设备端主动断开连接

## 附录

### 音频请求示例

> 识别+语义请求，包含风格化回复、自定义参数、个性化参数
> 多帧发送之首帧音频请求结构

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "a44e0f36",
        "stmid": "audio-1",
        "status": 0,
        "scene": "main_box",
        "msc.lat": 19.65309164062,
        "msc.lng": 109.259056086,
        "os_sys": "windows"
    },
    "parameter": {
        "nlp": {
            "nlp": {
                "compress": "raw",
                "format": "json",
                "encoding": "utf8"
            },
            "sub_scene": "cbm_v45",
            "new_session": false,
            "richness": "concise",
            "env": "{\"human\":{\"expand_persona\":true,\"persona\":\"{\\\"父亲|爸爸\\\":\\\"科大讯飞\\\",\\\"姓名|名字|称呼\\\":\\\"小飞\\\"}\"}}"
        },
        "iat": {
            "svad": "1",
            "bos": "5000",
            "eos": "800",
            "iat": {
                "compress": "raw",
                "format": "json",
                "encoding": "utf8"
            }
        }
    },
    "payload": {
        "cbm_semantic": {
            "compress": "raw",
            "format": "json",
            "text": "eyJ1c2VycGFyYW1zIjoiZXlKclpYa2lPaUoyWVd4MVpTSjkiLCJwZXJzX3BhcmFtIjoie1wiYXBwaWRcIjpcImE0NGUwZjM2XCIsXCJ1aWRcIjpcIjEyMzQ1Njc4OTBcIn0ifQ==",
            "encoding": "utf8",
            "status": 3
        },
        "cbm_reply": {
            "compress": "raw",
            "format": "json",
            "text": "W3sidHlwZSI6IuWuoOa6uueUt+WPiyIsInZhbHVlIjoi5rip5p+U5L2T6LS077ya5Lya5peg5b6u5LiN6Iez5Zyw54Wn6aG+5Lq677yM6K6p5Lq65oSf5Y+X5Yiw54ix5ZKM5YWz5b+D44CCIn1d",
            "encoding": "utf8",
            "status": 3
        },
        "audio": {
            "sample_rate": 16000,
            "channels": 1,
            "audio": "+//7//z/+v/9//3//f/7//r/+P/5//v//P/8//r//f/8//v//f/9//7/AAD///////8AAP//AwAFAAYAAgAAAAIAAgADAAIA//8CAAQABgADAAQAAQABAAUAAwADAAUABgAEAAUABAAFAAUAAwAEAAUAAgABAP7//v/+////AgACAAAAAAD6//f/9v/3//f/9P/1//f/+//+//z/AQAAAAAABAADAAMABQAIAAoACQAHAAYABgAFAAYABAAEAAUABAAAAAAA///////////+/////v/+//v//P/9//z//f/+//7//v///wEAAgACAP3//P/+//3//v8BAAEA/v8BAAYABgAGAAMAAwAFAAUABQAFAAQABAADAAQABQAEAAQABQAFAAMABAAEAAEAAgADAAIA/v/8/wEAAQD+////AgD///7//v/7//3/AAD6//v/+v/7//z/+v/3//j/+f/5//f/+P/3//f/9//6//n/+f/6//r/+P/5//j/+P/4//r//P/+////AgACAAIAAAD9/wAA//8BAAEA/f//////AAAAAAAAAgABAAUABAABAP7//v/9//3/+v/6//z//f/9//z///8BAAMAAwAEAAMABQAHAAcACAAKAA0ADgALAAgACwAMAAgACwAMAA8AEgASABQAFgASABQAEQAPAAgAAwAFAAYABAACAAEAAAD+//v/+f/1/+//5f/l/+b/5//m/+j/8f/7////AAAFAAUABQACAAEA///8//v/9//3//b/+f/6//r/+v/2//j/9P/2//f/9//4//z/AAD+/wAAAwAFAAcABAAEAAcABgADAAIABAAGAAwADQANAA0ADAAKAAwADAAMAA8ADwAMAA0ACgAJAAoACAAFAAMAAQD9//v/9//7//n/+f/3//f/9//6//j/+P/4//r/+P/2/w==",
            "encoding": "raw",
            "bit_depth": 16,
            "frame_size": 0,
            "status": 0
        }
    }
}
```

### 文本语义请求

> 语义请求，包含风格化回复、自定义参数、个性化参数
> 一帧请求

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "main_box",
        "msc.lat": 19.65309164062,
        "msc.lng": 109.259056086,
        "os_sys": "windows"
    },
    "parameter": {
        "nlp": {
            "nlp": {
                "compress": "raw",
                "format": "json",
                "encoding": "utf8"
            },
            "sub_scene": "cbm_v45",
            "new_session": false,
            "richness": "concise",
            "env": "{\"human\":{\"expand_persona\":true,\"persona\":\"{\\\"父亲|爸爸\\\":\\\"科大讯飞\\\",\\\"姓名|名字|称呼\\\":\\\"小飞\\\"}\"}}"
        }
    },
    "payload": {
        "cbm_semantic": {
            "compress": "raw",
            "format": "json",
            "text": "eyJ1c2VycGFyYW1zIjoiZXlKclpYa2lPaUoyWVd4MVpTSjkiLCJwZXJzX3BhcmFtIjoie1wiYXBwaWRcIjpcImE0NGUwZjM2XCIsXCJ1aWRcIjpcIjEyMzQ1Njc4OTBcIn0ifQ==",
            "encoding": "utf8",
            "status": 3
        },
        "cbm_reply": {
            "compress": "raw",
            "format": "json",
            "text": "W3sidHlwZSI6IuWuoOa6uueUt+WPiyIsInZhbHVlIjoi5rip5p+U5L2T6LS077ya5Lya5peg5b6u5LiN6Iez5Zyw54Wn6aG+5Lq677yM6K6p5Lq65oSf5Y+X5Yiw54ix5ZKM5YWz5b+D44CCIn1d",
            "encoding": "utf8",
            "status": 3
        },
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

### 文本合成请求

> 文本合成请求

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x4_lingxiaoying_em_v2",
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "lame"
            },
            "tts_res_type": "url"
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

### speex压缩关系等级表

> speex\_size与speex库压缩等级（quantity）关系表：

| quantity（压缩等级） | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| speex | 6 | 10 | 15 | 20 | 20 | 28 | 28 | 38 | 38 | 46 | 62 |
| speex-wb | 10 | 15 | 20 | 25 | 32 | 42 | 52 | 60 | 70 | 86 | 106 |
