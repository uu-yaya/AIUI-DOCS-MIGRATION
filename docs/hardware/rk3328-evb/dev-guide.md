---
title: RK3328 评估板开发手册
---

## 集成方式

AIUI评估板开发套件提供了多种集成方式，开发者可以根据自己的业务场景灵活选择。在后期量产时，请[联系我们](/faq/contact)获取更完整的集成流程和技术支持。下面为您详细介绍这几种集成方式。

## 1.1. 核心板模式

### 1.1.1. 适用场景

适用于故事机、智能音箱等一些无屏交互的场景。

### 1.1.2. 集成说明

开发者APP集成[AIUIServiceKit](/hardware/legacy-evb/aiui-service-kit)，运行在AIUI模块上，从AIUIService获取结果，进行解析处理，与评估板开发套件上AIUIProductDemo的效果类似，完整结构如下图所示：

![null](/media/202309/1695879568.0513992.png)

图1 核心板模式集成图示

具体集成方法请参见[AIUIServiceKit SDK](/hardware/legacy-evb/integration)。

### 1.1.3. 开发者程序自启动

Android 4.4之后的版本，默认新安装未启动的程序处于Stopped状态，无法接受系统广播BOOT\_COMPLETE实现自启动，所以AIUI添加对第三方应用自启动的支持。

第三方应用只需要创建Receiver，按照如下的配置接收AIUI的广播即可:

```xml
<receiver android:name=".BootReceiver">
    <intent-filter>
        <action android:name="com.iflytek.aiuilauncher.action.BOOT\_START"/>
    </intent-filter>
</receiver>
```

## 1.2. 软核模式

软核模式和[核心板模式](/hardware/legacy-evb/integration)的软件结构是一样的，区别在于软核模式将AIUIService及其他Apk运行在开发者的硬件上（操作系统需要是Android）。

集成的时候AIUI只提供AIUI软件APK，所以称为软核模式。

### 1.2.1. 适用场景

适用于硬件上需要灵活定制的场景。

### 1.2.2. 集成说明

AIUI软核方案对开发者的硬件设计和录音都有一定的要求：AIUI录音没有使用默认的录音机，而是系统定制中的Alsa(Advanced Linux
Sound Architecture)录音机，开发者集成软核方案时可以选择自己录音通过AIUI ServiceKitSDK写入原始音频，也可以修改系统支持Alsa。

具体的要求和对接开发事项请[联系我们](/faq/contact)。

### 1.2.3. 麦克风阵列方案迁移

如果采用了麦克风阵列的软核方案，那迁移到AIUI软核方案就十分简单，因为上面提到的录音要求已达到。

按以下步骤集成：

1. 修改AIUI配置文件中的alsa参数下的sound\_card和sample\_rate参数为麦克风软核阵列方案确定的录音参数；
2. 开发集成参考[核心板模式](/hardware/legacy-evb/integration)。

## 1.3. 上位机模式

### 1.3.1. 适用场景

适用：上位机和AIUI模块通过串口通信，适用于有屏幕需求或硬件扩展需求（如机器人，智能家居等）。

### 1.3.2. 集成说明

![null](/media/202309/1695879568.0611377.png)

图2 上位机模式集成图示

如上图所示，为上位机模式的开发结构图，UARTService充当AIUIService和上位机之间的中介，一面负责将AIUI的结果通过串口发送给上位机，一面将上位机通过串口发送的指令发送到AIUI。

AIUIProductDemo是个可选的选项，因为如果在上位机上对结果进行解析播放，那么AIUI模块上的AIUIProductDemo的播报就不必要了。

具体集成方法请参见[串口SDK](/hardware/legacy-evb/serial-sdk)。

## 软件包说明

在官网下载的SDK包中包含很多资源，为了让开发者充分了解并使用它们，下面将分别介绍下它们的功能。

## 2.1. bin目录

该目录下包含体验评估板开发套件语音交互能力所需的app以及更新app的批处理脚本。

| 应用名称 | 安装载体 | 功能 |
| --- | --- | --- |
| AIUILauncher | 评估板开发套件/核心板 | 系统级应用，安装时应push到/system/app/目录下，其主要功能是发送开机广播（开发者应用可监听此广播实现开机启动）、开机后拉起UARTService、ControlService服务。 |
| AIUIProductDemo | 评估板开发套件/核心板 | AIUI默认播报程序，包含完整的交互处理逻辑，如评估板开发套件的灯光控制、歌曲播报等。 |
| AIUIService | 评估板开发套件/核心板 | AIUI核心服务，包含语音唤醒、端点检测、离线命令词识别以及跟AIUI服务端通信等功能。 |
| ControlService | 评估板开发套件/核心板 | 评估板开发套件中给ControlClient提供服务的应用程序。 |
| UARTService | 评估板开发套件/核心板 | 负责串口通信的服务，作为上位机与评估板开发套件之间的通信入口。 |
| ControlClient | Android手机 | 运行在手机平台的应用，主要功能有：配置评估板开发套件授权信息以及负责手机端跟评估板开发套件之间的局域网通信。 |

表1 软件包内容说明

## 2.2. doc目录

该目录下包含核心板数据手册与麦克风设计参考文档。

## 2.3. lib目录

该目录下包含AIUIServiceKit.jar，开发者可在自己开发的评估板开发套件应用中集成该库，用来与AIUIService进行通信。详细使用可参考[AIUIServiceKit SDK](/hardware/legacy-evb/aiui-service-kit)。

## 2.4. sample目录

该目录下包含ControlService、ControlClient、AIUIProductDemo、UARTService等应用的源码工程，开发者可在此基础上开发出更多样化的产品。

Demo工程下提供的AIUIDemo是为演示AIUI接口的基本调用方法，该Demo需要界面操作，安装在评估板开发套件或核心板中，可以使用TotalControl或vysor进行操作；AIUIDemo与AIUIProductDemo不能同时安装，二选一即可。AIUIDemo与ControlService也不能同时安装，原因参考[AIUI配置provider](/sdk-dev/basics/params/)。

UART工程下提供的UARTKit是Android平台下[AIUI串口协议](/hardware/legacy-evb/serial-sdk)的封装实现；UARTKitCtrDemo是上位机（Android平台）集成[AIUI串口协议](/hardware/legacy-evb/serial-sdk)的基本实现与调用方法演示程序，开发者可参考此代码实现上位机程序。

