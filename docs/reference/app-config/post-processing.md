---
title: 应用后处理配置
description: AIUI 应用后处理服务通道的配置说明和协议规范，包括服务器验证、消息接收和加解密。
---

## 概述

应用后处理是 AIUI 服务链路提供的云端结果接收处理服务通道，不区分 AIUI 应用类型，配置方式统一。

## 配置说明

应用后处理提供能力开关项，操作配置时 AIUI 平台会主动发起一次 GET 校验请求。

配置内容主要包括：

| 配置项 | 说明 |
| --- | --- |
| 云服务和备用地址 | 开发者自定义的云服务地址 |
| 超时或出错尝试次数 | 异常重试次数 |
| 服务请求超时时间限制 | 最大时长 × 尝试次数 ≤ 9000ms |
| 消息加密开关 | 是否启用 AES 加密 |


### 后处理链接

配置开发者自定义的云服务地址，基础要求：

- 支持公网访问
- 推荐域名方式配置
- 服务支持 POST 和 GET 请求

### 重试次数和超时时间

交互链路中 AIUI 做服务转发时可配置异常重试次数。重试次数和超时时间之间存在关联：

**最大时长 × 尝试次数 ≤ 9000ms**

## 协议说明

AIUI 后处理能够根据识别、语义结果提供个性化的服务。

### 服务器验证（GET）

提交信息后，AIUI 发送 GET 请求到开发者服务器 URL，请求参数：

| 参数 | 描述 |
| --- | --- |
| signature | 加密签名，结合 Token、timestamp、rand 参数生成 |
| timestamp | 时间戳 |
| rand | 随机数 |

开发者校验 signature 后，返回 Token 值的 SHA1 加密内容即接入成功。

**加密/校验流程：**

1. 将 Token、timestamp、rand 三个参数值进行字典序排序
2. 将三个参数字符串拼接后进行 SHA1 加密
3. 开发者获得加密后的字符串与 signature 对比，验证请求来源于 AIUI 服务

**响应消息：**

将 Token 进行 SHA1 加密，放在响应的 Body 中返回。

::: info 说明
校验流程是可选操作，但消息返回必须正确才能校验成功。
:::

示例代码：

```java
Map<String, String[]> parameterMap = request.getParameterMap();
String rand = parameterMap.get("rand")[0];
String timestamp = parameterMap.get("timestamp")[0];
String signature = parameterMap.get("signature")[0];
// 字典序排序
ArrayList<String> signList = new ArrayList<>();
signList.add(aiuiToken);
signList.add(rand);
signList.add(timestamp);
Collections.sort(signList);
// 校验
String sign = StringUtils
    .strip(signList.toString(), "[]")
    .replace(" ", "")
    .replace(",", "");
if (StringUtils.compare(signature, DigestUtils.sha1Hex(sign)) != 0) {
    return "authentication failed";
} else {
    return DigestUtils.sha1Hex(aiuiToken);
}
```

### 接收消息（POST）

AIUI 正常完成服务后，将结果 POST 到开发者的 URL 上。

**注意事项：**

| 项目 | 说明 |
| --- | --- |
| 消息重试 | 每条消息最长超时 3 秒，超时后断开并重试 1 次，2 次均无响应返回超时消息 |
| 消息排重 | 根据消息主体中的 `MsgId` 和 `CreateTime` 结合进行排重 |
| 消息响应 | AIUI 透传开发者数据到设备 |
| 消息签名 | 由 Token + timestamp + rand + PostBody 字典排序后 SHA1 生成 |
| 消息加密 | 开启后数据使用 AES 加密，URL 中 `encrypttype` 参数值为 `aes` |

**消息签名参数：**

| 参数 | 描述 |
| --- | --- |
| token | 开发者设定的唯一标识 |
| timestamp | 时间戳 |
| srand | 固定字节随机串 |
| postbody | POST 接收到的 Body 信息 |

URL 中的 `msgsignature` 参数存储签名信息，`timestamp` 和 `rand` 参数也在 URL 中。

**HTTP 消息格式：**

```text
POST /yourserveruri?xx=xx HTTP 1.1
Connection: close
Host:xxx.xxx.xxx
Content-Type: application/json
Content-Length: 111
{消息主体}
```

::: info 说明
根据 `Content-Type` 类型解析消息主体。例如 `application/json` 时按 JSON 格式解析。
:::

**消息主体格式：**

```json
{
  "MsgId": "1234567",
  "CreateTime": 1348831860,
  "AppID": "12345678",
  "UserId": "d123455",
  "SessionParams": "Y21kPXNzYixzdWI9aWF0LHBsYXRmb3JtPWFuZG9yaWQ=",
  "UserParams": "PG5hbWU+eGlhb2JpYW5iaWFuPC9uYW1lPg==",
  "FromSub": "iat",
  "Msg": {}
}
```

**字段说明：**

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| MsgId | string | 消息 ID |
| CreateTime | int | 消息创建时间 |
| AppId | string | 开发者应用 ID |
| UserId | string | AIUI 唯一用户标识 |
| UserParams | string | 开发者自定义参数，通过客户端 `userparams` 上传，Base64 格式 |
| FromSub | string | 上游业务类型：`iat`（听写结果）、`kc`（语义结果） |
| Msg | object | 消息内容，参考 Msg 消息内容格式 |
| SessionParams | string | 本次会话交互参数，Base64 格式，解码后为 JSON |

**Msg 消息内容格式：**

```json
{
  "Type": "text",
  "ContentType": "Json",
  "Content": "eyJzbiI6MiwibHMiOnRydWUsImJnIjowLCJlZCI6MCwid3MiOlt7ImJnIjowLCJjdyI6W3sic2MiOjAsInciOiLvvJ8ifV19XX0="
}
```

| 参数 | 描述 |
| --- | --- |
| Type | 固定值 `text` |
| ContentType | 内容格式：`Json`（JSON 格式）、`plain`（无格式文本）、`xml`（XML 格式） |
| Content | Base64 编码的内容字符串 |

### 接入指引

#### 消息校验使用方法

消息响应 URL 参数中有四个字符串类型参数，用于校验完整性：

| 参数 | 描述 | 来源 |
| --- | --- | --- |
| msgsignature | 签名信息 | 存储消息的签名 |
| timestamp | 时间戳 | 由平台生成 |
| rand | 随机字符串 | 平台随机生成 |
| encrypttype | 加密类型 | 由页面配置决定（支持 `raw` 和 `aes`） |

校验过程（伪代码）：

```cpp
int message_sigcheck(token, msgsignature, timestamp, srand, data)
{
    // 对参数进行字典排序
    vector<std::string> s(4);
    for () { // 将参数 token, timestamp, srand, data 放入字典 }
    // 字典排序
    sort(s.begin(), s.end());
    // 拼接字符
    std::string str;
    for () { // 将四个值按顺序拼接到 str }
    // 对 str 进行 SHA1
    std::string signature = Sha1(str.c_str());
    // 校验签名字符串：0 为一致，-1 为不一致
    return signature.compare(msgsignature) ? -1 : 0;
}
```

::: tip 建议
为了消息的安全，建议进行签名校验。
:::

#### 消息加解密说明

勾选加密后，发给开发者服务器的 Body 是加密的，需用 AES 密钥解密。

1. 加密采用 AES 的 CBC 加密方式，密钥为 16 字节（128bit），初始化向量 IV 复用密钥 AES Key，填充方式为 PKCS7Padding。
2. 开发者服务器的响应也需以同样方式加密。AIUI 返回给客户端的数据是解密后的明文。
