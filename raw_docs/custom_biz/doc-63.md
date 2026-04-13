---
title: 云函数APIv2.0
source_url: https://aiui-doc.xf-yun.com/project-1/doc-63/
---

## 基本接口

温馨提示

AIUI平台自定义技能已全量升级切换到 v2.1协议，本协议文档仅做保留。如需开发请查看【[云函数APIv2.1](https://aiui-doc.xf-yun.com/project-1/doc-64/) 】文档说明

以下接口用来获取对象、request、response 结构体以及提交本次加工的结果

### 创建实例对象

**AIUI.create(version:string, callbackfunc) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| version | string | 获取该版本对应的对象，最新版本号为 v2 | 是 |
| callbackfunc | Function | 回调函数 | 是 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    console.log("hello aiui");
    aiui.commit();
 })
```cpp

### 获取 Request 结构体

**aiui.getRequest().getObject() -> Object**

```javascript
 AIUI.create("v2",  function(aiui,  err){
    requestObject = aiui.getRequest().getObject();
    console.log(requestObject);
    aiui.commit();
 })
```

### 终止技能后处理

**aiui.commit() -> void**

```javascript
 AIUI.create("v2",  function(aiui,  err){
    requestObject = aiui.getRequest().getObject();
    var response = aiui.getResponse();
    response.setOutputSpeech("请欣赏三国演义");
    aiui.commit();
 })
```cpp

> 该函数必须执行，且作为代码的最后一句执行。不执行会触发技能后处理 800ms 超时机制。

### 退出技能

**Response.withshouldExitSkill(bool:String) -> void**

是否退出当前技能，一旦退出，将清除技能相关的所有数据包括用户私有的session数据以及填槽对话历史，必须通过入口意图方可再次进入该技能。不调用时默认为为 false。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| bool | Boolean | 是否退出当前技能 | 是 |

## Response 处理接口

因为构造 response 对象较为复杂，aiui 对象中提供了若干辅助函数帮助开发者构建response 对象。

### 获取 Response 对象

**aiui.getResponse() -> Response**

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var response = aiui.getResponse();
    aiui.commit();
 })
```

### 添加语音回复

**Response.setOutputSpeech(outputSpeech？ : String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| outputSpeech | String | 本次返回结果中需要播报的语音信息 | 否 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var response = aiui.getResponse();
    response.setOutputSpeech("请欣赏三国演义");
    aiui.commit();
 })
```cpp

### 添加 data 字段

**Response.setData(data:Object) -> void**

为 Response 添加 Data 字段

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| data | Object | 本次返回结果中需要携带的 data | 是 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var response = aiui.getResponse();
    response.setOutputSpeech("合肥今天24到26摄氏度");

    var data = {"weather":"天气晴朗，阳光明媚"};
    response.setData(data);

    aiui.commit();
 })
```

### 获取 session 对象

**Aiui.getSession() -> session**

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var session = aiui.getSession();
    aiui.commit();
 })
```cpp

### 在session中增加或更新键值对

**session.setData(field:String,value:String) ->void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| field | String | 要增改的键名 | 是 |
| value | String | 要增改的键值 | 是 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var session = aiui.getSession();
    session.setData("UserSex","man");
    session.setData("UserAge","24");
    aiui.commit();
 })
```

### 根据键名取对应的键值

**session.getData(field:String) -> value**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| field | String | 要查询的键名 | 是 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var session = aiui.getSession();
    var userSex = session.getData("UserSex");
    aiui.commit();
 })
```cpp

### 清空session 中的所有数据

**session.clear() ->void**

```javascript
 AIUI.create("v2",  function(aiui,  err){
    var session = aiui.getSession();
    session.clear();
    aiui.commit();
 })
```

## Dialog 填槽对话接口

### 添加对话托管

**Response.addDelegateDirective(updatedIntent?: Object) -> void**

当使用DelegateDirective时，系统默认按照开发者在平台填写的信息进行追问反问

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    response = aiui.getResponse();
    response.addDelegateDirective();
    aiui.commit();
 })
```cpp

