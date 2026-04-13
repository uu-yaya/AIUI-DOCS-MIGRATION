---
title: 极速超拟人声纹管理 API
description: 声纹识别相关的成员管理和声纹特征管理接口
---

## 概述

声纹管理 API 提供声纹识别相关服务，包括成员管理和声纹特征管理两类接口。

> 使用前需先联系讯飞商务获取授权，或发送邮件到 aiui_support@iflytek.com 提交申请。接口调用前，指定设备（SN）需先调用 AIUI 服务完成设备激活。每个设备（SN）默认最多添加 10 个成员，每个成员最多注册 3 个声纹。

### 接口列表

**成员管理接口**

| 接口 | 方法 | 路径 |
|---|---|---|
| 成员添加 | POST | `/v3/aiint/members` |
| 成员查询 | GET | `/v3/aiint/members` |
| 成员编辑 | PUT | `/v3/aiint/members` |
| 成员删除 | DELETE | `/v3/aiint/members` |

**声纹管理接口**

| 接口 | 方法 | 路径 |
|---|---|---|
| 声纹注册 | POST | `/v3/aiint/vpr/features` |
| 声纹查询 | GET | `/v3/aiint/vpr/features` |
| 声纹更新 | PUT | `/v3/aiint/vpr/features` |
| 声纹删除 | DELETE | `/v3/aiint/vpr/features` |
| 声纹检索 | POST | `/v3/aiint/vpr/searchFea` |

## 接口说明

### 请求地址

```text
http[s]://aiui.xf-yun.com
```

### 接口鉴权

鉴权参数构建方式参考 [鉴权文档](./auth.md)。鉴权时间戳有时效性，建议每次请求时实时获取最新时间戳。

---

## 成员管理

### 成员添加

- **请求方式**：POST
- **路径**：`/v3/aiint/members`
- **Content-Type**：`application/json`

#### 请求示例

```json
{
    "appid": "5c8b403a",
    "sn": "test-sn",
    "member_id": "ifly-001",
    "name": "小飞",
    "age_sex": "child",
    "desc": "可爱的小飞飞"
}
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |
| member_id | string | 否 | 成员标识，不超过 32 位，不传则自动生成 UUID | `ifly-001` |
| name | string | 是 | 成员名称，不超过 16 个字符，同一 SN 下不可重复 | `小飞` |
| age_sex | string | 否 | 性别年龄：`child`、`male`、`female`、`oldmale`、`oldfemale` | `child` |
| desc | string | 否 | 描述，不超过 32 个字符 | `可爱的小飞飞` |

#### 响应示例

```json
{
    "sid": "acm00680001@dx191bbe967b5c444992",
    "code": 0,
    "msg": "success",
    "data": null
}
```

### 成员查询

- **请求方式**：GET
- **路径**：`/v3/aiint/members?appid={appid}&sn={sn}`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |

#### 响应示例

```json
{
    "sid": "acm00680001@dx191bbe967b5c444992",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "appid": "5c8b403a",
            "sn": "test-sn",
            "member_id": "ifly-001",
            "name": "小飞",
            "age_sex": "child",
            "desc": "可爱的小飞飞"
        }
    ]
}
```

### 成员编辑

- **请求方式**：PUT
- **路径**：`/v3/aiint/members`
- **Content-Type**：`application/json`

请求参数与成员添加相同。

### 成员删除

- **请求方式**：DELETE
- **路径**：`/v3/aiint/members`
- **Content-Type**：`application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |
| member_id | string | 是 | 成员标识 | `ifly-001` |

> 删除成员时会同时删除其声纹数据。

---

## 声纹管理

### 声纹注册

- **请求方式**：POST
- **路径**：`/v3/aiint/vpr/features`
- **Content-Type**：`multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |
| member_id | string | 否 | 成员标识，不传则自动生成新成员 | `ifly-001` |
| data | file | 是 | 音频文件，仅支持 PCM 16k 16bit 单通道，时长 1s ~ 2min | — |
| feature_info | string | 否 | 描述，不超过 32 个字符 | `小飞飞近场` |

#### 响应示例

```json
{
    "sid": "acm00010034@dx191749d8e5d0001562",
    "code": 0,
    "msg": "success",
    "data": {
        "feature_id": "fsdfwee234324",                       // 声纹特征 ID
        "member_id": "4b37ccbb6679c34389176ed5bc920196",     // 成员 ID
        "age_sex": "child"                                    // 检测结果
    }
}
```

### 声纹查询

- **请求方式**：GET
- **路径**：`/v3/aiint/vpr/features?appid={appid}&sn={sn}&member_id={member_id}`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识 | `test-sn` |
| member_id | string | 否 | 成员标识，不传则返回所有成员的声纹 | `ifly-001` |

#### 响应示例

```json
{
    "sid": "acm00680001@dx191bbe967b5c444992",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "appid": "5c8b403a",
            "sn": "test-sn",
            "member_id": "ifly-001",
            "name": "小飞",
            "age_sex": "child",
            "desc": "可爱的小飞飞",
            "features": [
                {
                    "feature_id": "w23ddfw3",
                    "merge_cnt": 1,
                    "feature_info": "近场"
                },
                {
                    "feature_id": "w23ddfw4",
                    "merge_cnt": 1,
                    "feature_info": "远场"
                }
            ]
        }
    ]
}
```

#### 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| data[i].features[j].feature_id | string | 声纹 ID | `w23ddfw3` |
| data[i].features[j].merge_cnt | int | 特征合并更新次数，初始值 1 | `1` |
| data[i].features[j].feature_info | string | 特征描述 | `近场` |

### 声纹更新

更新指定 ID 的声纹特征，可选择覆盖或与原有特征合并。

- **请求方式**：PUT
- **路径**：`/v3/aiint/vpr/features`
- **Content-Type**：`multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |
| feature_id | string | 是 | 声纹特征 ID（注册接口返回） | `fsdfwee234324` |
| cover | string | 否 | 是否覆盖原有特征：`true`（覆盖，默认）或 `false`（合并更新） | `false` |
| data | file | 是 | 音频文件，仅支持 PCM 16k 16bit 单通道，时长 1s ~ 2min | — |
| feature_info | string | 否 | 描述，不超过 32 个字符 | `小飞飞近场` |