## 2.5. tools（其他工具）目录

该目录下包含在PC端使用adb工具对评估板开发套件进行配网的批处理脚本与获取msc日志的配置文件。

开发者在开发过程中遇到问题，如10120错误，可将msc.cfg放入/sdcard/msc/目录下，重启后复现问题，然后将/sdcard/msc/目录下的所有日志文件pull出来，发送给技术支持分析。

## AIUIServiceKitSDK

## 3.1. 交互理解

AIUI的交互类似一个IO系统，I(Input)就是发送给AIUI的AIUIMessage， O(Output)就是AIUI抛出来的AIUIEvent。开发者通过集成AIUI SDK， 发送AIUIMessage、接收AIUIEvent。

AIUIServiceKit中提供的AIUIAgent就是和AIUIService交互的桥梁，通过发送不同的AIUIMessage控制AIUI的运行， AIUI通过AIUIListener将不同的AIUIEvent抛出来给开发者进行解析。

## 3.2. 接口说明

**AIUIAgent**

AIUIServiceKit中用于与AIUIService交互的接口类为AIUIAgent。AIUIAgent提供如下接口:

```java
//创建AIUIAgent实例
static void createAgent(Context context, AIUIListener listener)
//发送AIUI消息
void sendMessage(AIUIMessage message)
//销毁AIUIAgent实例
void destroy()
```

**AIUIListener**

创建AIUIAgent时传递的参数AIUIListener是用于接收AIUIService抛出事件的监听器。AIUIListener定义如下:

```java
interface AIUIListener{
 void onEvent(AIUIEvent event);}
```

**AIUIEvent**

AIUIListener中监听的抛出事件是AIUIEvent。AIUIEvent定义如下:

```java
class AIUIEvent{
     int eventType;        //事件类型
     int arg1;             //参数1
     int arg2;             //参数2
     String info;
     Bundle data;
 }
```

AIUI定义了多种AIUIEvent，有不同eventType。当AIUIEvent取不同的eventType时，其余字段有不同的定义，详细定义请见[AIUIEvent](/sdk-dev/basics/events)的定义说明。

**AIUIMessage**

AIUIAgent中sendMessage方法用于向AIUIService发送AIUI消息。消息类型是AIUIMessage。

AIUIMessage定义如下:

```java
class AIUIMessage{

     int msgType;        //消息类型
     int arg1;            //参数1 默认空值 0
     int arg2;            //参数2 默认空值0
     String params;        //默认空值 ""
     byte[] data;        //默认空值 null
 }
```

AIUI定义了多种AIUIMessage，有不同的msgType。当AIUIMessage取不同的msgType时，其他成员有不同的定义，详细定义解释请见[AIUIMessage](/sdk-dev/basics/events)的定义说明。

## 3.3. 调用流程

AIUIServiceKit的一般调用流程如下:

```java
AIUIListener listener = new AIUIListener() {

     @Override

     public void onEvent(AIUIEvent event) {

     switch (event.eventType) {

         //唤醒事件
         case AIUIConstant.EVENT_WAKEUP:
         {
             break;
         }

         //结果事件（包含听写，语义，离线语法结果，定义和解析格式参见4.6 AIUIEvent一节）
         case AIUIConstant.EVENT_RESULT:
         {
             break;
         }

         //休眠事件
         case AIUIConstant.EVENT_SLEEP:
         {
             break;
         }
         //错误事件
         case AIUIConstant.EVENT_ERROR:
         {
             break;
         }
    }
}

AIUIAgent agent = AIUIAgent.createAgent(MainActivity.this, listener);
agent.sendMessage(new AIUIMessage(AIUIConstant.CMD\_RESET\_WAKEUP, 0, 0, null, null);
```

具体的实现编码可以参考开发包中的AIUIDemo源码实现。

## 串口SDK

AIUI通过串口与上位机通信，定义了一套串口数据交互的协议，通过该协议上位机可以实现获取AIUI的结果，配置AIUI的网络，控制AIUI的状态，控制AIUI进行合成播报等功能。如果遇到目前定义的串口交互协议不能满足的需求，开发者也可以通过协议中定义的自定义数据消息进行扩展。

对于定义的串口交互协议，开发包中提供了Android上位机上的实现参考，对于其他平台也有很多开发者共享的实现可以参考。

## 4.1. AIUI串口协议

### 4.1.1. 概述

上位机和AIUI语音模块之间通过串口进行数据交互。上位机可以通过串口向AIUI语音模块发送握手消息同步状态，发送WIFI配置信息，发送AIUI配置消息，发送控制消息控制AIUI状态。

### 4.1.2. 通信接口及参数

- 波特率：115200
- 数据位：8
- 停止位：1
- 奇偶校验：无
- 流控：无

AIUI使用模块上的串口UART1，对应文件系统下的/dev/ttyS1。

### 4.1.3. 消息格式

|  |  |  |
| --- | --- | --- |
| **字节** | **值** | **含义说明** |
| 0 | 0xA5 | 同步头 |
| 1 | 0x01 | 用户ID |
| 2 | 0xXX | 消息类型 |
| 3~4 | 0xXXXX | 消息数据长度 |
| 5~6 | 0xXXXX | 消息ID |
| 7~n | 消息数据 | 消息数据 |
| n+1 | 0xXX | 内部校验码 |

表2 AIUI串口协议消息格式

### 4.1.4. 通信规则

- 双向通信，进行一问一答式通信；
- 不分主从机，双方都可向对方发送请求信息；
- 双方发送握手信号，确定与对方串口通信是否正常；在未接收到响应时，可以每隔100ms发送一次握手请求信号；
- 接收方接到请求后需在50ms内发送响应；
- 除确认消息外发送方发送完成后若超过300ms未得到响应则判定为超时进行重发，重发次数为3次。

### 4.1.5. 通信格式

通信格式定义了握手消息，AIUI配置消息，WIFI配置消息，AIUI消息，主控消息，确认消息。下面将分类详述：![download](/media/202309/1695882288.98919.png)

图3 AIUI串口协议通信格式

**消息长度：**

