---
title: 传统语义个性化 API
description: 传统语义链路的动态实体资源上传、查询和删除接口
---

## 概述

传统语义链路的个性化 API 用于动态实体资源管理，与大模型链路 / 极速超拟人链路的个性化 API 接口地址和协议不同。

> 通用大模型链路和极速超拟人链路请参考 [大模型个性化 API](../llm/personalization.md)。

### 特性说明

- 资源上传后需要 **5 分钟以上**才能生效（与大模型链路秒级生效不同）
- 上传后需调用查询接口确认打包状态
- 内置动态实体：`IFLYTEK.telephone`、`IFLYTEK.smartH_deviceAlias`

## 接口鉴权

传统语义个性化 API 使用 HTTP Header 方式传递鉴权参数。

| Header 名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| X-NameSpace | string | 是 | 命名空间 | `IFLYTEK` |
| X-Nonce | string | 是 | 随机数，最大 128 字符 | `abc123` |
| X-CurTime | string | 是 | 当前 UTC 时间戳（秒级） | `1693456789` |
| X-CheckSum | string | 是 | `MD5(accountKey + Nonce + CurTime)` | — |

> CheckSum 有效期为 5 分钟。

## 上传资源

- **请求方式**：POST
- **地址**：`http[s]://openapi.xfyun.cn/v2/aiui/entity/upload-resource`
- **Content-Type**：`application/x-www-form-urlencoded; charset=utf-8`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5adde3cf` |
| res_name | string | 是 | 资源名，格式：`{命名空间}.{动态实体名}` | `IFLYTEK.music` |
| pers_param | string | 是 | 个性化参数 JSON | `{"appid":"xxx"}` |
| data | string | 是 | Base64 编码的资源数据 | — |

### pers_param 维度说明

| 维度 | pers_param 取值 | 说明 |
|---|---|---|
| 应用级 | `{"appid":"xxx"}` | 全应用共享 |
| 用户级 | `{"auth_id":"xxx"}` 或 `{"uid":"xxx"}` | 按用户区分 |
| 自定义级 | `{"自定义key":"自定义value"}` | 自定义维度 |

### 资源数据格式

Base64 编码前的原始数据，每行一条记录，首行前需有换行符：

```json
{"name":"可乐","alias":"可口可乐|百事可乐"}
{"name":"维生素功能饮料","alias":"红牛|东鹏特饮|乐虎"}
```

### 请求示例

```bash
curl -X POST "https://openapi.xfyun.cn/v2/aiui/entity/upload-resource" \
  -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
  -H "X-NameSpace: IFLYTEK" \
  -H "X-Nonce: abc123" \
  -H "X-CurTime: 1693456789" \
  -H "X-CheckSum: <MD5签名>" \
  -d "appid=5adde3cf&res_name=IFLYTEK.music&pers_param=%7B%22appid%22%3A%22xxx%22%7D&data=<base64数据>"
```

### 响应示例

```json
{
    "code": "0",
    "data": {
        "sid": "psn003478f3@ch00070e3a78e06f2601",
        "csid": "rwa84b7a73b@ch372d0e3a78e0116200"
    },
    "desc": "success",
    "sid": "rwa84b7a73b@ch372d0e3a78e0116200"
}
```

### 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| code | string | 结果码，`0` 表示成功 | `0` |
| desc | string | 描述 | `success` |
| sid | string | 服务唯一标识 | — |
| data.sid | string | 上传 SID，用于查询打包状态 | `psn003478f3@ch...` |
| data.csid | string | 服务唯一标识 | — |

## 查询资源打包状态

上传资源后等待 5 ~ 10 秒，调用此接口查询打包状态。

- **请求方式**：POST
- **地址**：`http[s]://openapi.xfyun.cn/v2/aiui/entity/check-resource`
- **Content-Type**：`application/x-www-form-urlencoded; charset=utf-8`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| sid | string | 是 | 上传响应中返回的 SID | `psn003478f3@ch...` |

### 响应示例

```json
{
    "code": "0",
    "data": {
        "sid": "psn003478f3@ch00070e3a78e06f2601",
        "csid": "rwa84b7a73b@ch372d0e3a78e0116200",
        "reply": "success",
        "error": 0
    },
    "desc": "success",
    "sid": "rwa84b7a73b@ch372d0e3a78e0116200"
}
```

### 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| data.reply | string | 打包结果描述 | `success` |
| data.error | int | 错误码，`0` 表示成功 | `0` |

## 删除资源

- **请求方式**：POST
- **地址**：`http[s]://openapi.xfyun.cn/v2/aiui/entity/delete-resource`
- **Content-Type**：`application/x-www-form-urlencoded; charset=utf-8`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5adde3cf` |
| res_name | string | 是 | 资源名 | `IFLYTEK.music` |
| pers_param | string | 是 | 个性化参数 JSON | `{"appid":"xxx"}` |

### 响应示例

```json
{
    "code": "0",
    "data": {
        "sid": "psn003478f3@ch00070e3a78e06f2601",
        "csid": "rwa84b7a73b@ch372d0e3a78e0116200",
        "reply": "success",
        "error": 0
    },
    "desc": "success",
    "sid": "rwa84b7a73b@ch372d0e3a78e0116200"
}
```

## cURL 等效调用示例

### 上传资源

```bash
curl -X POST "https://openapi.xfyun.cn/v2/aiui/entity/upload-resource" \
  -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
  -H "X-NameSpace: IFLYTEK" \
  -H "X-Nonce: random123" \
  -H "X-CurTime: $(date +%s)" \
  -H "X-CheckSum: <MD5签名>" \
  -d "appid=your_appid&res_name=IFLYTEK.music&pers_param=%7B%22appid%22%3A%22your_appid%22%7D&data=<base64数据>"
```

### 查询打包状态

```bash
curl -X POST "https://openapi.xfyun.cn/v2/aiui/entity/check-resource" \
  -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
  -H "X-NameSpace: IFLYTEK" \
  -H "X-Nonce: random456" \
  -H "X-CurTime: $(date +%s)" \
  -H "X-CheckSum: <MD5签名>" \
  -d "sid=psn003478f3@ch00070e3a78e06f2601"
```

### 删除资源

```bash
curl -X POST "https://openapi.xfyun.cn/v2/aiui/entity/delete-resource" \
  -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
  -H "X-NameSpace: IFLYTEK" \
  -H "X-Nonce: random789" \
  -H "X-CurTime: $(date +%s)" \
  -H "X-CheckSum: <MD5签名>" \
  -d "appid=your_appid&res_name=IFLYTEK.music&pers_param=%7B%22appid%22%3A%22your_appid%22%7D"
```
