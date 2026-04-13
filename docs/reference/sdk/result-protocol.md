---
title: 交互结果协议说明
description: AIUI 各交互链路（传统语义、通用大模型、极速超拟人）的结果协议详细说明
---

## 协议概览

本文档重点介绍各 AIUI 交互类型结果协议，包含所有交互链路（传统语义、通用大模型、极速超拟人）、交互模式（在线交互、离线交互），提供结果示例和字段说明。

随着 AIUI 服务演进，极速超拟人交互链路与通用大模型交互链路下发的结果类型（SDK 解析结果 sub 字段取值）一致，但是结果协议有变更，主要是当前请求所在规整结果意图的指定位置有不同：

- **极速超拟人交互链路**：在与 `payload` 平级的 `parameter` 字段下存放说明
- **通用大模型交互链路**：在 `payload.cbm_meta` 字段下存放说明

下面就不同链路下常见的结果协议字段做详细说明。

### 通用结果

#### iat -- 在线语音识别

在线识别结果，解析 `event.info` 结果格式示例：

```json
{
    "text": {
        "bg": 0,
        "sn": 1,
        "ws": [
            {"bg": 0, "cw": [{"w": "叫", "sc": 0}]},
            {"bg": 0, "cw": [{"w": "什么", "sc": 0}]},
            {"bg": 0, "cw": [{"w": "名字", "sc": 0}]}
        ],
        "ls": false,
        "ed": 0
    }
}
```

| 参数名 | 参数全称 | 类型 | 说明 |
| --- | --- | --- | --- |
| sn | sentence | number | 第几句 |
| ls | last sentence | boolean | 是否最后一句 |
| bg | begin | number | 开始 |
| ed | end | number | 结束 |
| ws | words | array | 词 |
| cw | chinese word | array | 中文分词 |
| w | word | string | 单字 |
| sc | score | number | 分数 |

#### tts -- 语音合成

语音合成结果默认下发的就是数据流，开发者在 `EVENT_RESULT` 事件返回的 tts 类型事件时解析获取数据流即可。

#### tpp -- 应用后处理

应用后处理结果由开发者配置的后处理服务构造返回，协议格式无固定限制。开发者只需解析 `EVENT_RESULT` 事件返回的 tpp 类型的结果即可。

### 传统语义交互链路

#### nlp -- 语义技能

语义技能结果，解析 `event.data` 获取结果格式示例：

```json
{
    "intent": {
        "answer": {
            "text": "今天是2025年9月3号，星期三。",
            "type": "T"
        },
        "category": "IFLYTEK.datetimePro",
        "data": {
            "result": [
                {
                    "lunardate": "乙巳年七月十二",
                    "weekday": "星期三"
                }
            ]
        },
        "dialog_stat": "DataValid",
        "rc": 0,
        "save_history": true,
        "semantic": [
            {
                "intent": "WHATWEEK",
                "slots": [
                    {
                        "name": "datetime",
                        "normValue": "{\"datetime\":\"2025-09-03\",\"suggestDatetime\":\"2025-09-03\"}",
                        "value": "今天"
                    }
                ]
            }
        ],
        "service": "datetimePro",
        "shouldendsession": "true",
        "sid": "cid000141b6@dx1990e4763184010004",
        "state": {
            "fg::datetimePro::default::default": {
                "state": "default"
            }
        },
        "text": "今天星期几",
        "used_state": {
            "state": "default",
            "state_key": "fg::datetimePro::default::default"
        },
        "uuid": "cid000141b6@dx1990e4763184010004",
        "version": "536.0"
    }
}
```