数据格式中3 ~ 4字节为消息数据长度，消息长度编码为小端模式，即第3字节存储低字节，第4字节存储高字节。如握手请求消息中消息数据有4字节，则消息长度为4，编码到3 ~ 4字节就是0x04 0x00

**消息ID：**

数据格式中5 ~ 6字节为消息ID，与消息长度类似，也是小端模式编码。可以使用消息ID过滤因超时重发导致的重复消息。两字节长度的消息ID取值0-65535，所以在实际使用中需要循环使用，具体实现可以参考Android平台上的源码实现。

**校检码：**

数据格式中每种数据类型的最后一个字节都是校检码，用于检验串口传输的正确性。其计算方式为除校检码字节外所有字节求和取反并加1。公式如下:

checkcode = ~sum(字节0+字节2+…+字节n) + 1

**编码格式：**

消息中字符串类型的数据编码格式为UTF-8。

AIUI消息格式中的数据采用GZIP压缩格式，压缩前的编码格式也是UTF-8格式。

### 4.1.6. 确认消息

确认消息是一个特殊的消息类型，它是对其他类型消息的确认，它的消息ID与其要确认的消息的ID相同。

如一个AIUI消息的消息ID为0x9527，那对应的确认消息的消息ID也应该是0x9527。

### 4.1.7. WIFI配置

WIFI配置结果中，状态取值：

- 0：从机当前与路由连接

加密方式分为三类：

- 0：OPEN
- 1：WEP
- 2：WPA

### 4.1.8. AIUI配置

AIUI配置的格式为JSON，content中包含配置文件内容，可配置字段参考[AIUI配置文件](/sdk-dev/basics/params/)内容，除AIUI配置文件中的内容外还可以通过launch\_demo配置是否启动AIUIProductDemo。

配置appid，key，场景等示例如下:

```json
{
 "type": "aiui_cfg",
 "content": {
     "login":{
         "appid":"xxxxxxxx",
         "key":"xxxxxxxx"
     },
     "launch_demo": false
 }
}
```

::: warning 注意
AIUI只需配置一次，后面即使重启也会继续生效，AIUI配置生效需要重启服务，所以AIUI配置应尽可能只在首次启动无配置或配置修改的情况下使用。
:::

配置项字段取值参见中[AIUI配置文件](/sdk-dev/basics/params/)部分说明

### 4.1.9. 主控消息

主控消息是上位机发送给AIUI模块的消息，格式为JSON。
主控消息根据内部字段type的不同，控制AIUI的不同功能。

#### 4.1.9.1. AIUI控制

type为aiui\_msg，发送AIUI控制消息:

```json
{
 "type": "aiui_msg",
 "content": {
    "msg_type": 8, // CMD_RESET_WAKEUP 重置AIUI唤醒状态
    "arg1": 0,
    "arg2": 0,
    "params": "",
    "data": "" // 非必须，值为原数据的base64编码
 }
}
```

::: warning 注意
各个字段取值具体说明参见[AIUIMessage类型](/sdk-dev/basics/events)说明部分
:::

#### 4.1.9.2. 控制AIUI播放

type为voice，控制AIUI声音播放:

```json
{
 "type": "voice",
 "content": {
     "enable_voice":true/false // 是否禁止AIUI声音播放
 }
}
```

#### 4.1.9.3. 设置AIUI音量

type为voice，控制AIUI声音播放:

```json
{
 "type": "voice",
 "content": {
     "vol_value": 15 // 设置音量，范围7~15
 }
}
```

#### 4.1.9.4. WIFI状态查询

type为status，通过query字段查询不同状态:

```json
{
 "type": "status",
 "content": {
     "query": "wifi" // 查询AIUI WIFI状态信息
 }
}
```

#### 4.1.9.5. 音量查询

type为status，通过query字段查询不同状态:

```json
{
 "type": "status",
 "content": {
     "query": "volume" // 查询AIUI音量大小
 }
}
```

#### 4.1.9.6. 音频保存

type为save\_audio，控制AIUI保存原始音频，通过save\_len指定保存音频时长，单位为秒:

```json
{
 "type": "save_audio",
 "content": {
     "save_len": 10
 }
}
```

#### 4.1.9.7. 文本合成

type为tts，发送文本让AIUI开始合成播放或者停止合成播放:

- 开始合成命令(parameters为可选参数):

  ```
  {
  "type": "tts",
  "content": {
     "action": "start", //开始合成
     "text": "xxx", //需要合成播放的文本(注意文本的编码格式要为utf-8)
     "parameters" : {
         "emot" : "xxx", //emot值为neutral，happy，sorrow中一个
         "xxx" : "xxx" // TTS支持设置的其他参数
     }
  }
  }
  ```
- 暂停合成命令:

  ```
  {
  "type": "tts",
  "content": {
     "action": "pause" //停止合成
  }
  }
  ```
- 恢复合成命令:

  ```
  {
  "type": "tts",
  "content": {
     "action": "resume" //停止合成
  }
  }
  ```
- 停止合成命令:

  ```
  {
  "type": "tts",
  "content": {
     "action": "stop" //停止合成
  }
  }
  ```

  #### 4.1.9.8. AIUI结果过滤命令

默认情况下，AIUI会将用户在云端配置的所有语义场景类型的结果都通过串口发送给上位机。

但是可能在某些情况下，比如上位机是单片机，仅仅需要接收操控类的指令，对天气，音乐，故事类的结果仅希望在AIUI模块上播出，而不需要发送到上位机。

在这种情况下，开发者可以通过命令控制过滤选择发送到上位机的AIUI结果的场景类型：

```json
{
 "type": "event_filter",
 "content": {
     "type_filter" : {
         "select" : [],
         "unselect": []
     },
     "sub_filter": {
         "select" : [],
         "unselect": []
     },
     "service_filter": {
         "select" : [],
         "unselect": []
     }
 }
}
```

其中type\_filter根据AIUIEvent的eventType来过滤，具体取值请参考[AIUIEvent](/sdk-dev/basics/events)小节。select字段为允许发送的类型，unselect字段为不允许发送的类型。注意：取值类型为字符串类型，而不是int类型。如下为过滤唤醒事件示例：

