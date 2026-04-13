---
title: 传统链路个性化数据使用
---

个性化数据使用概述

个性化数据使用涉及多个环节，了解这些环节有助于更好地应用和管理个性化数据。下面详细说明相关内容。

## 流程介绍

温馨提示

1、传统语义链路个性化上传云端是异步操作，先接受上传的数据，在进行引擎加载处理

2、数据打包查询仅是查询引擎加载数据的状态，不是下载上传的内容

3、动态实体数据上传属于覆盖更新，上传后服务端将持久存储

4、动态实体上传后5min生效。

在传统语义链路下，个性化数据使用主要分三个步骤：

- 个性化数据上传
- 云端数据打包查询
- 生效使用配置

## 接口调用

### 2.1. 数据上传

**在`传统语义`链路**，个性化数据上传格式说明如下：
构建`CMD_SYNC` 类型事件进行个性化数据上传：

```
new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, null, syncData);
```

参数说明：

- msgType :消息事件，`CMD_SYNC` 代表个性化数据操作请求
- agr1：数据类型，数据上传对应`SYNC_DATA_SCHEMA`（常量对应值为`3`）
- arg2：默认空值 `0`
- params：默认空值 null
- data：同步JSON内容的utf-8二进制数据，JSON格式如下：

```json
{
    "param": {
        "id_name": "uid",   // 维度类型
        "id_value": "",     // 维度取值,当取值为uid或appid时，该项可取空或不传，AIUI会自动补全
        "res_name": "XXX.user_applist"  // 资源名，取值方式： 命名空间.实体资源名称
    },
    "data": "xxxxxx"    // 待上传的动态实体json数据内容base64编码（每条json换行隔开）
}
```

**`特别说明`：**
当上传的动态实体为自定义维度时候，同步的数据json格式如下：

```json
{
    "param": {
        "appid": "xxx",        // AIUI应用appid
        "id_name": "xxx",      // 自定义维度名
        "id_value": "xxx",     // 自定义维度value
        "res_name": "xxx"      // 资源名称
    },
    "data": "xxxxxx"// 与schema名称对应的数据内容base64编码
}
```

#### 2.1.1. 自定义动态实体实例

依据下方创建的自定义动态实体，确认上传的资源名称（OS8565315570.building），示例代码如下：

|  |
| --- |
| 自定义动态实体示例 |
| Image 1 Image 3 |

```java
// 构建待上传数据，每条json以换行符隔开
 String userData =
    "{\"building\":\"北京国家体育馆\",\"alias\":\"鸟巢\"}\n" +
    "{\"building\":\"天坛\",\"alias\":\"祈谷坛|圜丘\"}" +
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();
paramJson.put("id_name", "uid");
paramJson.put("res_name", "OS8565315570.building");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, "", syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

#### 2.1.2. 官方动态实体实例

官方动态实体，主要需要注意上传的资源名称（res\_name）取值，

- 以电话联系人举例：

```java
// 构建待上传数据，每条json以换行符隔开
String userData =
    "{\"name\":\"张三\",\"alias\":\"三弟\",\"phoneNumber\":\"18888888888\"}\n" +
    "{\"name\":\"王二\",\"alias\":\"二哥\",\"phoneNumber\":\"16666666666\"}";
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();
paramJson.put("id_name", "uid");
paramJson.put("res_name", "IFLYTEK.telephone_contact");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, "", syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

- 以智能家居alisa资源举例：

