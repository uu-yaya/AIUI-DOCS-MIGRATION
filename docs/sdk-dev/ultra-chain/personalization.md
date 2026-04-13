---
title: 极速超拟人链路个性化数据使用
---

::: info 概述
个性化数据使用涉及多个环节，了解这些环节有助于更好地应用和管理个性化数据。下面详细说明相关内容。
:::

## 流程介绍

温馨提示

1、在通用大模型或极速超拟人交互链路下个性化数据上传是实时生效的。

2、数据下载可以执行资源下载上传的内容信息，注意和传统语义链路的打包查询做区分。

3、动态实体数据上传属于覆盖更新，上传后服务端将持久存储

在**通用大模型**或**极速超拟人**交互链路下，个性化数据使用主要能力为：

- 个性化数据上传、下载、删除
- 生效使用配置

## 接口调用

### 2.1. 个性化数据上传

**在`通用大模型语义`或`极速超拟人`链路**，个性化数据上传格式说明如下：
构建`CMD_SYNC` 类型事件进行个性化数据上传：

```
new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_UPLOAD, 0, null, syncData);
```

参数说明：

- msgType :消息事件，`CMD_SYNC` 代表个性化数据操作请求
- agr1：数据类型，数据上传对应`SYNC_DATA_UPLOAD`（常量对应值为`6`）
- arg2：默认空值 `0`
- params：默认空值 null
- data：同步JSON内容的utf-8二进制数据，JSON格式如下（注意新增字段`name_space`）：

```json
{
    "param": {
        "id_name": "uid",   // 维度类型
        "id_value": "",     // 维度取值,当取值为uid或appid时，该项可取空或不传，AIUI会自动补全
        "name_space": "uid",   // 命名空间（资源名对应的命令空间）
        "res_name": "XXX.user_applist"  // 资源名，取值方式： 命名空间.实体资源名称

    },
    "data": "xxxxxx"    // 待上传的动态实体json数据内容base64编码（每条json换行隔开）
}
```

**`特别说明`：**
当上传的动态实体为自定义维度时候，同步的数据json格式如下（注意新增字段`name_space`）：

