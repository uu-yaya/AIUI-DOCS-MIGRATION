---
title: 云函数 API v2.1
---

## 基本接口

以下接口用来获取对象、request、response 结构体以及提交本次加工的结果

### 创建实例对象

**AIUI.create(version:string, callbackfunc) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| version | string | 获取该版本对应的对象，最新版本号为 v2.1 | 是 |
| callbackfunc | Function | 回调函数 | 是 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
   console.log("hello iflyos");
   aiui.commit();
})
```

### 获取 Request 结构体

**aiui.getRequest().getObject() -> Object**

```javascript
 AIUI.create("v2.1", function(aiui, err) {
     var requestObject = aiui.getRequest().getObject();
     var intentName = requestObject.request.intent.name;
     console.log('当前意图为：' + intentName);
     console.log(requestObject);
     aiui.commit();
 })
```

### 终止技能后处理

**该函数必须执行**，且作为代码的最后一句执行。不执行会触发技能后处理 800ms 超时机制。

**aiui.commit() -> void**

```javascript
 AIUI.create("v2.1", function(aiui, err) {
     var requestObject = aiui.getRequest().getObject();
     var response = aiui.getResponse();
     response.setOutputSpeech("请欣赏三国演义");
     aiui.commit();
 })
```

### 退出技能

**response.withShouldEndSession(bool:Boolean) -> void**

是否退出当前技能，一旦退出，将清除技能相关的所有数据包括用户私有的session数据以及填槽对话历史，必须通过入口意图方可再次进入该技能。true表示会话在响应后结束；false表示会话保持活动状态。如果未提供，则默认为true。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| bool | Boolean | 是否退出当前技能 | 是 |

```javascript
AIUI.create("v2.1", function(aiui, err) {
    var response = aiui.getResponse();
    response.withShouldEndSession(true);
    aiui.commit();
})
```

### 日志打印

**console.log(object:Object) -> void**

在脚本开发过程有时候可能需要日志调试，这时候可通过console.log()方法打印输出相关调试信息，需注意打印的内容必须是 String 或 Object

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| object | Object | 需要打印输出的信息 | 是 |

```javascript
AIUI.create("v2.1", function(aiui, err) {
    var requestObject = aiui.getRequest().getObject();
    var intentName = requestObject.request.intent.name;
    console.log('当前意图为：' + intentName);
    console.log(requestObject);
    var myObj = {
        name: "打印日志",
        description: "www.iflyos.cn"
    };
    console.log(myObj);
    response.setOutputSpeech("欢迎使用iflyos");
    aiui.commit();
})
```

## Response 处理接口

因为构造 response 对象较为复杂，aiui 对象中提供了若干辅助函数帮助开发者构建response 对象。

### 获取 Response 对象

**aiui.getResponse() -> Response**

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    aiui.commit();
 })
```

### 添加语音回复

**response.setOutputSpeech(outputSpeech:String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| outputSpeech | String | 本次返回结果中需要播报的语音信息 | 否 |

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    response.setOutputSpeech("请欣赏三国演义");
    aiui.commit();
 })
```

### 添加语音提示回复

**response.setReprompt(reprompt: String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| reprompt | String | 若该技能回复需要打开录音收听用户的语音回复（追问时），当用户在8秒内没有说话或用户的回复技能无法理解，设备将推送该语音文本，用于再次提示用户输入。 | 否 |

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    response.setReprompt("嗨，你还在吗");
    aiui.commit();
 })
```

### 添加 data 字段

**response.setData(data:Object) -> void**

为 Response 添加 Data 字段

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| data | Object | 本次返回结果中需要携带的 data | 是 |

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
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
 AIUI.create("v2.1",  function(aiui,  err){
    var session = aiui.getSession();
    aiui.commit();
 })
```

### 在session中增加或更新键值对

**session.setData(field:String,value:String) ->void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| field | String | 要增改的键名 | 是 |
| value | String | 要增改的键值 | 是 |

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
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
 AIUI.create("v2.1",  function(aiui,  err){
    var session = aiui.getSession();
    var userSex = session.getData("UserSex");
    aiui.commit();
 })
```

### 清空session 中的所有数据

**session.clear() ->void**

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    var session = aiui.getSession();
    session.clear();
    aiui.commit();
 })
