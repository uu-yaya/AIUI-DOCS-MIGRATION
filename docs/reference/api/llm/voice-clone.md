---
title: 通用大模型声音复刻 API
description: 声音复刻资源的注册、查询和删除管理接口
---

## 概述

声音复刻 API 用于录入一段音频生成 AI 定制音色。本接口提供复刻资源管理服务，包括**资源注册**、**资源查询**和**资源删除**。

> 使用前需先联系讯飞商务获取授权，或发送邮件到 aiui_support@iflytek.com 提交申请。接口调用前，指定设备（SN）需先调用 AIUI 服务完成设备激活。每个设备（SN）最多注册绑定 3 个资源 ID。

具体合成调用请参考 [合成能力使用](./tts.md)。

## 接口说明

### 请求地址

```text
http[s]://aiui.xf-yun.com
```

### 接口鉴权

鉴权参数构建方式参考 [鉴权文档](./auth.md)。

## 资源注册

根据用户输入的音频进行声音复刻，返回资源 ID。

- **请求方式**：POST
- **路径**：`/v2/aiint/voice-clone/sgen/reg`
- **Content-Type**：`multipart/form-data`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备 SN 号，长度不超过 32 位 | `device001` |
| data | file | 是 | 音频文件 | — |
| engine_version | string | 否 | 声音复刻版本：`v4`（默认）或 `omni_v1` | `omni_v1` |

### 音频文件要求

| 项目 | 要求 |
|---|---|
| 时长 | 建议 20s ~ 40s |
| 文件大小 | 480KB ~ 3MB |
| 采样率 | 24000 |
| 通道数 | 1 |
| 位深 | 16 |
| 编码格式 | PCM 原始音频 |

### 响应示例

```json
{
    "sid": "acm00010034@dx191749d8e5d0001562",
    "code": 0,
    "msg": "success",
    "data": {
        "res_id": "fsdfwee234324"  // 声音复刻资源 ID
    }
}
```

### 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| sid | string | 请求标识 | `acm00010034@dx...` |
| code | int | 状态码，`0` 成功 | `0` |
| msg | string | 描述信息 | `success` |
| data.res_id | string | 资源 ID | `fsdfwee234324` |

## 资源查询

- **请求方式**：GET
- **路径**：`/v2/aiint/voice-clone/sgen/res?appid={appid}&sn={sn}&res_id={res_id}`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备 SN 号 | `device001` |
| res_id | string | 否 | 指定查询的资源 ID | `ioixvtc9gps` |

### 响应示例

```json
{
    "sid": "acm00940002@dx192d6d3ae917aa9992",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 73,
            "appid": "5c8b403a",
            "sn": "device001",
            "res_id": "ioixvtc9gps",
            "version": "v4",
            "create_time": "2024-09-12 16:56:17"
        }
    ]
}
```

## 资源删除

- **请求方式**：DELETE
- **路径**：`/v2/aiint/voice-clone/sgen/del`
- **Content-Type**：`application/json`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备 SN 号 | `device001` |
| res_id | string | 是 | 待删除的资源 ID | `ioixvtc9gps` |

### 响应示例

```json
{
    "sid": "acm00010034@dx191749d8e5d0001562",
    "code": 0,
    "msg": "success",
    "data": null
}
```

## 合成调用说明

| 复刻版本 | vcn 取值 |
|---|---|
| v4 | `x5_clone` |
| omni_v1 | `x6_clone` |

详细合成调用方式参见 [合成能力使用](./tts.md)。

## cURL 等效调用示例

### 资源注册

```bash
curl -X POST "https://aiui.xf-yun.com/v2/aiint/voice-clone/sgen/reg?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -F "appid=your_appid" \
  -F "sn=device001" \
  -F "data=@voice.pcm" \
  -F "engine_version=v4"
```

### 资源查询

```bash
curl "https://aiui.xf-yun.com/v2/aiint/voice-clone/sgen/res?appid=your_appid&sn=device001&host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>"
```

### 资源删除

```bash
curl -X DELETE "https://aiui.xf-yun.com/v2/aiint/voice-clone/sgen/del?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -H "Content-Type: application/json" \
  -d '{"appid":"your_appid","sn":"device001","res_id":"ioixvtc9gps"}'
```
