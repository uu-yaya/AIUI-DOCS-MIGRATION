---
title: 技能后处理协议：请求校验
---

技能需要校验请求是否来源于 AIUI，所有发送给技能的请求Header都包含`Signature`字段

## 校验步骤

1. 从**AIUI开放平台 -> 技能工作室 -> 选择技能 -> 技能后处理 -> 使用Webhook**获取校验签名的公钥`public_key`
2. `Signature`是AIUI平台自动生成的，对`Signature`的值进行Base64-decode,得到`decoded_signature`
3. 使用SHA-1摘要算法（十六进制编码）对请求Body生成`hash`
4. 使用RSA算法, 使用公钥`public_key`对`decoded_signature`,`hash`进行校验，摘要类型为`sha256`

## 示例(Ruby)

假设用户从企业平台拿到的密钥为

```text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlN9BU3eBo9YbR/KaH42W
mgkE3j/Sm+WkXHDOeP5IDmehq0yTlWQtfUpoAj6T0/KIQgnhQm6MULXlRtvYIam4
W5I4gRSx1Yk4dpBTpJ8z6/QJG6DqywjuATfZgyEiEr9Nc6sjW2bXILHOLlCvMT+5
8aX9+QNB+WRqMSNkHN06Fa9aIfE7fbrjASlfZB4oYlr+ldTM1Q6pUOhLDJtZw906
VNqfgdZUPOBU7D9bYonBZrMCZN//YMr7jxSo9p6H4a0v9HNAvKPWFgPs7SmM/mC2
dWsF+A2TaA+znshWbmYPzNMphrBul+oDbYtOi6zP7Co00Xgg+ivNf3PdEhMuiJ6E
bQIDAQAB
-----END PUBLIC KEY-----
```

技能请求body为

```
"{\"message\":\"ok\"}"
```

Signature为

```
LG9565Z7KF92BKXWUdihbJ10oSelQg0YeR6QGYF4n4dd1QtP+2Gig8nWFkQaev06fJ2t30+Jh7ZmEdlZao
KJFEXxjXaG00mcVlc2VI0C7HJ/XXahBRcGt9guVrkDAfS0BEihN2hnsPev4QZ2WHVX/RLG+JnkA2j+eUKJ
nnMNIEjkgWJ8U17yWd9Etdn2Zj/8l/4TMqhvtG/5qB8ILkB7633agOj7z1ShD6eb9+blMYwx209pXPZomQ
6E8QA0vYw8AcK7BFbcw7ikU1Ii2LLKxDg6aYRg82nFGfNQZftNmb4AR60g55ZsFPo9aSfWYADDR1YczUI5
hPeLZkDoL9BaLw==
```

```cpp
public_key = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlN9BU3eBo9YbR/KaH42W     mgkE3j/Sm+WkXHDOeP5IDmehq0yTlWQtfUpoAj6T0/KIQgnhQm6MULXlRtvYIam4  W5I4gRSx1Yk4dpBTpJ8z6/QJG6DqywjuATfZgyEiEr9Nc6sjW2bXILHOLlCvMT+5  8aX9+QNB+WRqMSNkHN06Fa9aIfE7fbrjASlfZB4oYlr+ldTM1Q6pUOhLDJtZw906  VNqfgdZUPOBU7D9bYonBZrMCZN//YMr7jxSo9p6H4a0v9HNAvKPWFgPs7SmM/mC2  dWsF+A2TaA+znshWbmYPzNMphrBul+oDbYtOi6zP7Co00Xgg+ivNf3PdEhMuiJ6E              bQIDAQAB                                                                                     -----END PUBLIC KEY-----  "

body = "{\"message\":\"ok\"}"
hash = OpenSSL::Digest.hexdigest("SHA1", body)

signature = "LG9565Z7KF92BKXWUdihbJ10oSelQg0YeR6QGYF4n4dd1QtP+2Gig8nWFkQaev06fJ2t30   +Jh7ZmEdlZaoKJFEXxjXaG00mcVlc2VI0C7HJ/XXahBRcGt9guVrkDAfS0BEihN2hnsPev4QZ2WHVX/RLG+   JnkA2j+eUKJnnMNIEjkgWJ8U17yWd9Etdn2Zj/8l/4TMqhvtG/5qB8ILkB7633agOj7z1ShD6eb9+blMYwx   209pXPZomQ6E8QA0vYw8AcK7BFbcw7ikU1Ii2LLKxDg6aYRg82nFGfNQZftNmb4AR60g55ZsFPo9aSfWYAD   DR1YczUI5hPeLZkDoL9BaLw=="
decoded_signature = Base64.decode64(signature)

pub_key = OpenSSL::PKey::RSA.new(public_key)
pub_key.verify("SHA256", decoded_signature, hash) # => true
```