```

## Dialog 填槽对话接口

### 添加对话托管

**response.addDelegateDirective(updatedIntent?: Object) -> void**

当使用DelegateDirective时，系统默认按照开发者在平台填写的信息进行追问反问

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    var requestObject = aiui.getRequest().getObject();
    //获取当前对话的填槽状态
    var dialogState= requestObject.request.dialogState;
    //判断填槽状态是否已完成
    if(dialogState != null && dialogState != "COMPLETED") {
        response.addDelegateDirective();
    }else {
        response.setOutputSpeech("槽已填满，接下来我们做更多的事情吧");
    }
    aiui.commit();
})
```

### 添加询问槽位

**response.addElicitSlotDirective(slotToElicit: string, updatedIntent?: Intent) -> void**

当使用ElicitSlotDirective时，系统下一轮对话的内容将会去使用 outputSpeech 追问用户槽位信息，并期望用户回答相应的槽值来填充 slotToElicit 值。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotToElicit | string | 期望用户下一轮说出的槽位 | 是 |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    var cityValue = updatedIntent.getSlotValue('city');
    if (cityValue == null ) {
        response.addElicitSlotDirective("city");//意图下需要有对应的实体名方能生效
        response.setOutputSpeech("请问你要查询哪个城市的天气呢？");
    } else {
        response.setOutputSpeech("我取到槽值啦，我知道你想查" + cityValue + "的天气");
    }
    aiui.commit();
})
```

### 添加槽位确认

**response.addConfirmSlotDirective(slotToConfirm: string, updatedIntent?: Intent) -> void**

当使用 ConfirmSlotDirective 时，系统下一轮对话的内容将会去使用 outputSpeech 询问用户是否确认槽位，并期望用户回答“确认”、“否认”的话术。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotToConfirm | string | 期望用户确认的槽位 | 是 |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    //获取槽值
    var cityValue = updatedIntent.getSlotValue('city');
    if (cityValue == null ) {
        response.addElicitSlotDirective("city");//意图下需要有对应的实体名方能生效
        response.setOutputSpeech("请问你要查询哪个城市的天气呢？");
    } else {
        //获取槽值的确认状态
        var cityConfirmationStatus = updatedIntent.getSlotConfirmationStatus('city');
        if (cityConfirmationStatus === 'NONE') {
            response.addConfirmSlotDirective("city");//意图下需要有对应的实体名、且该槽位已被填充方可生效。
            response.setOutputSpeech("你是不是想查" + cityValue + "的天气？");
        } else {
            response.setOutputSpeech("我知道了，我确定你想查" + cityValue + "的天气");
        }
    }
    aiui.commit();
})
```

### 添加意图确认

**response.addConfirmIntentDirective(updatedIntent?: Intent) -> void** 当使用 ConfirmSlotDirective 时，系统下一轮对话的内容将会去使用 outputSpeech 询问用户是否确认意图，并期望用户回答“确认”、“否认”的话术。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| updatedIntent | Object | 要更新的意图 | 否 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    var requestObject = aiui.getRequest().getObject();
    //获取当前对话的填槽状态
    var dialogState= requestObject.request.dialogState;
    //判断填槽状态是否已完成
    if(dialogState != null && dialogState != "COMPLETED") {
        response.addDelegateDirective();
    }else {
        var intentConfirmationStatus = updatedIntent.getIntentConfirmationStatus(); //获取意图确认状态
        if (intentConfirmationStatus === 'NONE') {
            response.addConfirmIntentDirective();
        } else {
            //获取槽值
            var cityValue = updatedIntent.getSlotValue('city');
            response.setOutputSpeech("我确定你想查" + cityValue + "的天气");
        }
    }
    aiui.commit();
})
```

### 进行追问

**response.withExpectSpeech(bool:String) -> void**

在某些对话场景下，技能开发者期望设备主动打开麦克风拾音，此时请将 bool 设置为 true。不调用该函数时，默认为 false。添加了 Directive 时请勿调用该函数，系统会根据 Directive 自动返回合理的 Boolean 值。该函数不会清除任何历史，只影响返回到客户端的参数，控制客户端麦克风是否主动开启拾音。

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| bool | Boolean | 客户端是否需要主动打开麦克风 | 是 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    response.withExpectSpeech(true);
    aiui.commit();
 })
```