传统语义结构详细协议可查看[语义协议文档](/custom-biz/protocols/semantic-protocol)，基础参数说明如下：

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| rc | int | 语义理解结果 0（成功） 1（输入异常） 2（系统内部异常） 3（业务操作失败，没搜索到结果或信源异常） 4（说法未命中技能） |
| error | Object | 错误信息 |
| text | String | 用户的输入，可能和请求中的原始 text 不完全一致，因服务器可能会对 text 进行语言纠错 |
| vendor | String | 技能提供者，不存在时默认表示为 IFLYTEK 提供的开放技能 |
| service | String | 技能的全局唯一名称 |
| semantic | Object | 语义信息，每个技能自定义 |
| data | Object | 数据结构化表示，各技能自定义 |
| answer | Object | 对结果内容的最简化文本/图片描述，各技能自定义 |
| dialog\_stat | String | 用于客户端判断是否使用信源返回数据 |
| moreResults | Object | 在存在多个候选结果时，用于提供更多的结果描述 |
| shouldEndSession | Boolean | 当该字段为空或为 true 时表示技能已完成一次对话，如果为 false 时，表示技能期待用户输入，远场交互设备此时应该主动打开麦克风拾音 |
| category | String | 技能标识，与 service 取值区别在于会携带命名空间信息 |
| version | String | 技能版本 |
| uuid | String | （历史字段，请忽略）同 sid |
| used\_state | Object | （历史字段，请忽略）交互使用状态 |
| state | Object | （历史字段，请忽略）交互状态 |
| sid | String | 会话 ID，用于标识会话，调试时提供给讯飞帮助定位问题 |
| save\_history | Boolean | 是否有会话历史 |

#### itrans -- 翻译

:::info
1. 最新 AIUI 应用已不提供语音翻译能力，如需翻译能力请联系讯飞技术同事咨询。
2. 支持的模式有：中英互译、粤语翻英语、四川话翻英语，中文到其他语种（日语、韩语、法语、西班牙语、俄语、阿拉伯语、彝语、维语、藏语）翻译。
:::

翻译结果，解析 `event.data` 获取结果格式示例：

