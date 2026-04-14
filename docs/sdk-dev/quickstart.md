---
title: AIUI SDK 接入流程
---

::: info 概述
本文档主要给开发者提供SDK接入指导。
:::

## 前言

AIUI平台SDK，目前主要覆盖主流开发平台，包括:Android、Windows、Linux、Ios，该类SDK开发者可以通过创建AIUI应用，在应用管理的资源下载页面可直接下载。
另外AIUI针对广大rtos系统对接需求，基于平台最新的极速超拟人服务体系也适配了一套SDK，可以[查看文档](/sdk-dev/ultra-chain/rtos)详细了解。

## SDK接入流程

对接AIUI SDK做程序开发前，首先需要先了解AIUI SDK的服务接口、业务参数、结果回调等。这些部分都可以通过文档 [AIUI SDK基础信息](/sdk-dev/basics/ "AIUI SDK基础信息")查看了解。
当了解完AIUI SDK基础部分后，就可以进行SDK集成开发了。程序开发需要注意一下两点：

- 业务能力
   AIUI平台默认下载的AIUI SDK仅支持在线语音服务，除语音唤醒外，如需其他离线能力可以联系讯飞商务申请线下提供AIUI SDK和引擎资源。
- 服务链路
   根据AIUI应用实际使用的服务链路，对应查看[传统语义链路接入](/sdk-dev/classic-chain/ "传统语义链路接入")、[通用大模型链路接入](/sdk-dev/llm-chain/ "通用大模型链路接入")、[极速超拟人链路接入](/sdk-dev/ultra-chain/ "极速超拟人链路接入")调用方式，各个服务链路的区别详见[AIUI服务链路介绍](/platform-service/service-chain "AIUI服务链路介绍")说明。至于当前AIUI应用具体使用的哪个服务链路，可以查看[AIUI应用介绍](/platform-service/app-intro "AIUI应用介绍")了解。

![](/media/202509/2025-09-16_174624_9954980.5898940674594813.png)

## SDK集成指导

### 3.1. Android 集成步骤

::: warning 注意
其他平台接口有略微差别，但过程一致，具体见下一节其他平台接入参考。
:::

点击“资源下载”，点击下载最新版AIUI SDK。

![](/media/202508/2025-08-15_170442_8356490.26842023261177794.png)

#### 3.1.1. 导入SDK

打开Android Studio，创建一个新的工程，将下载的Android SDK压缩包中libs目录下的libaiui.so以及AIUI.jar拷贝至Android工程的libs目录下，并将SDK包中assets目录下cfg文件夹以及res目录下vad文件夹拷贝至工程中。工程结构如下图所示：

![](/media/202305/2023-05-03_151930_7459390.590354326194595.png)

将AIUI.jar添加至工程依赖，将app module下的gradle配置文件中指定默认jniLibs目录为libs。

```groovy
android {
...
    sourceSets {
        main {
            jniLibs.srcDirs = ['libs']
        }
    }
...
}
```

#### 3.1.1.1. 混淆配置(可选)

```text
-dontoptimize
-keep class com.iflytek.**{*;}
-keepattributes Signature
```

#### 3.1.2. 修改AIUI配置

打开cfg/aiui.cfg，编辑AIUI配置。重点关注的配置项:

login.AppID={你的应用ID}
global.scene={你的场景名称}（注意沙盒场景与线上场景的区别）

![](/media/202305/2023-05-03_151950_4662750.5216125118584767.png)

#### 3.1.3. 设置设备装机量计量标识

使用AIUISetting 系统设置类，传入设备计量标识：SN号

```text
// 取值说明：设置设备唯一标识，保证每台设备不变。
// 调用顺序：在初始化AIUI SDK之前（即createAgent之前）

//设置装机量SN标识,
AIUISetting.setSystemInfo(AIUIConstant.KEY_SERIAL_NUM, "xxx")；
```

#### 3.1.4. 创建AIUIAgent

AIUIAgent是和AIUI交互的桥梁。创建`AIUIAgent`示例：