```java
// 构建待上传数据，每条json以换行符隔开
 String AliasData =
    "{\"modifier\":\"LED\",\"location\":{\"room\":\"客厅\"},\"did\":\"light-001\",\"device\":\"light\",\"alias\":\"吊灯\"}\n" +
    "{\"modifier\":\"吊扇\",\"location\":{\"room\":\"客厅\"},\"did\":\"fan-001\",\"device\":\"fan\",\"alias\":\"三叶大侠\"}" +
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();
paramJson.put("id_name", "uid");
paramJson.put("res_name", "IFLYTEK.smartH_deviceAlias");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, "", syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

#### 2.1.3. 回调解析

发送`CMD_SYNC` 完成数据上传后会有`EVENT_CMD_RETURN`事件回调，可以获取该操作对应的sid，便于后面查询使用:

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                processCmdReturnEvent(event);
            }
        }
    }
}

private void processCmdReturnEvent(AIUIEvent event) {
    switch (event.arg1) {
        case AIUIConstant.CMD_SYNC: {
            int dtype = event.data.getInt("sync_dtype");

            //arg2表示结果
            if (0 == event.arg2) {  // 同步成功
                if (AIUIConstant.SYNC_DATA_SCHEMA == dtype) {
                    mSyncSid = event.data.getString("sid");
                    showTip("schema数据同步成功，sid=" + mSyncSid);
                }
            } else {
                if (AIUIConstant.SYNC_DATA_SCHEMA == dtype) {
                    mSyncSid = event.data.getString("sid");
                    showTip("schema数据同步出错：" + event.arg2 + "，sid=" + mSyncSid);
                }
            }
        } break;
    }
}
```

### 2.2. 数据打包查询

温馨提示

动态实体数据上传完成后，在调用打包查询事件前需要等待5~10s，这是由于云端数据打包是异步处理，有一定耗时。

#### 2.2.1. 接口调用

上传数据完成后，通过`CMD_QUERY_SYNC_STATUS`查询处理状态
arg1表示状态查询的类型，动态实体对应`SYNC_DATA_SCHEMA`（常量对应值为3），params为json，包含需要对应同步上传操作的sid，示例如下:

```
JSONObject paramsJson = new JSONObject();
paramsJson.put("sid", mSyncSid);

AIUIMessage querySyncMsg = new AIUIMessage(AIUIConstant.CMD_QUERY_SYNC_STATUS,AIUIConstant.SYNC_DATA_SCHEMA, 0,paramsJson.toString(), null);
mAIUIAgent.sendMessage(querySyncMsg);
```

#### 2.2.2. 回调解析

`CMD_QUERY_SYNC_STATUS`执行完成后会有`EVENT_CMD_RETURN`事件回调，表示查询结果，解析示例如下:

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                processCmdReturnEvent(event);
            }
        }
    }
}

private void processCmdReturnEvent(AIUIEvent event) {
    switch (event.arg1) {
        //schema数据打包结果查询结果
        case AIUIConstant.CMD_QUERY_SYNC_STATUS: {
            int syncType = event.data.getInt("sync_dtype");

            if (AIUIConstant.SYNC_DATA_QUERY == syncType) {
                String result = event.data.getString("result");

                if (0 == event.arg2) {
                    showTip("查询结果：" + result);
                } else {
                    showTip("schema数据状态查询出错：" + event.arg2 + ", result:" + result);
                }
            }
        } break;
    }
}
```

## 生效使用

个性化数据生效使用，按照AIUI参数配置也分两种方式：

- aiui.cfg静态参数配置
- 动态参数设置或请求参数写入

### 3.1. 静态参数配置生效

在aiui参数配置文件aiui.cfg中直接配置pers\_param参数，可以多种级别的动态实体同时设置。
加载用户级和应用级别动态实体资源：

```json
{
    "audioparams": {
        "pers_param":"{\"appid\":\"\",\"uid\":\"\"}"
    }
}
```

### 3.2. 动态参数配置生效

温馨提示

动态参数设置pers\_param这种方式只会对语音交互生效，文本语义参考下面数据写入带pers\_param的方式

```
JSONObject params = new JSONObject();
JSONObject audioParams = new JSONObject();
audioParams.put("pers_param", "{\"appid\":\"\",\"uid\":\"\"}");
params.put("audioparams", audioParams);
AIUIMessage setMsg = new AIUIMessage(CMD_SET_PARAMS, 0 , 0, params.toString(), "");
mAgent.sendMessage(setMsg);
```

也可以在音频写入时设置该参数：

```java
//写入音频
byte[] audio = xxx; //初始化
String params = "data_type=audio,sample_rate=16000,pers_param={\"appid\":\"\",\"uid\":\"\"}";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, audio);
mAIUIAgent.sendMessage(msg);
```

文本语义请求：

```java
// 构建请求文本
byte[] content= "XXX".getBytes();
String params = "data_type=text,pers_param={\"appid\":\"\",\"uid\":\"\"}";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, content);
mAIUIAgent.sendMessage(msg);
```
