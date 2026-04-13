---
title: 应用后处理配置
---

应用后处理配置概述

该配置项，是AIUI服务链路提供开发者做云端结果接受处理的服务通道，不区分AIUI应用类型，配置方式都是一样的。其中包括：

**-配置说明：**

**-协议说明：**

## 配置说明

应用后处理提供能力开关项，操作能力配置时，AIUI平台会主动发起一次GET校验请求。
内容配置主要分4大块

- 云服务和备用地址填写
- 超时或出错尝试次数
- 服务请求超时时间限制
- 消息是否加密开关

![](/media/202512/2025-12-22_164334_0983570.46803998989003825.png "null")

### 1.1. 后处理链接

这里配置开发者自己的云服务地址，开发者可通过该地址在对话交互中接受服务转发结果，关于服务地址基础要求有：

- 支持公网访问
- 推荐域名方式配置
- 服务支持POST和GET请求【详见第2节协议配置说明】

### 1.2. 重试次数和超时时间

交互链路中AIUI做服务转发，可以配置异常重试次数。重试次数和超时时间之间有信息关联。
请求超时最大时长是依赖尝试次数来决定的，即 **最大时长 \* 尝试次数 ≤ 9000ms**

## 协议说明

AIUI 后处理能够根据识别、语义结果，提供个性化的服务。

### 2.1. 服务器验证-GET

1. 提交信息后，AIUI发送GET请求到开发者服务器URL，请求参数如下：

|  |  |
| --- | --- |
| **参数** | **描述** |
| signature | 加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、rand参数。 |
| timestamp | 时间戳 |
| rand | 随机数 |

2. 开发者校验signature（下面有校验方式），返回开放平台中token值的sha1加密内容，则接入成功。

**👤加密/校验流程**

- 将token、timestamp、rand三个参数值进行字典序排序

- 将三个参数字符串拼接成一个字符串进行sha1加密

- 开发者获得加密后的字符串可与signature对比，标识该请求来源于AIUI服务

**🔍响应消息：**

- 将token进行sha1加密，放在响应的body中返回

### 注意：

校验流程是可选操作，但消息返回必须正确才能校验成功

示例：

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

### 2.2. 接收消息-POST

AIUI正常完成服务后，把结果POST到开发者的URL上。
注意：

1. **消息重试**：每条消息最长超时时间为3秒，3秒后将会断开连接并重试1次，如果2次均无响应将返回超时消息。
2. **消息排重**：每条消息有一个id，请根据消息主体中的MsgId和CreateTime两者结合进行排重。（MsgId为字符串，CreateTime为整数）
3. **消息响应**：AIUI透传开发者数据到设备。
4. **消息签名**：用于检验AIUI消息的完整性，不用于校验开发者服务响应消息。签名是由token+timestamp+rand+postbody 进行字典排序，然后sha1生成的。
   url中的`msgsignature`参数存储了签名信息。timestamp和rand参数也在url里。

   |  |  |
   | --- | --- |
   | **参数** | **描述** |
   | token | 开发者设定的唯一标识 |
   | timestamp | 时间戳 |
   | srand | 固定字节随机串 |
   | postbody | post接收到的body信息 |

5. **消息加密**：开启加密后，会生成一个AES KEY，此时数据是加密的，且请求url中的`encrypttype`参数值为`aes`（未加密为`raw`）。解析消息前要解密。同时开发者服务器的响应也要用AES KEY加密。AIUI返给客户端的数据是解密的。
6. **消息格式**：
   HTTP消息格式定义：

   ```
   POST /yourserveruri?xx=xx HTTP 1.1
   Connection: close
   Host:xxx.xxx.xxx
   Content-Type: application/json
   Content-Length: 111
   {消息主体}
   ```

### 注意：

可以根据Content-Type的类型来解析相应的消息主体。例如：当POST请求的Content-Type为application/json时,要根据Json格式解析消息主体。

- 消息主体格式

```json
{
    "MsgId":"1234567",
    "CreateTime":1348831860,
    "AppID":"12345678",
    "UserId":"d123455",
    "SessionParams":"Y21kPXNzYixzdWI9aWF0LHBsYXRmb3JtPWFuZG9yaWQ=",
    "UserParams":"PG5hbWU+eGlhb2JpYW5iaWFuPC9uYW1lPg==",
    "FromSub":"IAT（语音识别）",
    "Msg":{},
}
```

- 格式说明

|  |  |
| --- | --- |
| **参数** | **描述** |
| MsgId | 消息id，字符串类型 |
| CreateTime | 消息创建时间，整型 |
| AppId | 开发者应用Id，字符串类型 |
| UserId | AIUI唯一用户标注，字符串类型 |
| UserParams | 开发者自定义参数，通过客户端的userparams参数上传，Base64格式字符串 |
| FromSub | 上游业务类型，目前包括两种（iat：听写结果，kc：语义结果），字符串类型 |
| Msg | 消息内容，json object参考Msg消息内容格式 |
| SessionParams | 本次会话交互参数，Base64格式字符串，解码后为json格式 |

- Msg消息内容格式

```text
文本内容
{
    "Type":"text",
    "ContentType":"Json",
    "Content":"eyJzbiI6MiwibHMiOnRydWUsImJnIjowLCJlZCI6MCwid3MiOlt7ImJnIjowLCJjdyI6W3sic2MiOjAsInciOiLvvJ8ifV19XX0="
}
```

|  |  |
| --- | --- |
| **参数** | **描述** |
| Type | text |
| ContentType | 内容格式 Json：JSON格式 plain：无格式文本 xml：XML格式 |
| Content | Base64内容字符串 |

### 2.3. 接入指引

#### 2.3.1. 消息校验使用方法

- 消息响应的url参数中有四个字符串类型参数，用于校验完整性

|  |  |  |
| --- | --- | --- |
| **参数** | **描述** | **来源** |
| msgsignature | 签名信息 | 存储消息的签名 |
| timestamp | 时间戳 | 由平台生成 |
| rand | 随机字符串 | 平台随机生成的随机串 |
| encrypttype | 加密类型 | 由页面配置决定（目前支持raw和aes） |

- 校验过程（伪代码）

```cpp
int message_sigcheck（token ，msgsignature ，timestamp ，srand ，data）
{
    //对参数进行字典排序
    vector<std::string> s(4);
    for (){ // 将参数token,timestamp,srand,data放入字典}
    //字典排序
    sort(s.begin(), s.end());
    //链接字符
    std::string str;
    for (){ // 将四个s里的值按顺序链接到str里}
    //对str进行sha1
    std::string signature = Sha1（str.c_str());
    //校验签名字符串 0为一致，-1为不一致
    return signature.compare(msgsignature)?-1:0;
}
```

### 注意：

为了消息的安全，建议校验。

#### 2.3.2. 消息加解密说明

![](/media/202212/2022-12-23_143529_6453900.0922315957714811.png "null")
勾选加密后，发给开发者服务器的body是加密的。需要用AES秘钥解密。

1. 加密采用AES的CBC加密方式，秘钥为16字节（128bit），初始化向量IV复用秘钥AESKEY，填充方式为PKCS7Padding。
2. 返回的消息要以同样的方式加密。
