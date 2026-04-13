---
title: WebSocket API 接入教程
description: 通过 WebSocket API 接入 AIUI 服务，实现语音和文本交互
---

## 前置条件

- 已创建 AIUI 应用并获取 AppID、APIKey、APISecret（参考 [创建应用教程](/tutorials/create-app)）
- 熟悉 WebSocket 协议基础
- 具备 HTTP 签名鉴权的基本知识

## 你将完成的目标

通过本教程，你将学会：

1. 生成 AIUI API 鉴权签名
2. 建立 WebSocket 连接
3. 发送文本和语音数据进行交互
4. 解析返回的语义结果

## 接口概述

AIUI WebSocket API 支持在线语音交互能力，交互流程分三个阶段：

1. **建立连接** — 通过鉴权参数握手
2. **交互请求** — 发送文本或语音数据
3. **断开连接** — 结束会话

请求地址：

```text
wss://aiui.xf-yun.com/v2/aiint/ws
```

::: warning 超时断开
单次会话超过 60 秒未发送数据，云端将主动断开连接。
:::

## 第一步：鉴权签名

连接时需要在 URL 中携带鉴权参数。

### 鉴权参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `host` | 请求域名 | `aiui.xf-yun.com` |
| `date` | RFC1123 格式时间戳 | `Wed, 23 Aug 2023 06:45:26 GMT` |
| `authorization` | Base64 编码的签名信息 | 见下方生成规则 |

### 生成 authorization

`authorization` 由四个子参数拼接而成：

```text
api_key="$api_key",algorithm="hmac-sha256",headers="host date request-line",signature="$signature"
```

#### 生成 signature

1. 构建签名原文（header）：

```text
host: aiui.xf-yun.com
date: Wed, 23 Aug 2023 06:45:26 GMT
GET /v2/aiint/ws HTTP/1.1
```

::: tip 格式要求
- 冒号后有一个空格
- 行之间使用 `\n` 换行符
:::

2. 使用 APISecret 对 header 进行 HMAC-SHA256 签名，再 Base64 编码：

```text
signature = base64(hmac-sha256(header, apiSecret))
```

3. 拼接完整 authorization 后 Base64 编码。

### Java 代码示例

```java
String apiKey = "你的 APIKey";
String apiSecret = "你的 APISecret";
String host = "aiui.xf-yun.com";
String path = "/v2/aiint/ws";

// 生成 date
SimpleDateFormat df = new SimpleDateFormat(
    "EEE, dd MMM yyyy HH:mm:ss z", Locale.US
);
df.setTimeZone(TimeZone.getTimeZone("GMT"));
String date = df.format(new Date());

// 构建 header 签名原文
String header = "host: " + host + "\n"
    + "date: " + date + "\n"
    + "GET " + path + " HTTP/1.1";

// 计算 signature
byte[] hmac = hmacSha256(header, apiSecret);
String signature = Base64.getEncoder().encodeToString(hmac);

// 拼接 authorization
String authOrigin = String.format(
    "api_key=\"%s\", algorithm=\"hmac-sha256\", "
    + "headers=\"host date request-line\", signature=\"%s\"",
    apiKey, signature
);
String authorization = Base64.getEncoder()
    .encodeToString(authOrigin.getBytes("UTF-8"));

// 最终连接 URL
String url = String.format(
    "wss://%s%s?host=%s&date=%s&authorization=%s",
    host, path,
    URLEncoder.encode(host, "UTF-8"),
    URLEncoder.encode(date, "UTF-8"),
    URLEncoder.encode(authorization, "UTF-8")
);
```

HMAC-SHA256 工具方法：

```java
public static byte[] hmacSha256(String data, String key) {
    try {
        Mac mac = Mac.getInstance("HmacSHA256");
        SecretKeySpec secretKey = new SecretKeySpec(
            key.getBytes(StandardCharsets.UTF_8), "HmacSHA256"
        );
        mac.init(secretKey);
        return mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}
```

## 第二步：发送交互请求

连接建立后，通过 WebSocket 发送 JSON 格式的请求数据。

### 文本交互示例

```json
{
  "header": {
    "appid": "你的 AppID",
    "sn": "device-001",
    "stmid": "text-1",
    "status": 3,
    "scene": "main_box"
  },
  "parameter": {
    "nlp": {
      "nlp": {
        "compress": "raw",
        "format": "json",
        "encoding": "utf8"
      },
      "new_session": true
    }
  },
  "payload": {
    "text": {
      "compress": "raw",
      "format": "plain",
      "text": "5L2g5aW95ZWK",
      "encoding": "utf8",
      "status": 3
    }
  }
}
```

::: tip 文本编码
`payload.text.text` 字段的值需要使用 Base64 编码。例如「你好啊」编码后为 `5L2g5aW95ZWK`。
:::

### 关键参数说明

| 参数 | 说明 |
|------|------|
| `header.appid` | AIUI 应用的 AppID |
| `header.sn` | 设备/用户唯一标识，不超过 32 位 |
| `header.stmid` | 会话请求 ID，每次请求需更新 |
| `header.status` | 数据帧状态：0-首帧、1-中间帧、2-尾帧、3-一帧发完 |
| `header.scene` | 场景名称：`main_box`（测试）或 `main`（线上） |
| `parameter.nlp` | 语义参数设置 |
| `parameter.iat` | 语音识别参数（语音输入时使用） |
| `parameter.tts` | 语音合成参数 |

### 语音交互

语音交互时，将音频数据分帧发送：

1. **首帧**（status=0）：携带 header + parameter + 音频数据
2. **中间帧**（status=1）：携带音频数据
3. **尾帧**（status=2）：携带最后一帧音频数据

## 第三步：解析返回结果

AIUI 通过 WebSocket 返回 JSON 格式的结果，包含语音识别、语义理解和语音合成等数据。根据返回数据中的 `sub` 字段区分结果类型：

| sub 值 | 说明 |
|--------|------|
| `iat` | 语音识别结果 |
| `nlp` | 语义理解结果 |
| `tts` | 语音合成结果 |

## 更多资源

- [WebSocket Demo（Gitee）](https://gitee.com/iflytek-aiui/AIUILiteDemo) — 完整的 WebSocket 接入示例代码
- [服务鉴权详情](/api-dev/llm-chain/auth) — 鉴权参数生成的完整说明
- [交互 API 详情](/api-dev/llm-chain/interact-api) — 完整的请求和响应协议说明

## 下一步

- [Android SDK 集成](/tutorials/sdk-android) — 使用 SDK 方式接入（更简单）
- [三方大模型配置](/tutorials/third-party-llm) — 接入第三方大模型
- [声音复刻教程](/tutorials/voice-clone) — 使用声音复刻功能
