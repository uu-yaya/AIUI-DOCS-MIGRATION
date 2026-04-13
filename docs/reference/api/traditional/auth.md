---
title: 传统语义链路鉴权
description: AIUI 传统语义链路 API 的 MD5/SHA256 签名鉴权机制
---

## 概述

传统语义链路使用基于 `checksum` 的鉴权方式，与大模型链路和极速超拟人链路的 HMAC-SHA256 鉴权方式不同。

## 鉴权方式

鉴权参数通过 WebSocket 握手 URL 的查询字符串传递：

```text
ws[s]://wsapi.xfyun.cn/v1/aiui?appid=XXX&checksum=XXX&param=XXX&curtime=XXX&signtype=md5
```

## 鉴权参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|---|---|---|---|---|
| appid | string | 是 | AIUI 应用 AppID | `a44e0f36` |
| curtime | string | 是 | 当前 UTC 时间戳（秒级） | `1693456789` |
| signtype | string | 否 | 签名类型：`md5`（默认）或 `sha256` | `md5` |
| checksum | string | 是 | 签名校验值 | 参见下方生成规则 |
| param | string | 是 | Base64 编码的业务参数 JSON | 参见下方说明 |

## checksum 生成规则

```text
checksum = MD5(apikey + curtime + param)
```

或使用 SHA256：

```text
checksum = SHA256(apikey + curtime + param)
```

其中：
- `apikey`：AIUI 应用信息中的 APIKey
- `curtime`：当前 UTC 时间戳（秒级字符串）
- `param`：Base64 编码后的业务参数 JSON 字符串

> checksum 有效期为 5 分钟，建议每次请求时实时计算。

## param 参数

`param` 是 Base64 编码的 JSON 字符串，包含业务配置参数：

```json
{
    "auth_id": "d3b6d50a9f8194b623b5e2d4e298c9d6",
    "data_type": "audio",
    "aue": "raw",
    "sample_rate": "16000",
    "scene": "main_box",
    "result_level": "plain",
    "close_delay": "200",
    "context": "{\"sdk_support\":[\"iat\",\"nlp\",\"tts\"]}"
}
```

param 内各字段的详细说明请参考 [交互 API](./interaction.md)。

## 代码示例（Python）

```python
import hashlib
import base64
import time
import json

appid = "your_appid"
api_key = "your_apikey"

# 业务参数
param = {
    "auth_id": "d3b6d50a9f8194b623b5e2d4e298c9d6",
    "data_type": "text",
    "scene": "main_box",
    "result_level": "plain"
}

# Base64 编码 param
param_base64 = base64.b64encode(json.dumps(param).encode("utf-8")).decode("utf-8")

# 当前时间戳
cur_time = str(int(time.time()))

# 计算 checksum（MD5）
checksum_origin = api_key + cur_time + param_base64
checksum = hashlib.md5(checksum_origin.encode("utf-8")).hexdigest()

# 拼接 WebSocket URL
url = f"ws://wsapi.xfyun.cn/v1/aiui?appid={appid}&checksum={checksum}&param={param_base64}&curtime={cur_time}&signtype=md5"
```

## cURL 等效调用示例

```bash
APPID="your_appid"
API_KEY="your_apikey"
CURTIME=$(date +%s)

# 业务参数 Base64 编码
PARAM=$(echo -n '{"auth_id":"test","data_type":"text","scene":"main_box","result_level":"plain"}' | base64)

# 计算 checksum
CHECKSUM=$(echo -n "${API_KEY}${CURTIME}${PARAM}" | md5sum | awk '{print $1}')

# 建立 WebSocket 连接
wscat -c "ws://wsapi.xfyun.cn/v1/aiui?appid=${APPID}&checksum=${CHECKSUM}&param=${PARAM}&curtime=${CURTIME}&signtype=md5"
```