### 构造UpdatedIntent

**aiui.getUpdatedIntent() -> UpdatedIntent**

获取updatedIntent对象，该对象创建成功后，会默认复制 request 中的槽位信息。

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
     var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    response.addDelegateDirective(updatedIntent.getObject());
    aiui.commit();
 })
```

### 根据槽名获取槽值

**updatedIntent.getSlotValue(slotName:String) -> String**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望获取槽位信息的槽名 | 是 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    var requestObject = aiui.getRequest().getObject();
    //获取当前对话的填槽状态
    var dialogState= requestObject.request.dialogState;
    //判断填槽状态是否已完成
    if(dialogState != null && dialogState != "COMPLETED") {
        response.addDelegateDirective();
    }else {
        var cityValue = updatedIntent.getSlotValue('city');
        response.setOutputSpeech("我确定你想查" + cityValue + "的天气");
    }
    aiui.commit();
})
```

### 根据槽名获取规整后的槽值

**updatedIntent.getSlotNormValue(slotName:String) -> String**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望获取槽位信息的槽名 | 是 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    var requestObject = aiui.getRequest().getObject();
    //获取当前对话的填槽状态
    var dialogState= requestObject.request.dialogState;
    //判断填槽状态是否已完成
    if(dialogState != null && dialogState != "COMPLETED") {
        response.addDelegateDirective();
    }else {
        var cityNormValue = updatedIntent.getSlotNormValue('city');
        response.setOutputSpeech("你要查的是" + cityNormValue + "的天气");
    }
    aiui.commit();
})
```

### 获取槽确认状态

**updatedIntent.getSlotConfirmationStatus(slotName:String) -> String**

获取 slotName 槽值是否确认，返回值为”CONFIRMED”，”NONE”, “DENIED”

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望获取槽位确认信息的槽名 | 是 |

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    //获取槽值
    var cityValue = updatedIntent.getSlotValue('city');
    if (cityValue == null ) {
        response.addElicitSlotDirective("city");//意图下需要有对应的实体名方能生效
        response.setOutputSpeech("请问你要查询哪个城市的天气呢？");
    } else {
        //获取槽值的确认状态
        var cityConfirmationStatus = updatedIntent.getSlotConfirmationStatus('city');
        if (cityConfirmationStatus === 'NONE') {
            response.addConfirmSlotDirective("city");//意图下需要有对应的实体名、且该槽位已被填充方可生效。
            response.setOutputSpeech("你是不是想查" + cityValue + "的天气？");
        } else {
            response.setOutputSpeech("我知道了，我确定你想查" + cityValue + "的天气");
        }
    }
    aiui.commit();
})
```

### 获取意图确认状态

**updatedIntent.getIntentConfirmationStatus() -> String**

获取意图是否确认，返回值为”CONFIRMED”，”NONE”, “DENIED”

```javascript
AIUI.create("v2.1",  function(aiui,  err){
    var updatedIntent = aiui.getUpdatedIntent();
    var response = aiui.getResponse();
    var requestObject = aiui.getRequest().getObject();
    //获取当前对话的填槽状态
    var dialogState= requestObject.request.dialogState;
    //判断填槽状态是否已完成
    if(dialogState != null && dialogState != "COMPLETED") {
        response.addDelegateDirective();
    }else {
        var intentConfirmationStatus = updatedIntent.getIntentConfirmationStatus(); //获取意图确认状态
        if (intentConfirmationStatus === 'NONE') {
            response.addConfirmIntentDirective();
        } else {
            //获取槽值
            var cityValue = updatedIntent.getSlotValue('city');
            response.setOutputSpeech("我确定你想查" + cityValue + "的天气");
        }
    }
    aiui.commit();
})
```

### 设置指定语义槽的槽值以及状态