```text
//创建AIUIAgent
AIUIAgent mAIUIAgent = AIUIAgent.createAgent(context,getAIUIParams(),mAIUIListener);
```

createAgent方法包含三个参数：

- 1.Context；
- 2.String（读取aiui.cfg配置文件而获得的字符串）
- 3.AIUIListener（是AIUI事件回调监听器）

mAIUIListener具体示例如下所示：

```java
AIUIListener mAIUIListener = new AIUIListener() {

    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            //唤醒事件
            case AIUIConstant.EVENT_WAKEUP:
            {
                break;
            }
            //结果事件（包含听写，语义，离线语法结果）
            case AIUIConstant.EVENT_RESULT:
            {
                break;
            }
            //休眠事件
            case AIUIConstant.EVENT_SLEEP:
            {
                break;
            }
            // 状态事件
            case AIUIConstant.EVENT_STATE: {
                mAIUIState = event.arg1;
                if (AIUIConstant.STATE_IDLE == mAIUIState) {
                    // 闲置状态，AIUI未开启
                } else if (AIUIConstant.STATE_READY == mAIUIState) {
                    // AIUI已就绪，等待唤醒
                } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                    // AIUI工作中，可进行交互
                }
            } break;
            //错误事件
            case AIUIConstant.EVENT_ERROR:
            {
                break;
            }
        }
    }
}
```

#### 3.1.5. 语义理解示例

发送CMD\_WAKEUP消息给AIUI，使AIUI处于唤醒状态，再发送开始录音消息，使麦克风录入音频，并通过AIUIListener的回调，获取语义结果。代码示例：

```java
// 先发送唤醒消息，只有唤醒状态才能接收语音输入
if( AIUIConstant.STATE_WORKING != mAIUIState ){
    AIUIMessage wakeupMsg = new AIUIMessage(AIUIConstant.CMD_WAKEUP, 0, 0, "", null);
    mAIUIAgent.sendMessage(wakeupMsg);
}

// 打开AIUI内部录音机，开始录音
String params = "sample_rate=16000,data_type=audio";
AIUIMessage writeMsg = new AIUIMessage( AIUIConstant.CMD_START_RECORD, 0, 0, params, null );
mAIUIAgent.sendMessage(writeMsg);
```

如出现20006错误，请注意下应用是否拥有录音权限。返回的语义结果，参考[语义结果说明文档](/custom-biz/protocols/semantic-protocol)

#### 3.1.6. 结果解析

在AIUIEventListener回调中，可以收到来自AIUI的多种消息，示例：

```java
private AIUIListener mAIUIListener = new AIUIListener() {

    @Override
    public void onEvent(AIUIEvent event) {
        switch (event.eventType) {
            case AIUIConstant.EVENT_WAKEUP:
                //唤醒事件
                Log.i( TAG,  "on event: "+ event.eventType );
            break;

            case AIUIConstant.EVENT_RESULT: {
                //结果解析事件
                try {
                    JSONObject bizParamJson = new JSONObject(event.info);
                    JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
                    JSONObject params = data.getJSONObject("params");
                    JSONObject content = data.getJSONArray("content").getJSONObject(0);

                    if (content.has("cnt_id")) {
                        String cnt_id = content.getString("cnt_id");
                        JSONObject cntJson = new JSONObject(new String(event.data.getByteArray(cnt_id), "utf-8"));
                        String sub = params.optString("sub");
                        if ("nlp".equals(sub)) {
                            // 解析得到语义结果
                            String resultStr = cntJson.optString("intent");
                            Log.i( TAG, resultStr );
                        }
                    }
                } catch (Throwable e) {
                    e.printStackTrace();
                }
            } break;

            case AIUIConstant.EVENT_ERROR: {
                //错误事件
                Log.i( TAG,  "on event: "+ event.eventType );
                Log.e(TAG, "错误: "+event.arg1+"\n"+event.info );
            } break;

            case AIUIConstant.EVENT_VAD: {
                if (AIUIConstant.VAD_BOS == event.arg1) {
                    //语音前端点
                } else if (AIUIConstant.VAD_EOS == event.arg1) {
                    //语音后端点
                }
            } break;

            case AIUIConstant.EVENT_START_RECORD: {
                Log.i( TAG,  "on event: "+ event.eventType );
                //开始录音
            } break;

            case AIUIConstant.EVENT_STOP_RECORD: {
                Log.i( TAG,  "on event: "+ event.eventType );
                // 停止录音
            } break;

            case AIUIConstant.EVENT_STATE: {
                // 状态事件
                mAIUIState = event.arg1;
                if (AIUIConstant.STATE_IDLE == mAIUIState) {
                    // 闲置状态，AIUI未开启
                } else if (AIUIConstant.STATE_READY == mAIUIState) {
                    // AIUI已就绪，等待唤醒
                } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                    // AIUI工作中，可进行交互
                }
            } break;

            default:
                break;
        }
    }
};
```

