---
title: 通用大模型个性化 API
description: 用户个性化数据的上传、下载和删除接口，适用于通用大模型交互和极速超拟人交互链路
---

## 概述

个性化 API 用于在产品交互中对用户个性化数据进行上传管理。本接口适用于**通用大模型交互**和**极速超拟人交互**链路。

> 传统语义链路的个性化数据使用方式不同，请参考 [传统语义链路个性化 API](../traditional/personalization.md)。

### 特性说明

- 同步接口，响应即为处理成功，无需检查上传状态
- 秒级生效
- 多个个性化实体需分开上传

## 接口地址

| 地址 | 功能 | 请求方式 |
|---|---|---|
| `https://aiui-personal.xf-yun.com/v1/aiui/personal/upload` | 上传个性化资源 | POST |
| `https://aiui-personal.xf-yun.com/v1/aiui/personal/download` | 下载个性化资源 | POST |
| `https://aiui-personal.xf-yun.com/v1/aiui/personal/delete` | 删除个性化资源 | POST |

### 接口鉴权

鉴权参数构建方式参考 [鉴权文档](./auth.md)。鉴权时间戳有时效性，建议每次请求时实时获取最新时间戳。

## 上传资源

### 请求示例

```json
{
    "header": {
        "app_id": "123456",       // 应用 AppID
        "uid": "1234567890"       // 用户 ID
    },
    "parameter": {
        "personal": {
            "name_space": "IFLYTEK",                    // 命名空间
            "res_name": "IFLYTEK.telephone_contact",    // 资源名
            "id_name": "uid",                           // 实体维度
            "id_value": "1234567890"                    // 维度值
        }
    },
    "payload": {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "text": "<base64编码的个性化数据>"  // 整体不超过 1MB，总条数不超过 2000
        }
    }
}
```

### header 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| app_id | string | 是 | 应用 AppID | `123456` |
| uid | string | 否 | 用户 ID，最大长度 32 | `1234567890` |

### parameter.personal 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| name_space | string | 是 | AIUI 开放平台的命名空间，在「技能工作室 - 我的实体 - 动态实体密钥」中查看 | `IFLYTEK` |
| res_name | string | 是 | 资源名，格式为 `{命名空间}.{资源类型}` | `IFLYTEK.telephone_contact` |
| id_name | string | 是 | 实体维度：应用级（`appid`）、用户级（`uid`）或自定义级别（不超过 32 位） | `uid` |
| id_value | string | 是 | 当前维度对应的值 | `1234567890` |

### payload.text 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| encoding | string | 是 | 文本编码 | `utf8` |
| compress | string | 是 | 压缩方式 | `raw` |
| format | string | 是 | 数据格式 | `plain` |
| text | string | 是 | Base64 编码的个性化资源数据，整体不超过 1MB，总条数不超过 2000 | — |

### 个性化资源数据格式

以 `res_name` 为 `IFLYTEK.telephone_contact` 为例，Base64 解码后格式如下（每行一条记录）：

```json
{"name":"张三","alias":"三弟","phoneNumber":"18888888888"}
{"name":"李四","alias":"四妹","phoneNumber":"18666666666"}
{"name":"王五","alias":"老五","phoneNumber":"18666777777"}
```

## 下载资源

### 请求示例

```json
{
    "header": {
        "app_id": "123456",
        "uid": "1234567890"
    },
    "parameter": {
        "personal": {
            "name_space": "IFLYTEK",
            "res_name": "IFLYTEK.telephone_contact",
            "id_name": "uid",
            "id_value": "1234567890"
        }
    }
}
```

请求参数与上传接口的 `header` 和 `parameter.personal` 部分相同，无需 `payload`。

## 删除资源

请求参数与下载接口相同。

## 响应结果

### 响应示例

```json
{
    "header": {
        "code": 0,
        "message": "success",
        "sid": "gty000c0027@dx181a9a024ea7824532"
    },
    "payload": {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "text": "<base64编码的资源数据>"  // 仅下载接口返回
        }
    }
}
```

### header 响应参数

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| code | int | 错误码，`0` 表示成功 | `0` |
| message | string | 操作描述 | `success` |
| sid | string | 会话唯一 ID，用于问题反馈时的日志索引 | `gty000c0027@dx...` |

### payload.text 响应参数（仅下载接口）

| 参数名 | 类型 | 说明 | 示例 |
|---|---|---|---|
| encoding | string | 响应数据编码 | `utf8` |
| compress | string | 响应数据压缩方式 | `raw` |
| format | string | 响应数据格式 | `plain` |
| text | string | Base64 编码的个性化资源数据 | — |

## cURL 等效调用示例

```bash
curl -X POST "https://aiui-personal.xf-yun.com/v1/aiui/personal/upload?host=aiui-personal.xf-yun.com&date=<URL编码时间戳>&authorization=<鉴权签名>" \
  -H "Content-Type: application/json" \
  -d '{
    "header": {"app_id": "your_appid", "uid": "user001"},
    "parameter": {
      "personal": {
        "name_space": "IFLYTEK",
        "res_name": "IFLYTEK.telephone_contact",
        "id_name": "uid",
        "id_value": "user001"
      }
    },
    "payload": {
      "text": {
        "encoding": "utf8",
        "compress": "raw",
        "format": "plain",
        "text": "eyJuYW1lIjoi5byg5LiJIiwicGhvbmVOdW1iZXIiOiIxODg4ODg4ODg4OCJ9"
      }
    }
  }'
```