```json
{
    "param": {
        "appid": "xxx",          // AIUI应用appid
        "id_name": "xxx",      // 自定义维度名
        "id_value": "xxx",       // 自定义维度value
        "name_space": "uid",   // 命名空间（资源名对应的命令空间）
        "res_name": "xxx"      // 资源名，取值方式： 命名空间.实体资源名称
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
// 注意大模型链路和通用语义链路的区别：新增参数
// aiui开放平台的命名空间，在「技能-实体-动态实体密钥」中查看
paramJson.put("name_space","OS8565315570");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_UPLOAD, 0, "", syncData);
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
// 注意大模型链路和通用语义链路的区别：新增参数
// 官方动态实体，固定取值为:IFLYTEK
paramJson.put("name_space","IFLYTEK");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_UPLOAD, 0, "", syncData);
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
// 注意大模型链路和通用语义链路的区别：新增参数
// 官方动态实体，固定取值为:IFLYTEK
paramJson.put("name_space","IFLYTEK");
syncSchemaJson.put("param", paramJson);
syncSchemaJson.put("data", Base64.encodeToString(userData.getBytes(),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_UPLOAD, 0, "", syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

### 2.2. 个性化数据下载

上传数据完成后，还可以下载已上传的数据
构建`CMD_SYNC` 类型事件进行个性化数据下载：

```
new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_DOWNLOAD, 0, null, syncData);
```

参数说明：

- msgType :消息事件，`CMD_SYNC` 代表个性化数据操作请求
- agr1：数据类型，数据下载对应`SYNC_DATA_DOWNLOAD`（常量对应值为`7`）
- arg2：默认空值 `0`
- params：默认空值 null
- data：同步JSON内容的utf-8二进制数据，JSON格式如下：

```json
{
    "param": {
        "id_name": "uid",   // 维度类型
        "id_value": "",     // 维度取值,当取值为uid或appid时，该项可取空或不传，AIUI会自动补全
        "name_space": "uid",   // 命名空间（资源名对应的命令空间）
        "res_name": "XXX.user_applist"  // 资源名，取值方式： 命名空间.实体资源名称
    }
}
```

```
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();
paramJson.put("id_name", "uid");
paramJson.put("res_name", "OS8565315570.building");
// 注意大模型链路和通用语义链路的区别：新增参数
// aiui开放平台的命名空间，在「技能-实体-动态实体密钥」中查看
paramJson.put("name_space","OS8565315570");
syncSchemaJson.put("param", paramJson);

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage downLoadMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_DOWNLOAD, 0, "", syncData);
mAIUIAgent.sendMessage(downLoadMessage);
```

### 2.3. 个性化数据删除

上传数据完成后，如果数据不想要了可以发送删除事件删除云端存储的个性化数据：
构建`CMD_SYNC` 类型事件进行个性化数据下载：

```
new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_DELETE, 0, null, syncData);
```

参数说明：

- msgType :消息事件，`CMD_SYNC` 代表个性化数据操作请求
- agr1：数据类型，数据下载对应`SYNC_DATA_DELETE`（常量对应值为`8`）
- arg2：默认空值 `0`
- params：默认空值 null
- data：同步JSON内容的utf-8二进制数据，JSON格式如下：

```json
{
    "param": {
        "id_name": "uid",   // 维度类型
        "id_value": "",     // 维度取值,当取值为uid或appid时，该项可取空或不传，AIUI会自动补全
        "name_space": "uid",   // 命名空间（资源名对应的命令空间）
        "res_name": "XXX.user_applist"  // 资源名，取值方式： 命名空间.实体资源名称
    }
}
```

```
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();
paramJson.put("id_name", "uid");
paramJson.put("res_name", "OS8565315570.building");
// 注意大模型链路和通用语义链路的区别：新增参数
// aiui开放平台的命名空间，在「技能-实体-动态实体密钥」中查看
paramJson.put("name_space","OS8565315570");
syncSchemaJson.put("param", paramJson);

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage deleteMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_DELETE, 0, "", syncData);
mAIUIAgent.sendMessage(deleteMessage);
```

### 2.4. 回调解析

发送`CMD_SYNC`完成数据操作后会有`EVENT_CMD_RETURN`事件回调，可以获取该操作对应的sid，便于后面查询使用:

```java
private static String mSyncSid = null;
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {

  @Override
  public void onEvent(AIUIEvent event) {

      switch (event.eventType) {
         case AIUIConstant.EVENT_CMD_RETURN: {
              if (AIUIConstant.CMD_SYNC == event.arg1) {    // 数据同步的返回
                  int dtype = event.data.getInt("sync_dtype", -1);
                  int retCode = event.arg2;
                  if (AIUIConstant.SUCCESS == retCode){
                          // 个性化请求sid,问题排查时可提交讯飞同事
                          mSyncSid = event.data.getString("sid");
                          // 获取上传调用时设置的自定义tag
                          String tag = event.data.getString("tag");
                          switch (dtype){
                              case AIUIConstant.SYNC_DATA_UPLOAD:
                                  Log.e("个性化数据上传成功，tag=" + tag );
                                  break;
                              case AIUIConstant.SYNC_DATA_DOWNLOAD:
                                  String base64 = event.data.getString("text", "");
                                  String content = new String(Base64.decode(base64,
                                          Base64.DEFAULT));
                                  Log.e("个性化数据下载成功，内容为: \n" + content );
                                  break;
                              case AIUIConstant.SYNC_DATA_DELETE:
                                  Log.e("个性化数据删除成功，tag=" + tag );
                                  break;
                          }
                      }else {
                          mSyncSid = "";
                          showTip("操作失败，错误码：" + retCode);
                      }
              }
          }break;
      }
  }
}
```

## 生效使用

个性化数据生效使用，按照AIUI参数配置也分两种方式：

- aiui.cfg静态参数配置
- 动态参数设置或请求参数写入

#### 2.4.1. 静态参数配置生效

在aiui参数配置文件aiui.cfg中直接配置pers\_param参数，可以多种级别的动态实体同时设置。
加载用户级和应用级别动态实体资源：

```json
{
    "audioparams": {
        "pers_param":"{\"appid\":\"\",\"uid\":\"\"}"
    }
}
```

#### 2.4.2. 动态参数配置生效

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
