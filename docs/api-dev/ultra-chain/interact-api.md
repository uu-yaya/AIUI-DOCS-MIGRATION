---
title: 交互 API
---

概述

交互API概述涵盖了接口使用的基础信息、服务详情、API说明、接入指南、结果解析及使用注意事项，帮助开发者快速掌握接口使用方法。

## 前言

### 关于 API 接口的说明

- 必须符合 WebSocket 协议规范（rfc6455）。
- websocket握手成功后用户在10秒内没有发送请求数据，服务侧会主动断开。
- 本接口默认采用全双工交互的模式，即每次建立连接可以持续不断的发送音频数据，云端会持续处理音频数据并将处理结果返回给用户，单个连接最长可持续使用 30 分钟。
- 服务侧下发错误码后，客户端应重建连接，否则后续处理过程会连续报错。

### 关于输入输出内容审核说明

接口会对用户输入内容和AI输出内容进行文本审核，会对包括但不限于

- 涉及国家安全的信息；
- 涉及政治与宗教类的信息；
- 涉及暴力与恐怖主义的信息；
- 涉及黄赌毒类的信息；
- 涉及不文明的信息；

当请求的输入或输出触发审核拦截时，AIUI会赋予错误码返回（详见[错误码列表](/sdk-dev/error-codes "错误码列表")下的10014和10019说明）

## 服务介绍

本协议接口仅适用于`极速超拟人交互链路`服务场景，提供在线语音交互能力。
[WebSocket DEMO](https://gitee.com/iflytek-aiui/aiuiv3-demo)

## API 介绍

极速交互是语音交互的端到端方案，通过持续输入用户侧音频，云端处理后下发合成音频完成全双工多模的交互流程。

## API 接入说明

### 建立链接

WebSocket 握手阶段用于设置鉴权参数，参数在url 中指定，握手请求和参数必须符合 WebSocket 协议。

#### 请求地址

```
ws[s]://aiui.xf-yun.com/v3/aiint/sos
```

#### 请求示例

> ws[s]://aiui.xf-yun.com/v3/aiint/sos?host=xxx&date=xxx&authorization=xxx

#### 接口鉴权

具体鉴权参数构建见[鉴权文档](/api-dev/ultra-chain/auth "大模型API服务鉴权")说明。

### 注意：

鉴权的时间戳有时效性，建议每次请求鉴权时都实时的获取最新时间戳，生成鉴权参数

#### 结果回调类型说明

当前API协议结果返回的结果类型为字节流，端侧做解析处理时需先转成字符串在处理。

### 交互请求

WebSocket连接后进入通信阶段，此时客户端主动操作有：上传数据或断开连接，被动操作有：接收结果和错误信息。

#### 请求数据结构示例

> 请求数据格式由header，parameter 和 payload 构成。示例如下

```json
{
    "header": {
        "appid": "", // 应用id
        "sn": "",     // 设备唯一标识号，
        "status": 0, // 客户端发送数据的状态   0：开始；1：中间状态；2：结束
        "stmid": "audio-1", // 会话id。使用oneshot单工模式时，一次ws连接内的每一轮对话【必须】递增更新stmid。  使用continuous双工模式时，取值固定不变。
        "scene": "main", // 平台上，appid下面创建的情景模式
        "msc.lat": 19.65309164062,
        "msc.lng": 109.259056086,
        "os_sys": "android",
        "interact_mode":"oneshot" //交互模式选择，依赖云端vad时传 continuous，依赖本地vad时传oneshot，默认continuous
    },
    "parameter": {
        "iat": {
            "iat": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            },
            "vgap":50
        },
        "nlp": {
            "nlp": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            },
            "new_session": "true",
            "prompt":"自定义prompt 信息， 例如：你是小明，一个小学学生，热爱画画"
        },
        "tts": {
            "vcn": "x5_lingfeiyi_flow",
            "res_id": "xxxx",
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "encoding": "raw",
                "sample_rate": 16000,
                "channels": 1,
                "bit_depth": 16,
                "frame_size": 0
            }
        }
    },
    "payload": {
        "audio": {
            "status": 0,
            "audio": "base64的音频数据",
            "encoding": "raw",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
            "frame_size": 0
        }
    }
}
```

> 数据请求协议字段说明

#### header 数据参数详细说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | 是 | AIUI应用信息中的appid取值 | a44e0f36 |
| sn | string | 是 | 设备(用户)唯一标识，长度不超过32位。 | 1234567890 |
| status | int | 是 | 取值范围 0 1 2 3；（0-代表首帧、1-代表中间帧、2-代表尾帧、3-代表数据一帧发送完毕，文本请求固定为3） | 0 |
| stmid | string | 是 | 会话请求id,长度不超过32位：取值是字符串，但实际值需要为数值内容（可以解析为整数的字符串），比如”0”, “1”, “2” … | 0 |
| scene | string | 是 | AIUI应用情景模式 | main、main\_box |
| interact\_mode | string | 是 | 对话交互协议，音频交互时可选：continuous 、Oneshot（单轮交互） ；文本交互时仅支持：Oneshot（单轮交互） | Oneshot（单轮交互） |
| msc.lat | double | 否 | 纬度，取值范围 -90 ~ +90，建议最长8位精度 | 19.65309164 |
| msc.lng | double | 否 | 经度，取值范围 -180 ~ +180，建议最长8位精度 | 109.25905608 |
| os\_sys | string | 否 | 应用系统类型 | windows |

#### parameter 数据参数详细说明

> IAT（语音识别） 识别参数设置

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| eos | string | 否 | 云端识别引擎音频尾端点时长检测设置 | 1000 |
| vgap | string | 否 | 云端识别引擎会话断句时长检测设置 | 800 |
| IAT（语音识别）.compress | string | 是 | 识别结果类型 | 目前仅支持raw |
| IAT（语音识别）.format | string | 是 | 识别结果格式 | 目前仅支持json |
| IAT（语音识别）.encoding | string | 是 | 识别结果编码格式 | 目前仅支持utf8 |

> NLP（语义理解） 语义参数设置

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| new\_session | string | 否 | 是否清除本次会话历史 | true |
| sn | string | 否 | 信源激活绑定设备标识，与header中sn取值保持一致 | 1234567890 |
| prompt | string | 否 | 自定义prompt，可借助此参数修改系统默认的人设，暂不支持占位符替换 | 你是小飞语音助手} |
| NLP（语义理解）.compress | string | 是 | 语义结果类型 | 目前仅支持raw |
| NLP（语义理解）.format | string | 是 | 语义结果格式 | 目前仅支持json |
| NLP（语义理解）.encoding | string | 是 | 语义结果编码格式 | 目前仅支持utf8 |

