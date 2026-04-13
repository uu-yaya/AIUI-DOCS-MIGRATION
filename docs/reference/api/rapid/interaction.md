---
title: 极速超拟人交互 API
description: 极速超拟人链路的 WebSocket 交互接口，支持 Continuous（全双工）和 Oneshot（单轮交互）两种模式
---

## 概述

极速超拟人交互 API 是语音交互的端到端方案。通过 WebSocket 持续输入用户侧音频，云端处理后下发合成音频，完成全双工多模态交互流程。

- 必须符合 WebSocket 协议规范（RFC 6455）
- WebSocket 握手成功后，10 秒内未发送数据，服务端会主动断开连接
- 默认采用 Continuous（全双工）模式，单次连接最长可持续 30 分钟
- 服务端下发错误码后，客户端应重新建立连接

> 接口会对输入内容和 AI 输出内容进行文本审核，包括涉及国家安全、政治宗教、暴力恐怖、黄赌毒及不文明信息等。触发审核拦截时，会返回错误码 `10014` 或 `10019`。

## 建立连接

WebSocket 握手阶段用于设置鉴权参数，参数在 URL 中指定。

### 请求地址

```text
ws[s]://aiui.xf-yun.com/v3/aiint/sos
```

### 请求示例

```text
wss://aiui.xf-yun.com/v3/aiint/sos?host=xxx&date=xxx&authorization=xxx
```

鉴权参数的构建方式请参考 [鉴权文档](./auth.md)。鉴权时间戳有时效性，建议每次请求时实时获取最新时间戳。

### 结果回调类型

API 返回结果为字节流，端侧解析时需先转为字符串再处理。

## 请求数据结构

请求数据由 `header`、`parameter` 和 `payload` 三部分构成。

### 完整请求示例

```json
{
    "header": {
        "appid": "a44e0f36",          // 应用 AppID
        "sn": "device001",            // 设备唯一标识
        "status": 0,                  // 数据状态：0-首帧 1-中间帧 2-尾帧 3-一帧发完
        "stmid": "audio-1",           // 会话 ID
        "scene": "main",              // 情景模式
        "interact_mode": "continuous", // 交互模式：continuous / oneshot
        "msc.lat": 19.65309164,       // 纬度（可选）
        "msc.lng": 109.25905608,      // 经度（可选）
        "os_sys": "android"           // 系统类型（可选）
    },
    "parameter": {
        "iat": {
            "iat": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            },
            "vgap": 50
        },
        "nlp": {
            "nlp": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "json"
            },
            "new_session": "true",
            "prompt": "你是小明，一个小学学生，热爱画画"
        },
        "tts": {
            "vcn": "x5_lingfeiyi_flow", // 发音人
            "res_id": "xxxx",            // 声音复刻资源 ID（仅复刻时需要）
            "speed": 50,
            "volume": 50,
            "pitch": 50,
            "tts": {
                "encoding": "raw",       // 音频格式：raw / lame / opus / opus-wb / speex / speex-wb
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
            "audio": "base64编码的音频数据",
            "encoding": "raw",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
            "frame_size": 0
        }
    }
}
```

### header 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用的 AppID | `a44e0f36` |
| sn | string | 是 | 设备（用户）唯一标识，长度不超过 32 位 | `device001` |
| status | int | 是 | 数据状态：`0`-首帧、`1`-中间帧、`2`-尾帧、`3`-一帧发完（文本请求固定为 3） | `0` |
| stmid | string | 是 | 会话 ID，长度不超过 32 位，值须为可解析为整数的字符串 | `0` |
| scene | string | 是 | AIUI 应用情景模式 | `main` |
| interact_mode | string | 是 | 交互模式：音频可选 `continuous` 或 `oneshot`；文本仅支持 `oneshot` | `continuous` |
| msc.lat | double | 否 | 纬度，取值 -90 ~ +90，建议 8 位精度 | `19.65309164` |
| msc.lng | double | 否 | 经度，取值 -180 ~ +180，建议 8 位精度 | `109.25905608` |
| os_sys | string | 否 | 应用系统类型 | `windows` |

### parameter 参数

#### IAT（语音识别）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| eos | string | 否 | 云端识别引擎音频尾端点检测时长 | `1000` |
| vgap | string | 否 | 云端识别引擎会话断句时长检测 | `800` |
| iat.compress | string | 是 | 识别结果压缩方式 | `raw` |
| iat.format | string | 是 | 识别结果格式 | `json` |
| iat.encoding | string | 是 | 识别结果编码格式 | `utf8` |

