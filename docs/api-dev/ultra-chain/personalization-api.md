---
title: 用户个性化 API
---

用户个性化API

用户个性化API提供了针对用户特征和行为进行定制化处理的完整接口体系，包含服务说明、接口规范、功能接口及响应结果格式。

## 服务介绍

本API服务是提供给客户在产品交互中需要针对用户个性化数据做上传管理时使用的。本协议接口适用于`大模型交互`和`极速超拟人交互`链路服务场景。

## 接口说明

由于大模型协议不兼容传统语义个性化数据，所以在大模型链路中单独提供了本个性化使用文档。
 如果使用的是传统语义链路，个性化数据使用请参考[文档](/custom-biz/skill-studio/dynamic-entities)

个性化数据说明：

- 个性化数据上传为同步接口，响应即为上传成功，无需进行上传状态检查
- 生效时间目前为秒级生效
- 如果存在多个个性化实体，请分开上传

`请求地址`介绍：

| 地址 | 接口功能 | 请求方式 |
| --- | --- | --- |
| <https://aiui-personal.xf-yun.com/v1/aiui/personal/upload> | 上传个性化资源 | POST |
| <https://aiui-personal.xf-yun.com/v1/aiui/personal/download> | 下载个性化资源 | POST |
| <https://aiui-personal.xf-yun.com/v1/aiui/personal/delete> | 删除个性化资源 | POST |

`接口鉴权`说明：

具体鉴权参数构建见[鉴权文档](/api-dev/llm-chain/auth "大模型API服务鉴权")说明。

### 注意：

鉴权的时间戳有时效性，建议每次请求鉴权时都实时的获取最新时间戳，生成鉴权参数

## 3 功能接口

### 上传资源

请求参数：

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
    },
    "payload": {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "text": "eyJuYW1lIjoi5byg5LiJIiwiYWxpYXMiOiLkuInlvJ8iLCJwaG9uZU51bWJlciI6IjE4ODg4ODg4ODg4IiwibG9jYXRpb24iOnt9fQp7Im5hbWUiOiLmnY7lm5siLCJhbGlhcyI6IuWbm+WmuSIsInBob25lTnVtYmVyIjoiMTg2NjY2NjY2NjYiLCJsb2NhdGlvbiI6e319CnsibmFtZSI6IueOi+S6lCIsImFsaWFzIjoi6ICB5LqUIiwicGhvbmVOdW1iZXIiOiIxODY2Njc3Nzc3NyIsImxvY2F0aW9uIjp7fX0="
        }
    }
}
```

接口请求字段由三个部分组成：header，parameter, payload。 字段解释如下：

**header部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| app\_id | string | 是 |  | 应用appid，从平台控制台创建的应用中获取 |
| uid | string | 否 | 最大长度32 | 每个用户的id，用于区分不同用户 |

**parameter.personal部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| name\_space | string | 是 |  | aiui开放平台的命名空间，在「技能工作室-我的实体-动态实体密钥」中查看 |
| res\_name | string | 是 |  | 资源名,XXX为用户的命名空间，如XXX.music |
| id\_name | string | 是 | 自定义级别需要小于32位 | 当前上传实体的维度，包括应用级(AppID)、用户级(uid)、自定义级别 |
| id\_value | string | 是 | 自定义级别需要小于32位 | 当前级别对应的值 |

**payload.text.text部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| encoding | string | 是 | utf8 | 请求的文本数据对应的编码 |
| compress | string | 是 | raw | 请求的文本数据对应的压缩方式 |
| format | string | 是 | plain | 请求的文本数据对应的格式 |
| text | string | 是 | base64 | 个性化资源数据。整体数据不能大于1M，并且总条数小于2000 |

个性化资源示例：

例如：res\_name是IFLYTEK.telephone\_contact时， payload.text.text数据的格式如下示例： （每行是一个联系人数据，对数据进行base64解码）

```json
{"name":"张三","alias":"三弟","phoneNumber":"18888888888"}
{"name":"李四","alias":"四妹","phoneNumber":"18666666666"}
{"name":"王五","alias":"老五","phoneNumber":"18666777777"}
```

### 下载资源

请求参数

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

接口请求字段由三个部分组成：header，parameter。 字段解释如下：

**header部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| app\_id | string | 是 |  | 应用appid，从平台控制台创建的应用中获取 |
| uid | string | 否 | 最大长度32 | 每个用户的id，用于区分不同用户 |

**parameter.personal部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| name\_space | string | 是 |  | aiui开放平台的命名空间，在「技能工作室-我的实体-动态实体密钥」中查看 |
| res\_name | string | 是 |  | 资源名,XXX为用户的命名空间，如XXX.music |
| id\_name | string | 是 | 自定义级别需要小于32位 | 当前上传实体的维度，包括应用级(AppID)、用户级(uid)、自定义级别 |
| id\_value | string | 是 | 自定义级别需要小于32位 | 当前级别对应的值 |

### 删除资源

请求参数

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

接口请求字段由三个部分组成：header，parameter。 字段解释如下：

**header部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| app\_id | string | 是 |  | 应用appid，从平台控制台创建的应用中获取 |
| uid | string | 否 | 最大长度32 | 每个用户的id，用于区分不同用户 |

**parameter.personal部分**

| 参数名称 | 类型 | 必传 | 参数要求 | 参数说明 |
| --- | --- | --- | --- | --- |
| name\_space | string | 是 |  | aiui开放平台的命名空间，在「技能工作室-我的实体-动态实体密钥」中查看 |
| res\_name | string | 是 |  | 资源名,XXX为用户的命名空间，如XXX.music |
| id\_name | string | 是 | 自定义级别需要小于32位 | 当前上传实体的维度，包括应用级(AppID)、用户级(uid)、自定义级别 |
| id\_value | string | 是 | 自定义级别需要小于32位 | 当前级别对应的值 |

## 响应结果

响应示例如下：

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
            "text": "eyJuYW1lIjoi5byg5LiJIiwiYWxpYXMiOiLkuInlvJ8iLCJwaG9uZU51bWJlciI6IjE4ODg4ODg4ODg4IiwibG9jYXRpb24iOnt9fQp7Im5hbWUiOiLmnY7lm5siLCJhbGlhcyI6IuWbm+WmuSIsInBob25lTnVtYmVyIjoiMTg2NjY2NjY2NjYiLCJsb2NhdGlvbiI6e319CnsibmFtZSI6IueOi+S6lCIsImFsaWFzIjoi6ICB5LqUIiwicGhvbmVOdW1iZXIiOiIxODY2Njc3Nzc3NyIsImxvY2F0aW9uIjp7fX0="
        }
    }
}
```

接口返回字段分为两个部分，header，payload，其中payload字段仅有下载接口时会返回。字段解释如下

**header部分**

| 字段名 | 类型 | 字段说明 |
| --- | --- | --- |
| code | int | 错误码，0表示正常，非0表示出错；详细释义可在接口说明文档最后的错误码说明了解 |
| message | string | 会话是否成功的描述信息 |
| sid | string | 会话的唯一id，用于反馈问题的日志索引字段，注意留存 |

**payload.text部分**

| 字段名 | 类型 | 字段说明 |
| --- | --- | --- |
| encoding | string | 响应的文本数据对应的编码 |
| compress | string | 响应的文本数据对应的压缩方式 |
| format | string | 响应的文本数据对应的格式 |
| text | string | 个性化资源数据，base64编码 |