```json
{
    "from": "cn",
    "ret": 0,
    "sid": "its00262192@dx21dd0ea7978b6f2300",
    "to": "en",
    "trans_result": {
        "src": "合肥的天气",
        "dst": "Weather in Hefei"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| from | string | 原语言 cn：中文 en：英文 |
| to | string | 目标语言 |
| ret | int | 翻译执行结果 0：代表成功 其他取值为错误码 |
| sid | string | 对话唯一标识 |
| src | string | 源语言结果 |
| dst | string | 翻译结果 |

### 极速超拟人交互链路

#### event -- 服务事件

服务事件结果，解析 `event.data` 获取结果格式示例：

```json
{
    "event": {
        "compress": "",
        "encoding": "",
        "format": "",
        "seq": 0,
        "status": 0,
        "text": "{\"type\":\"Vad\",\"data\":\"\",\"key\":\"Bos\",\"desc\":{}}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| text | string | event 事件结果详细内容，**JSON 格式字符串** |
| type（event.text 取值中） | string | 能力模块说明 Vad：云端 VAD（端点检测）事件 |
| key（event.text 取值中） | string | 结果类型 Bos：检测到云端 VAD（端点检测）前端点 Eos：检测到云端 VAD（端点检测）尾端点 Silence：云端链接断开后原因说明事件 |

#### cbm\_tidy -- 语义规整

语义规整结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_tidy": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "parameter": {
            "loc": {
                "ability": "workflow_sos_interaction_lite",
                "intent": 0,
                "unique_id": "workflow_sos_interaction_lite"
            },
            "unique_id": "cbm_tidy_default"
        },
        "seq": 0,
        "status": 2,
        "text": "{\"query\":\"打开客厅空调关闭厨房油烟机\",\"intent\":[{\"index\":0,\"value\":\"打开客厅空调\"},{\"index\":1,\"value\":\"关闭厨房油烟机\"}]}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 语义规整结果详细内容，**JSON 格式字符串** |
| query（cbm\_tidy.text 取值中） | string | 用户请求原始文本 |
| index（cbm\_tidy.text 取值中） | int | 规整的子问题数据标记，从 0 开始计数 |
| value（cbm\_tidy.text 取值中） | string | 规整后的子问题内容 |

#### cbm\_semantic -- 传统语义技能

传统语义技能结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_semantic": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "plain",
        "parameter": {
            "loc": {
                "ability": "workflow_sos_interaction_lite",
                "intent": 0,
                "unique_id": "workflow_sos_interaction_lite"
            },
            "unique_id": "cbm_semantic"
        },
        "seq": 0,
        "status": 3,
        "text": "{\"category\":\"IFLYTEK.smartControlPro\",\"dialog_stat\":\"DataValid\",\"rc\":0,...}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 传统技能结果详细内容，**JSON 格式字符串**，详细内容见上方 nlp 结果格式说明 |

#### cbm\_tool\_pk -- 意图落域

意图落域结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_tool_pk": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "plain",
        "parameter": {
            "loc": {
                "ability": "workflow_sos_interaction_lite",
                "intent": 1,
                "unique_id": "workflow_sos_interaction_lite"
            },
            "unique_id": "cbm_tool_pk_ai"
        },
        "seq": 0,
        "status": 2,
        "text": "{\"pk_type\":\"cbm_semantic\",\"pk_source\":{\"domain\":\"smartControlPro\"},\"tool\":{}}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 意图落域结果详细内容，**JSON 格式字符串** |
| pk\_type（cbm\_tool\_pk.text 取值中） | string | 落域结果判定来源模块 |
| pk\_source.domain（cbm\_tool\_pk.text 取值中） | string | 落域结果，常见取值有：chat、技能标识、智能体名称 |
| pk\_source.intent（cbm\_tool\_pk.text 取值中） | string | 落域到智能体时才有该字段，对应智能体某个意图取值 |

#### cbm\_retrieval\_classify -- 知识分类

知识分类结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_retrieval_classify": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "plain",
        "parameter": {
            "loc": {
                "ability": "workflow_sos_interaction_lite",
                "intent": 0,
                "unique_id": "workflow_sos_interaction_lite"
            },
            "unique_id": "cbm_retrieval_classify"
        },
        "seq": 0,
        "status": 2,
        "text": "{\"type\":0,\"label\":1}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 知识分类结果详细内容，**JSON 格式字符串** |
| type（cbm\_retrieval\_classify.text 取值中） | int | 知识分类查询类型 0：不走知识查询或联网搜索 1：走知识查询或联网搜索 |

#### cbm\_plugin -- 智能体

智能体结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_plugin": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "parameter": {
            "loc": {
                "ability": "workflow_20250814zfpci",
                "loc": {
                    "ability": "workflow_sos_interaction_lite",
                    "intent": 0,
                    "unique_id": "workflow_sos_interaction_lite"
                },
                "unique_id": "workflow_20250814zfpci"
            },
            "unique_id": "cbm_plugin"
        },
        "seq": 0,
        "status": 3,
        "text": "{\"success\":true,\"err_code\":\"0\",\"data\":{...}}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 结果详细内容，**JSON 格式字符串** |

#### cbm\_knowledge -- 知识溯源

知识溯源结果，该结果为交互业务触发联网搜索或本地文档问答，给出知识来源信息。

解析 `event.data` 获取**联网搜索**类结果格式示例：

```json
{
    "compress": "raw",
    "encoding": "utf8",
    "format": "json",
    "parameter": {
        "loc": {
            "ability": "workflow_sos_interaction_lite",
            "intent": 0,
            "unique_id": "workflow_sos_interaction_lite"
        },
        "unique_id": "cbm_knowledge"
    },
    "seq": 0,
    "status": 3,
    "text": "[{\"repoId\":\"agg_knowledge\",\"docId\":\"https://example.com/article\",\"title\":\"文章标题\",\"summary\":\"摘要内容\",\"content\":\"正文内容\",\"detail\":\"详情\",\"publishTime\":\"发布时间\",\"docName\":\"文档名称\",\"repoName\":\"联网搜索\"}]"
}
```