#### NLP（语义理解）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| new_session | string | 否 | 是否清除本次会话历史 | `true` |
| sn | string | 否 | 信源激活绑定设备标识，与 header 中 `sn` 保持一致 | `device001` |
| prompt | string | 否 | 自定义 prompt，可修改系统默认人设，暂不支持占位符替换 | `你是小飞语音助手` |
| nlp.compress | string | 是 | 语义结果压缩方式 | `raw` |
| nlp.format | string | 是 | 语义结果格式 | `json` |
| nlp.encoding | string | 是 | 语义结果编码格式 | `utf8` |

#### TTS（语音合成）参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| vcn | string | 否 | 合成发音人，使用声音复刻时固定取值 `x5_clone` | `x2_xiaojuan` |
| res_id | string | 否 | 声音复刻资源 ID，仅 `vcn=x5_clone` 时需要 | `kps77sqew4k` |
| tts.bit_depth | int | 是 | 合成音频位数 | `16` |
| tts.channels | int | 是 | 合成音频通道数 | `1` |
| tts.encoding | string | 是 | 合成音频格式：`raw`（PCM）、`lame`（MP3）、`opus`（8k）、`opus-wb`（16k）、`speex`（8k）、`speex-wb`（16k） | `raw` |
| tts.sample_rate | int | 是 | 合成音频采样率：`8000` 或 `16000`，需与编码格式对应 | `16000` |

### payload 参数

#### payload.audio（音频请求）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| encoding | string | 是 | 音频编码：`raw`、`opus`、`opus-wb`、`speex-wb` | `raw` |
| frame_size | int | 否 | 音频帧大小，使用 speex 压缩且配置通用中文普通话引擎时必传 | `42` |
| sample_rate | int | 是 | 采样率：`8000` 或 `16000` | `16000` |
| channels | int | 是 | 通道数：`1` 或 `2` | `1` |
| bit_depth | int | 是 | 位数：`8` 或 `16` | `16` |
| status | int | 是 | 数据状态：`0`-首帧、`1`-中间帧、`2`-尾帧 | `0` |
| audio | string | 是 | Base64 编码的音频数据 | — |

#### payload.text（文本请求）

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| encoding | string | 是 | 文本编码 | `utf8` |
| compress | string | 是 | 文本压缩格式 | `raw` |
| format | string | 是 | 文本内容格式 | `plain` |
| status | int | 是 | 数据帧状态，固定取值 `3` | `3` |
| text | string | 是 | Base64 编码的文本数据 | `5L2g5aW95ZWK` |

## Continuous（全双工）模式

依赖讯飞云端 VAD（端点检测）模块做音频端点检测的连续对话场景。

### 协议要点

- `header.stmid` **不需要**更新，一次连接中保持不变
- `header.status`：首帧 `0`，后续 `1`，结束 `2`
- `payload.audio.status`：与 `header.status` 保持一致
- 首个数据包发送全部参数，后续数据包可省略 `parameter`，仅包含 `header` 和 `payload`
- **持续不断发送音频**：即使用户没有说话，也要一直发送音频，服务端自动判断用户是否在说话
- 发送结束帧后会话截止，云端将不再推送结果

### 数据流示例

```text
建立 WebSocket 连接

# 首帧：发送全部参数 (header.status=0, payload.audio.status=0)
{
  "header": {"appid":"abc123","sn":"testDev","status":0,"stmid":"0",
    "scene":"main_box","interact_mode":"continuous",
    "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
  "parameter": {
    "iat": {"vgap":60,"dwa":"wpgs","iat":{"encoding":"utf8","compress":"raw","format":"json"}},
    "nlp": {"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},
    "tts": {"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,
      "tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}
  },
  "payload": {"audio":{"status":0,"audio":"<base64音频>",
    "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}
}

# 后续帧：省略 parameter (header.status=1, payload.audio.status=1)
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"0",
  "scene":"main_box","interact_mode":"continuous",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "payload":{"audio":{"status":1,"audio":"<base64音频>",
  "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}
...

# 结束帧 (header.status=2, payload.audio.status=2)
{"header":{"appid":"abc123","sn":"testDev","status":2,"stmid":"0",
  "scene":"main_box","interact_mode":"continuous",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "payload":{"audio":{"status":2,"audio":"<base64音频>",
  "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 关闭 WebSocket 连接
ws.close()
```

## Oneshot（单轮交互）模式 — 音频

依赖本地 VAD（端点检测）做音频端点检测的单轮对话场景。

### 协议要点

- 每轮对话**必须**更新 `header.stmid`，取值不能重复（如 `audio-1`、`audio-2`）
- `header.status`：每轮对话首帧 `0`，中间帧 `1`，尾帧 `2`
- `payload.audio.status`：与 `header.status` 保持一致
- 每轮对话的首个数据包发送全部参数，后续可省略 `parameter`

### 数据流示例

