---
title: 声音复刻 API
---

声音复刻API概述

声音复刻API提供了将特定声音特征进行提取与复刻的接口服务，包含服务说明、接口规范及核心功能接口详情。

# 文档更新说明

|  |  |  |
| --- | --- | --- |
| **版本** | **更新内容** | **更新时间** |
| V1.0 | 初始文档 | 2024.10.17 |
| V1.1 | 1、新增复刻新版本：omni\_v1 2、优化相关接口说明 | 2026.01.04 |

## 服务介绍

声音复刻是录入一段音频生成AI定制音色的能力。

温馨提示

1、本服务使用前需先联系讯飞商务获取授权或发送邮件到 aiui\_support@iflytek.com 提交申请。

2、每个设备（SN）最多注册绑定3个资源id。

本协议主要提供复刻资源管理服务，包括**资源注册**、**资源查询**和**资源删除**。具体合成调用需再交互服务API或AIUI SDK中具体实现。

`示例Demo`
点击超链接下载：[HTTP DEMO](https://gitee.com/iflytek-aiui/AIUICbmLiteDemo/tree/master/res-mngr/voice-clone "点击下载")

## 接口说明

### 请求地址

> http[s]://aiui.xf-yun.com

### 接口鉴权

具体鉴权参数构建见[鉴权文档](/api-dev/llm-chain/auth "大模型API服务鉴权")说明。

### 注意：

鉴权的时间戳有时效性，建议每次请求鉴权时都实时的获取最新时间戳，生成鉴权参数

## 功能接口

### 3.1. 资源注册

根据用户输入的音频进行声音复刻，返回资源id。1个SN最多同时绑定注册3个资源，删除已有资源后可继续注册。

- METHOD: POST
- PATH: /v2/aiint/voice-clone/sgen/reg
- Content-Type: multipart/form-data
- HTTP 请求示例：

```http
POST /v2/aiint/voice-clone/sgen/reg HTTP/1.1
Host: 127.0.0.1:9996
Content-Length: 412
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="appid"

5c8b403a
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="sn"

12334454543dfsdfsf
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="data"; filename="/D:/文件/tts/2-正常音色文件-zzy.pcm"
Content-Type: <Content-Type header here>

(data)
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

`表单参数`说明

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | AIUI应用appid | 是 | 5c8b403a |
| sn | string | 设备sn号，长度不超过32位 | 是 | 12334454543dfsdfsf |
| data | file | 音频文件 | 是 | - |
| engine\_version | string | 声音复刻版本：v4、omni\_v1 默认取值：v4 （对应初始版本） | 否 | omni\_v1 |

`注册音频文件格式要求`说明如下：

> 时长: 建议20s~40s
>  文件大小范围：[480KB, 3MB]
>  采样率: 24000
>  通道数: 1
>  位深: 16
>  编码格式: pcm原始音频

`返回值`示例:

```json
  {
      "sid": "acm00010034@dx191749d8e5d0001562",
      "code": 0,
      "msg": "success",
      "data": {
          "res_id": "fsdfwee234324"
      }
  }
```

`返回值参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 请求标识 | 是 | - |
| code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
| msg | string | 描述 | 是 | - |
| data | object | 返回数据 | 否 | - |
| data.res\_id | string | 资源id | 否 | fsdfwee234324 |

### 3.2. 资源查询

根据指定的SN号，查询当前设备已注册资源id。

- METHOD: GET
- PATH: /v2/aiint/voice-clone/sgen/res?AppID=5c8b403a&sn=12334454543dfsdfsf&res\_id=ioixvtc9gps

`参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | AIUI应用appid | 是 | 5c8b403a |
| sn | string | 设备sn号，长度不超过32位 | 是 | 12334454543dfsdfsf |
| res\_id | string | 当前设备已注册资源id | 否 | ioixvtc9gps |

`返回值`示例:

```json
{
    "sid": "acm00940002@dx192d6d3ae917aa9992",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 73,
            "appid": "5c8b403a",
            "sn": "12334454543dfsdfsf",
            "res_id": "ioixvtc9gps",
            "version": "v4",
            "create_time": "2024-09-12 16:56:17"
        },
        {
            "id": 3,
            "appid": "5c8b403a",
            "sn": "12334454543dfsdfsf",
            "res_id": "fsdfwee234324",
            "version": "v4",
            "create_time": "2024-08-19 19:27:29"
        }
    ]
}
```

`返回值参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 请求标识 | 是 | - |
| code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
| msg | string | 描述 | 是 | - |
| data | object | 返回数据 | 否 | - |
| data[i].id | int | 资源id，自增主键 | 是 | 1 |
| data[i].AppID | string | 应用id | 是 | - |
| data[i].sn | string | 设备sn号 | 是 | - |
| data[i].res\_id | string | 资源id，合成时使用 | 是 | - |
| data[i].version | string | 资源版本：v4（旧）、omni\_v1（新） | 是 | - |
| data[i].create\_time | string | 资源创建时间 | 是 | - |

### 3.3. 资源删除

根据指定的SN号下注册存在的资源id，删除该资源id信息。

- METHOD: DELETE
- PATH: /v2/aiint/voice-clone/sgen/del
- Content-Type: application/json

`参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | AIUI应用appid | 是 | 5c8b403a |
| sn | string | 设备sn号，长度不超过32位 | 是 | 12334454543dfsdfsf |
| res\_id | string | 当前设备已注册资源id | 是 | ioixvtc9gps |

`返回值`示例:

```json
 {
      "sid": "acm00010034@dx191749d8e5d0001562",
      "code": 0,
      "msg": "success",
      "data": null
  }
```

`返回值参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 请求标识 | 是 | - |
| code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
| msg | string | 描述 | 是 | - |
| data | object | 返回数据 | 否 | - |

## 合成调用

在通用大模型链路中，声音复刻合成调用见 [4.2.5合成能力使用](/api-dev/llm-chain/tts-usage "4.2.5合成能力使用")文档说明。

温馨提示

声音复刻新增创建版本指定后，合成使用时需要注意vcn参数资源版本的取值关系

|  |  |
| --- | --- |
| **声复刻版本** | **vcn对应取值** |
| v4 | x5\_clone |
| omni\_v1 | x6\_clone |