### 添加询问槽位

**Response.addElicitSlotDirective(slotToElicit: string, updatedIntent?: Intent) -> void**

当使用ElicitSlotDirective时，系统下一轮对话的内容将会去使用 outputSpeech 追问用户槽位信息，并期望用户回答相应的槽值来填充 slotToElicit 值。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotToElicit | string | 期望用户下一轮说出的槽位 | 是 |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    response = aiui.getResponse();
    response.addElicitSlotDirective("age");//意图下需要有对应的实体名方能生效
    aiui.commit();
 })
```

### 添加槽位确认

**Response.addConfirmSlotDirective(slotToConfirm: string, updatedIntent?: Intent) -> void**

当使用 ConfirmSlotDirective 时，系统下一轮对话的内容将会去使用 outputSpeech 询问用户是否确认槽位，并期望用户回答“确认”、“否认”的话术。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotToConfirm | string | 期望用户确认的槽位 | 是 |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    response = aiui.getResponse();
    response.addConfirmSlotDirective("age");//意图下需要有对应的实体名、且该槽位已被填充方可生效。
    aiui.commit();
 })
```cpp

### 添加意图确认

**Response.addConfirmIntentDirective(updatedIntent?: Intent) -> void**
当使用 ConfirmSlotDirective 时，系统下一轮对话的内容将会去使用 outputSpeech 询问用户是否确认意图，并期望用户回答“确认”、“否认”的话术。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
 AIUI.create("v2",  function(aiui,  err){
    response = aiui.getResponse();
    response.addConfirmIntentDirective();
    aiui.commit();
 })
```

### 进行追问

**Response.withShouldEndSession(bool:String) -> void**

在某些对话场景下，技能开发者期望设备主动打开麦克风拾音，此时请将 bool 设置为 false。不调用该函数时，默认为 true。添加了 Directive 时请勿调用该函数，系统会根据 Directive 自动返回合理的 Boolean 值。该函数不会清除任何历史，只影响返回到客户端的参数，控制客户端麦克风是否主动开启拾音。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| bool | Boolean | 客户端是否需要主动打开麦克风 | 是 |

### 构造UpdatedIntent

**Aiui.getUpdatedIntent() -> UpdatedIntent**

获取updatedIntent对象，该对象创建成功后，会默认复制 request 中的槽位信息。

```javascript
 AIUI.create("v2",  function(aiui,  err){
     updatedIntent = aiui.getUpdatedIntent;
    response = aiui.getResponse();
    response.addDelegateDirective(updatedIntent.getObject());
    aiui.commit();
 })
```cpp

### 根据槽名获取槽值

**UpdatedIntent.getSlotValue(slotName:String) -> String**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望获取槽位信息的槽名 | 是 |

### 获取槽确认状态

**UpdatedIntent.getSlotConfirmationStatus(slotName:String) -> String**

获取 slotName 槽值是否确认，返回值为”CONFIRMED”，”NONE”, “DENIED”

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望获取槽位确认信息的槽名 | 是 |

### 获取意图确认状态

**UpdatedIntent.getIntentConfirmationStatus() -> String**

获取意图是否确认，返回值为”CONFIRMED”，”NONE”, “DENIED”

### 设置指定语义槽的槽值以及状态

**UpdatedIntent.setSlot(slotName:String, slotValue:String, slotConfirmationStatus:String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望更改的槽位名 | 是 |
| slotValue | String | 更改的槽值 | 是 |
| slotConfirmationStatus | String | 更改的槽位确认信息，取值范围是”CONFIRMED”，”NONE”, “DENIED” | 是 |

### 设置意图的确认状态

**UpdatedIntent.setIntentConfirmationStatus(intentConfirmationStatus:String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| intentConfirmationStatus | String | 期望获取槽位确认信息的槽名，取值范围是”CONFIRMED”，”NONE”, “DENIED” | 是 |