将语义结果输出到屏幕，同时将合成结果播报出来。至此，就将应用能力添加到开发者应用中，此时开启应用，语音输入“我要查信息”开启对话，完成演示。
![](/media/202305/2023-05-03_152225_2678220.6065979187037359.png)

### 3.2. Windows&Linux 集成步骤

#### 3.2.1. 导入SDK

在cmake工程里将include及lib文件夹加入到工程中，可参考aiui\_sample中的CMakeList.txt

```cpp
include_directories(${CMAKE_CURRENT_LIST_DIR}/../../include)
link_directories(${CMAKE_CURRENT_LIST_DIR}/../../libs/${PLATFORM})
link_libraries(aiui)
```

#### 3.2.2. 添加配置文件和资源文件

开发者需要将aiui\_sample/build 中AIUI文件夹添加到开发者自己的工程中，该文件夹下包括AIUI需要读取的配置参数文件和语音识别过程中需要的vad资源。

#### 3.2.3. 初始化前系统设置

- 日志设置相关
  设置日志是否开启、日志打印级别和设置工作目录等。只需要保证在创建AIUI客户端代理之前调用即可，开发者可以自行选择。
- 装机量统计
  设置设备统计唯一标识

```cpp
    // AIUI工作目录和日志设置
    AIUISetting::setAIUIDir("./AIUI/");
    AIUISetting::setNetLogLevel(aiui::_none);
    AIUISetting::setLogLevel(aiui::_none);
    // 装机量设置
    AIUISetting::setSystemInfo(AIUI_KEY_SERIAL_NUM, "xxx");
```

#### 3.2.4. 创建AIUIAgent

AIUIAgent就是和AIUI交互的桥梁。先创建AIUIAgent，然后发送唤醒消息使AIUI处于Working状态，示例：

```cpp
string fileParam = readFileAsString("./AIUI/cfg/aiui.cfg");
agent = IAIUIAgent::createAgent(fileParam.c_str(), &listener);
```

#### 3.2.5. 语义理解示例

发送CMD\_WAKEUP消息至AIUI，使AIUI处于唤醒状态，再发送文本数据，代码示例如下：

```cpp
//发送唤醒消息
IAIUIMessage* wakeupMsg = IAIUIMessage::create(AIUIConstant::CMD_WAKEUP);
agent->sendMessage(wakeupMsg);
wakeupMsg->destroy();

//发送开始文本消息
string text = "合肥明天天气怎么样";
Buffer* textData = Buffer::alloc(text.length());
text.copy((char*)textData->data(), text.length());

IAIUIMessage* writeMsg = IAIUIMessage::create(
        AIUIConstant::CMD_WRITE, 0, 0, "data_type=text,tts_res_type=url", textData);
agent->sendMessage(writeMsg);
writeMsg->destroy();
```

#### 3.2.6. 结果回调

实现IAIUIListener协议类接口，在onEvent事件获取结果回调。代码示例如下：

