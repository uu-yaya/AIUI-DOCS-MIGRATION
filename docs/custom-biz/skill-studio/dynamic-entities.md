---
title: 动态实体
---

::: info 概述
**实体**：就是词库，在语料中与词槽绑定的内容，模板语料中词槽用{}包裹。`例：{city}词槽绑定的实体词库包含北京，上海，深圳`
:::

### 1.1. 动态实体的资源

一个动态实体可以包含多个资源(Resource)，资源定义中包含了`资源名称`，`生效维度`、`词条字段名`、`词条别名字段`。

![](/media/202305/2023-05-12_151507_3275640.8786141149674311.png)

**资源**包含以下几个重要属性：

**资源名称**：词条资源在当前账号下唯一的名字，一般搭配命名空间使用，如在后文中，配置resName字段值`为namespace.资源名称`（如：OS0000007.entity\_app）格式内容。命名空间获取见下文。

**资源维度**：即词条的**生效维度**，有`应用级`、`用户级`、`自定义级`，在客户端上传对应的资源数据时，维度信息（包括维度名称和维度值）需要和定义时保持一致。
具体使用可见后文实体上传和请求部分。

| 生效维度 | 维度名称 | 维度值 |
| --- | --- | --- |
| 应用级 | AppID | 如：e0xxxx5e |
| 用户级 | uid（SDK) auth\_id（http：上传、查询；weboscket：请求） | 如：sn007 auth\_id需要为32位字符串，包括英文小写字母与数字 |
| 自定义级 | 自定义维度名称，如上图中为custom\_id | 如：custom\_007 |

**词条名字段**：默认为`name`，可在动态实体页面按需修改

**词条别名字段**：默认为`alias`，可在动态实体页面按需修改、添加

> 1. 一个动态实体下可配置多个维度的资源（见上图）
> 2. 如果需要在SDK和websocket使用同一套用户级动态实体内容，需要将uid和auth\_id均设置为32位字符串。

### 1.2. 生效维度

#### 1.2.1. 应用级

在同一个appid下生效的资源内容

<!-- TODO: 需手动补充图片，原始 URL: https://xfyun-doc.cn-bj.ufileos.com/1516610912333334/2应用级.jpg -->
![待补充：动态实体应用级作用域示意图](/images/placeholder.svg)

**举例**
以开发《水浒传》和《西游记》2个app为例：

```text
用户说法：
    《水浒传》：介绍李逵
    《西游记》：介绍孙悟空

提取说法语料加入小说技能：介绍{name}
```

《水浒传》和《西游记》均使用了小说技能，但上传的name实体内容不同。

| 水浒传 name 实体 | 西游记 name 实体 |
| --- | --- |
| 宋江 | 唐僧 |
| 鲁智深 | 孙悟空 |
| 林冲 | 猪八戒 |
| …… | …… |

`动态实体(应用级)`可以在实体名相同的情况下，为每个 AppID 设置不同的词库，永久生效。

#### 1.2.2. 用户级

在同一个设备id下生效的资源内容
<!-- TODO: 需手动补充图片，原始 URL: https://xfyun-doc.cn-bj.ufileos.com/1516610928159418/3用户级.jpg -->
![待补充：动态实体用户级作用域示意图](/images/placeholder.svg)

**举例**
以打电话技能为例：

```text
用户说法：打给张三，打给李四
抽象为技能：打给{contacts}
```

不同用户的联系人不同，使用`用户级动态实体`为每个用户配置一个私有词库，永久生效。

#### 1.2.3. 自定义级

在同一个`自定义级别维度的值`下生效的资源内容

<!-- TODO: 需手动补充图片，原始 URL: https://xfyun-doc.cn-bj.ufileos.com/1516610939214227/4自定义级.jpg -->
![待补充：动态实体自定义级作用域示意图](/images/placeholder.svg)

**举例**
以全国连锁餐厅点餐 App 为例

```text
用户说法：我想吃杭椒牛柳，我想吃宫保鸡丁
抽象为技能：我想吃{meal}
```

因不同省份的菜单不一样，无法使用同一份实体内容，因此使用`自定义级动态实体`来支持不同的菜单内容。