```json
{
"type": "event_filter",
"content": {
     "type_filter" : {
         "select" : ["4"] //结果事件对应取值为4
     }
}
}
```

sub\_filter根据结果事件中的sub字段来过滤，具体取值：iat、nlp、asr、tpp。如下为过滤后处理结果示例：

```json
{
 "type": "event_filter",
 "content": {
     "sub_filter" : {
         "select" : ["tpp"]
     }
 }
}
```

service\_filter根据结果事件中的service字段来过滤，如下为过滤天气结果示例：

```json
{
 "type": "event_filter",
 "content": {
     "service_filter" : {
         "select" : ["weather"]
     }
 }
}
```

### 4.1.10. AIUI消息

AIUI消息是AIUI模块传递给上位机的消息，表示听写语义数据返回或者主控消息操作的结果。原始内容格式为JSON，**但是为了传输的效率，实际消息内容采用了GZIP压缩格式**。

AIUI消息根据type字段的不同值解析数据。

#### 4.1.10.1. WIFI状态

type为wifi\_status，代表WIFI状态查询返回或者当AIUI网络状态变化时主动通知，示例如下:

```json
{
 "type": "wifi_status",
 "content": {
     "connected": true/false, //AIUI WIFI查询状态信息
     "ssid": "connected_ssid" //当connected为true时，此字段表示当前连接的wifi名称
 }

}
```

#### 4.1.10.2. AIUI结果事件

type为aiui\_event，代表AIUI结果返回，总体结构示例：

```json
{
 "type": "aiui_event",
 "content": {
     "eventType":1, //事件类型
     "arg1":0, //参数1
     "arg2":0, //参数2
     "info":{}, //描述信息
     "result":{} //结果
 }
}
```

::: warning 注意
具体字段参考[AIUIEvent类型](/sdk-dev/basics/events)说明部分。
:::

#### 4.1.10.3. 合成

type为tts\_event，表示合成事件:

- 合成开始事件:

  ```
  {
  "type": "tts_event",
  "content": {
     "eventType": 0 // 合成开始事件
  }
  }
  ```
- 合成结束事件:

  ```
  {
  "type": "tts_event",
  "content": {
     "eventType": 1, //合成结束事件
     "error": ttsErrorCode //0表示成功;发生错误时代表合成错误码
  }
  }
  ```

## 4.2. 串口协议实现参考

### 4.2.1. Android实现

根据通信协议和通信格式，在Android平台进行了实现以供开发参考。如果上位机平台是Android平台，可以直接集成使用。
开发包中包含串口开发包下的UARTKit是AIUI串口协议实现的Library工程，UARTKitCtrDemo是运行在Android上位机上依赖UARTKit的Application工程，用于UARTKit接口使用的示例，AIUI中串口收发也是使用的UARTKit Library。
Android串口SDK架起了上位机与AIUIService交互的桥梁，通过收发AIUI消息，获取AIUI结果和控制AIUI的运行。

#### 4.2.1.1. 权限

串口通信需要应用有读写对应串口设备的权限（即对/dev/下的串口设备文件有rw权限）。

#### 4.2.1.2. 调用流程

调用主要接口类是UARTAgent。
在程序首次初始化的地方调用静态方法createAgent创建UARTAgent实例，传入EventListener参数用于接收串口事件，后面调用创建的UARTAgent实例的sendMessage方法发送串口消息，在程序结束前调用UARTAgent实例的destroy方法释放资源。

#### 4.2.1.3. 接口说明

UARTAgent
包含如下接口:

```java
//创建UARTAgentUARTAgent
createAgent(String device, int speed, EventListener listener)
//发送串口消息boolean
sendMessage(MsgPacket reqPacket)
//销毁串口，释放资源
void destroy()
```

EventListener
创建UARTAgent传入的listener，用于监听串口的状态和数据回调，定义如下:

```java
interface EventListener {
    void onEvent(UARTEvent event);}
```

UARTEvent
UARTEvent即为串口事件，定义如下:

```python
class UARTEvent {
    int eventType; //串口事件类型
    Object data;   //串口事件数据}
```

MsgPacket
MsgPacket是构造发送给AIUI的消息的类型，可以通过PacketBuilder提供的静态工具方法很方便的构造：

- 构造AIUI配置请求数据包

  ```
  MsgPacket.obtainAIUIConfPacket(String appid, String key, String sence, boolean launchDemo)
  ```
- 构造获取WIFI状态请求数据包
  MsgPacket.obtainWIFIStatusReqPacket()
- 构造AIUI控制请求数据包

  ```
  MsgPacket obtainAIUICtrPacket(int msgType, int arg1, int arg2, String params)
  ```

  更多消息类型的构造可以参考源码自行实现。

#### 4.2.1.4. 代码示例

下面代码示例了上位机集成使用的通用流程（更全面的代码参考开发包下的UARTKitCtrDemo):

```java
mAgent = UARTAgent.createAgent("/dev/ttyS2", 115200, new EventListener() {

    @Override
    public void onEvent(UARTEvent event) {
        switch (event.eventType) {
            case UARTConstant.EVENT_INIT_SUCCESS:              //处理初始化成功事件
                Log.d(TAG, "Init UART Success");
                break;

            case UARTConstant.EVENT_INIT_FAILED:               //处理初始化失败事件
                Log.d(TAG, "Init UART Failed");
                break;

            case UARTConstant.EVENT_MSG:                       //消息回调事件
                MsgPacket recvPacket = (MsgPacket) event.data;
                processPacket(recvPacket);
                break;

            case UARTConstant.EVENT_SEND_FAILED:               //消息发送失败事件
                MsgPacket sendPacket = (MsgPacket) event.data;
                mAgent.sendMessage(sendPacket);
                break;
            default:
                break;
        }
    }});
//消息处理private void processPacket(MsgPacket packet) {
    switch (packet.getMsgType()) {
        case MsgPacket.AIUI_PACKET_TYPE:
                Log.d(TAG, "recv aiui result" + new String(((AIUIPacket) packet).content));
                break;
        default:
                break;
    }}
//发送AIUI配置信息
mAgent.sendMessage(PacketBuilder.obtainAIUIConfPacket("AppID", "key", "scene", false));
```

### 4.2.2. 其他平台实现