```java
class MyListener : public IAIUIListener
{
public:
    void onEvent(const IAIUIEvent& event) const override
    {
        switch (event.getEventType()) {
            //SDK 状态回调
            case AIUIConstant::EVENT_STATE: {
                switch (event.getArg1()) {
                    case AIUIConstant::STATE_IDLE: {
                        cout << "EVENT_STATE:"
                             << "IDLE" << endl;
                    } break;

                    case AIUIConstant::STATE_READY: {
                        cout << "EVENT_STATE:"
                             << "READY" << endl;
                    } break;

                    case AIUIConstant::STATE_WORKING: {
                        cout << "EVENT_STATE:"
                             << "WORKING" << endl;
                    } break;
                }
            } break;
                //唤醒事件回调
            case AIUIConstant::EVENT_WAKEUP: {
                cout << "EVENT_WAKEUP:" << event.getInfo() << endl;
            } break;
                //休眠事件回调
            case AIUIConstant::EVENT_SLEEP: {
                cout << "EVENT_SLEEP:arg1=" << event.getArg1() << endl;
            } break;
                //VAD事件回调，如找到前后端点
            case AIUIConstant::EVENT_VAD: {
                switch (event.getArg1()) {
                    case AIUIConstant::VAD_BOS: {
                        cout << "EVENT_VAD: BOS" << endl;
                    } break;

                    case AIUIConstant::VAD_EOS: {
                        cout << "EVENT_VAD: EOS" << endl;
                    } break;

                    case AIUIConstant::VAD_VOL: {
                        cout << "EVENT_VAD: VOL" << endl;
                    } break;
                }
            } break;
                //最重要的结果事件回调
            case AIUIConstant::EVENT_RESULT: {
                Json::Value bizParamJson;
                Json::Reader reader;

                if (!reader.parse(event.getInfo(), bizParamJson, false)) {
                    cout << "parse error!" << endl << event.getInfo() << endl;
                    break;
                }
                Json::Value& data = (bizParamJson["data"])[0];
                Json::Value& params = data["params"];
                Json::Value& content = (data["content"])[0];

                string sub = params["sub"].asString();

                if (sub == "nlp" || sub == "iat" || sub == "tts" || sub == "asr") {
                    Json::Value empty;
                    Json::Value contentId = content.get("cnt_id", empty);

                    if (contentId.empty()) {
                        cout << "Content Id is empty" << endl;
                        break;
                    }

                    string cnt_id = contentId.asString();
                    int dataLen = 0;
                    const char* buffer = event.getData()->getBinary(cnt_id.c_str(), &dataLen);

                    if (sub == "tts") {
                        Json::Value&& isUrl = content.get("url", empty);

                        if (isUrl.asString() == "1") {
                            std::cout << string(buffer, dataLen) << std::endl;
                        } else {
                            std::cout << event.getInfo() << std::endl;
                        }
                    } else {
                        if (buffer) {
                            string resultStr = string(buffer, dataLen);
                            cout << sub << ": " << resultStr << endl;
                        }
                    }
                }
            } break;

                //上传资源数据的返回结果
            case AIUIConstant::EVENT_CMD_RETURN: {
                if (AIUIConstant::CMD_BUILD_GRAMMAR == event.getArg1()) {
                    if (event.getArg2() == 0) {
                        cout << "build grammar success." << endl;
                    } else {
                        cout << "build grammar error, errcode = " << event.getArg2() << endl;
                        cout << "error reasion is " << event.getInfo() << endl;
                    }
                } else if (AIUIConstant::CMD_UPDATE_LOCAL_LEXICON == event.getArg1()) {
                    if (event.getArg2() == 0) {
                        cout << "update lexicon success" << endl;
                    } else {
                        cout << "update lexicon error, errcode = " << event.getArg2() << endl;
                        cout << "error reasion is " << event.getInfo() << endl;
                    }
                }
            } break;

            case AIUIConstant::EVENT_ERROR: {
                cout << "EVENT_ERROR:" << event.getArg1() << endl;
                cout << " ERROR info is " << event.getInfo() << endl;
            } break;
        }
    }
};
```