```text
建立 WebSocket 连接

# 第 1 轮对话 (stmid="audio-1")
# 首帧：发送全部参数 (header.status=0, payload.audio.status=0)
{"header":{"appid":"abc123","sn":"testDev","status":0,"stmid":"audio-1",
  "scene":"main_box","interact_mode":"oneshot",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "parameter":{...},  // 完整 parameter 参数
 "payload":{"audio":{"status":0,"audio":"<base64音频>",
  "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 中间帧 (header.status=1, payload.audio.status=1)
{"header":{"appid":"abc123","sn":"testDev","status":1,"stmid":"audio-1",
  "scene":"main_box","interact_mode":"oneshot",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "payload":{"audio":{"status":1,"audio":"<base64音频>",
  "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 尾帧 (header.status=2, payload.audio.status=2)
{"header":{"appid":"abc123","sn":"testDev","status":2,"stmid":"audio-1",
  "scene":"main_box","interact_mode":"oneshot",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "payload":{"audio":{"status":2,"audio":"<base64音频>",
  "encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}}

# 第 N 轮对话 (stmid="audio-N"，重新发送全部参数)
...

# 关闭 WebSocket 连接
ws.close()
```

## Oneshot（单轮交互）模式 — 文本

文本交互场景下，每轮对话以一帧发送完毕。

### 协议要点

- 每轮对话**必须**更新 `header.stmid`，取值不能重复（如 `text-1`、`text-2`）
- `header.status` 固定取值 `3`
- `payload.text.status` 固定取值 `3`
- 无需 `parameter.iat` 参数

### 数据流示例

```text
建立 WebSocket 连接

# 第 1 轮对话 (stmid="text-1")
{"header":{"appid":"abc123","sn":"testDev","status":3,"stmid":"text-1",
  "scene":"main_box","interact_mode":"oneshot",
  "pers_param":"{\"appid\":\"abc123\",\"uid\":\"testDev\"}"},
 "parameter":{
  "nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"},"new_session":"false"},
  "tts":{"vcn":"x5_lingxiaoyue_flow","speed":50,"volume":50,"pitch":50,
    "tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},
 "payload":{"text":{"format":"plain","text":"<base64文本>","encoding":"utf8","status":3}}}

# 第 N 轮对话 (stmid="text-N")
...

# 关闭 WebSocket 连接
ws.close()
```

## 响应结果

### 首帧响应

首帧数据发送成功时的响应，通常用于返回参数错误、鉴权错误等错误码。

```json
{
    "header": {
        "code": 0,            // 0 表示成功
        "message": "success",
        "sid": "xgo00010205@dx192743899eb0001822-audio-1",
        "status": 0,
        "stmid": "1"
    }
}
```

### 中间结果

