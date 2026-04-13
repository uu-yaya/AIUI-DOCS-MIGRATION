---
title: 回调解析说明
source_url: https://aiui-doc.xf-yun.com/project-1/doc-16/
---

回调解析说明概述

AIUI回调解析是SDK使用中的重要部分，包含回调方式和事件解析两个核心内容，下面进行详细说明。

[**- 1、AIUI SDK回调方式>>>点击跳转**](#AIUI SDK回调方式)
   [**- 2、事件解析>>>点击跳转**](#事件解析)

## AIUI SDK回调方式

AIUI SDK交互中所有结果都是通过初始化时传入的回调对象`AIUIListener`进行数据抛出，端侧做`AIUIEvent`事件解析，监听各项结果输出即可。
在使用过程中，开发者常见可处理结果回调事件类型有（`event.eventType`）：

- 服务链接成功：EVENT\_CONNECTED\_TO\_SERVER
- 唤醒结果：EVENT\_WAKEUP
- 语音交互结果：EVENT\_RESULT
- VAD状态：EVENT\_VAD
- SDK状态：EVENT\_STATE
- 托管SDK播放播放器状态：EVENT\_TTS
- 个性化数据使用：EVENT\_CMD\_RETURN
- SDK报错：EVENT\_ERROR

## 事件解析

### 2.1. 服务链接

`EVENT_CONNECTED_TO_SERVER` 事件属于AIUI SDK与云服务链接建立成功的回调。通常开发者可以不用关心SDK内部链接建立情况，该回调可用于使用场景为：

- 在`传统语义链路`下获取SDK链接建立成功的`uid`信息
  示例代码（Android）：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CONNECTED_TO_SERVER:{
                String uid = event.data.getString("uid");
                Log.i(TAG, "已连接服务器" + uid);
                setText("当前uid:"+uid);
                break;
            }
        }
    }
}
```text

### 2.2. 语音唤醒

`EVENT_WAKEUP`事件属于AIUI SDK唤醒事件的回调，目前支持两种类型回调结果：

- 通过`CMD_WAKEUP`手动唤醒
  对应 event.arg1 = 1，`event.info` 取值为空。
- 通过语音唤醒
  对应 event.arg1 = 0，`event.info` 有具体返回值，具体格式如下（**单麦语音唤醒**可忽略除 `keyword` 外其他字段取值）：

```json
{
    "angle": 0,
    "beam": 0,
    "ivw_result": {
        "angle": 0,                                    // 角度，单麦唤醒忽
        "beam": 0,                                    // 波束，单麦唤醒忽略
        "end_ms": 3430,
        "keyword": "xiao3 fei1 xiao3 fei1",        // 匹配的唤醒词
        "physical": 0,
        "power": 0,
        "score": 1054,                            // 唤醒得分
        "start_ms": 2730
    },
    "type": 0                                    // 唤醒类型，非免唤醒方案忽略
}
```java

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_WAKEUP:{
                String info = event.info;
                Log.i(TAG, "on EVENT_WAKEUP: " + info);
                if(info != null &&  !info.isEmpty()){
                    JSONObject jsInfo = new JSONObject(info);
                    String ivwResult = jsInfo.getString("ivw_result");
                    JSONObject ivwInfo = new JSONObject(ivwResult);
                    String keyword = ivwInfo.getString("keyword");
                    Log.i("本次唤醒为：" + keyword);
                }
                break;
            }
        }
    }
}
```text

### 2.3. 语音交互结果

`EVENT_RESULT`事件属于AIUI SDK交互结果回调。AIUI数据交互不区分在线、离线，也不区分语音还是文本，离线引擎或在线服务返回的结果都通过该回调事件抛出。
解析 `event.info` 获取结果格式如下：

```json
{
    "data": [
        {
            "content": [
                {
                    "cnt_id": "0",
                    "dte": "utf8"
                }
            ],
            "params": {
                "sub": "iat"        // 结果标识符
            }
        }
    ]
}
```

`sub`字段确定结果类型，下面按照在线和离线交互场景细分如下：

温馨提示

1、注意传统语义链路下 **nlp** 与大模型相关链路下 **cbm\_semantic** 和 **nlp** 结果的区别.

2、合成 **tts** 不区分在线和离线.