**updatedIntent.setSlot(slotName:String, slotValue:String, slotConfirmationStatus:String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| slotName | String | 期望更改的槽位名 | 是 |
| slotValue | String | 更改的槽值 | 是 |
| slotConfirmationStatus | String | 更改的槽位确认信息，取值范围是”CONFIRMED”，”NONE”, “DENIED” | 是 |

### 设置意图的确认状态

**updatedIntent.setIntentConfirmationStatus(intentConfirmationStatus:String) -> void**

| 参数 | 类型 | 描述 | 必须出现 |
| --- | --- | --- | --- |
| intentConfirmationStatus | String | 期望获取槽位确认信息的槽名，取值范围是”CONFIRMED”，”NONE”, “DENIED” | 是 |

## 指令集设置接口

### 获取当前指令集

**response.getDirectives() -> Array**

获取当前脚本中包含的所有指令集集合

```javascript
 AIUI.create("v2.1",  function(aiui,  err){
    var response = aiui.getResponse();
    var directives = response.getDirectives()
    aiui.commit();
 })
```

### 设置指令集

**response.setDirectives(directives:Array) -> void**

设置自定义指令集集合，注意每个指令的type属性不能为空，否则设置失败。

**该接口用于制作技能时，向设备返回开放指令，如音频播放指令等。**

```javascript
 AIUI.create("v2.1", function(aiui, err) {
     var response = aiui.getResponse();
     var directives = [{
         "type": "AudioPlayer.ClearQueue",
         "clearBehavior": "CLEAR_ALL"
     }];
     response.setDirectives(directives);
     aiui.commit();
 })
```

## 简单完整的例子

> 以下脚本提供一个完整的云函数demo，包括意图处理和信源访问

```javascript
//引入request模块，用于网络请求
const rq = require('request-promise');

AIUI.create("v2.1",  async function(aiui,  err){
    var requestObject = aiui.getRequest().getObject();
    var response = aiui.getResponse();
    var updatedIntent = aiui.getUpdatedIntent();
    // 判断请求类型
    var requestType =requestObject.request.type;
    console.log("技能请求类型为:" + requestType);
    if(requestType === "LaunchRequest"){
        // 会话保持活动状态
        response.withShouldEndSession(false);
        response.setOutputSpeech("很高兴再次和你相遇");
    } else if(requestType === "IntentRequest"){
        // 会话保持活动状态
        response.withShouldEndSession(false);

        // 获取当前意图名
        intentName = requestObject.request.intent.name;
        console.log("本次意图来自:" + intentName);
        switch(intentName){
            case 'query_city_weather':
                //获取当前对话的填槽状态
                var dialogState= requestObject.request.dialogState;
                //判断填槽状态是否已完成
                if(dialogState != null && dialogState != "COMPLETED") {
                    response.addDelegateDirective();
                }else {
                    var cityValue = updatedIntent.getSlotValue('city');
                    //获取槽值之后，调用信源查询
                    var requestParams = {
                        "city":cityValue,
                        "key":"bd640cbd2ac06fe89f0e25c334c56e17"
                    }
                    //获取信源结果
                    var res =  await renderData(requestParams)
                    //打印信源结果
                    console.log(res);
                    if (res.error_code == 0 && res.result){
                        var realtime = res.result.realtime;
                        response.setOutputSpeech(cityValue + '目前天气' + realtime.info + '，温度' + realtime.temperature + '度' );
                    } else {
                        response.setOutputSpeech('信源查询失败啦，请稍后再试吧');
                    }
                }
                break;
            default:
                response.setOutputSpeech("这是一条来自IntentRequest未知意图的 answer");
                break;
        }
    } else if(requestType === "SessionEndedRequest"){
        response.withShouldEndSession(true);
        response.setOutputSpeech("退出技能啦，期待再次和你相遇");
    }
    aiui.commit();
})

async function renderData(requestParams) {
    return new Promise(async function(resolve, reject){
        let res = await getContent(requestParams)
        return resolve(res);
    })
}

//获取信源结果
function getContent(requestParams) {
    //信源地址
    var apiUrl = 'http://apis.juhe.cn/simpleWeather/query';

    var options = {
        uri: apiUrl,
        method: 'POST',
        qs: requestParams,
        headers: {'User-Agent': 'Request-Promise'},
        json: true,
        timeout: 750  //设置http请求超时时间
    };
    return rq(options).then((res) => {
        return res;
    }).catch((err) => {
        console.log(err.message);
        return {
            "error_code":'-1',
            "reason":"网络异常或者请求超时"
        }
    });

}
```