新建`动态实体meal`，在这个实体下添加资源维度为自定义级的资源，如`meal_province`，资源维度设置为`province`。
技能工作室内设置如下：

![](/media/202305/2023-05-12_154130_5599090.3894091528683097.png)

可以通过设置维度名 province的维度值为不同省份，上传各个省份的菜单。例如：

| 维度名 | 维度值 | 词条内容 |
| --- | --- | --- |
| province | beijing | 北京烤鸭、驴打滚 |
| province | guangdong | 猪脚饭、卤鹅饭 |
| province | shandong | 葱烧海参、把子肉 |

使用`自定义级动态实体`开发者可以自定义分组，实体设置成功后，只对属于特定分组的终端生效。

---

## 动态实体的上传及使用

动态实体的使用有2种方式： WebAPI 接口、 AIUI SDK。

动态实体的使用分三步：

1. 上传资源：每次上传都会覆盖之前的资源数据
2. 查询打包状态以生效
3. 请求命中

Android、iOS、Windows、Linux 推荐通过`CMD_SET_PARAMS`设置`pers_param`使之生效，WebSocket API 应用推荐传`pers_param`参数使之生效。

### 2.1. WebAPI

通过 HTTP 上传动态实体。

- 为了授权认证，调用接口需要将nameSpace，nonce，curtime和checkSum信息放在HTTP请求头中。
- 所有接口统一为UTF-8编码。
- 所有接口支持http和https。

**调用示例Demo**

[Github](https://github.com/IflytekAIUI/DemoCode/tree/master/webapi_v2_entity)

#### 2.1.1. 授权认证

**必要参数说明**

- AccountKey：账户级Key
- namespace：命名空间,代表用户唯一标识

AccountKey和namespace可在技能控制台查看相关值：
![](/media/202304/2023-04-04_140636_3941070.2450630459741926.png)

- 资源名称：动态实体里的资源标识，在动态实体中查看

![](/media/202304/2023-04-04_143333_9541120.04796546046896455.png)

调用动态实体相关业务接口时，都需要在Http Request Header中加入以下参数作为授权验证

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| X-NameSpace | namespace，命名空间 | 是 |
| X-Nonce | 随机数（最大长度128个字符） | 是 |
| X-CurTime | 当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String) | 是 |
| X-CheckSum | MD5(accountKey + Nonce + CurTime),三个参数拼接的字符串，进行MD5哈希计算 | 是 |

注意：

- CheckSum有效期：出于安全性考虑，每个CheckSum的有效期为5分钟(用curTime计算)，同时CurTime要与标准时间同步，否则，时间相差太大，服务端会直接认为CurTime无效。
- checkSum生成示例：

  ```
  accountKey="abcd1234";
  Nonce="12";
  CurTime="1502607694";
  CheckSum=MD5(accountKey+Nonce+CurTime);
  //最终CheckSum输出为32位小写字符串 bf5aa1f53bd173cf7413bf370ad4bddc
  ```

**IP 白名单**
可通过设置ip白名单来限制调用服务的设备来源。

- 关闭状态：只要appid和appkey正确就能使用AIUI 服务
- 开启状态：授权认证通过后，系统检查请求方ip是否在白名单中，非白名单ip请求则拒绝服务。

![](/media/202305/2023-05-12_155830_8077310.9435715656495699.png)

拒绝服务结果示例：

```json
{
  "code":"20004",
  "desc":"ip非法",
  "data":null,
  "sid":"rwabb52e660@dx6c9b0e56f81d3ef000"
}
```

#### 2.1.2. 上传资源接口

本接口用于上传动态实体资源。

接口地址