#### 3.2.7. 多语言调用

为了方便非C/C++开发者的快速集成，SDK也提供C接口，以供其他开发者使用，需要注意的是，Windows平台下函数导出基于`__stdcall`调用，其他平台则是基于`__cdecl` 调用，所所有接口如下，具体含义可参考C++的接口

```java
const char *aiui_get_version();

/*******************************AIUIDataBundle********************************/
typedef void* AIUIDataBundle;

int aiui_db_int(AIUIDataBundle db, const char* key, int defaultVal);
long aiui_db_long(AIUIDataBundle db, const char* key, long defaultVal);
const char *aiui_db_string(AIUIDataBundle db, const char* key, const char* defaultVal);
const char *aiui_db_binary(AIUIDataBundle db, const char* key, int* dataLen);

/*******************************AIUI_AIUIEvent*********************************/
typedef void* AIUIEvent;
typedef void (*AIUIMessageCallback)(const AIUIEvent ae, void *data);

int aiui_event_type(const AIUIEvent ae);
int aiui_event_arg1(const AIUIEvent ae);
int aiui_event_arg2(const AIUIEvent ae);
const char *aiui_event_info(const AIUIEvent ae);
AIUIDataBundle aiui_event_databundle(const AIUIEvent ae);
int aiui_strlen(const char * str);

/**********************************AIUIBuffer***********************************/
typedef void* AIUIBuffer;

void aiui_buffer_destroy(AIUIBuffer ab);
AIUIBuffer aiui_create_buffer_from_data(const void* data, size_t len);

/**********************************AIUIMessage**********************************/
typedef void* AIUIMessage;

AIUIMessage aiui_msg_create(int msgType, int arg1, int arg2, const char* params, AIUIBuffer data);
void aiui_msg_destroy(AIUIMessage msg);

/***********************************AIUI_Agent***********************************/
typedef void* AIUIAgent;
AIUIAgent aiui_agent_create(const char* params, AIUIMessageCallback callback, void *data);
void aiui_agent_send_message(AIUIAgent agent, AIUIMessage msg);
void aiui_agent_destroy(AIUIAgent agent);

/***********************************AIUI_Setting**********************************/
enum LogLevel { _info, _debug, _warn, _error, _none };

bool aiui_set_aiui_dir(const char* szDir);
const char * aiui_get_aiui_dir();
bool aiui_set_msc_dir(const char* szDir);
bool aiui_set_msc_cfg(const char* szCfg);
bool aiui_init_logger(const char* szLogDir = "");
void aiui_set_log_level(LogLevel level);
void aiui_set_net_log_level(LogLevel level);
void aiui_set_save_data_log(bool save, int logSizeMB = -1);
bool aiui_set_data_log_dir(const char* szDir);
bool aiui_set_raw_audio_dir(const char* dir);
bool aiui_is_mobile_version();
void aiui_set_system_info(const char* key, const char* val);
```

##### 3.2.7.1. python