Android平台上位机只需集成开发包中串口SDK UARTKit即可便捷地进行开发。若上位机是其他平台，可以先通过AIUI串口历险记熟悉AIUI串口协议的一些具体内容，再参考串口Android SDK的示例熟悉处理流程。在Windows上也有分享的AIUI串口工具，参见AIUI串口调试助手。

## 4.3. 自定义消息

串口通信格式中定义了网络，配置，控制，接收几类消息，这些消息大部分格式是json文本，接收的AIUI消息的格式还是gzip压缩，对于性能较弱的机器（如单片机）来说，这些消息解析较慢。所以在串口通信格式中加入自定义数据类型，以扩展现有串口的适用性。

### 4.3.1. 格式定义

分类 同步头 用户ID 消息类型 消息长度 消息ID 消息数据 校检码
自定义消息 0xA5 0x01 0x2A 见下文解释 见下文解释 自定义消息数据 见下文解释

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **分类** | **同步头** | **用户ID** | **消息类型** | **消息长度** | **消息ID** | **消息数据** | **消息数据** |
| 自定义消息 | 0xA5 | 0x01 | 0x2A | 见下文解释 | 见下文解释 | 自定义消息数据 | 见下文解释 |

表3 自定义消息格式定义

### 4.3.2. 基本流程

自定义数据的基本工作流程：

1. AIUI模块上开发者的Android应用发送含数据的特定广播，AIUI会把数据通过串口发送给上位机。
2. 上位机也可以发送自定义数据给AIUI模块，AIUI模块上的开发者应用接收后进行处理即可。
   对应上述流程，分别对应如下广播：
   com.iflytek.aiui.devboard.action.SEND\_CUSTOM\_DATA
   com.iflytek.aiui.devboard.action.RECEIVE\_CUSTOM\_DATA

### 4.3.3. 代码示例

下列代码演示功能：在AIUI模块中接收上位机发送的自定义消息后自动回复给上位机一串数据为{1, 1, 2, 3, 5, 8}的自定义消息。
AIUI模块中开发者应用负责接收自定义消息的Receiver：

```java
class CustomDataReceiver extends BroadcastReceiver{
    private static final String ACTION_SEND_CUSTOM_DATA = "com.iflytek.aiui.devboard.action.SEND_CUSTOM_DATA";
    private static final String CUSTOM_DATA_KEY = "custom_data";

    @Override
    public void onReceive(Context context, Intent intent) {
        byte[] customData = intent.getByteArrayExtra(CUSTOM_DATA_KEY);
        Log.d("CustomDataReceiver", "recv custom data " + Arrays.toString(customData));

        Intent respAck = new Intent(ACTION_SEND_CUSTOM_DATA);
        respAck.putExtra(CUSTOM_DATA_KEY, new byte[]{1, 1, 2, 3, 5, 8});
        context.sendBroadcast(respAck);
    }}
```

在manifest中注册如下

```xml
<receiver android:name="com.example.uartcustomdata.CustomDataReceiver">
    <intent-filter>
        <action android:name="com.iflytek.aiui.devboard.action.RECEIVE_CUSTOM_DATA"/>
    </intent-filter></receiver>
```

## 4.4. 常见问题

Q: 怎么查看AIUI上串口消息的处理接收？
A: 通过adb logcat -s UART\_Manager:\*（adb连接参照调试）查看AIUI串口的日志。

Q: 串口消息构造后发送给AIUI，为什么没有执行对应操作（如发了合成命令，没有合成播放等）？
A: 没有执行对应操作可能的原因分三种：
1)消息格式构造问题
2)消息ID重复
3)消息内容构造问题
对于上述三种原因可以按如下方法依次排查：
如果收到了AIUI对消息的确认消息，那说明消息构造没问题，反之应该检查下消息构造的格式是否有问题。
因为协议中消息ID的说明，AIUI会对消息ID与之前接受的200条消息ID进行比较，如果有相同则认为是因确认超时重发的消息，而进行过滤，直接返回对应的确认消息，不会对消息进行解析处理。
通过adb logcat -s UART\_Manager:\*（adb连接参照调试）查看AIUI串口的日志。 如果log中有:

```java
recv same data, send ack drop it !!!
```

那说明消息ID与之前有重复，请检查消息ID的构造逻辑问题。
消息内容的构造问题，请仔细对照主控消息内定义的消息内容格式，比如合成消息中的文本内容的编码格式要为utf-8。

Q: 底板上有两个串口，AIUI使用了UART1，开发程序可以使用UART0吗？
A: UART2是AIUI的调试串口，不能正常读写，所以UART2不能使用。如果对AIUI本身的串口功能有依赖，第三方应用如果需要读写串口发送自己的数据内容，可以考虑使用串口自定义的功能。如果对AIUI本身的串口功能无依赖，AIUI软件内部关系中UARTService负责串口通信，所以将UARTService卸载即可独立读写串口（不推荐）。

Q: 使用UARTKit SDK时设备初始化失败怎么办？
A: 导致设备初始化失败的原因有两种，第一是设备打开失败，可能由于设备不存在、没有权限；第二是设备设置失败，因为不同上位机的串口配置不一样，UARTKit SDK的串口初始化设置仅在评估板开发套件上测试可用，所以需要开发者自己更改UARTKit SDK中设备初始化参数的代码，自行修改测试实现。

Q: 使用UARTKit SDK串口功能不正常怎么办？
A: 通过adb logcat -s UART\_Manager:\*查看上位机和AIUI模块的串口收发日志，确定收发不成功的问题点。比如一方有发送日志显示，但是另外一方无对应的接收日志，那可以通过将发送TX线通过USB转接线接到电脑上，用一般的串口查看助手，确认数据是不是已发送。可以用AIUI串口调试助手测试确定是否是由AIUI数据发送问题。

Q: 使用UARTKit SDK时日志中频繁出现DropHead，长时间不回调消息接收怎么办？
A: 串口数据结构定义中定义了同步头，在底层进行数据接收中，会从数据流中匹配同步头，作为一条消息的数据开始标记，如果数据流中一直没有同步头，那就会一直打印drop head的日志。这种情况大部分的原因是上位机接收有误导致，可以打印具体接收的数据和定义的串口数据格式比较确定。可以用AIUI串口调试助手测试确定是否是由AIUI数据发送问题。

