---
title: 表情标签配置
description: AIUI 极速超拟人交互系统的表情标签（Facial Expression）配置，支持 25 种情绪标签。
---

::: warning 注意
该能力仅在**极速超拟人交互链路**下可用。
:::

## 概述

除了文字与语音播报，AIUI 极速超拟人交互系统还提供了丰富的表情表达。**表情标签（Facial Expression）** 代表 AI 回复时的情绪与内心状态，让开发者和用户能感知到 AI 的"心情"与"意图"，为产品带来拟人灵动的交互体验。

目前表情的颗粒度为会话级别，即一轮 AI 回复带一个表情标签。

## 用途

- **增强聊天沉浸感** — 在聊天气泡旁展示对应表情，根据情绪改变交互界面设计
- **驱动面部表情** — 通过读取表情标签，让 2D/3D 虚拟形象或机器人面部实时做出对应表情
- **情绪分析统计** — 后台统计用户与 AI 交互过程中的情绪变化趋势，分析对话质量

## 表情列表

AIUI 当前支持 25 个表情标签，按情绪类型分类如下：

### 中性情绪

| 情绪类型 | 描述 |
| --- | --- |
| neutral | 中性、平静 |
| embarrassed | 尴尬、害羞 |
| surprised | 惊讶 |
| thinking | 思考、疑惑 |
| sleepy | 困倦、疲惫 |
| comfort | 安慰 |
| pleading | 撒娇、恳求 |

### 正面情绪

| 情绪类型 | 描述 |
| --- | --- |
| happy | 开心、幸福、满足、元气 |
| cheerful | 大笑 |
| tears_of_joy | 笑哭 |
| loving | 喜爱 |
| cool | 酷 |
| relax | 放松 |
| drool | 馋 |
| blow_a_kiss | 飞吻 |
| congratulate | 庆祝、祝贺 |
| playful | 调皮 |
| silly_ghost | 搞怪 |

### 负面情绪

| 情绪类型 | 描述 |
| --- | --- |
| angry | 愤怒 |
| sad | 悲伤、失望 |
| sigh | 叹息、无奈 |
| crying | 哭泣、难过 |
| unlucky | 衰、倒霉 |
| anxiety | 焦虑、恐惧 |
| sorry | 对不起 |

## 使用方式

如需接入表情驱动能力，请联系商务/技术支持获得授权。授权后在应用配置中打开表情驱动即可获得云端下发的表情结果。

下发数据结构示例：

```json
{
  "cbm_facial_expression": {
    "compress": "raw",
    "encoding": "utf8",
    "format": "plain",
    "seq": 0,
    "status": 2,
    "text": "happy"
  }
}
```

| 字段 | 说明 |
| --- | --- |
| compress | 压缩方式，固定为 `raw` |
| encoding | 编码方式，固定为 `utf8` |
| format | 格式，固定为 `plain` |
| seq | 序号 |
| status | 状态码 |
| text | 表情标签值，对应上方表情列表中的情绪类型 |