```java
#引入库
# windows
aiui = ctypes.windll.LoadLibrary("aiui.dll")
# Linux
aiui = ctypes.cdll.LoadLibrary("libaiui.so")

class AIUIEventListener:
    @abc.abstractmethod
    def OnEvent(self, ev: IAIUIEvent): #回调函数
        pass

class IAIUIAgent:
    aiui_agent = None
    listenerWrapper = None
    AIUIListenerCallback = None

    def __init__(self, aiui_agent):
        self.aiui_agent = aiui_agent
        self.aiui_agent_send_message = aiui.aiui_agent_send_message
        self.aiui_agent_send_message.argtypes = [c_void_p, c_void_p]
        self.aiui_agent_destroy = aiui.aiui_agent_destroy
        self.aiui_agent_destroy.argtypes = [c_void_p]

    # 函数原型 void aiui_agent_send_message(void* agent, void *msg)
    def sendMessage(self, msg: IAIUIMessage):
        return self.aiui_agent_send_message(self.aiui_agent, msg.aiui_msg)

    # 函数原型 void aiui_agent_destroy(void* agent)
    def destroy(self):
        self.aiui_agent_destroy(self.aiui_agent)
        self.AIUIListenerCallback = None
        self.listenerWrapper = None
        self.aiui_agent = None

    # 函数原型 IAIUIAgent *aiui_agent_create(const char *cfg, void *listener, void *user_data)
    @staticmethod
    def createAgent(params: str, listener):
        _f = aiui.aiui_agent_create
        _f.argtypes = [c_char_p, c_void_p, c_void_p]
        _f.restype = c_void_p

        agent = IAIUIAgent(None)
        agent.listenerWrapper = EventCallback(listener)
        agent.AIUIListenerCallback = CFUNCTYPE(None, c_void_p, c_void_p)(agent.listenerWrapper)
        agent.aiui_agent = _f(c_char_p(params.encode('utf-8')), agent.AIUIListenerCallback, None)

        return agent
```

##### 3.2.7.2. C#

```java
class IAIUIAgent {
    public delegate void AIUIMessageCallback(IAIUIEvent ev);
    private IntPtr mAgent = IntPtr.Zero;
    private static AIUIMessageCallback messageCallback;

    private static void onEvent(IntPtr ev_) {
        messageCallback(new IAIUIEvent(ev_));
    }
    private IAIUIAgent(AIUIMessageCallback cb, IntPtr agent) {
        messageCallback = cb;
        mAgent = agent;
    }
    public static IAIUIAgent Create(string param, AIUIMessageCallback cb) {
        return new IAIUIAgent(cb, aiui_agent_create(Marshal.StringToHGlobalAnsi(param), onEvent));
    }
    public void SendMessage(IAIUIMessage msg) {
        if (IntPtr.Zero != mAgent)
            aiui_agent_send_message(mAgent, msg.Ptr);
    }
    public void Destroy() {
        if (IntPtr.Zero != mAgent) {
            aiui_agent_destroy(mAgent);
            mAgent = IntPtr.Zero;
        }
    }

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    private delegate void AIUIMessageCallback_(IntPtr ev);

    [DllImport("aiui", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.StdCall)]
    private extern static IntPtr aiui_agent_create(IntPtr param, AIUIMessageCallback_ cb);

    [DllImport("aiui", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.StdCall)]
    private extern static void aiui_agent_send_message(IntPtr agent, IntPtr msg);

    [DllImport("aiui", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.StdCall)]
    private extern static void aiui_agent_destroy(IntPtr agent);
}
```

### 3.3. iOS 集成步骤

#### 3.3.1. 导入SDK

将下载的iOS SDK压缩包中l的iflyAIUI.framework添加到开发者工程中，配置iflyAIUI.framework路径。假设开发者的Xcode工程目录与iflyAIUI.framework的目录位置关系是如下图所示这样的：

![](/media/202506/2025-06-10_142129_8196260.6420059247793698.png)

那么，开发者需要注意正确设置iflyAIUI.framework的路径：
依次点击TARGETS -> Build Setting -> Framework Search Path,双击修改路径，如下图所示。

![](/media/202506/2025-06-10_142203_8832440.5574866970491155.png)

#### 3.3.2. 添加配置文件和资源文件

开发者需要将AIUIDemo中resource文件夹添加到开发者自己的工程中，该文件夹下包括AIUI需要读取的配置参数文件和语音识别过程中需要的vad资源。

#### 3.3.3. 添加系统库依赖

开发者集成AIUI SDK可以复用AIUIDemo中的部分源码以提高开发效率。AIUIService.h、AIUIService.mm、TTSViewController.h、TTSViewController.m、UnderstandViewController.h以及UnderstandViewController.mm 等文件实现了AIUI SDK 接口调用参考示例，由于这些文件使用C++和OC编写，开发者在使用XCode进行编译时要额外注意添加libicucore.tbd、libc++.tbd和libz.tbd三个系统库依赖。如下图所示：

