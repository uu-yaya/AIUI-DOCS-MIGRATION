---
title: 协议规范
description: AIUI 技能交互协议与后处理接口规范
---

::: info 概述
本节汇总了 AIUI 技能工作室涉及的各类协议规范，包括语义协议字段定义、技能后处理请求与响应格式、请求校验机制及资源限制说明，是技能后处理开发的核心参考文档。
:::

## 本节内容

<div class="nav-cards">

- **[技能后处理协议：Request v2.1](/custom-biz/protocols/post-process-request-v21)** — 自定义技能开发包括以下步骤：
- **[技能后处理协议：标准请求](/custom-biz/protocols/post-process-request)** — 通过AIUI链路，标准请求request中包含经过AIUI解析后的用户请求有4类，
- **[技能后处理协议：Response v2.1](/custom-biz/protocols/post-process-response-v21)** — 协议v2.1比v2.0协议，存在字段增删，和支持取值的增加。
- **[技能后处理协议：请求校验](/custom-biz/protocols/post-process-verify)** — 技能需要校验请求是否来源于 AIUI，所有发送给技能的请求Header都包含Signature字段
- **[技能资源限制](/custom-biz/protocols/resource-limits)** — 已下关于AIUI技能工作室技能或问答库创建资源限制说明,针对的都是单个AIUI平台账号，而不是某个AIUI应用。
- **[语义协议：重要字段和通用字段](/custom-biz/protocols/semantic-protocol)** — 交互返回数据为JSON格式:

</div>