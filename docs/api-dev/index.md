---
title: AIUI API 开发
---

::: info 概述
AIUI API 是讯飞开放平台为开发者提供的一组 WebSocket / HTTP 云端接口。开发者无需集成 SDK，即可在服务器端、Web、IoT 设备等任意环境中直接调用讯飞云端的语音识别、语义理解、大模型对话、语音合成等 AI 能力，实现灵活的人机语音交互。
:::

## 什么是 AIUI API

AIUI API 是 **讯飞开放平台** 对外发布的一套标准化云端接口协议，通过 WebSocket 长连接或 HTTP 请求向讯飞云端发送音频/文本请求，云端返回识别结果、语义理解结果、合成音频等。

- **面向人群**：服务端开发者、跨语言/跨平台开发者、Web 应用、IoT 设备固件开发者
- **部署形态**：无需在本地集成任何客户端库，任何能发起 WebSocket/HTTP 请求的环境均可使用
- **鉴权方式**：使用 AppID + APIKey + APISecret 计算签名，云端校验通过后建立连接

## API 与 SDK 的区别

| 维度 | API | SDK |
|------|-----|-----|
| 集成方式 | 直接发 HTTP/WebSocket 请求 | 在应用中集成讯飞提供的客户端库 |
| 适用平台 | 任意（服务端、Web、嵌入式） | Android / iOS / Windows / Linux |
| 开发语言 | 任意（Python、Node.js、Java、Go 等） | 依 SDK 平台（Java / Swift / C++ 等） |
| 依赖 | 仅需网络 + 签名计算 | 需要集成 SDK 库与资源文件 |
| 典型场景 | 服务端中转、Web 应用、跨平台工具 | 移动 App、嵌入式硬件、本地离线能力 |

## 三大交互链路

AIUI 提供三条不同能力特性的接入链路，开发者可以根据场景自由选择：

## 传统语义链路

基于传统语义理解的交互链路，成熟稳定，适合指令明确、领域固定的场景。

<div class="nav-cards">

- **[交互 API](/api-dev/classic-chain/interact-api)** — 传统语义交互核心接口，支持语音识别、语义理解和结果返回的完整链路调用。
- **[用户个性化 API](/api-dev/classic-chain/personalization-api)** — 支持用户信息管理、个性化配置和历史交互数据查询，实现个性化语义理解。
- **[合成能力使用](/api-dev/classic-chain/tts-usage)** — 介绍传统语义交互链路下使用 API 协议进行主动合成服务调用说明。

</div>

## 通用大模型链路

接入讯飞星火大模型，具备开放式对话、知识问答、逻辑推理能力。

<div class="nav-cards">

- **[服务鉴权](/api-dev/llm-chain/auth)** — 大模型交互链路服务鉴权介绍。
- **[交互 API](/api-dev/llm-chain/interact-api)** — 大模型交互核心接口，支持多轮对话、上下文管理和智能响应生成的完整链路调用。
- **[用户个性化 API](/api-dev/llm-chain/personalization-api)** — 支持用户画像管理、偏好设置和个性化对话风格定制，实现大模型的个性化交互体验。
- **[声音复刻 API](/api-dev/llm-chain/voice-clone-api)** — 提供语音特征提取、声音模型训练和定制化语音合成功能，实现个性化声音复刻效果。
- **[合成能力使用](/api-dev/llm-chain/tts-usage)** — 介绍在通用大模型交互链路下使用 API 协议进行主动合成服务调用说明。

</div>

## 极速超拟人链路

低延迟、多模态、情感化的拟人交互链路，适合追求沉浸体验的实时应用。

<div class="nav-cards">

- **[服务鉴权](/api-dev/ultra-chain/auth)** — 极速超拟人链路服务鉴权介绍。
- **[交互 API](/api-dev/ultra-chain/interact-api)** — 极速超拟人交互核心接口，支持毫秒级响应的拟人化对话，融合语音、语义和情感表达的全链路调用。
- **[用户个性化 API](/api-dev/ultra-chain/personalization-api)** — 支持用户画像管理、偏好设置和个性化对话风格定制。
- **[声音复刻 API](/api-dev/ultra-chain/voice-clone-api)** — 提供语音特征提取、声音模型训练和定制化语音合成功能。
- **[合成能力使用](/api-dev/ultra-chain/tts-usage)** — 介绍在极速超拟人链路下使用 API 协议进行主动合成服务调用说明。

</div>
