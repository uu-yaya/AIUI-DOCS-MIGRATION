---
title: 交互 API
---

::: info 概述
交互API提供了与AIUI平台进行数据交互的接口规范，涵盖从连接建立到断开的全流程，以及相关的安全设置说明。
:::

## 服务介绍

本协议接口仅适用于`传统语义交互链路`服务场景，提供在线语音交互能力。关于AIUI平台交互链路区别可以查看[AIUI服务链路介绍](/platform-service/service-chain "AIUI服务链路介绍")文档详细了解。

**调用示例Demo**：[WebSocket Demo](https://gitee.com/xiaosumay/DemoCode/tree/master/websocket)

## 接口说明

温馨提示

1、本协议API仅适用于**传统语义交互链路**服务访问，不可与通用大模型或极速超拟人交互链路服务混用。

2、接口是短连接，每次交互要新建连接，会话完成后，讯飞断开连接。单次会话过程中支持流式交互（客户端不断上传音频数据，讯飞不断下发结果）。

`交互时序`图示：

- 设备有vad功能：

![](/media/202506/2025-06-10_142851_8019780.5301268858413158.png)

- 设备无vad功能，依赖云端vad：

![](/media/202506/2025-06-10_142902_9350360.909355181468449.png)

## 建立连接

温馨提示

握手成功后：1. 连接>60s超时,讯飞断开连接
2. >10s无数据交互，讯飞断开连接。

WebSocket握手阶段鉴权，参数在url中指定。

### 请求地址

```
ws[s]://wsapi.xfyun.cn/v1/aiui
```

### 请求参数

> 参数格式：  需 url encode

```ini
key1=value1&key2=value2…
```

> 请求示例：

```java
ws[s]://wsapi.xfyun.cn/v1/aiui?appid=xxx&checksum=xxx&curtime=xxx&param=xxx
```

> 参数说明：

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | 是 | AIUI开放平台注册申请应用的应用ID(AppID) | 594bxxc3 |
| curtime | string | 是 | 当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数 | 1502607694 |
| signtype | string | 否 | 签名算法，可选 md5（默认），sha256 |  |
| checksum | string | 是 | 令牌，生成方法：(APIKey + curtime + param拼接字符串)，根据signtype参数的算法加密 | 02607694eyjzy2vuzsi6im1haw4ifq |
| param | string | 是 | 参数用 Base64 编码后的字符串，详见 param 字段说明 | eyJzY2VuZSI6Im1haW4ifQ== |

### 注意：

APIKey：接口密钥，在 AIUI 开放平台查看；

checksum 有效期： 5 分钟(用curtime计算)， curtime必须是东八区标准时间，否则无效；

BASE64 编码采用 MIME 格式，编码后大小增加约1/3

**checksum**生成示例，假设加密算法为 md5：

```java
String apikey="abcd1234";
String curtime="1502607694";
String param="eyAiYXVmIjogImF1ZGlvL0wxNjtyYXR...";
String checksum=MD5(apikey+curtime+param);
```

### param构建说明

param字段存放交互业务参数，除通用配置相关参数外还可以指定识别、语义、合成、翻译功能相关参数。简单示例如下：

```json
{
    "result_level": "plain",
    "auth_id": "894c985bf8b1111c6728db79d3479aef",
    "pers_param":"{\"auth_id\":\"894c985bf8b1111c6728db79d3479aef\"}",
    "data_type": "audio",
    "aue": "raw",
    "scene": "main_box",
    "sample_rate": "16000",
    "vad_info": "end",
    "close_delay": "200"
}

BASE64编码取值赋值param参数：
eyAicmVzdWx0X2xldmVsIjogInBsYWluIiwgImF1dGhfaWQiOiAiODk0Yzk4NWJmOGIxMTExYzY3MjhkYjc5ZDM0NzlhZWYiLCAicGVyc19wYXJhbSI6IntcImF1dGhfaWRcIjpcIjg5NGM5ODViZjhiMTExMWM2NzI4ZGI3OWQzNDc5YWVmXCJ9IiwgImRhdGFfdHlwZSI6ICJhdWRpbyIsICJhdWUiOiAicmF3IiwgInNjZW5lIjogIm1haW5fYm94IiwgInNhbXBsZV9yYXRlIjogIjE2MDAwIiwgInZhZF9pbmZvIjogImVuZCIsICJjbG9zZV9kZWxheSI6ICIyMDAiIH0=
```

下面按照参数分属功能进行详细说明：

#### 通用配置参数

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| scene | string | 是 | 情景模式 | main |
| auth\_id | string | 是 | 设备唯一ID（鉴权），自定义的**32位**字符串，包括英文小写字母与数字 | 2049a1b2fdedae553bd03ce6f4820ac4 |
| data\_type | string | 是 | 上传数据类型： text（文本） audio（音频） | text |
| interact\_mode | string | 否 | 交互模式: continuous（一次唤醒，持续交互） Oneshot（单轮交互）（一次唤醒，一次交互） | continuous |
| close\_delay | string | 否 | 交互完成后，云端延迟关闭连接时间，单位ms。取值范围：[0,200] |  |
| sn | string | 否 | 唯一设备id，推荐公司名+mac地址。使用音乐时需要与音乐设备注册激活请求的sn值一样 | iflytek-00:09:5B:EC:EE:F2 |

#### 语义参数

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **参数** | **类型** | **必须** | **说明** | **示例** |
| lat | string | 否 | 纬度，用于地理定位 | 31.83 |
| lng | string | 否 | 经度，用于地理定位 | 117.14 |
| topn | string | 否 | 多候选词 | 2 |
| pers\_param | string | 否 | 动态实体生效范围： 1. 用户级（auth\_id） 2. 应用级（AppID） 3. 自定义级 | "{\"auth\_id\":\"xxxxxx\"}" |
| clean\_dialog\_history | string | 否 | 清除交互历史： 1. user（手动清除） 2. auto（系统清除，默认） | user |

#### 识别参数

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| aue | string | 否 | 音频编码，可选： raw（默认，pcm或wav格式） speex（sample\_rate=8000） speex-wb（宽频speex格式，sample\_rate=16000） opus（sample\_rate=8000） opus-wb（宽频opus格式，sample\_rate=16000） |  |
| sample\_rate | string | 否 | 音频采样率：16000（默认）、8000 |  |
| speex\_size | string | 否 | speex音频帧大小，speex音频必传。详见speex\_size与speex库压缩等级关系表 | 60 |
| result\_level | string | 否 | 结果级别：plain（精简，默认），complete（完整） |  |
| VAD（端点检测）\_info | string | 否 | 是否需要云端返回 VAD（端点检测） 信息：end（末端点） | end |
| cloud\_vad\_eos | string | 否 | 后端点静音时长，单位ms | 700 |
| vrto | string | 否 | 无效交互等待时间（有音频但没识别结果），超时讯飞断开连接，单位ms | 10000 |

*speex\_size与speex库压缩等级（quantity）关系表：*

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

#### 所见即可说参数

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **参数** | **类型** | **必须** | **说明** | **示例** |
| IAT（语音识别）\_user\_data | string | 是 | 所见即可说-识别，总长度<4000字节 | 见下发json示例 |
| NLP（语义理解）\_user\_data | string | 否 | 所见即可说-语义，总长度<4000字节 | 见下发json示例 |

`iat\_user\_data`取值示例：

```json
{
    "recHotWords":"播报内容|地图显示|路线优先",//会话级热词
    "sceneInfo":{}
}
```

`nlp_user_data`取值示例：

```json
{
    "res":[{
        "res_name":"vendor_applist",//资源名称
        "data":"xxxxx"//数据的base64编码
    }],
    "skill_name":"telephone"//对应的技能名称
}
```

#### 合成参数

温馨提示

当需要发送文本合成请求时，注意 scene 参数取值需要固定为 IFLYTEK.TTS（语音合成）

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| ent | string | 否 | 引擎类型 | xtts |
| vcn | string | 是 | 发音人，[发音人列表](/sdk-dev/features/tts) | x\_xiaoyan |
| speed | string | 否 | 语速，取值范围：[0,100]，值越大语速越快。默认值：50 | 50 |
| volume | string | 否 | 音量，取值范围：[0,100]。默认值：50 | 50 |
| pitch | string | 否 | 语调，取值范围：[0,100]。默认值：50 | 50 |
| TTS（语音合成）\_aue | string | 否 | 合成音频编码格式：，raw（pcm格式，默认），lame（mp3） | raw |
| TTS（语音合成）\_res\_type | string | 否 | 合成音频下发格式，取值范围：  url：以url链接形式流式下发音频，仅支持mp3格式，返回内容可参考文章接收结果部分的合成返回内容 url\_v2：云端合成完毕后以url链接形式一次性下发音频，默认为mp3链接 | url |

#### 语义后合成参数

温馨提示

在传统语义链路下对接API协议，需要托管AIUI进行全链路交互下发语音合成数据，除了在AIUI应用下开启语音合成，还需携带下面固定参数取值

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| context | string | 是（语义后合成必传） | json字符串，参数设置时注意转义符号不能丢，内容为”{\“SDK\_support\“:[\“TTS（语音合成）\“]}” | “{\“SDK\_support\“:[\“TTS（语音合成）\“]}” |

#### 翻译参数

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **参数** | **类型** | **必须** | **说明** | **示例** |
| from | string | 是 | 源语言，支持选项： • cn（中文） • en（英文） | cn |
| to | string | 是 | 目标语言，支持选项： • cn（中文） • en（英文） • ug（维吾尔语） • ja（日语） • ko（韩语） • fr（法语） • es（西班牙语） • ru（俄语） | en |

## 交互请求

温馨提示

音频数据请求限制：1、单次会话音频总时长**<60s**、音频数据大小**<2M**； 2、音频发送总帧数**<3000帧** ；3、上传 **speex压缩音频**时 每次发送的字节数应为 **speex\_size的整数倍**。

### 数据上传

链接建立成功后，后续只要不断地进行请求数据发送即可，内容是音频或文本的二进制数据。

- 发送方式
  - 音频数据：分帧发送
  - 文本数据：一帧发送完毕

### 上传结束符

当数据发送完毕后，如不使用云端vad+延迟断开链接服务，需要客户端主动发送结束标志，内容是字符串 `--end--` 的二进制数据。

## 结果说明

### 结果类型展示

下面介绍传统语义链路API，交互下发的所有结果种类

#### 链接建立结果

点击查看

```json
    {
    　　"action":"started",
    　　"code":"0",
    　　"data":"",
    　　"desc":"success",
    　　"sid":"awa00000001@ch27f00e2d00fe430100"
    }
```

#### 识别结果（完整）

指定参数 result\_level 取值为 complete 时

点击查看

```json
    {
        "action":"result",
        "code":"0",
        "data":{
            "sub":"iat",
            "auth_id":"xxx",
            "text":{
                "sn":1,
                "ls":false,
                "bg":0,
                "ed":0,
                "ws":[
                    {"bg":0,"cw":[{"sc":0,"w":"今天"}]},
                    {"bg":0,"cw":[{"sc":0,"w":"星期几"}]}]
            },
            "json_args":{
                "language":"zh-cn",
                "accent":"mandarin"
            },
            "result_id":1,
            "is_last":true,
            "is_finish":true
    　　},
    　　"desc":"success",
    　　"sid":"awa00000001@ch27f00e2d00fe430100"
    }
```

#### 识别结果（精简）

指定参数 result\_level 取值为 plain 时

点击查看完整json示例

```json
    {
    　　"action":"result",
    　　"code":"0",
    　　"data":{
    　　　　"sub":"iat",
            "auth_id":"xxx",
            "text":"今天星期几",
            "json_args":{
                "language":"zh-cn",
                "accent":"mandarin"
            },
            "result_id":1,
            "is_last":true,
            "is_finish":true
    　　},
    　　"desc":"success",
    　　"sid":"awa00000001@ch27f00e2d00fe430100"
    }
```

#### 语义结果

点击查看完整json示例

```json
    {
        "action":"result",
        "code":"0",
        "data":{
            "sub":"nlp",
            "auth_id":"xxx",
            "intent":{
                "answer":{
                    "text":"今天是3月1日",
                    "type":"T"
                },
                "match_info":{
                    "type":"gparser_path",
                    "value":"-----"
                },
                "operation":"ANSWER",
                "rc":0,
                "service":"datetime",
                "sid":"ara00000002@ch5aa00e0ba5e72a0100",
                "state":{

                },
                "text":"今天星期几",
                "uuid":"atn004a008d@ch1aa50e0ba5e96f1d01"
            },
            "result_id":1,
            "is_last":true,
            "is_finish":true
        },
        "desc":"success",
        "sid":"awa00000001@ch03040e2d0ad3430100"
    }
```

#### tpp 应用后处理结果

点击查看完整json示例

```json
    {
        "action":"result",
        "code":"0",
        "data":{
            "sub":"tpp",
            "auth_id":"xxx",
            "content":"xxx",
            "result_id":1,
            "is_last":true,
            "is_finish":true
        },
        "desc":"success",
        "sid":"awa00000001@ch03040e2d0ad3430100"
    }
```

#### 合成结果

点击查看完整json示例

```json
    {
        "action":"result",
        "code":"0",
        "data":{
            "sub":"tts",
            "auth_id":"xxx",

            //content是音频数据，需要base64解码，android解析示例
            //步骤1 保存字符串：String base64String = "YXNkZmFz......"
            //步骤2 base64解码： byte[] audio = Base64.decode(base64String, Base64.DEFAULT);
            //步骤3 保存音频：new FileOutputStream(new File(filePath), true).write(audio);
            "content":"YXNkZmFz......",
            "result_id":0,
            "json_args":{
                "cancel":"0",//合成过程中是否被取消
                "dte":"raw",
                 //dts音频序号,0（长音频，开始），1（长音频中间结果，可出现多次）,2（长音频结束),3（短音频，结束）
                 //长音频dts示例：0 1 1 1 ... 2
                 //短音频dts示例: 3
                "dts":1,
                // frame_id：音频段id，取值：1,2,3,...
                "frame_id":59,
                "text_end":220,
                //text_percent：合成进度
                "text_percent":11
            },
            "is_last":true,
            "is_finish":true
        },
        "desc":"success",
        "sid":"awa00000001@ch03040e2d0ad3430100"
    }
```

#### vad结果

请求参数中携带vad\_info配置时，云端才会下发

点击查看完整json示例

```json
    {
        "action":"vad",
        "code":"0",
        "data":{
            "vad_info":"end"
        },
        "desc":"success",
        "sid":"awa00000001@ch2ba00e4f8e8c430100"
    }
```

#### 错误结果

服务异常时（如会话超时），将异常信息以 text message 形式返回给客户端并关闭连接。

点击查看完整json示例

```json
    {
    　　"action":"error",
    　　"code":"10205",
    　　"data":"",
    　　"desc":"websocket read error|read dispatch data error: i/o timeout",
    　　"sid":"awa00000003@ch78b90e18f1d4630100"
    }
```

### 结果参数说明

`响应结果`字段说明：

|  |  |  |
| --- | --- | --- |
| **参数** | **类型** | **说明** |
| action | string | 操作类型，支持以下取值： • started（握手） • result（结果） • error（出错） • VAD（端点检测）（端点检测） |
| code | string | 返回码，具体含义详见 [错误码文档](/sdk-dev/error-codes) |
| data | object | 接口返回的结果数据（具体结构需结合实际业务场景确定） |
| desc | string | 对操作结果或状态的描述信息（如成功提示、错误原因说明等） |
| sid | string | 会话唯一标识（sid），调试时需提供该参数给讯飞技术支持，用于定位问题 |

`data字段`详细说明：

|  |  |  |
| --- | --- | --- |
| **参数** | **类型** | **说明** |
| sub | string | 业务类型（NLP（语义理解）-语义，IAT（语音识别）-识别，tpp-后处理，itrans-翻译，TTS（语音合成）-合成） |
| intent | object | 语义结果数据 |
| text | object/string | 识别结果，object-分词结果，string-精简结果 |
| content | object | 后处理、翻译、合成等结果 |
| auth\_id | string | 用户ID回传 |
| is\_last | bool | 是否为该业务的最后一条结果（如识别的最后一条结果，语义的最后一条结果） |
| is\_finish | bool | 是否为本次会话的最后一条结果 |
| result\_id | int | 结果序号 |
| json\_args | object | 结果参数 |

`intent字段`详细说明：

详见 [语义协议](/custom-biz/protocols/semantic-protocol)

`text字段`详细说明

|  |  |  |  |
| --- | --- | --- | --- |
| **参数** | **全称** | **类型** | **说明** |
| sn | sentence | number | 第几句 |
| ls | last sentence | boolean | 是否最后一句 |
| bg | begin | number | 开始 |
| ed | end | number | 结束 |
| ws | words | array | 词 |
| cw | chinese word | array | 中文分词 |
| w | word | string | 单字 |
| sc | score | number | 分数 |

合成结果中`json_args字段`详细说明：

|  |  |  |
| --- | --- | --- |
| **参数** | **类型** | **说明** |
| dte | string | 合成数据编码，如raw等 |
| dts | int | 数据状态 |
| frame\_id | int | 合成音频编号，从1开始 |
| text\_percent | int | 音频合成的进度百分比 |
| error | string | 错误信息 |
| cancel | string | 是否已取消 |
| text\_end | int | 当前合成音频对应文本的结束位置（按照UTF16编码计算） |

## 连接断开

温馨提示

如果客户要中断数据上传，必须发送 end 指令(--end--)给服务端，讯飞下发完相应结果后会主动断开连接。

连接的断开应由讯飞服务端发起，客户端不应主动断开；
连接断开情况：

1. 会话正常结束，is\_finish = true 的结果下发后断开；
2. 会话报错，下发错信息action=”error”后断开；
3. 会话超时，在连接时长>60s 或 10s 无有效数据交互时断开。

## IP白名单

AIUI应用也提供ip白名单方式给客户做请求客户端限制，该服务`仅支持传统语义交互API`。
在 AIUI应用配置页面 –> 资源下载页面 –> WEB SOCKET接入 下配置

- 关闭状态：只要appid和appkey正确就能使用AIUI 服务
- 开启状态：授权认证通过后，系统检查请求方ip是否在白名单中，非白名单ip请求则拒绝服务。

![](/media/202509/2025-09-09_162937_8204270.6099227460893577.png)
