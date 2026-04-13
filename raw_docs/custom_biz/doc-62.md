---
title: 技能后处理
source_url: https://aiui-doc.xf-yun.com/project-1/doc-62/
---

**技能后处理**帮助开发者实现自定义功能，可直接与万维网通信。

## 业务逻辑

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/4_skill_develop/4_private_skill/post_process_flow.png -->
![待补充：技能后处理流程图](/_images/placeholder.svg)

## 能力

1. 实现多轮对话。
2. 获取语义结果后，直接与万维网通信，缩短链路时间。
3. 开发者无需拥有服务器。

每次请求都会触发技能后处理，开发者拿到语义结果（request：JSON），处理后返回（response：JSON），引擎解析 response 来决定最终下发到客户端的数据。

## 调用方式

技能后处理支持**云函数**和**webhook**

### 云函数

云函数可以在线编辑，调用信源，处理业务逻辑，填写技能的回复 answer，通过 HTTP 请求通信。

温馨提示

1、AIUI平台自定义技能已全量升级切换到 v2.1协议，云函数技能后处理开发请查看【[云函数APIv2.1](https://aiui-doc.xf-yun.com/project-1/doc-64/) 】文档说明

2、技能后处理托管业务整体处理耗时不能超1000ms，超时后技能将退出。

云函数的是 FaaS （Function as a Service）服务，运行在讯飞服务器。

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/4_skill_develop/4_private_skill/cloud_function.png -->
![待补充：云函数架构图](/_images/placeholder.svg)

#### 运行环境

云端NodeJS 环境为v9.10.1。除 nodejs 携带的标准模块（http crypto https url dgram net stream string\_decoder timers buffer）外，还提供以下第三方模块：

```kotlin
promise asap async bson caseless concat-stream

data-format double-ended-queue fibers http-basic

http-response-object inherits ioredis isarray

json5 minimist ms node-zookeeper-client qs

readable-stream resolve-from safe-buffer semver

streamroller string_decoder request-promise

then-request typedarray util-deprecate
```text

云函数有全局变量 AIUI，用于打印日志的 console。点击查看更多云函数接口：[v2.0](https://aiui-doc.xf-yun.com/project-1/doc-63/)，[v2.1](https://aiui-doc.xf-yun.com/project-1/doc-64/)

#### 示例

云函数通过 `dialogState`判断填槽对话是否完成，未完成时，开发者不做操作。完成填槽对话后， 回复`answer`到客户端 。

示例代码：

```javascript
AIUI.create("v2.1",  function(aiui,  err){
  //打印 request 结构体
  requestObject = aiui.getRequest().getObject();
  console.log(requestObject);
  //获取 response 对象
  var response = aiui.getResponse();
  // 获取填槽对话状态
  dialogState= requestObject.request.dialogState;

  if(dialogState!=null&&dialogState!="COMPLETED"){
  // 填槽对话未完成时，托管给系统管理
    response.addDelegateDirective();
  }else{
    // 填槽对话完成时，回复用户一句 answer
    updatedIntent = aiui.getUpdatedIntent();
    companyValue = updatedIntent.getSlotValue("company");
    numberValue = updatedIntent.getSlotValue("number");
    answer="你的"+companyValue+"快递，快递单号是是："+numberValue+"，已经达到合肥市"
    response.setOutputSpeech(answer);
  }
  // 提交
  aiui.commit();
})
```

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/4_skill_develop/4_private_skill/cf_exp.png -->
![待补充：云函数调用示例截图](/_images/placeholder.svg)

如果您不会编写代码，但是想为您的技能增加回复，只需要把以下代码复制进入代码编辑框，修改第12行之后，保存并构建即可。

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    requestObject = aiui.getRequest().getObject();
    var response = aiui.getResponse();
    // 获取当前意图名
    intentName = requestObject.request.intents[0].name;
    console.log("本次意图来自:"+intentName);
    // 获取填槽对话状态
    dialogState= requestObject.request.dialogState;
    if(dialogState!=null&&dialogState!="COMPLETED"){
        response.addDelegateDirective();
    }else{
        response.setOutputSpeech("这里修改成您想要的回复");
    }
    aiui.commit();
 })
```text

如果您想根据 intent 回复不同的 answer，可以使用以下代码。

```
 AIUI.create("v2.1",  function(aiui,  err){
    requestObject = aiui.getRequest().getObject();
    var response = aiui.getResponse();
    // 获取当前意图名
    intentName = requestObject.request.intents[0].name;
    console.log("本次意图来自:"+intentName);
    // 获取填槽对话状态
    dialogState= requestObject.request.dialogState;
    if(dialogState!=null&&dialogState!="COMPLETED"){
        response.addDelegateDirective();
    }else if(intentName==="这里填写intent A 的名称"){
        response.setOutputSpeech("这里是是 intent A的回复");
    }else if(intentName==="这里填写intent B 的名称"){
        response.setOutputSpeech("这里是是 intent B的回复");
    }else if(intentName==="这里填写intent C 的名称"){
        response.setOutputSpeech("这里是是 intent C的回复");
    }else{
        response.setOutputSpeech("这里是一个默认回复");
    };
    aiui.commit();
 })
```text

#### 安全

云端进行了资源隔离以及监测，危险代码并不会影响服务器运行，但系统检测到代码异常时，将下线该技能。

NodeJS 标准不建议的代码请勿编写，如：阻止事件循环。NodeJS 为单线程环境运行，如果存在死循环，技能将不能接收用户消息，技能会被下线。默认每次请求交互1000毫秒超时，开发者技能应该在该超时时间内调用 api 的 response 接口，否则云端返回超时错误，此类情况可能出现在：

- 上述事件循环阻塞。
- 开发者在异步操作（如 http 调用）回调中调用返回接口，该异步操作可能返回时间较长，此类情况应该对该异步操作设置超时，不要让云端触发超时。

### Webhook

Webhook的本质是一个web调用，若通过公网部署，技能耗时会增加。

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/4_skill_develop/4_private_skill/webhook.png -->
![待补充：Webhook 架构图](/_images/placeholder.svg)

使用Webhook流程

- 在平台填写技能部署地址（URL地址）
- 技能需要验证发送的请求，验证步骤请参考[技能请求校验](https://aiui-doc.xf-yun.com/project-1/doc-72/)。

### 注意：

Webhook只支持[v2.1协议](https://aiui-doc.xf-yun.com/project-1/doc-64/)。