Q: 使用UARTKit SDK时底层打印接收日志，但是一直不回调消息接收怎么办？
A: 如上Drop Head的问题，串口接收数据时在寻找到消息数据开始的同步头后，会根据其后的长度信息接收一定长度的数据，然后校验通过后向上传递，如果接收数据有误，导致长度信息解析过大，那后面所有正常的消息都会当作这条消息的数据一直接收，导致上层长时间没有消息回调接收，即使该消息接收完成，也会因为校验不通过直接丢弃。串口接收数据出错也是导致如上异常的原因，需要排查上位机的串口接收功能。如果只是在音乐、火车、新闻等数据量大的情况下有这个问题，可以通过串口结果过滤将大数据量的技能消息过滤，只在AIUI模块上处理，不传输到上位机。也可以在底层接收数据时，对解析接收长度做过滤，解析出超过限值的消息直接丢弃，AIUI压缩过后的数据量是6k以内。

## 评估板开发套件参数配置

AIUIService在启动时会读取参数配置，根据配置初始化各个内部模块。

## 5.1. 配置读取

AIUIService通过android:authorities=”com.iflytek.aiui.cfg.provider”的ContentProvider读取配置，配置文件的格式和字段说明在[配置文件](/sdk-dev/basics/params/)有详细的说明。

ControlService中实现的提供AIUI配置的ContentProvider简略代码如下:

```java
public class AIUIConfigProvider extends ContentProvider {

 private static final String TAG = "AIUIConfigProvider";
 @Override
 public Bundle call(String method, String arg, Bundle extras) {
     if ("readAIUICfg".equals(method)) {
         // /sdcard/AIUI/cfg/aiui.cfg配置文件由ControlService管理的，ControlService被卸载后，该配置文件就没用了
         String config = ConfigUtil.readSdcardCfg(ServiceConstant.SDCARD\_AIUI\_CFG\_PATH);
         Bundle bundle = new Bundle();
         bundle.putString("config", config);
         return bundle;
     }
     return super.call(method, arg, extras);
 }}
```

Manifest中注册信息如下source:

```xml
<!-- AIUI配置provider --><provider
 android:name="com.iflytek.aiui.devboard.controlservice.provider.AIUIConfigProvider"
 android:authorities="com.iflytek.aiui.cfg.provider"
 android:exported="true"
 android:multiprocess="false"></provider>
```

如上的配置可以参考开发包中AIUIDemo中AIUIConfigProvider.java的实现。

评估板开发套件控制端ControlClient配置的appid和key就是通过tcp发送给ControlService，ControlService再通过如上的ContentProvider提供给AIUIService。

### 5.1.1. 注意事项

谁定义了配置的ContentProvider，就读取谁的配置。

ControlService和AIUIDemo都定义了相同的ContentProvider，这是不能同时安装的原因。

**ControlService:**

配置文件位于/sdcard/AIUI/cfg/aiui.cfg

**AIUIDemo:**

配置文件位于工程assets/cfg/aiui.cfg下

/sdcard/AIUI/cfg/aiui.cfg配置文件由ControlService管理，如果ControlServie被卸载后，这个配置文件就没用了。

## 5.2. 配置文件

除了使用上节中提到的AIUIMessage和AIUIEvent来控制使用AIUI的功能外，还可以通过修改配置文件中的不同字段来控制AIUI的运作。

### 配置文件示例

AIUI的配置内容格式是json，配置了AIUI运行时各方面的参数：

```bash
/* AIUI参数设置 */

{

 /* 语音云平台登录参数 */

 "login":{
     "AppID":"xxxxxxxx",
     "key":"xxxxxxxx"
 },

 /* 场景设置 */

 "global":{
     "scene":"main",
     "clean_dialog_history":"auto"
 },

 /* 交互参数 */

 "interact":{
     "interact_timeout":"60000",
     "result_timeout":"5000"
 },

 // 离线语法识别参数
 "asr":{
     "threshold":"50",
     "res_type":"assets",
     "res_path":"asr/common.jet"
 },

 // 语音合成参数
 "TTS（语音合成）":{
     "res_type":"assets",
     "res_path":"TTS（语音合成）/common.jet;TTS（语音合成）/mengmeng.jet",
     "voice_name":"mengmeng"
 },

 // 唤醒参数
 "ivw":{
     "res_type":"assets",
     "res_path":"ivw/ivw_resource.jet"
 },

 // 语音业务流程
 "speech":{
     "intent_engine_type":"mixed",
     "interact_mode":"continuous",
     //rec_only（仅使用当麦克风阵列录音）、intent（对音频进行处理，返回意图分析结果）
     "work_mode":"intent"
 },

 /* 硬件参数设置 */

 // alsa录音参数
 "alsa":{
     "sound_card":"2",
     "card_sample_rate":"96000"
 },

 /* 音频参数(非必须)*/
 "audioparams":{
     "msc.lng": "", //经度
     "msc.lat": "" //纬度
 },

 /* 用户参数，用于后处理(非必须)*/
 "userparams":{
     "xxxx": "xxx" //自定义字段
 },

 /* 日志设置 */
 "log":{
     "debug_log":"1",
     "save_datalog":"1",
     "datalog_path":"",
     "datalog_size":1024
 }

}
```

#### 5.2.1.1. 配置字段说明

：
：
：