```http
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/upload-resource HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

##### 2.1.2.1. 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| appid | string | 是 | 应用id | 5axxx3cf |
| res\_name | String | 是 | 所需上传的资源名称，格式： namespace.动态实体资源名称 | OSxxxxxx.music |
| pers\_param | String | 是 | 个性化参数（json） | {"appid":"xxxxxx"} |
| data | String | 是 | Base64编码的资源 | 示例1 |

其中，pers\_param为个性化参数。示例如下：

| 维度 | 示例 | 说明 |
| --- | --- | --- |
| 应用级 | {"appid":"xxxxxx"} |  |
| 用户级 | {"auth\_id": "d3b6d50a9f8194b623b5e2d4e298c9d6"} | auth\_id为用户唯一ID（32位字符串，包括英文小写字母与数字，开发者需保证该值与终端用户一一对应） |
| 自定义级 | {"xxxxxx”:”xxxxxx"} |  |

data为web页面定义的主字段、从字段给的json格式对应的base64。例如，主字段为song、从字段singer，上传资源的格式为：

```json
{"song":"给我一首歌的时间","singer":"周杰伦"}
{"song":"忘情水","singer":"刘德华"}
```

注：

1. 每条数据之间用换行符隔开。
2. 代码拼接时需要在第一行前边添加换行符

Base64编码为

```
eyJzb25nIjoi57uZ5oiR5LiA6aaW5q2M55qE5pe26Ze0Iiwic2luZ2VyIjoi5ZGo5p2w5LymIn0NCnsic29uZyI6IuW/mOaDheawtCIsInNpbmdlciI6IuWImOW+t+WNjiJ9DQp7InNvbmciOiLmmpfpppkiLCJzaW5nZXIiOiLliJjlvrfljY4ifQ0KeyJzb25nIjoi6YCG5YWJIiwic2luZ2VyIjoi5qKB6Z2Z6Iy5In0=
```

##### 2.1.2.2. 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| sid | String | 是 | 本次上传sid，可用于查看上传资源是否成功 | psn003478f3@ch00070e3a78e06f2601 |
| csid | String | 是 | 本次服务唯一标识 | rwa84b7a73b@ch372d0e3a78e0116200 |

#### 2.1.3. 查询打包状态

只有查询后，资源才能正常快速生效

> 上传资源后至少等10秒再查是否成功

接口地址

```http
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/check-resource
    HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

##### 2.1.3.1. 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 是 | sid | psn开头的sid |

##### 2.1.3.2. 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| sid | String | 是 | 上传sid |
| csid | String | 是 | 上传sid |
| reply | String | 是 | 查看上传资源是否成功描述 |
| error | int | 是 | 查看上传资源是否成功错误码 |

#### 2.1.4. 资源生效

