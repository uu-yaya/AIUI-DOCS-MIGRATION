---
title: 三方大模型配置
---

::: info 概述
AIUI平台目前支持配置三方大模型作为回复大模型。

**前提：配置的三方大模型服务需要满足OpenAI API协议。**

需要在开源的三方平台获取API接入的url、应用的API\_key，下文以通义千问为例介绍配置步骤：
:::

## 获取三方平台信息

**步骤1、注册：** [点击注册](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api)、 并进行[实名认证](https://myaccount.console.aliyun.com/cert-info)。
![](/media/202507/2025-07-10_095350_1331000.8623484235809503.png)

**步骤2、开通阿里云百炼的模型服务：** 在页面中点击下图中的立即开通。
![](/media/202507/2025-07-10_095530_7950570.5983903907619165.png)

**步骤3、获取API\_key：** [获取API\_key](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.1aae60e9pnUmZ3&tab=model#/api-key)，点击【创建我的API-KEY（1/10）】复制即可。
![](/media/202507/2025-07-10_095647_8440800.17106721485349885.png)

**步骤4、获取API接入url：** 在官方API接入文档中[获取API接入url](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?spm=a2c4g.11186623.0.i29)，如<https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions。>
![](/media/202507/2025-07-18_111856_5892080.02948256054090881.png)

## 创建AIUI应用

在AIUI平台点击我的应用，进入[创建新应用](https://aiui.xfyun.cn/app)。
![](/media/202507/2025-07-10_110142_3548150.9944395000022348.png)

## 模型配置

**步骤1、模型配置界面：** 在应用配置页选择模型-三方大模型后，点击模型配置。
![](/media/202507/2025-07-10_110427_3827570.1572343381652862.png)

**步骤2、填写配置信息：** 进入模型配置页面，【接口地址】中填写接口上述第一步获取的url，【鉴权信息】中填写获取的apikey，【模型标识】中填写模型domain，可在[第三方模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market，如qwen-plus)查找。
![](/media/202507/2025-07-10_110828_6523110.31375463968566175.png)
![](/media/202507/2025-07-10_110938_6516530.7671663795992344.png)
**步骤3、测试：** 输入问题，若有回复，即配置成功。
![](/media/202507/2025-07-10_110957_7946020.6858498026719815.png)