|  |  |  |  |
| --- | --- | --- | --- |
| 参数类型 | | 参数名称和说明 | |
| login | 语音云登录参数 | appid | 在讯飞开放平台上注册的8位应用唯一标识。 |
| key | appid校验串 |
| global | 全局参数设置 | scene | 用户定制的场景参数，不同的场景可对应不同的云端处理流程 |
| clean\_dialog\_history | 清除交互历史：设置auto 自动清除历史（默认模式）， user 用户手动清除历史 |
| interact | 交互参数 | interact\_timeout | 交互超时(单位：ms)：即唤醒之后，如果在这段时间内 无有效交互则重新进入待唤醒状态，取值：[10000,180000)，默认为1min。 |
| result\_timeout | 结果超时（单位：ms）：即检测到语音后端点后一段时间内无结果返回则抛出超时错误。默认值：5000。 |
| tts | 语音合成参数 | engine\_type | 引擎类型,取值：local（本地），cloud（云端）。 |
| res\_type | 资源类型,取值: assets资源（AIUIService.apk的assets文件）， res资源（AIUIService.apk的res文件）， path资源（sdcard文件）。 使用合成时必须设置。 |
| res\_path | 合成资源路径,以“；”隔开，前面为合成共用资源，后面为发音人模型资源。 |
| voice\_name | 发音人名称 |
| vad | 音频端点检测参数 | vad\_enable | vad开启配置，取值：1（vad开启）， 0（vad关闭）。默认值：1。 |
| engine\_type | vad引擎类型，取值：meta（模型vad），默认值：meta。 |
| res\_type | 资源类型，使用模型vad时必须设置，取值：assets资源（apk工程的assets文件），res资源（apk工程的res文件），path资源（sdcard文件） |
| res\_path | 资源文件路径，使用模型vad时必须设置。 |
| vad\_bos | VAD前端超时时间：单位：毫秒 示例 "5000" |
| vad\_eos | VAD后端超时时间：单位：毫秒 示例 "1000" |
| cloud\_vad\_eos | 云端VAD后端超时时间，单位：毫秒 示例 "30000" |
| cloud\_vad\_gap | 云端VAD分句间隔，上限值：1800，单位：毫秒 示例 "400" |
| ivw | 语音唤醒参数 | res\_type | 资源类型，取值同tts参数res\_type说明 |
| res\_path | 唤醒资源文件路径，必须与res\_type匹配。 |
| asr | 离线语法识别参数 | threshold | 语法识别得分门限值，只有当识别结果得分高于门限时才对外抛出。取值：[0，100]，默认值：0。 |
| res\_type | 同ivw，使用离线语法时必须设置。 |
| res\_path | 离线识别资源路径，必须与res\_type匹配。 |
| speech | 业务相关参数 | intent\_engine\_type | 将语音转换成意图的引擎类型，取值： cloud（云端语义），mixed（云端语义+本地语法混合模式），local（本地语法识别）。默认值：cloud。 |
| interact\_mode | 交互模式设置 continuous（默认模式）：持续交互，对于语音即“一次唤醒，多次交互”， oneshot：一次交互，对于语音即“一次唤醒，一次交互”。 oneshot举例： 问：叮咚叮咚，给我唱首歌 //说完后AIUI即进入休眠状态 答：请欣赏xxxx 后续AIUI因已休眠不能继续交互,需重新唤醒才能继续交互。 |
| data\_source | 录音数据来源配置：sdk（sdk内部录音），user（外部录音) |
| alsa | alsa录音参数 | sound\_card | 声卡设备号。请根据实际情况设置，在使用麦克风阵列时必须设置正确的设备号。 |
| card\_sample\_rate | 声卡采样率。请根据实际情况设置，在使用麦克风阵列时必须设置正确的采样率。 |
| audioparams | 音频透传参数设置 | msc.lng | 经度。示例：117.16334474130745 |
| msc.lat | 纬度。示例：31.821021912318592 |
| log | 日志相关参数 | debug\_log | Debug日志开关。取值：1（打开），0（关闭），默认值：0。日志打开时会向logcat打印调试日志。 |
| save\_datalog | 是否保存数据日志。取值：1（打开），0（关闭），默认值：0。打开之后会将所有上传到云端的音频和云端返回的结果保存到本地。 |
| datalog\_path | 数据日志的保存路径。当不设置或者为空值时，使用默认值：“/sdcard/AIUI/data/”。 |
| datalog\_size | 数据日志的大小限制（单位：MB）。取值：[-1，+∞)，默认值：-1（表示无大小限制）。注意：设置成-1可能会造成SD卡被日志写满，从而导致AIUIService性能下降，影响体验效果。 |

表4 参数配置字段说明

## 5.3. 唤醒/合成配置

AIUI允许开发者通过修改本地配置文件或者云端语义技能的配置，改变AIUI默认反馈。

### 唤醒词配置

评估板开发套件默认唤醒词为叮咚叮咚，如想体验其他唤醒词效果，可以根据以下步骤进行更新：