资源上传成功后5min生效。你可以通过webapi 请求，传`pers_param`参数验证是否已生效。[查看交互API文档]((/api-dev/classic-chain/interact-api)

#### 2.1.5. 删除资源接口

本接口提供动态实体删除资源功能，用于动态删除实体资源。

接口地址

```http
    POST http[s]://openapi.xfyun.cn/v2/aiui/entity/delete-resource HTTP/1.1
    Content-Type:application/x-www-form-urlencoded; charset=utf-8
```

##### 2.1.5.1. 参数说明

| 参数 | 类型 | 必须 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| appid | string | 是 | 应用id | 5adde3cf |
| res\_name | String | 是 | 资源名,XXX为用户的命名空间 | XXX.music |
| pers\_param | String | 是 | 个性化参数（json），资源生效维度名称和维度值 | {"appid":"xxxxxx"} |

其中，pers\_param为个性化参数。示例如下：

| 维度 | 示例 | 说明 |
| --- | --- | --- |
| 应用级 | {"appid":"xxxxxx"} |  |
| 用户级 | {"auth\_id": "d3b6d50a9f8194b623b5e2d4e298c9d6"} | auth\_id为用户唯一ID（32位字符串，包括英文小写字母与数字，开发者需保证该值与终端用户一一对应） |
| 自定义级 | {"xxxxxx":"xxxxxx"} |  |

##### 2.1.5.2. 返回说明

| 参数名 | 说明 | 是否必须 |
| --- | --- | --- |
| code | 结果码 | 是 |
| data | 返回结果，见data字段说明 | 是 |
| desc | 描述 | 是 |
| sid | 本次webapi服务唯一标识 | 是 |

data字段说明

| 参数 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| sid | String | 是 | 本次删除sid |
| csid | String | 是 | 本次服务唯一标识 |
| reply | String | 是 | 查看删除资源是否成功描述 |
| error | int | 是 | 查看删除资源是否成功错误码 |

---

### 2.2. AIUI SDK

除WebAPI接口外，动态实体的上传也可以配合客户端 SDK 进行，完整文档建议参阅 [AIUI SDK 接入文档](/sdk-dev/basics/)。

#### 2.2.1. 动态实体上传资源数据

上传动态实体数据，伪代码如下：

```text
// 上传动态实体的消息类型
aiuiMessage.msgType = AIUIConstant.CMD_SYNC;
// 上传的同步数据类型
aiuiMessage.arg1 = AIUIConstant.SYNC_DATA_SCHEMA;
aiuiMessage.arg2 = 0;
// 本次上传动态实体的tag标签，非必须
aiuiMessage.params = paramJson.toString();
// 上传的动态实体相关内容信息的base64编码内容，包含动态实体维度、资源名、数据内容
aiuiMessage.data = syncSchemaJson.toString().getBytes(StandardCharsets.UTF_8);
mAIUIAgent.sendMessage(aiuiMessage);
```

AIUIMessage中data需要构建以下结构的json数据:

```json
{
    "param": {
        // 维度
        "id_name": "uid",
        // 维度具体值，当维度取uid或appid时，该值可取空，AIUI会自动补全
        "id_value": "",
        // 资源名称,结构为命名空间.资源名
        "res_name": "XXX.user_applist"
    },
    // 动态实体数据内容的base64编码
    "data": "xxxxxx"
}
```

### 注意：

CheckSum有效期：出于安全性考虑，每个CheckSum的有效期为5分钟(用curTime计算)，同时CurTime要与标准时间同步，否则，时间相差太大，服务端会直接认为CurTime无效。

\*\*XXX为用户的命名空间（namespace），在技能工作室任意一个技能的基本信息中可以查看。\*\*

1. `id_name`与动态实体定义资源时指定的维度对应，如果定义时是用户级，那此处`id_name`就对应`uid`。
2. `id_value`是维度具体值，如`id_name`为`uid`，`id_value`就需要是该资源针对生效的用户的具体UID，AIUI会使用 当前用户UID进行补全，appid同理。自定义维度因为是由开发者自定义，所以`id_name`、`id_value`都需要设置具体值。

> 通过指定`id_name`、`id_value`，上传的动态实体资源数据到服务端就有了唯一的从属，在生效使用时就可以指定此处的`id_name`、`id_value`的值就能[生效使用](#生效使用)当前上传的动态实体资源。

3. `res_name`对应的是平台自定义动态实体资源名，格式：“命名空间.资源名”。
4. data中是原始资源数据的base64编码内容。原始资源数据是包含多条json记录的文本，通过动态实体定义时的抽取字段名可以从每条 json记录中抽取出定义支持的说法。
   如定义资源时词条名字段为appName，词条别名字段为alias，则需要确保每条json记录中都要包含如上的字段（可以包含冗余字段，如下面的extra字段）， 示例如下:

   ```
   {"appName": "微信"， "alias": "wechat", "extra": "xxx"}
   {"appName": "新浪微博"， "alias": "微博", "extra": "yyy"}
   {"appName": "Telegram"， "alias": "电报", "extra": "zzz"}
   {"appName": "讯飞输入法"， "alias": "", "extra": "uuu"}
   ```

   ### 注意：

   1. 每条数据之间用换行符隔开。

   2. 代码拼接时，第一行前边需要添加换行符

   data的实际内容是将以上json数据使用base64编码后的结果。

**同步上传的代码示例**

```
JSONObject syncSchemaJson = new JSONObject();
JSONObject paramJson = new JSONObject();

// 构建param数据
paramJson.put("id_name", "uid");
paramJson.put("res_name", "OSXXX.user_applist");
syncSchemaJson.put("param", paramJson);

// 读取文件内容编码后作为上传的data数据内容
syncSchemaJson.put("data", Base64.encodeToString(./fileUtil.readAssetsFile(context, "file_path"),  Base64.DEFAULT | Base64.NO_WRAP));

// 传入的数据一定要为utf-8编码
byte[] syncData = syncSchemaJson.toString().getBytes("utf-8");

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, "", syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

`CMD_SYNC`消息发出后，会有`EVENT_CMD_RETURN`事件回调，可在回调信息中获取sid，用于打包状态查询:

```java
private void processCmdReturnEvent(AIUIEvent event) {
    switch (event.arg1) {
        case AIUIConstant.CMD_SYNC: {
            int dtype = event.data.getInt("sync_dtype");
            //arg2表示结果，同步成功
            if (AIUIConstant.SUCCESS == event.arg2) {
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

**成功返回结果**

```
// event.data
{
    "error": 0,
    "sid": "psn1fcc6de4@dx000117eda0c9a71401",
    "csid": "atncd13f1a4@aaffff17eda0c90938ff",
    "reply": "success"
}
```

##### 2.2.1.1. 自定义维度动态实体资源上传

对于自定义维度需要用后台定义实体时的自定义维度名作为key，使用[动态上传](#动态上传资源数据)指定的自定义维度作为值。如 后台定义的自定义维度名为vendor，那在[动态上传](#动态上传资源数据)时就需要构造如下数据进行上传:

```json
{
    "param": {
        "AppID": "xxxxxx",// AppID
        "id_name": "vendor",// 自定义维度名
        "id_value": "spec_vendor",  // 自定义维度value
        "res_name": "user_applist"  // 资源名称
    },
    "data": "xxxxxx"// 与schema名称对应的数据内容base64编码
}
```

##### 2.2.1.2. 多组或多维度数据上传

若用户需要同时上传多条数据，但在上传结果回调里无法将上传数据与结果一一对应时，可在上传资源数据时加上sync\_tag标签，数据上传后，在结果回调里也会将此标签带出。用户可通过此标签，将结果与上传数据对应。

上传使用示例如下：

```java
String dataTag = "data_tag_1";
JsonObject params = new JsonObject();
params.put("tag", dataTag);

AIUIMessage syncAthenaMessage = new AIUIMessage(AIUIConstant.CMD_SYNC,AIUIConstant.SYNC_DATA_SCHEMA, 0, params.toString(), syncData);
mAIUIAgent.sendMessage(syncAthenaMessage);
```

结果回调示例如下：

```java
    private void processCmdReturnEvent(AIUIEvent event) {
        switch (event.arg1) {
            case AIUIConstant.CMD_SYNC: {
                int dtype = event.data.getInt("sync_dtype");
                String sync_tag = event.data.getString("tag");
            } break;
        }
    }
```

#### 2.2.2. 查询打包状态

通过`CMD_SYNC`上传同步动态实体的资源数据后，AIUI服务端会进行处理然后生效，处理的过程是异步的，可以间隔10秒后通过`CMD_QUERY_SYNC_STATUS`消息查询上传的资源数据是否处理成功。

arg1表示状态查询的类型，动态实体对应`SYNC_DATA_SCHEMA`（常量对应值为3），params为json，包含需要对应同步上传操作的sid，示例如下:

```
JSONObject paramsJson = new JSONObject();
paramsJson.put("sid", mSyncSid);

AIUIMessage querySyncMsg = new AIUIMessage(AIUIConstant.CMD_QUERY_SYNC_STATUS,AIUIConstant.SYNC_DATA_SCHEMA, 0,paramsJson.toString(), null);
mAIUIAgent.sendMessage(querySyncMsg);
```

`CMD_QUERY_SYNC_STATUS`执行完成后会有`EVENT_CMD_RETURN`事件回调，表示查询结果，解析示例如下:

```java
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

### 注意：

1、请上传资源数据后至少间隔10秒后再进行查询打包状态操作。

2、具体代码示例工程可参考AIUIChatDemo中AIUIRepository类的queryDynamicSyncStatus方法实现。

3、动态实体上传后5min生效。

**成功查询返回**

```json
{
    "error": 0,
    "sid": "psn1fd18e5f@dx000117eda39ca71401",
    "csid": "psn1fd18d30@dx000117eda39ca71401",
    "reply": "success"
}
```

#### 2.2.3. 生效使用

动态实体上传后5min生效。届时可以通过`CMD_SET_PARAMS`设置或cfg文件内配置`pers_param`字段，以使用已上传的的动态实体。
a. `CMD_SET_PARAMS`设置
具体用法参考链接底部动态配置：</sdk-dev/basics/params

b. cfg文件配置

- 生效应用级动态实体：
  如果需要在本机器上生效当前应用对应的所有应用级的动态实体，在`pers_param`加入`\"appid\":\"\"`。值留空， AIUI中会自动补全appid的值。

  ```
  {
    "audioparams": {
        "pers_param":"{\"appid\":\"\"}"
    }
  }
  ```
- 生效用户级动态实体：
  如果需要在本机器上生效当前设备对应的所有用户级的动态实体，在`pers_param`加入`\"uid\":\"\"`。值留空， AIUI中会自动补全uid的值。

  ```
  {
    "audioparams": {
        "pers_param":"{\"uid\":\"\"}"
    }
  }
  ```
- 生效自定义级动态实体：

  ```
  {
    "audioparams": {
        "pers_param":"{\"custom_key\":\"custom_val\"}"
    }
  }
  ```

那对应需要在交互时使用该自定义维度对应的动态实体就需要加入`\"vendor\":\"spec_vendor\"`。

### 注意：

set audioParams这种方式只会对语音交互生效，文本语义参考下面数据写入带pers\_param的方式

```java
public static void MSG_sendTextForNlp(String text, String scene) {
    //aiui未初始化就退出
    if (!AIUI_Initialized()) {
        return;
    }
    // SDK的文本请求需要先手动唤醒后请求
    if (EngineConstants.mAIUIState != AIUIConstant.STATE_WORKING) {
        //先唤醒aiui
        MSG_wakeup(EngineConstants.WAKEUPTYPE_TEXT);
    }
    AIUIMessage msg = new AIUIMessage(0, 0, 0, "", null);
    msg.msgType = AIUIConstant.CMD_WRITE;
    msg.arg1 = 0;
    msg.arg2 = 0;
    // 添加tag，aiuilistener回调将携带tag，可用于关联输入输出
    // 添加per_param，设置本次请求所需的动态实体生效维度
    msg.params = "data_type=text,tag=text-tag,pers_param={\"uid\":\"\"}";
    msg.data = text.getBytes(StandardCharsets.UTF_8);
    mAIUIAgent.sendMessage(msg);
}
```

也可以在音频写入时设置该参数：

```java
//写入音频
byte[] audio = xxx; //初始化
String params = "data_type=audio,sample_rate=16000,pers_param={\"uid\":\"\"}";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, audio);
mAIUIAgent.sendMessage(msg);
```

如需同时生效使用多种级别的动态实体，可直接在`pers_param`里添加对应的级别的参数即可，示例如下：

```json
{
    "audioparams": {
        "pers_param":"{\"AppID\":\"\", \"uid\":\"\"}"
    }
}
```

或

```
audioParams.put("pers_param", "{\"AppID\":\"\", \"uid\":\"\"}");
```

### 注意：

具体代码示例工程可参考[AIUIChatDemo](https://github.com/9oo9le/AIUIChatDemo)中AIUIRepository类的queryDynamicSyncStatus方法实现。

动态实体需要5min才能生效。

### 2.3. 动态实体QA

**Q：上传资源数据返回的状态与查询打包状态有什么区别？**

**A：**上传资源数据时返回的状态代表数据是否上传成功至服务端，主要是用来反馈上传的数据格式是否正确；查询打包状态代表数据上传至后台后是否将这些资源数据处理成功，主要是用来反馈数据能否被正常生效使用。

**Q：动态实体上传失败的原因一般有哪些？**

**A：**

1. res\_name未加上命名空间
2. 上传资源字段与后台不对应

**Q：动态实体不能正常生效使用的原因一般有哪些？**

**A：**

1. 未设置pers\_param参数，即生效维度
2. 上传资源数据时如果是在文本文件里读取的内容，请注意不要将文件的BOM头带入数据中或者直接将其转为无BOM头的文件
3. aiui.cfg文件里未指定appid
4. 动态实体词条存在重复项
