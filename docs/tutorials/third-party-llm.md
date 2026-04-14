---
title: 三方大模型配置教程
description: 在 AIUI 应用中接入第三方大模型作为回复模型
---

## 前置条件

- 已创建 AIUI 应用（参考 [创建应用教程](/tutorials/create-app)）
- 已在第三方大模型平台注册账号并完成实名认证
- 第三方大模型服务需兼容 **OpenAI API 协议**

## 你将完成的目标

通过本教程，你将学会：

1. 在第三方平台获取 API 接入信息
2. 在 AIUI 应用中配置三方大模型
3. 测试验证配置是否生效

本教程以阿里云通义千问为例，其他兼容 OpenAI API 协议的大模型（如 DeepSeek、智谱 GLM 等）流程类似。

## 第一步：获取第三方平台信息

以通义千问为例，需要获取三项信息：

### 1. 注册并认证

1. [注册阿里云账号](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api)
2. 完成 [实名认证](https://myaccount.console.aliyun.com/cert-info)

### 2. 开通模型服务

进入 [阿里云百炼](https://bailian.console.aliyun.com/) 控制台，点击「立即开通」。

### 3. 获取 API Key

在 [API-KEY 管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并复制 API Key。

### 4. 获取 API 接入 URL

在官方 [API 接入文档](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api) 中获取接入地址，例如：

```text
https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
```

### 需要记录的信息

| 信息 | 说明 | 示例 |
|------|------|------|
| 接口地址 | 兼容 OpenAI 的 Chat Completions 端点 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` |
| API Key | 平台生成的鉴权密钥 | `sk-xxxxxxxxxxxxxxxx` |
| 模型标识 | 要使用的模型名称 | `qwen-plus` |

## 第二步：配置 AIUI 应用

1. 登录 [AIUI 平台](https://aiui.xfyun.cn/)，进入应用配置页面
2. 在 **模型选择** 区域，选择「三方大模型」
3. 点击 **模型配置**

## 第三步：填写配置信息

在模型配置页面中填写以下内容：

| 配置项 | 填写内容 |
|--------|---------|
| 接口地址 | 第三方平台的 API URL |
| 鉴权信息 | 第三方平台的 API Key |
| 模型标识 | 第三方平台的模型 domain 标识 |

::: tip 模型标识
不同平台的模型标识名称不同，可在对应平台的模型广场查找。例如通义千问可在 [百炼模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market) 查看可用模型。
:::

## 第四步：测试验证

配置完成后，在配置页面的测试窗口中输入一个问题。如果收到正常回复，说明三方大模型配置成功。

::: warning 常见问题
- **无响应**：检查接口地址是否正确，是否加了 `/chat/completions` 路径
- **鉴权失败**：检查 API Key 是否正确，是否已过期
- **模型不存在**：检查模型标识是否与平台提供的名称一致
:::

## 下一步

- [创建应用教程](/tutorials/create-app) — 了解应用创建和基础配置
- [API 接入教程](/tutorials/api-integration) — 通过 WebSocket API 接入 AIUI
- [自定义技能开发](/tutorials/custom-skill) — 为应用添加自定义技能