1. 获取新资源。登录[AIUI应用管理](https://www.xfyun.cn/aiui/manage)，选择您的评估板开发套件应用，进入语音资源界面，制作并下载唤醒词资源。
2. 拷贝资源。将下载的资源拷贝到评估板开发套件，路径可自定义。

   ```
   adb push xxxxxx.jet /sdcard/AIUI/ivw/xxxxxxxx.jet
   ```
3. 更新配置。AIUI首次启动后会自动在/sdcard/AIUI/cfg/aiui.cfg生成aiui.cfg文件， 使用adb命令将文件导出。

   ```
   adb pull /sdcard/AIUI/cfg/aiui.cfg aiui.cfg
   ```

   修改配置文件中资源路径，确保和拷贝的资源路径一致，示例如下:

   ```
   // 注：资源在sdcard中，res\_type一定要写path；
   // push资源前先确保目录已经创建；
   // 阵列参数---唤醒词资源
   "ivw":{
     "res_type":"path",
     "res_path":"/sdcard/AIUI/ivw/xxxxxxxx.jet"
   }
   ```

::: warning 注意
资源在 sdcard 中，`res_type` 一定要写 `path`。
:::

修改完成后使用adb导入配置文件:

```bash
adb push aiui.cfg /sdcard/AIUI/cfg/aiui.cfg
```

1. 重启。使用adb命令重启系统：adb shell reboot，或者在手机端点击“同步配置”都可以让配置加载生效。

::: warning 注意
如需恢复默认配置，通过手机端ControlClient清空配置即可
:::

### 5.3.2. 发音人配置

评估板开发套件默认合成的发音人为萌萌（mengmeng），如想体验其他发音人效果，可以根据以下步骤进行更新

1. 获取新资源。登录[AIUI应用管理](https://www.xfyun.cn/aiui/manage)，进入语音资源界面，下载您需要的发音人资源。
2. 拷贝资源。将下载的资源拷贝到评估板开发套件，路径可自定义。

   ```
   adb push common.jet /sdcard/AIUI/tts/common.jet
   adb push xxxxxxxx.jet /sdcard/AIUI/tts/xxxxxxxx.jet
   ```
3. 更新配置。AIUI首次启动后会自动在/sdcard/AIUI/cfg/aiui.cfg生成aiui.cfg文件， 使用adb命令将文件导出。

   ```
   adb pull /sdcard/AIUI/cfg/aiui.cfg aiui.cfg
   ```

   修改配置文件中资源路径，确保和拷贝的资源路径一致，示例如下：

   ```
   // 注：资源在sdcard中，res\_type一定要写path；
   // 多个资源间用“;”分割；（合成需要同时替换common.jet 和 发音人.jet）
   // push资源前先确保目录已经创建；
   //阵列参数---唤醒词资源
   // 合成参数
   "tts":{
     "engine_type":"local",
     "res_type":"path",
     "res_path":"/sdcard/AIUI/tts/common.jet;/sdcard/AIUI/tts/xiaoyan.jet",
     "voice_name":"xiaoyan"
   }
   ```

::: warning 注意
资源在 sdcard 中，`res_type` 一定要写 `path`。
:::

修改完成后使用adb导入配置文件:

```bash
adb push aiui.cfg /sdcard/AIUI/cfg/aiui.cfg
```

1. 重启。使用adb命令重启系统：adb shell reboot，或者在手机端点击“同步配置”都可以让配置加载生效。

::: warning 注意
如需恢复默认配置，通过手机端ControlClient清空配置即可
:::

**AIUI支持在线发音人，在线发音人下不需要指定资源路径，按如下配置即可：**

```
"TTS（语音合成）":{
     "engine_type":"cloud",
     "voice_name":"xiaoyan"
}
```

#### 5.3.2.1. 语速、音量及语调调节示例

```
"TTS（语音合成）":{
     "res_type":"assets",
     "res_path":"TTS（语音合成）/common.jet;TTS（语音合成）/mengmeng.jet",
     "voice_name":"mengmeng"
     "speed": 50 //语速，不设置情况默认50 范围 0~100
     "volume": 50 //音量，不设置情况默认50 范围 0~100
     "pitch": 50 //语调，不设置情况默认50 范围 0~100
}
```

### 5.3.3. 常见问题

**Q: 唤醒词替换后，无法唤醒**

**A:** 查看手机端的错误码信息并且AIUI模块开机后立即开始保存logcat日志3分钟，发送给技术支持分析。

**Q: 发音人替换后其他声音改变，但是唤醒后还是萌萌的声音**

**A:** 目前处理唤醒为了更好的体验效果，AIUIProductDemo播放的是录制好的音频，而不是合成的声音。所以换了合成资源，只会影响后面交互的合成播放。如需修改，可以通过修改开发包中开放的AIUIProductDemo中对应位置源码实现。

**Q: 替换配置文件后，开机后提示APPID未配置**

**A:** 如果SD卡下的aiui.cfg配置文件不是**UTF-8无BOM的JSON**格式，配置文件会被自动清空，导致开机后出现该提示。

**Q: 替换发音人，闲聊技能下某些回答不能播报，音乐天气等技能正常**

**A:** AIUI在闲聊的回答中带有情感标签，目前仅有萌萌的发音人支持[情感合成](/sdk-dev/features/tts)，所以替换不支持情感合成的发音人后，会导致不能播报的情况。

## 5.4. 动态配置

AIUI支持运行过程中动态修改配置参数，并且实时生效。

### 切换场景

配置文件中的情景模式和后台应用定义的情景模式对应，在后台可以为不同情景模式配置不同语义技能、问答库，通过本地的配置文件或者动态设置使用的情景模式。

动态切换场景代码示例如下：

String setParams = “{"global":{"scene":"main"}}”AIUIMessage setMsg = new AIUIMessage(CMD\_SET\_PARAMS, 0 , 0, setParams, null);

mAgent.sendMessage(setMsg);

### 切换唤醒词

通过构造CMD\_SET\_PARAMS消息，params字段包含新唤醒词设置的json即可动态切换唤醒词，实时生效。代码示例如下：

String ivwParams = “{"ivw":{"res\_type":"path","res\_path":"/sdcard/AIUI/ivw/ivw\_resource.jet"}}”AIUIMessage setMsg = new AIUIMessage(CMD\_SET\_PARAMS, 0 , 0, ivwParams, null);

mAgent.sendMessage(setMsg);

## 调试升级

## 6.1. ADB调试

### 6.1.1. USB ADB 调试

评估板开发套件上有个Micro USB口，连接电脑后即可进行adb调试。

### 6.1.2. WIFI ADB 调试

AIUI开机启动后会开启WIFI ADB功能，这样通过同网络下的电脑不用连USB也能ADB。调试AIUI模块。通过如下步骤：

1. 首先得到AIUI模块的IP，可以通过路由器查询或者IP扫描；
2. adb connect aiui\_ip:5555 提示连接成功；
3. adb devices 即可看到设备。

## 6.2. 音频保存

下面描述的音频保存的位置都是在AIUI模块的内置SD卡上。

### 6.2.1. 原始音频

原始音频是麦克风阵列采集到的多通道原始数据，通过手机端评估板开发套件控制端，扫描连接设备，进入控制端界面后依次点击 调试 ->
保存音频 即可最长保存3min的原始音频。

原始音频保存在/sdcard/AIUI/audio/raw中，**评估板开发套件内置SD卡存储空间有限，请及时清理不需要的原始音频。**

### 6.2.2. 识别音频

识别音频是麦克风阵列算法对原始音频进行降噪处理后的16k 16bit单声道音频，该音频最终会送到云端进行识别。

修改配置文件：

```
"log":{
     "debug_log":"1",
     "save_datalog":"1",
     "datalog_path":"",
     "datalog_size":1024,
     "raw_audio_path":""
}
```

将save\_datalog置为1，即可把每次交互的识别音频保存下来，保存的位置位于/sdcard/AIUI/data/（此路径可以通过datalog\_path配置修改）下，每一次唤醒后的交互音频都保存在此目录下wakeXX开始的文件夹下。

all.pcm是本次唤醒后交互的全部识别音频，audio-x.pcm是经过本地vad切分后的识别音频，audio-x.txt是对应音频的结果信息。