解析 `event.data` 获取**文档问答**类结果格式示例：

```json
{
    "cbm_knowledge": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "parameter": {
            "loc": {
                "ability": "workflow_sos_interaction_lite",
                "intent": 0,
                "unique_id": "workflow_sos_interaction_lite"
            },
            "unique_id": "cbm_knowledge"
        },
        "seq": 0,
        "status": 3,
        "text": "[{\"score\":0.9989267,\"repoId\":\"insight_spark_201024_2wxqn\",\"docId\":\"d6cc977e08f742c19f344b7ead0706fb\",\"chunkId\":\"0\",\"title\":\"0\",\"content\":\"文档内容...\",\"detail\":\"详情...\",\"docName\":\"文档名称.docx\",\"repoName\":\"知识库名称\"}]"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 当前结果指向规整结果的第几个意图 |
| loc.unique\_id | string | 结果执行服务组件 |
| text | string | 知识溯源结果详细内容，**数组结构，存储 JSON 格式字符串** |
| repoId（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**知识库的唯一标识符，不具备语义** 2、联网搜索时取值固定为：**agg\_knowledge** |
| docId（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档或数据记录的唯一标识符，不具备语义** 2、联网搜索时取值为：**网页 URL** |
| repoName（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档库名称** 2、联网搜索时取值固定为：**联网搜索** |
| docName（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档名称** 2、联网搜索时取值为：**网页名称** |

#### nlp -- 大模型回复

:::warning
注意与传统语义链路下的 nlp 结果做区分。
:::

大模型回复结果，解析 `event.data` 获取结果格式示例：

```json
{
    "nlp": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "plain",
        "parameter": {
            "loc": {
                "ability": "workflow_20250814zfpci",
                "loc": {
                    "ability": "workflow_sos_interaction_lite",
                    "intent": 0,
                    "unique_id": "workflow_sos_interaction_lite"
                },
                "unique_id": "workflow_20250814zfpci"
            },
            "unique_id": "nlp"
        },
        "seq": 0,
        "status": 0,
        "text": "您好，看起来"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| parameter | object | 参数字段 |
| loc | object | 结果补充字段，添加结果执行来源 |
| loc.intent | string | 语义规整结果对应的 index 取值 |
| loc.unique\_id | string | 结果执行服务组件 |
| seq | int | 结果帧序号，取值从 0 开始，顺序追加 |
| status | int | 结果帧状态，取值从 0 开始 0：首帧 1：中间帧 2：尾帧 |
| text | string | 大模型回复结果，纯文本 |

### 通用大模型交互链路

:::tip
与极速超拟人交互链路下的结果相比，通用大模型结果协议中关于技能所在结果的说明信息在外层 `cbm_meta` 字段中进行说明。
:::

#### cbm\_tidy -- 语义规整

语义规整结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 2,
        "text": "{\"cbm_tidy\":{\"intent\":0}}"
    },
    "cbm_tidy": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 2,
        "text": "{\"query\":\"今天是多少号\",\"intent\":[{\"index\":0,\"value\":\"今天是多少号\"}]}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明，规整结果可以忽略 |
| cbm\_tidy.text | string | 语义规整结果详细内容 |
| query（cbm\_tidy.text 取值中） | string | 原始请求文本 |
| index（cbm\_tidy.text 取值中） | int | 规整的子问题数据标记，从 0 开始计数 |
| value（cbm\_tidy.text 取值中） | string | 规整后的子问题内容 |

#### cbm\_semantic -- 传统技能

传统技能结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 3,
        "text": "{\"cbm_semantic\":{\"intent\":0}}"
    },
    "cbm_semantic": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 3,
        "text": "{\"answer\":{\"text\":\"今天是2025年9月3号，星期三，乙巳年七月十二。\",\"type\":\"T\"},\"category\":\"IFLYTEK.datetimePro\",...}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明 |