> TTS（语音合成） 合成参数设置

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| vcn | string | 否 | 合成发音人   使用声音复刻时固定取值为： x5\_clone | x2\_xiaojuan |
| res\_id | string | 否 | 声音复刻资源id。 注意：仅在使用声音复刻（vcn=x5\_clone） 时需要携带本参数 | kps77sqew4k |
| TTS（语音合成）.bit\_depth | int | 是 | 合成音频位数 | 16 |
| TTS（语音合成）.channels | int | 是 | 合成音频通道数 | 1 |
| TTS（语音合成）.encoding | string | 是 | 合成音频格式说明如下  **raw**：pcm音频 **lame**： mp3音频 **opus**：8k opus音频 **opus-wb**：16k opus音频 **speex**：8k speex音频 **speex-wb**：16k opus音频  音频压缩关系可查看[**【附录】**](#附录) 了解 | raw |
| TTS（语音合成）.sample\_rate | int | 是 | 合成音频采样率 ：8000、16000  注意与合成音频压缩格式对应 | 16000 |

#### payload 数据参数详细说明

payload项提供交互数据类型说明及对应参数设置，现阶段主要有：音频、文本两种请求，具体参数设置如下。

> payload.audio 设置 (音频请求参数和内容)

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 音频编码（取值：raw，opus，opus-wb，speex-wb 其他编码格式可联系讯飞技术人员确认） 注意：使用speex或opus压缩音频时，注意查看[**【附录】**](#附录) 了解音频压缩信息 | raw |
| frame\_size | int | 否 | 音频帧大小 注意：speex音频交互且配置默认 **通用-中文-普通话** 识别引擎时本参数必传，关于音频帧大小与压缩比关系表可查看[**【附录】**](#附录) 了解 | 42 |
| sample\_rate | int | 是 | 采样率（取值 ：8000、16000） | 16000 |
| channels | int | 是 | 通道数（取值 ：1、2） | 1 |
| bit\_depth | int | 是 | 位数（取值 ：8、16） | 16 |
| status | int | 是 | 数据状态：首帧 0、中间帧 1、尾帧2 | 0 |
| audio | string | 是 | 音频数据：需经base64编码 |  |

> payload.text 设置 (文本请求参数和内容)

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | 文本编码：默认 utf8 | utf8 |
| compress | string | 是 | 文本压缩格式：默认 raw | raw |
| format | string | 是 | 文本内容格式：默认 plain | plain |
| status | int | 是 | 数据帧发送帧状态 | 固定取值：3 |
| text | string | 是 | 文本数据：需经base64编码 | 5L2g5aW95ZWK |

### 简化请求数据介绍

温馨提示

1、continuous协议：当依赖讯飞云端vad模块做音频端点检测的连续对话，建议选择该协议模式

2、oneshot协议：当依赖本地vad做音频端点检测或进行文本交互，建议选择该协议模式

#### continuous协议

- **不需要**更新header.stmid的取值：一次会话链接中取值**保持不变**。
- header.status： 会话的状态。建立链接后的第一个数据包的header.status是0，后续都是1，结束时传2。
- payload.audio.status：音频的状态。建立链接后的第一个数据包的header.status是0，后续都是1，结束时传2。
- 第一个数据包，发送全部参数的字段。后续的数据包，可以发送简化的内容（不携带parameter参数，仅构建 header、payload）。
- 持续不断的发送音频：即使用户没有说话，也要一直发送音频。服务侧会自动判断用户有没有说话。

  根据下面示例，关注 header.status 和 payload.audio.status 取值变化规律、以及每轮对话非首帧参数精简 。

温馨提示

1、注意只有在链接建立的首帧需要携带全量参数，协议是依赖云端识别vad进行会话切换，端侧持续送音频即可

2、当发送结束帧时代表会话截止，此时AIUI云将不再推送结果下发（不管上一次对话结果有没有下发完毕）

```text
建立ws连接

# 第一个数据包：需要发送全部的字段  (header.status=0, payload.audio.status=0)
{"header":{"appid":"abc123","sn":"testDev","status":0,"stmid":"0","scene":"main_box","interact_mode":"continuous","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"parameter":{"iat":{"vgap":60,"dwa":"wpgs","iat":{"encoding":"utf8","compress":"raw","format":"json"}},"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},"tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,"tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"audio":{"status":0,"audio":"base64的音频","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 后续的数据包(header.status=1, payload.audio.status=1，不携带parameter参数)
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"0","scene":"main_box","interact_mode":"continuous","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":1,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
...
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"0","scene":"main_box","interact_mode":"continuous","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":1,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

...
# 即使用户没有说话，也要一直发送音频
...

# 结束会话 (header.status=2, payload.audio.status=2，不携带parameter参数)
{"header":{"appid":"abc123","sn":"testDev","status":2,"stmid":"0","scene":"main_box","interact_mode":"continuous","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":2,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
# 关闭ws连接
ws.close()
```

#### oneshot协议（音频交互）

- 每轮对话**必须**更新**header.stmid**的值 ：取值不能重复，比如”audio-0”, “audio-1”……
- header.status： 会话的状态。按照切分的对话处理，**每轮对话**首帧数据 header.status是0，中间帧都是1，结束帧传2。（payload.audio.status保持一致）
- payload.audio.status：音频的状态。按照切分的对话处理，**每轮对话**首帧数据 header.status是0，中间帧都是1，结束帧传2。（header.status保持一致）
- **每轮对话**的第一个数据包，发送全部参数的字段。后续的数据包，可以发送简化的内容（不携带parameter参数，仅构建 header、payload）。

  根据下面示例，关注 header.status 和 payload.audio.status 取值变化规律、以及每轮对话非首帧参数精简 。

```
建立ws连接

# 【第1轮对话  设置header.stmid="audio-1"】
# 第1轮对话首帧：需要发送全部的字段 【header.status=0, payload.audio.status=0】
{"header":{"appid":"abc123","sn":"testDev","status":0,"stmid":"audio-1","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"parameter":{"iat":{"vgap":60,"dwa":"wpgs","iat":{"encoding":"utf8","compress":"raw","format":"json"}},"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},"tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,"tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"audio":{"status":0,"audio":"base64的音频","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
# 第1轮对话中间帧：【header.status=1, payload.audio.status=1】
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"audio-1","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":1,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
...
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"audio-1","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":1,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
# 第1轮对话尾帧：【header.status=2, payload.audio.status=2】
{"header":{"appid":"abc123","sn":"testDev","status":2,"stmid":"audio-1","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":2,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

……

# 【第N轮对话  更新header.stmid="audio-N"】
# 第N轮对话首帧：需要发送全部的字段【header.status=0, payload.audio.status=0】
{"header":{"appid":"abc123","sn":"testDev","status":0,"stmid":"audio-N","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"parameter":{"iat":{"vgap":60,"dwa":"wpgs","iat":{"encoding":"utf8","compress":"raw","format":"json"}},"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},"tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,"tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"audio":{"status":0,"audio":"base64的音频","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
# 第N轮对话中间帧：【header.status=1, payload.audio.status=1】
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"audio-N","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":1,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
# 第N轮对话尾帧：【header.status=2, payload.audio.status=2】
{"header":{"appid":"abc123","sn":"testDev","status":2,"stmid":"audio-N","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"payload":{"audio":{"status":2,"audio":"base64的音频数据","encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 关闭ws连接
ws.close()
```

#### oneshot协议（文本交互）

- 每轮对话**必须**更新**header.stmid**的值 ：取值不能重复，比如”text-1”, “text-2”……
- 每轮对话一帧发送结束
  - header.status： 会话的状态，固定取值 3；
  - payload.text.status：请求文本状态，固定取值 3；

```text
建立ws连接

# 【第1轮对话  设置header.stmid="text-1"】
# 第1轮对话首帧：发送全部的字段 【header.status=3, payload.text.status=3】
{"header":{"appid":"abc123","sn":"testDev","status":3,"stmid":"text-1","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"parameter":{"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},"tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,"tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"text":{"format":"plain","text":"base64的文本","encoding":"utf8","status":3}}}

……

# 【第N轮对话  更新header.stmid="text-N"】
# 第N轮对话首帧：发送全部的字段 【header.status=3, payload.text.status=3】
{"header":{"appid":"abc123","sn":"testDev","status":3,"stmid":"text-N","scene":"main_box","interact_mode":"oneshot","pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},"parameter":{"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},"tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,"tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"text":{"format":"plain","text":"base64的文本","encoding":"utf8","status":3}}}

# 关闭ws连接
ws.close()
```

## 结果说明

### 响应结果示例

#### 首帧响应

首帧数据发送成功时的响应 ，该结果不报错时可以省略掉，通常用于返回参数错误、链接错误、鉴权等错误码

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xgo00010205@dx192743899eb0001822-audio-1",
        "status": 0,
        "stmid": "1"
    }
}
```

#### 中间结果

包含 event事件结果（下发前端点、后端点事件）、IAT（语音识别）（识别）结果、NLP（语义理解）（大模型）结果、TTS（语音合成）（合成）结果等。

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xgo00010205@dx192743899eb0001822-audio-1",
        "status": 0,
        "stmid":"1"
    },
    "payload": {
        "event": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "text": "eyJ0eXBlIjoiVmFkIiwiZGF0YSI6IiIsImtleSI6IkJvcyIsImRlc2MiOnt9fQ=="
        },
        "iat": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "json",
            "seq": 1,
            "status": 2,
            "text": "eyJ0ZXh0Ijp7InNuIjoxLCJscyI6ZmFsc2UsImJnIjowLCJyZyI6bnVsbCwiZWQiOjAsInBncyI6IiIsInJzdCI6IiIsInNpZ24iOiIiLCJ3cyI6W3siYmciOjAsImN3IjpbeyJzYyI6MCwidyI6IuS9oCIsInBoIjoiIn1dfSx7ImJnIjowLCJjdyI6W3sic2MiOjAsInciOiLlj6siLCJwaCI6IiJ9XX0seyJiZyI6MCwiY3ciOlt7InNjIjowLCJ3Ijoi5LuA5LmIIiwicGgiOiIifV19LHsiYmciOjAsImN3IjpbeyJzYyI6MCwidyI6IuWQjeWtlyIsInBoIjoiIn1dfV19fQ=="
        },
         "nlp": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "text": "5bGV56S65LqG5LiA5Liq"
        },
         "tts": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "audio": "Base64 audio data"
        }
    }
}
```

#### 报错结果

```json
{
    "header": {
        "code": 10110,
        "message": "server licence error",
        "sid": "xgo00010205@dx192743899eb0001822-audio-1",
        "status": 2,
        "stmid": "1"
    }
}
```

### 响应参数说明

- header 结果字段说明

| 字段名 | 类型 | 含义 | 备注 |
| --- | --- | --- | --- |
| header.code | int | 服务错误码 | 0表示成功，其他值表示失败。 |
| header.sid | string | 会话的sid |  |
| header.status | int | 会话的状态 | 0，1，1，…，1，2 |
| header.stmid | string | 会话的id | 一次长连接中，每个会话对应一个会话id。一次连接的多次对话，stmid 会递增；云端返回的 stmid 会在客户端发起请求的 stmid 基础上迭代，例如 0-1；0-2；0-3 |
| header.message | string | 返回消息描述 |  |

- payload结果字段说明

极速交互过程过程中，可能会返回多种类型的数据，代表交互过程中的状态切换，用户可根据返回结果及状态，定制化接入全双工交互流程

| 字段名 | 类型 | 含义 | 备注 |
| --- | --- | --- | --- |
| payload.$sub | object | 数据部分 |  |
| payload.$sub.text | string | 数据内容 | 数据的 base64编码后内容，部分特殊的数据字段不为 text，比如合成结果数据内容字段为audio |
| payload.$sub.status | int | 数据的状态 | 可选值0，1，2。 其中0表示首帧结果，1表示中间帧，2表示最后一帧。 |
| payload.$sub.encoding | string | 数据的编码格式 |  |
| payload.$sub.seq | int | 数据段的编号 |  |
| payload.$sub.format | string | 数据内容的格式 |  |
| payload.$sub.compress | string | 数据内容的压缩方法 |  |

具体的 `sub` 类型根据调用方式的不同，会有不同的变化，详细内容如下

#### 事件数据

云端的识别会判断用户音频的断点信息，会下发相应的事件，目前主要分为三类事件，包括开始说话，结束说话，无人说话，事件结果在 payload.event.text 中
事件目前分三种事件，详细说明如下：

```text
// 以下结果已经 base64decode text的内容
Bos 事件，检测到音频中有人说话，触发该事件返回
{"type":"Vad","data":"","key":"Bos","desc":{}}

Eos事件，检测到音频中子句说完了，触发该事件返回
{"type":"Vad","data":"","key":"Eos","desc":{}}

Silence 事件，检测到音频无人说话，最终结束事件，收到后结束会话即可，一般静音事件过长，或者上传status=2时会触发
{"type":"Vad","data":"","key":"Silence","desc":{}}
```

#### 识别数据

和传统的识别结果稍有区别，极速场景下的sn和ls字段没有实际意义
识别结果在 payload.IAT（语音识别）.text 字段中（注意示例为流式结果，当前默认识别无流式结果）

```text
//以下结果已经 base64decode text的内容
{"sn":1,"ls":false,"bg":0,"ed":0,"pgs":"apd","ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]}]}
{"sn":2,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,1],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"1385"}]}]}
{"sn":3,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,2],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"13856"}]}]}
...
{"sn":21,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,20],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"13856901234"}]},{"bg":0,"cw":[{"sc":0.00,"w":"充"}]},{"bg":0,"cw":[{"sc":0.00,"w":"6888"}]},{"bg":0,"cw":[{"sc":0.00,"w":"."}]},{"bg":0,"cw":[{"sc":0.00,"w":"8"}]},{"bg":0,"cw":[{"sc":0.00,"w":"元"}]},{"bg":0,"cw":[{"sc":0.00,"w":"话费"}]}]}
{"sn":22,"ls":true,"bg":0,"ed":0,"pgs":"apd","ws":[{"bg":0,"cw":[{"sc":0.00,"w":"。"}]}]}
```

流式识别（wpgs）解析时，相关字段含义说明：

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| pgs | string | “apd”:结果是追加到前面的最终结果；”rpl” :替换前面的部分结果，替换范围为rg字段 |
| rg | array | 替换范围，开启wpgs会有此字段 假设值为[2,5]，则代表要替换的是第2次到第5次返回的结果 |

#### 大模型回复数据

模型结果在 payload.NLP（语义理解）.text 结果中，流式下发：

```text
//以下结果已经 base64decode text的内容
今天
天气晴朗
，气温 10～12℃，
东北风微风
```

#### 工具结果数据

工具结果是生成回复文本之前的一些工具、插件等执行过程的中间结果，目前会下发的工具结果类型有

- cbm\_tidy 识别文本的规整结果
- cbm\_retrieval\_classify 知识分类的结果
- cbm\_semantic 语义理解结果
- cbm\_knowledge 知识检索结果，若知识分类命中则会返回

工具结果数据示例如下（部分数据段过大，简略显示）：解析方式也是通过 payload.xxx.text 解base64 获取明文结果，具体示例如下（部分数据段过大，简略显示）

```text
//以下结果已经 base64decode text的内容
# cbm_tidy
{"query": "告诉我明天北京天气怎么样", "intent": [{"index": 0, "value": "明天北京天气怎么样"}]}

# cbm_retrieval_classify
{"type": 0}
{"type": 1, "keyword": "北京的历史悠久的建筑"}

# cbm_semantic
{"answer": {"text": "明天北京全天晴转多云，气温-2***********"}}

# cbm_knowledge
[{"score": 0, "repoId": "agg_knowledge","summary": "北京的历史太厚重，为了控制******"}]
```

#### 合成音频数据

> 合成音频数据在 payload.TTS（语音合成）.audio 中，需要客户端 base64 decode，可按照音频参数encoding、sample\_rate、bit\_depth 播放

合成音频数据示例如下，音频数据段大，流式下发:

```json
{
    "payload": {
        "tts": {
            "audio": "Base64 tts audio data",
            "bit_depth": 16,
            "channels": 1,
            "encoding": "raw",
            "frame_size": 0,
            "sample_rate": 24000,
            "seq": 1,
            "status": 0
        }
    }
}
```

## 注意事项

在语音交互上传音频时需要注意：
**双工交互场景** `interact_mode = continuous`

- 上传音频不能中断，需实时上传录音器收集到的音频，不可额外添加音频、不可间断性丢弃音频
- 音频上传间隔建议为 40ms，大小 1280 字节（采样率 16000）
- 若期望在嘈杂的环境使用全双工极速交互，借助识别结果的 eos 事件，可临时关闭录音设备并同时上传伪造音频内容，即每隔 40ms 上传 1280 字节伪造的空白音频字节流
- 链接建立成功后，本次链接会话中所有对话历史不受new\_session参数影响，会默认加载使用。

## 附录

**frame\_size与speex库压缩等级（quantity）关系表：**

|  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **quantity（压缩等级）** | **0** | **1** | **2** | **3** | **4** | **5** | **6** | **7** | **8** | **9** | **10** |
| speex | 6 | 10 | 15 | 20 | 20 | 28 | 28 | 38 | 38 | 46 | 62 |
| speex-wb | 10 | 15 | 20 | 25 | 32 | 42 | 52 | 60 | 70 | 86 | 106 |

**opus编码说明：**
每个编码帧加上两个字节头信息存储编码帧长度，`大端存储`方式。

“opus”编码：8k

```
   0                    1                   2
   0  1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
   +--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   | 20 |     20字节压缩音频数据                  |
   +--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

“opus-wb”编码：16k

```
   0                    1                   2                       3                   4
   0  1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
   +--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  40|                            40字节压缩音频数据                                       |
   +--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