![](/media/202506/2025-06-10_142219_0537080.20679774358792424.png)

#### 3.3.4. 设置Bitcode

Xcode 7,8默认开启了Bitcode，而Bitcode 需要工程依赖的所有类库同时支持。AIUI SDK暂时还不支持Bitcode，需要开发者关闭该设置。只需在Targets -> Build Settings 中搜索Bitcode 即可，找到相应选项，设置为NO。 如下图所示：

![](/media/202506/2025-06-10_142228_6439660.6344005846999853.png)

#### 3.3.5. 用户隐私权限配置

iOS 10增加了隐私权限设置，可在info.plist 新增相关privacy字段，AIUI SDK需要的权限：麦克风、联系人、地理位置：

```xml
<key>NSMicrophoneUsageDescription</key>
<string></string>
<key>NSLocationUsageDescription</key>
<string></string>
<key>NSLocationAlwaysUsageDescription</key>
<string></string>
<key>NSContactsUsageDescription</key>
<string></string>
```

即在Info.plist 中增加下图设置：

![](/media/202506/2025-06-10_142254_2070930.7206896687926101.png)

#### 3.3.6. 初始化工作目录

AppDelegate中初始化，设置日志是否开启、日志打印级别和设置工作目录等。初始化设置不强制要求放在在AppDelegate中，只需要保证在创建AIUI客户端代理之前调用即可，开发者可以自行选择。

```
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{

    NSArray  *paths = NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask, YES);

    NSString *cachePath = [paths objectAtIndex:0];
    cachePath = [cachePath stringByAppendingString:@"/"];
    NSLog(@"cachePath=%@",cachePath);

    [IFlyAIUISetting setSaveDataLog:NO];
    [IFlyAIUISetting setLogLevel:LV_INFO];
    [IFlyAIUISetting setAIUIDir:cachePath];
    [IFlyAIUISetting setMscDir:cachePath];

    return YES;
}
```

#### 3.3.7. 创建AIUIAgent

SDK中提供的AIUIAgent就是和AIUI交互的桥梁。先创建AIUIAgent，然后发送唤醒消息使AIUI处于Working状态，示例如下：

```objc
@property IFlyAIUIAgent *aiuiAgent;

// 读取aiui.cfg配置文件
NSString *cfgFilePath = [[NSBundle mainBundle] pathForResource:@"aiui" ofType:@"cfg"];
NSString *cfg = [NSString stringWithContentsOfFile:cfgFilePath encoding:NSUTF8StringEncoding error:nil];

//创建AIUIAgent
_aiuiAgent = [IFlyAIUIAgent createAgent:cfg withListener:self];
```

#### 3.3.8. 语义理解示例

发送CMD\_WAKEUP消息至AIUI，使AIUI处于唤醒状态，再发送开始录音消息，使麦克风录入音频。代码示例如下：

```objc
//发送唤醒消息
IFlyAIUIMessage *wakeuMsg = [[IFlyAIUIMessage alloc]init];
wakeuMsg.msgType = CMD_WAKEUP;
[_aiuiAgent sendMessage:wakeuMsg];

//发送开始录音消息
IFlyAIUIMessage *msg = [[IFlyAIUIMessage alloc] init];
msg.msgType = CMD_START_RECORD;
[_aiuiAgent sendMessage:msg];
```

#### 3.3.9. 结果回调

实现IFlyAIUIListener协议类接口，在onEvent事件获取结果回调。代码示例如下：

