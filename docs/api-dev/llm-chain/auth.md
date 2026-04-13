---
title: 服务鉴权
---

::: info 概述
服务鉴权文档详细介绍了平台接口的安全验证机制，包括鉴权流程和所需参数说明，确保接口访问的安全性与合法性。
:::

## 服务鉴权文档

请求方对请求进行签名，服务端校验签名合法性。

- ws[s]：请求类型固定为GET请求
- http[s]：请求类型根据实际类型传值，常见有POST、DELETE、GET、PUT等

## 鉴权说明

鉴权方式：请求地址后面添加鉴权参数，例：

示例如下：

- ws请求：

```text
ws://当前请求的url?authorization=XXX&host=XXX&date=XXX
```

- http请求：

```text
http://当前请求的url?authorization=XXX&host=XXX&date=XXX
```

## 鉴权参数

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| host | string | 是 | 请求地址的域名 | demo.example.com |
| date | string | 是 | 当前时间戳，RFC1123格式(Wed, 10 Jul 2019 07:35:43 GMT) | Wed, 23 Aug 2023 06:45:26 GMT |
| authorization | string | 是 | 使用base64编码的签名相关信息（签名基于hmac-sha256计算） | 参考下方 **authorization** 参数生成规则说明 |

## 3.1. authorization参数生成

authorization由四个⼦参数拼接而成：API\_key，algorithm，headers 和 signature。拼接格式及对应参数说明如下：

```ini
api_key="$api_key",algorithm="hmac-sha256",headers="host date request-line",signature="$signature"
```

| 参数 | 类型 | 是否必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| API\_key | string | 是 | AIUI应用信息中的APPKEY取值 | 726812ec4b28bfa901ef569fdc83ee35 |
| algorithm | string | 是 | 加密方式名称 | 固定取值：hmac-sha256 |
| headers | string | 是 | 由 host、date、request-line三个字符串加空格拼接组成 | 固定取值：host date request-line |
| signature | string | 是 | 由header、APISecret参数进行hmac-sha256加密，然后进行base64后得到 | 具体参考下方 **header、signature** 参数生成示例 |

### 3.1.1. header 生成：

**header** 参数拼接格式如下：

```
    host: $host\ndate: $date\n$request-line
```

温馨提示

1. "\n"为换⾏符，不可省略

2. ":"后⾯有⼀个空格，不可省略

| 参数 | 类型 | 是否必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| host | string | 是 | 请求地址的域名，复用鉴权参数取值 | demo.example.com |
| date | string | 是 | 当前时间戳，复用鉴权参数取值 | Wed, 23 Aug 2023 06:45:26 GMT |
| request-line | string | 是 | 由 请求类型{method}、请求路径{url.path)、固定字符串“HTTP/1.1”三部分组成，中间用空格隔开 | GET /API HTTP/1.1 |

- **ws协议** host、date、request-line 参数拼接如下：

  ```
    host: {url.host}
    date: Wed, 23 Aug 2023 06:45:26 GMT
    GET {url.path} HTTP/1.1
  ```
- **http协议** host、date、request-line 参数拼接如下：

  ```
    host: {url.host}
    date: Wed, 23 Aug 2023 06:45:26 GMT
    {method} {url.path} HTTP/1.1
  ```

**举例说明**：

- 当请求 url： ws[s]://demo.example.com/api 时（说明：ws请求固定为GET类型）， 构建 header 为：

  ```
    header="host: demo.example.com\ndate: Wed, 23 Aug 2023 06:45:26 GMT\nGET /api HTTP/1.1"
  ```
- 当请求 url：`http[s]://demo.example.com/api，请求类型为` DELETE ， 构建 header 为：

  ```
    header="host: demo.example.com\ndate: Wed, 23 Aug 2023 06:45:26 GMT\nDELETE /api HTTP/1.1"
  ```

### 3.1.2. signature 生成：

1. AIUI平台应用信息中获取apiSecret参数
2. hmac-sha256算法对header、apiSecret签名

   ```
    signature_sha=hmac-sha256(header, $apiSecret)
   ```
3. signature\_sha进行base64编码

   ```
    signature=base64(signature_sha)
   ```

## 3.2. 代码示例(java)

```java
    // 应用密钥信息
String apiKey = "xxx";
String APISecret = "xxx";

    // url.host 取值
String host = "demo.example.com";
    // url.path 取值
String path = "/API";
    // ws请求固定：GET， http请求，按实际类型填写（POST、GET、DELETE、PUT……）
String method = "GET";

    // date 取值
SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z",Locale.US);
df.setTimeZone(TimeZone.getTimeZone("GMT"));
String date = df.format(new Date());
    /**
     * header 取值
     * 注意冒号后面有一个空格
     */
String header = "host: " + host + "\n" +
                 "date: " + date + "\n" +
                 method + " " + path + "  HTTP/1.1";

    // signature 取值
String signature =  new String(Base64.encodeBase64(getHmacSha256(header,APISecret)));
    /**
     * 拼接 authorization
     * api_key="$api_key",algorithm="hmac-sha256",headers="host date request-line",signature="$signature"
     */
String algorithm = "hmac-sha256";
String headers = "host date request-line";
String authorization_origin = String.format("api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"", apiKey, algorithm, headers, signature);
String authorization = new String(Base64.encodeBase64(authorization_origin.getBytes("UTF-8")));

public static byte[] getHmacSha256(String data,String key){
    try {
        Mac mac = Mac.getInstance("HmacSHA256");
        byte[] keyBytes = key.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, "HmacSHA256");
        mac.init(secretKey);
        byte[] hmacBytes = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
        return hmacBytes;
    } catch (Exception e) {
        e.printStackTrace();
    }
    return null;
}
```