| intent（cbm\_meta.text 取值中） | int | 当前请求所属规整的子问题，对应语义规整结果 intent 数组下 index 取值 |
| cbm\_semantic.text | string | 传统技能结果详细内容，具体格式见传统语义链路 nlp 结果说明 |

#### cbm\_tool\_pk -- 意图落域

意图落域结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 2,
        "text": "{\"cbm_tool_pk\":{\"intent\":0}}"
    },
    "cbm_tool_pk": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "plain",
        "seq": 0,
        "status": 2,
        "text": "{\"pk_type\":\"cbm_semantic\",\"pk_source\":{\"domain\":\"datetimePro\"},\"tool\":{}}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明 |
| intent（cbm\_meta.text 取值中） | int | 当前请求所属规整的子问题，对应 cbm\_tidy.text 中 intent 数组下 index 取值 |
| cbm\_tool\_pk.text | string | 意图落域结果详细内容，**JSON 格式字符串** |
| pk\_type（cbm\_tool\_pk.text 取值中） | string | 落域结果判定来源模块 |
| pk\_source.domain（cbm\_tool\_pk.text 取值中） | string | 落域结果，常见取值有：chat、技能标识、智能体名称 |
| pk\_source.intent（cbm\_tool\_pk.text 取值中） | string | 落域到智能体时才有该字段，对应智能体某个意图取值 |

#### cbm\_retrieval\_classify -- 知识分类

知识分类结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 2,
        "text": "{\"cbm_retrieval_classify\":{\"intent\":0}}"
    },
    "cbm_retrieval_classify": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 2,
        "text": "{\"type\":1,\"label\":0,\"keyword\":\"天空是蓝色的原因\"}"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明 |
| intent（cbm\_meta.text 取值中） | int | 当前请求所属规整的子问题，对应 cbm\_tidy.text 中 intent 数组下 index 取值 |
| cbm\_retrieval\_classify.text | string | 知识分类结果内容，**JSON 格式字符串** |
| type（cbm\_retrieval\_classify.text 取值中） | int | 知识分类查询类型 0：不走知识查询或联网搜索 1：走知识查询或联网搜索 |

#### cbm\_knowledge -- 知识溯源

知识溯源结果，该结果为交互业务触发联网搜索或本地文档问答，给出知识来源信息。

解析 `event.data` 获取**联网搜索**类结果格式示例：

```json
{
    "cbm_knowledge": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 3,
        "text": "[{\"repoId\":\"agg_knowledge\",\"docId\":\"https://example.com/article\",\"title\":\"文章标题\",\"summary\":\"摘要\",\"content\":\"正文...\",\"detail\":\"详情\",\"publishTime\":\"发布时间\",\"docName\":\"文档名称\",\"repoName\":\"联网搜索\"}]"
    },
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 3,
        "text": "{\"cbm_knowledge\":{\"intent\":0}}"
    }
}
```

解析 `event.data` 获取**文档问答**类结果格式示例：