#### 响应示例

```json
{
    "sid": "acm00010034@dx191749d8e5d0001562",
    "code": 0,
    "msg": "success",
    "data": {
        "feature_id": "fsdfwee234324",
        "merge_cnt": 2,               // 合并次数
        "member_id": "ifly-001",
        "age_sex": "child"
    }
}
```

### 声纹删除

- **请求方式**：DELETE
- **路径**：`/v3/aiint/vpr/features`
- **Content-Type**：`application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识，长度不超过 32 位 | `test-sn` |
| feature_id | string | 是 | 声纹特征 ID | `fsdfwee234324` |

### 声纹检索

检索指定设备声纹库中与上传音频匹配的声纹信息，用于效果验证。

- **请求方式**：POST
- **路径**：`/v3/aiint/vpr/searchFea`
- **Content-Type**：`multipart/form-data`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | 应用 AppID | `5c8b403a` |
| sn | string | 是 | 设备唯一标识 | `test-sn` |
| data | file | 是 | 音频文件，PCM 16k 16bit 单通道 | — |

#### 响应示例

```json
{
    "sid": "acr005c0001@dx19a4333de9f0001992",
    "code": 0,
    "msg": "success",
    "data": [
        {
            "member": {
                "appid": "5c8b403a",
                "sn": "test-sn",
                "member_id": "ifly-001",
                "name": "小飞",
                "age_sex": "child",
                "desc": "可爱的小飞飞"
            },
            "feature_id": "fhptu9n1kl4",
            "score": 0.85,
            "age": "youth",
            "gender": "male"
        }
    ]
}
```

#### 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| data[i].member | object | 匹配到的成员信息 | — |
| data[i].feature_id | string | 匹配的声纹特征 ID | `fhptu9n1kl4` |
| data[i].score | float | 相似度得分 0 ~ 1，精确到小数点后两位 | `0.85` |
| data[i].age | string | 年龄（仅参考）：`child`、`youth`、`old`、`unknown` | `youth` |
| data[i].gender | string | 性别（仅参考）：`male`、`female`、`child`、`unknown` | `male` |

---

## 在交互链路中使用声纹

### 功能开启

在 AIUI 极速交互类应用中，需要：

1. 选择最新的大模型识别引擎
2. 在 AIUI 应用配置中开启声纹能力（语义模型配置 - 个性化设置项，需授权后可见）

### 结果解析

集成 [极速超拟人交互 API](./interaction.md) 进行音频对话请求时，确保 `appid` 和 `sn` 与声纹注册信息一致。在识别结束帧结果中，解析 `extra` 字段获取声纹匹配结果。

#### 匹配到声纹

```json
{
    "payload": {
        "iat": {
            "text": "{\"extra\":{\"feature_id\":\"99ijf7om8zs\",\"score\":0.51},\"text\":{...}}",
            "status": 2
        }
    }
}
```

`extra` 字段包含 `feature_id`（匹配的声纹 ID）和 `score`（相似度得分）。

#### 未匹配到声纹

```json
{
    "payload": {
        "iat": {
            "text": "{\"extra\":{},\"text\":{...}}",
            "status": 2
        }
    }
}
```

`extra` 为空对象表示未匹配到已注册的声纹。

## cURL 等效调用示例

### 成员添加

```bash
curl -X POST "https://aiui.xf-yun.com/v3/aiint/members?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -H "Content-Type: application/json" \
  -d '{"appid":"your_appid","sn":"test-sn","member_id":"ifly-001","name":"小飞","age_sex":"child"}'
```

### 声纹注册

```bash
curl -X POST "https://aiui.xf-yun.com/v3/aiint/vpr/features?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -F "appid=your_appid" \
  -F "sn=test-sn" \
  -F "member_id=ifly-001" \
  -F "data=@voice.pcm"
```

### 声纹检索

```bash
curl -X POST "https://aiui.xf-yun.com/v3/aiint/vpr/searchFea?host=aiui.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -F "appid=your_appid" \
  -F "sn=test-sn" \
  -F "data=@test_voice.pcm"
```