包含事件（event）、IAT（语音识别）、NLP（语义理解）、TTS（语音合成）等多种数据类型。

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "xgo00010205@dx192743899eb0001822-audio-1",
        "status": 0,
        "stmid": "1"
    },
    "payload": {
        "event": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "text": "<base64编码的事件数据>"
        },
        "iat": {
            "compress": "raw",
            "encoding": "utf8",
            "format": "json",
            "seq": 1,
            "status": 2,
            "text": "<base64编码的识别结果>"
        },
        "nlp": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "text": "<base64编码的语义结果>"
        },
        "tts": {
            "compress": "",
            "encoding": "",
            "format": "",
            "seq": 0,
            "status": 0,
            "audio": "<base64编码的合成音频>"
        }
    }
}
```

### 错误响应

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

### header 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| code | int | 服务错误码，`0` 表示成功 | `0` |
| sid | string | 会话 SID | `xgo00010205@dx...` |
| status | int | 会话状态，依次为 `0, 1, 1, ..., 1, 2` | `0` |
| stmid | string | 会话 ID，一次连接中每轮对话递增（如 `0-1`、`0-2`、`0-3`） | `0-1` |
| message | string | 返回消息描述 | `success` |

### payload 响应参数

交互过程中会返回多种类型的数据，代表不同的状态切换。

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| payload.$sub | object | 数据部分，`$sub` 为具体类型（event / iat / nlp / tts 等） | — |
| payload.$sub.text | string | Base64 编码的数据内容（合成结果使用 `audio` 字段） | — |
| payload.$sub.status | int | 数据状态：`0`-首帧、`1`-中间帧、`2`-末帧 | `0` |
| payload.$sub.encoding | string | 数据编码格式 | `utf8` |
| payload.$sub.seq | int | 数据段编号 | `1` |
| payload.$sub.format | string | 数据内容格式 | `json` |
| payload.$sub.compress | string | 数据压缩方法 | `raw` |

## 响应数据类型详解

### 事件数据（event）

云端识别引擎检测到音频断点信息时下发事件，结果在 `payload.event.text` 中（Base64 解码后）。

| 事件名 | 触发条件 | 解码后数据 |
|---|---|---|
| Bos | 检测到有人说话 | `{"type":"Vad","data":"","key":"Bos","desc":{}}` |
| Eos | 检测到子句说完 | `{"type":"Vad","data":"","key":"Eos","desc":{}}` |
| Silence | 检测到无人说话 / 静音过长 / 发送 status=2 | `{"type":"Vad","data":"","key":"Silence","desc":{}}` |

### IAT（语音识别）数据

识别结果在 `payload.iat.text` 中，默认流式返回。Base64 解码后示例：

```json
{"sn":1,"ls":false,"bg":0,"ed":0,"pgs":"apd",
 "ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]}]}
```

流式识别（wpgs）关键字段：

| 参数名 | 类型 | 说明 |
|---|---|---|
| pgs | string | `apd`-追加到最终结果；`rpl`-替换前面的部分结果（范围由 `rg` 指定） |
| rg | array | 替换范围，如 `[2, 5]` 表示替换第 2 次到第 5 次返回的结果 |

### NLP（大模型回复）数据

模型结果在 `payload.nlp.text` 中，流式下发。Base64 解码后为逐段文本：

```text
今天
天气晴朗
，气温 10～12℃，
东北风微风
```

### 工具结果数据

生成回复文本之前的工具 / 插件执行中间结果，通过对应的 `payload.xxx.text` 字段 Base64 解码获取：

| 工具类型 | 说明 | 解码后示例 |
|---|---|---|
| cbm_tidy | 识别文本规整结果 | `{"query":"告诉我明天北京天气","intent":[...]}` |
| cbm_retrieval_classify | 知识分类结果 | `{"type":1,"keyword":"北京的历史建筑"}` |
| cbm_semantic | 语义理解结果 | `{"answer":{"text":"明天北京全天晴转多云..."}}` |
| cbm_knowledge | 知识检索结果（命中知识分类时返回） | `[{"score":0,"repoId":"agg_knowledge","summary":"..."}]` |

### TTS（语音合成）数据

合成音频在 `payload.tts.audio` 中，Base64 解码后按 `encoding`、`sample_rate`、`bit_depth` 参数播放。

```json
{
    "payload": {
        "tts": {
            "audio": "<base64合成音频>",
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

## cURL 等效调用示例

由于本接口使用 WebSocket 协议，无法直接使用 cURL 调用。以下使用 `wscat` 工具演示连接过程：

```bash
# 安装 wscat
npm install -g wscat

# 建立 WebSocket 连接（鉴权参数需实时生成）
wscat -c "wss://aiui.xf-yun.com/v3/aiint/sos?host=aiui.xf-yun.com&date=<URL编码的时间戳>&authorization=<鉴权签名>"
```

连接成功后发送 JSON 数据：

```json
{"header":{"appid":"your_appid","sn":"device001","status":3,"stmid":"text-1","scene":"main","interact_mode":"oneshot"},"parameter":{"nlp":{"nlp":{"encoding":"utf8","compress":"raw","format":"json"}},"tts":{"vcn":"x5_lingfeiyi_flow","tts":{"encoding":"raw","sample_rate":16000,"channels":1,"bit_depth":16}}},"payload":{"text":{"format":"plain","text":"5L2g5aW9","encoding":"utf8","status":3}}}
```

## 注意事项

### Continuous（全双工）模式

- 上传音频不能中断，需实时上传录音器采集到的音频，不可额外添加或间断性丢弃音频
- 音频上传间隔建议 40ms，大小 1280 字节（采样率 16000 时）
- 在嘈杂环境中使用全双工交互时，可借助识别结果的 Eos 事件临时关闭录音设备，同时每隔 40ms 上传 1280 字节空白音频字节流
- 连接建立后，本次连接中所有对话历史不受 `new_session` 参数影响，会默认加载使用

### Oneshot（单轮交互）模式

- 每轮对话必须更新 `header.stmid` 的值，取值不能重复
- 文本交互时 `header.status` 和 `payload.text.status` 固定为 `3`

## 附录：音频压缩参数

### frame_size 与 speex 压缩等级关系

| 压缩等级（quantity） | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| speex | 6 | 10 | 15 | 20 | 20 | 28 | 28 | 38 | 38 | 46 | 62 |
| speex-wb | 10 | 15 | 20 | 25 | 32 | 42 | 52 | 60 | 70 | 86 | 106 |

### opus 编码说明

每个编码帧加上两个字节头信息存储编码帧长度，使用大端存储方式。

- **opus**（8k）：每帧 2 字节头 + 20 字节压缩音频数据
- **opus-wb**（16k）：每帧 2 字节头 + 40 字节压缩音频数据