```json
{
    "cbm_knowledge": {
        "compress": "raw",
        "format": "json",
        "text": "[{\"score\":0.9989267,\"repoId\":\"知识库ID\",\"docId\":\"文档ID\",\"chunkId\":\"0\",\"title\":\"0\",\"content\":\"文档内容...\",\"detail\":\"详情...\",\"docName\":\"文档名称.docx\",\"repoName\":\"知识库名称\"}]",
        "encoding": "utf8",
        "seq": 0,
        "status": 3
    },
    "cbm_meta": {
        "compress": "raw",
        "format": "json",
        "text": "{\"cbm_knowledge\":{\"intent\":0}}",
        "encoding": "utf8",
        "seq": 0,
        "status": 3
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明 |
| intent（cbm\_meta.text 取值中） | int | 当前请求所属规整的子问题，对应 cbm\_tidy.text 中 intent 数组下 index 取值 |
| cbm\_knowledge.text | string | 知识溯源详细内容，**JSON 格式字符串** |
| repoId（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**知识库的唯一标识符，不具备语义** 2、联网搜索时取值固定为：**agg\_knowledge** |
| docId（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档或数据记录的唯一标识符，不具备语义** 2、联网搜索时取值为：**网页 URL** |
| repoName（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档库名称** 2、联网搜索时取值固定为：**联网搜索** |
| docName（cbm\_knowledge.text 取值中） | string | 1、文档问答时取值为：**文档名称** 2、联网搜索时取值为：**网页名称** |

#### nlp -- 大模型回复

大模型回复结果，解析 `event.data` 获取结果格式示例：

```json
{
    "cbm_meta": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 0,
        "text": "{\"nlp\":{\"intent\":0,\"nlp_origin\":\"cbm_retrieval\"}}"
    },
    "nlp": {
        "compress": "raw",
        "encoding": "utf8",
        "format": "json",
        "seq": 0,
        "status": 0,
        "text": "天空之所以呈现"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| encoding | string | 编码格式 |
| compress | string | 压缩格式 |
| format | string | 内容格式 |
| seq | int | 结果帧序号 |
| status | int | 结果帧状态 |
| cbm\_meta.text | string | 结果补充说明 |
| intent（cbm\_meta.text 取值中） | int | 当前请求所属规整的子问题，对应 cbm\_tidy.text 中 intent 数组下 index 取值 |
| nlp\_origin（cbm\_meta.text 取值中） | string | 大模型回复内容参考来源 cbm\_reply：代表大模型自己生成 cbm\_retrieval：代表参考知识查询结果 cbm\_semantic：代表参考传统技能结果 |
| nlp.text | string | 大模型回复内容 |

### 离线交互

下面主要介绍离线语音识别相关结果。

#### esr\_pgs -- 离线听写流式

离线听写流式结果，解析 `event.data` 获取结果格式示例：

```json
{
    "text": {
        "content": "点一"
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| content | string | 离线流式识别结果 |

#### esr\_iat -- 离线听写

离线听写结果，解析 `event.data` 获取结果格式示例：

```json
{
    "text": {
        "bg": "-1",
        "ed": "-1",
        "ismandarin": "true",
        "mode": "wfst",
        "sc": "9014",
        "ws": [
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"", "w":"你"},
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"", "w":"叫"},
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"", "w":"什么"},
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"", "w":"名字"},
            {"sc":"0", "slot":"", "w":"。"}
        ]
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| bg | string | 开始 |
| ed | string | 结束 |
| ismandarin | string | true：中文识别引擎 |
| mode | string | wfst 代表离线识别模式 |
| ws | array | 词条列表 |
| sc | string | 分词得分 |
| pinyin | string | 分词拼音 |
| slot | string | 分词所在槽位 |
| w | string | 分词结果 |

#### esr\_fsa -- 离线命令词

离线命令词结果，解析 `event.data` 获取结果格式示例：

```json
{
    "intent": {
        "bg": "-1",
        "ed": "-1",
        "ismandarin": "true",
        "mode": "fsa",
        "rc": 0,
        "sc": "8803",
        "ws": [
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"open", "w":"打开"},
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"location", "w":"客厅"},
            {"boundary":"", "pinyin":"", "sc":"0", "slot":"device_light", "w":"灯"},
            {"sc":"0", "slot":"", "w":"。"}
        ]
    }
}
```

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| bg | string | 开始 |
| ed | string | 结束 |
| ismandarin | string | true：中文识别引擎 |
| mode | string | fsa 代表离线语法结果 |
| ws | array | 词条列表 |
| sc | string | 分词得分 |
| pinyin | string | 分词拼音 |
| slot | string | 分词所在槽位 |
| w | string | 分词结果 |