|  |  |  |
| --- | --- | --- |
| **交互场景** | **sub取值** | **结果介绍** |
| **离线交互** | esr\_pgs | 离线听写流式结果 |
| esr\_iat | 离线听写结果 |
| esr\_fsa | 离线命令词结果 |
| tts | 合成结果 |
| **在线交互-传统语义交互链路** | iat | 语音识别结果 |
| nlp | 传统语义技能结果 |
| tpp | 应用后处理结果 |
| tts | 合成结果 |
| itrans | 翻译结果 |
| **在线交互-通用大模型交互链路** | iat | 语音识别结果 |
| cbm\_tidy | 语义规整结果 |
| cbm\_semantic | 传统语义技能结果 |
| cbm\_tool\_pk | 意图落域结果 |
| cbm\_knowledge | 知识溯源结果 |
| nlp | 大模型回复结果 |
| tpp | 应用后处理结果 |
| tts | 合成结果 |
| **在线交互-极速超拟人交互链路** | event | 事件结果（vad事件Bos、Eos，结束交互事件：Silence） |
| iat | 语音识别结果 |
| cbm\_tidy | 语义规整结果 |
| cbm\_semantic | 传统语义技能结果 |
| cbm\_tool\_pk | 意图落域结果 |
| cbm\_knowledge | 知识溯源结果 |
| cbm\_plugin | 智能体结果 |
| nlp | 大模型回复结果 |
| tpp | 应用后处理结果 |
| tts | 合成结果 |

`EVENT_RESULT`的data中包含的结果数据，需要根据info描述信息获取，不同SDK获取的方式有差异：

温馨提示

注意合成**tts**结果解析后是音频数据流，不能和其他结果混合处理（json转义会直接报错）

Android 示例代码：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_RESULT: {
                JSONObject data = new JSONObject(event.info).getJSONArray("data").getJSONObject(0);
                String sub = data.getJSONObject("params").optString("sub");
                JSONObject content = data.getJSONArray("content").getJSONObject(0);

                 if (content.has("cnt_id") && !"tts".equals(sub)) {
                    String cnt_id = content.getString("cnt_id");
                    // 获取结果，业务处理
                    String cntStr = new String(event.data.getByteArray(cnt_id), "utf-8");
                    JSONObject cntJson = new JSONObject(cntStr);
                    ……
                }

                if ("tts".equals(sub)) {
                    // 合成数据获取
                    int dts = content.getInt("dts");
                    String cnt_id = content.getString("cnt_id");
                    byte[] audio = event.data.getByteArray(cnt_id);
                    ……
                }
            }
        }
    }
}
```cpp

iOS/Windows/Linux示例代码：

```cpp
using namespace VA;
Json::Value bizParamJson;
Json::Reader reader;

if(!reader.parse(event.getInfo(), bizParamJson,false)){
    NSLog(@"parse error!,getinfo=%s",event.getInfo());
}

Json::Value data = (bizParamJson["data"])[0];
Json::Value params = data["params"];
Json::Value content = (data["content"])[0];
std::string sub =  params["sub"].asString();

if(sub == "iat"){
    Json::Value empty;
    Json::Value contentId = content.get("cnt_id", empty);

    if(contentId.empty()){
            NSLog(@"Content Id is empty");
            break;
    }
    std::string cnt_id = contentId.asString();
    Buffer *buffer = event.getData()->getBinary(cnt_id.c_str());

    if(NULL != buffer){
        const char * resultStr = (char *) buffer->data();
        if(resultStr == NULL){
            return;
        }
        NSLog(@"resultStr=%s",resultStr);
    }
}
```java

### 2.4. VAD端点检查结果

`EVENT_VAD`事件属于AIUI SDK本地VAD模块结果回调。该回调主要提供音频会话前后端点检测信息，也可以返回识别音频音量信息。

温馨提示

音频音量信息是SDK内部做的数据相关信息映射回调，取值范围为[0,30]

解析方式示例如下：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
                case AIUIConstant.EVENT_VAD: {
                    switch (event.arg1) {
                        case AIUIConstant.VAD_BOS:
                            // 发现前端点
                            break;
                        case AIUIConstant.VAD_VOL:
                            // 交互音频音量回调
                            int audioVol = event.arg2;
                            break;
                        case AIUIConstant.VAD_EOS:
                            // 发现尾端点
                            break;
                        case AIUIConstant.VAD_BOS_TIMEOUT:
                            // 音频无有效信息
                            break;
                    }
                } break;
        }
    }
}
```java

### 2.5. SDK状态

