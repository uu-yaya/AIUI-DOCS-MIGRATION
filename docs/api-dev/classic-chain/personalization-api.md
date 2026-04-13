---
title: 用户个性化 API
---

::: info 概述
用户个性化API提供了针对用户特征和行为进行定制化处理的接口服务，支持个性化体验的构建与管理。
:::

## 服务介绍

本API服务是提供给客户在产品交互中需要针对用户个性化数据做上传管理时使用的。本协议接口仅适用于`传统语义交互链路`服务场景。

**调用示例Demo**：[HTTP Demo](https://gitee.com/zrmei/DemoCode/tree/master/webapi_v2_entity)

## 接口说明

温馨提示

1、本协议API仅适用于**传统语义交互链路**下个性化数据上传使用。

2、所有接口统一为**UTF-8编码**、协议支持 **http** 和 **https**。

3、调用本API协议需要注意在HTTP请求头中添加**鉴权参数**,详见下面说明。

**`公共鉴权参数`**:

> 调用本协议接口进行个性化数据操作时，需要在Http Request Header中加入以下参数作为授权验证

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| X-NameSpace | namespace，命名空间 | 是 |
| X-Nonce | 随机数（最大长度128个字符） | 是 |
| X-CurTime | 当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String) | 是 |
| X-CheckSum | MD5(accountKey + Nonce + CurTime),三个参数拼接的字符串，进行MD5哈希计算 | 是 |

### 注意：

CheckSum有效期：出于安全性考虑，每个CheckSum的有效期为5分钟(用curTime计算)，同时CurTime要与标准时间同步，否则，时间相差太大，服务端会直接认为CurTime无效。

\* checkSum生成示例：
```java
accountKey="abcd1234";
Nonce="12";
CurTime="1502607694";
CheckSum=MD5(accountKey+Nonce+CurTime);
//最终CheckSum输出为32位小写字符串 bf5aa1f53bd173cf7413bf370ad4bddc
```

**`必要参数获取说明`**

- AccountKey：账户级Key
- namespace：命名空间,代表用户唯一标识

AccountKey和namespace可在技能控制台查看相关值：

![](/media/202509/2025-09-09_104527_8216090.04970018551554978.png)

## 功能接口

### 3.1. 上传资源

接口地址

```http
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/upload-resource HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

#### 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | 是 | 应用id | 5axxx3cf |
| res\_name | String | 是 | 所需上传的资源名称，格式： namespace.动态实体资源名称 | OSxxxxxx.music |
| pers\_param | String | 是 | 个性化参数（json） | {"AppID":"xxxxxx"} |
| data | String | 是 | Base64编码的资源 | 参考下方说明示例 |

**`动态实体资源名称`参数获取示例说明：**

- 自定义动态实体资源名称获取方式
  ![](/media/202509/2025-09-09_143539_8005410.8519926582746234.png)
- 官方技能内置动态实体（详见文档说明）

  - 电话技能内置动态实体 IFLYTEK.telephone
  - 家居技能内置动态实体 IFLYTEK.smartH\_deviceAlias等

**`pers_param`参数为个性化参数维度指定，示例如下：**

| 维度 | 示例 | 说明 |
| --- | --- | --- |
| 应用级 | {"AppID":"xxxxxx"} | 取值传当前AIUI应用appid |
| 用户级 | {"auth\_id":"d3b6d50a9f8194b623b5e2d4e298c9d6"} 或 {"uid":"xxxxxx"} | 1、基于传统语义API交互用户，上传用户级使用相同auth\_id指定唯一用户ID（32位字符串，包括英文小写字母与数字，开发者需保证该值与终端用户一一对应） 2、基于传统语义SDK交互用户，可以直接通过指定通过SDK回调获取的uid进行上传 |
| 自定义级 | {"xxxxxx”:”xxxxxx"} | 自定义key和value，注意key不能和appid、auth\_id和uid 重复 |

data为web页面定义的主字段、从字段给的json格式对应的base64。按照上图示例：主字段为 name，从字段为 alias，上传资源的格式为：

```
{"name":"可乐","alias":"可口可乐|百事可乐"}
{"name":"维生素功能饮料","alias":"红牛|东鹏特饮|乐虎"}
```

### 注意：

每条数据之间用换行符隔开。

代码拼接时需要在第一行前边添加换行符

Base64编码为

```
eyJuYW1lIjoi5Y+v5LmQIiwiYWxpYXMiOiLlj6/lj6Plj6/kuZB855m+5LqL5Y+v5LmQIn0NCnsibmFtZSI6Iue7tOeUn+e0oOWKn+iDvemlruaWmSIsImFsaWFzIjoi57qi54mbfOS4nOm5j+eJuemlrnzkuZDomY4ifQ==
```

#### 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| sid | String | 是 | 本次上传sid，可用于查看上传资源是否成功 | psn003478f3@ch00070e3a78e06f2601 |
| csid | String | 是 | 本次服务唯一标识 | rwa84b7a73b@ch372d0e3a78e0116200 |

### 3.2. 查询资源打包

只有查询成功后，上传的资源才可以在交互中生效

> 上传资源后至少等5~10秒再查是否成功

接口地址

```
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/check-resource
    HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

#### 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 是 | sid | psn开头的sid |

#### 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| sid | String | 是 | 上传sid |
| csid | String | 是 | 上传sid |
| reply | String | 是 | 查看上传资源是否成功描述 |
| error | int | 是 | 查看上传资源是否成功错误码 |

### 3.2. 删除资源

本接口提供动态实体删除资源功能，用于动态删除实体资源。

接口地址

```http
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/delete-resource HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

#### 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| AppID | string | 是 | 应用id | 5adde3cf |
| res\_name | String | 是 | 资源名,XXX为用户的命名空间 | XXX.music |
| pers\_param | String | 是 | 个性化参数（json），资源生效维度名称和维度值 | {"AppID":"xxxxxx"} |

其中，pers\_param为个性化参数。示例如下：

| 维度 | 示例 | 说明 |
| --- | --- | --- |
| 应用级 | {"AppID":"xxxxxx"} |  |
| 用户级 | {"auth\_id": "d3b6d50a9f8194b623b5e2d4e298c9d6"} | auth\_id为用户唯一ID（32位字符串，包括英文小写字母与数字，开发者需保证该值与终端用户一一对应） |
| 自定义级 | {"xxxxxx":"xxxxxx"} |  |

#### 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| sid | String | 是 | 本次删除sid |
| csid | String | 是 | 本次服务唯一标识 |
| reply | String | 是 | 查看删除资源是否成功描述 |
| error | int | 是 | 查看删除资源是否成功错误码 |

## 其他特性说明

### 个性化资源生效使用

资源上传成功后5min生效。你可以通过webapi 请求，传`pers_param`参数验证是否已生效。[查看交互API文档]((/api-dev/classic-chain/interact-api)