```objc
- (void) onEvent:(IFlyAIUIEvent *) event {

    switch (event.eventType) {

        case EVENT_CONNECTED_TO_SERVER:
        {
            //服务器连接成功事件
            NSLog(@"CONNECT TO SERVER");
        } break;

        case EVENT_SERVER_DISCONNECTED:
        {
            //服务器连接断开事件
            NSLog(@"DISCONNECT TO SERVER");
        } break;

        case EVENT_START_RECORD:
        {
            //开始录音事件
            NSLog(@"EVENT_START_RECORD");
        } break;

        case EVENT_STOP_RECORD:
        {
            //停止录音事件
            NSLog(@"EVENT_STOP_RECORD");
        } break;

        case EVENT_STATE:
        {
            //AIUI运行状态事件
            switch (event.arg1)
            {
                case STATE_IDLE:
                {
                    NSLog(@"EVENT_STATE: %s", "IDLE");
                } break;

                case STATE_READY:
                {
                    NSLog(@"EVENT_STATE: %s", "READY");
                } break;

                case STATE_WORKING:
                {
                    NSLog(@"EVENT_STATE: %s", "WORKING");
                } break;
            }
        } break;

        case EVENT_WAKEUP:
        {
            //唤醒事件
            NSLog(@"EVENT_WAKEUP");
        } break;

        case EVENT_SLEEP:
        {
            //休眠事件
            NSLog(@"EVENT_SLEEP");
        } break;

        case EVENT_VAD:
        {
            switch (event.arg1)
            {
                case VAD_BOS:
                {
                        //前端点事件
                    NSLog(@"EVENT_VAD_BOS");
                } break;

                case VAD_EOS:
                {
                    //后端点事件
                    NSLog(@"EVENT_VAD_EOS");
                } break;

                case VAD_VOL:
                {
                        //音量事件
                    NSLog(@"vol: %d", event.arg2);
                } break;
            }
        } break;

        case EVENT_RESULT:
        {
            NSLog(@"EVENT_RESULT");
            [self processResult:event];
        } break;

        case EVENT_CMD_RETURN:
        {
            NSLog(@"EVENT_CMD_RETURN");
        } break;

        case EVENT_ERROR:
        {
            NSString *error = [[NSString alloc] initWithFormat:@"Error Message：%@\nError Code：%d",event.info,event.arg1];
            NSLog(@"EVENT_ERROR: %@",error);
        } break;
    }
}

//处理结果
- (void)processResult:(IFlyAIUIEvent *)event{

    NSString *info = event.info;
    NSData *infoData = [info dataUsingEncoding:NSUTF8StringEncoding];
    NSError *err;
    NSDictionary *infoDic = [NSJSONSerialization JSONObjectWithData:infoData options:NSJSONReadingMutableContainers error:&err];
    if(!infoDic){
        NSLog(@"parse error! %@", info);
        return;
    }

    NSLog(@"infoDic = %@", infoDic);

    NSDictionary *data = [((NSArray *)[infoDic objectForKey:@"data"]) objectAtIndex:0];
    NSDictionary *params = [data objectForKey:@"params"];
    NSDictionary *content = [(NSArray *)[data objectForKey:@"content"] objectAtIndex:0];
    NSString *sub = [params objectForKey:@"sub"];

    if([sub isEqualToString:@"nlp"]){

        NSString *cnt_id = [content objectForKey:@"cnt_id"];
        if(!cnt_id){
            NSLog(@"Content Id is empty");
            return;
        }

        NSData *rltData = [event.data objectForKey:cnt_id];
        if(rltData){
            NSString *rltStr = [[NSString alloc]initWithData:rltData encoding:NSUTF8StringEncoding];
            NSLog(@"nlp result: %@", rltStr);
        }
    } else if([sub isEqualToString:@"tts"]){
        NSLog(@"receive tts event");

        NSString *cnt_id = [content objectForKey:@"cnt_id"];
        if(cnt_id){
            //合成音频数据
            NSData *audioData = [event.data objectForKey:cnt_id];

            //当前音频块状态：0（开始）,1（中间）,2（结束）,3（一块）
            int dts = [(NSNumber *)[content objectForKey:@"dts"] intValue];

            //合成进度
            int text_per = [(NSNumber *)[content objectForKey:@"text_percent"] intValue];

            NSLog(@"dataLen=%lu, dts=%d, text_percent=%d", (unsigned long)[audioData length], dts, text_per);
        }
    }
}
```