`EVENT_STATE`事件属于AIUI SDK状态结果回调，可以基于该事件判断请求数据是否会被处理。
解析方式示例如下：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
                case AIUIConstant.EVENT_STATE: {    // 状态事件
                    String mAIUIState = event.arg1;
                    if (AIUIConstant.STATE_IDLE == mAIUIState) {
                        // 闲置状态，AIUI未开启
                    } else if (AIUIConstant.STATE_READY == mAIUIState) {
                        // AIUI已就绪，等待唤醒
                    } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                        // AIUI工作中，可进行交互
                    }
                } break;
        }
    }
}
```

### 2.6. 播放器状态

`EVENT_TTS`事件属于AIUI SDK托管合成结果系统播放的播放器状态结果回调，返回播放开始和结束相关事件。
解析方式示例如下：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_TTS: {
                switch (event.arg1) {
                    case AIUIConstant.TTS_SPEAK_BEGIN:
                        Log.i(TAG,"开始播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_PAUSED:
                        Log.i(TAG,"暂停播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_RESUMED:
                        Log.i(TAG,"恢复播放");
                        break;
                    case AIUIConstant.TTS_SPEAK_COMPLETED:
                        Log.i(TAG,"播放完成");
                        break;
                    case AIUIConstant.TTS_SPEAK_PROGRESS:
                        Log.i(TAG,"播放进度"+event.data.getInt("percent"));
                        break;
                    default:
                        break;
                }
            } break;
        }
    }
}
```java

### 2.7. 数据执行

`EVENT_CMD_RETURN`事件属于AIUI SDK进行数据执行相关处理的回调，尝用于`个性化数据使用`和`离线语法操作`相关事件回调。

#### 个性化数据使用

个性化数据操作时的结果回调，按照交互链路处理方式也不同，分为

- 传统语义交互链路
  个性化数据主要分为：`数据上传`和`数据打包查询`操作回调解析。示例如下：

  ```
  //AIUI事件监听器
  private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (AIUIConstant.CMD_SYNC == event.arg1) {    // 数据同步的返回
                    int dtype = event.data.getInt("sync_dtype", -1);
                    int retCode = event.arg2;

                    switch (dtype) {
                        case AIUIConstant.SYNC_DATA_SCHEMA: {
                            if (AIUIConstant.SUCCESS == retCode) {
                                // 上传成功，记录上传会话的sid，以用于查询数据打包状态
                                // 注：上传成功并不表示数据打包成功，打包成功与否应以同步状态查询结果为准，数据只有打包成功后才能正常使用
                                mSyncSid = event.data.getString("sid");

                            } else {
                                mSyncSid = "";
                                showTip("上传失败，错误码：" + retCode);
                            }
                        } break;
                    }
                } else if (AIUIConstant.CMD_QUERY_SYNC_STATUS == event.arg1) {    // 数据同步状态查询的返回
                    // 获取同步类型
                    int syncType = event.data.getInt("sync_dtype", -1);
                    if (AIUIConstant.SYNC_DATA_QUERY == syncType) {
                        // 获取查询结果，结果中error字段为0则表示上传数据打包成功，否则为错误码
                        String result = event.data.getString("result");
                        showTip("查询结果为：" + result);
                    }
                }
            } break;
        }
    }
  }
  ```
- 通用大模型和极速超拟人交互链路
  个性化数据主要分为：`数据上传`、`数据下载`和`数据删除`操作回调解析。示例如下：

  ```
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

#### 离线语法操作

当SDK进行离线语法操作时，例如构建语法，或更新离线槽位取值，可以监听回调获取执行结果，解析示例代码如下：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_CMD_RETURN: {
                if (AIUIConstant.CMD_SYNC == event.arg1) {
                    int dtype = event.data.getInt("sync_dtype", -1);
                    int retCode = event.arg2;

                    switch (dtype) {
                        case AIUIConstant.CMD_BUILD_GRAMMAR:
                            if(retCode == 0){
                                Log.e(TAG,"build grammer success");
                            }else {
                                Log.e(TAG,"build grammer failed");
                            }
                            break;
                        case AIUIConstant.CMD_UPDATE_LOCAL_LEXICON: {
                            Log.d("UPDATE_LOCAL_LEXICON", "arg1 " + event.arg1 + " ret " + event.arg2 + " info " + event.info);
                        }
                    }
                }
            } break;
        }
    }
}
```java

### 2.8. SDK报错

`EVENT_ERROR`事件属于AIUI SDK错误信息结果回调，当报错时获取错误信息和错误码，按照错误码列表描述进行处理。
解析示例如下：

```java
//AIUI事件监听器
private AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_ERROR: {
                int errCode  = event.arg1;
                String errInfo = event.info;
                Log.i("EVENT_ERROR","错误码："+errCode+" ,错误信息："+errInfo);
            }break
        }
    }
}
```
