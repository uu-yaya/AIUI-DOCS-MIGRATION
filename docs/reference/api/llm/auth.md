---
title: 通用大模型链路鉴权
description: AIUI 通用大模型链路 API 的 HMAC-SHA256 签名鉴权机制
---

## 概述

请求方对请求进行签名，服务端校验签名合法性。

- **WebSocket 请求**：固定为 GET 方式
- **HTTP 请求**：根据实际类型传值（POST、DELETE、GET、PUT 等）

## 鉴权方式

在请求地址后附加鉴权参数：

```text
# WebSocket 请求
ws://当前请求的url?authorization=XXX&host=XXX&date=XXX

# HTTP 请求
http://当前请求的url?authorization=XXX&host=XXX&date=XXX
```

## 鉴权参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| host | string | 是 | 请求地址的域名 | `aiui.xf-yun.com` |
| date | string | 是 | 当前时间戳，RFC 1123 格式 | `Wed, 23 Aug 2023 06:45:26 GMT` |
| authorization | string | 是 | Base64 编码的签名信息（基于 HMAC-SHA256 计算） | 参见下方生成规则 |

> 鉴权时间戳有时效性，建议每次请求时实时获取最新时间戳。

## authorization 参数生成

`authorization` 由四个子参数拼接而成：

```text
api_key="$api_key",algorithm="hmac-sha256",headers="host date request-line",signature="$signature"
```

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| api_key | string | 是 | AIUI 应用信息中的 APIKey | `726812ec4b28bfa901ef569fdc83ee35` |
| algorithm | string | 是 | 加密方式 | 固定值：`hmac-sha256` |
| headers | string | 是 | 签名头字段列表 | 固定值：`host date request-line` |
| signature | string | 是 | 由 header 签名原文和 APISecret 进行 HMAC-SHA256 加密后 Base64 编码 | 参见下方生成步骤 |

### 第一步：生成 header 签名原文

```text
host: $host\ndate: $date\n$request-line
```

> `\n` 为换行符，不可省略；冒号后面有一个空格，不可省略。

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| host | string | 是 | 请求地址域名 | `aiui.xf-yun.com` |
| date | string | 是 | 当前时间戳（复用鉴权参数） | `Wed, 23 Aug 2023 06:45:26 GMT` |
| request-line | string | 是 | 由 `{method} {url.path} HTTP/1.1` 组成 | `GET /v2/aiint/ws HTTP/1.1` |

#### WebSocket 请求示例

```text
host: aiui.xf-yun.com
date: Wed, 23 Aug 2023 06:45:26 GMT
GET /v2/aiint/ws HTTP/1.1
```

#### HTTP 请求示例

```text
host: aiui.xf-yun.com
date: Wed, 23 Aug 2023 06:45:26 GMT
POST /v2/aiint/voice-clone/sgen/reg HTTP/1.1
```

### 第二步：生成 signature

1. 从 AIUI 平台应用信息中获取 APISecret
2. 使用 HMAC-SHA256 算法对 header 签名原文和 APISecret 签名：
   ```text
   signature_sha = hmac-sha256(header, $apiSecret)
   ```
3. 对签名结果进行 Base64 编码：
   ```text
   signature = base64(signature_sha)
   ```

## 代码示例（Java）

```java
// 应用密钥信息
String apiKey = "xxx";
String apiSecret = "xxx";

// url.host 取值
String host = "aiui.xf-yun.com";
// url.path 取值
String path = "/v2/aiint/ws";
// WebSocket 请求固定 GET，HTTP 请求按实际类型填写
String method = "GET";

// date 取值（RFC 1123 格式）
SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z", Locale.US);
df.setTimeZone(TimeZone.getTimeZone("GMT"));
String date = df.format(new Date());

// 构建 header 签名原文
String header = "host: " + host + "\n"
              + "date: " + date + "\n"
              + method + " " + path + " HTTP/1.1";

// 生成 signature
String signature = new String(Base64.encodeBase64(getHmacSha256(header, apiSecret)));

// 拼接 authorization
String algorithm = "hmac-sha256";
String headers = "host date request-line";
String authorizationOrigin = String.format(
    "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"",
    apiKey, algorithm, headers, signature);
String authorization = new String(Base64.encodeBase64(authorizationOrigin.getBytes("UTF-8")));

// HMAC-SHA256 工具方法
public static byte[] getHmacSha256(String data, String key) {
    try {
        Mac mac = Mac.getInstance("HmacSHA256");
        byte[] keyBytes = key.getBytes(StandardCharsets.UTF_8);
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, "HmacSHA256");
        mac.init(secretKey);
        return mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
    } catch (Exception e) {
        e.printStackTrace();
    }
    return null;
}
```

## cURL 等效调用示例

```bash
HOST="aiui.xf-yun.com"
DATE=$(date -u +"%a, %d %b %Y %H:%M:%S GMT")
PATH_URL="/v2/aiint/ws"

# 构建签名原文
SIGN_ORIGIN="host: ${HOST}\ndate: ${DATE}\nGET ${PATH_URL} HTTP/1.1"

# HMAC-SHA256 签名 + Base64
SIGNATURE=$(echo -ne "$SIGN_ORIGIN" | openssl dgst -sha256 -hmac "$API_SECRET" -binary | base64)

# 拼接 authorization 并 Base64 编码
AUTH_ORIGIN="api_key=\"${API_KEY}\", algorithm=\"hmac-sha256\", headers=\"host date request-line\", signature=\"${SIGNATURE}\""
AUTHORIZATION=$(echo -n "$AUTH_ORIGIN" | base64)

# 发起 WebSocket 连接
wscat -c "wss://${HOST}${PATH_URL}?host=${HOST}&date=$(python3 -c 'import urllib.parse; print(urllib.parse.quote("'"$DATE"'"))')&authorization=${AUTHORIZATION}"
```
