---
title: 串口SDK
source_url: https://aiui-doc.xf-yun.com/project-1/doc-35/
---

AIUI通过串口与上位机通信，如当前协议不能满足的需求，可以通过协议的自定义数据消息扩展

开发包提供了Android上位机上实现demo，其他平台也可以参考。

## AIUI串口协议

### 概述

上位机可以通过串口向AIUI语音模块发送握手消息同步状态，例如发送WIFI配置信息。

### 通信接口及参数

![](./images/electric.png "null")

- 波特率：115200
- 数据位：8
- 停止位：1
- 奇偶校验：无
- 流控：无

AIUI使用模块上的串口UART1，对应文件系统下的/dev/ttyS2。

### 消息格式

|  |  |  |
| --- | --- | --- |
| 字节 | 值 | 含义说明 |
| 0 | 0xA5 | 同步头 |
| 1 | 0x01 | 用户ID |
| 2 | 0xXX | 消息类型 |
| 3~4 | 0xXXXX | 消息数据长度 |
| 5~6 | 0xXXXX | 消息ID |
| 7~n | 消息数据 | 消息数据 |
| n+1 | 0xXX | 内部校验码 |

### 通信规则

- 双向通信，进行一问一答式通信；
- 不分主从机，双方都可向对方发送请求信息；
- 双方发送握手信号，确定与对方串口通信是否正常；在未接收到响应时，可以每隔100ms发送一次握手请求信号；
- 接收方接到请求后需在50ms内发送响应；
- 除确认消息外发送方发送完成后若超过300ms未得到响应则判定为超时进行重发，重发次数为3次。

### 通信格式

通信格式定义了握手消息，AIUI配置消息，WIFI配置消息，AIUI消息，主控消息，确认消息。下面将分类详述：

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 分类 | 同步头 | 用户ID | 消息类型 | 消息长度 | 消息ID | 消息数据 | | | | | | | | | 校检码 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7 | 8 | | | 9 | | 10 | | | 11 |
| **握手请求** | 0xA5 | 0x01 | 0x01 | 见下文解释 | 见下文解释 | 0xA5 | 0x00 | | | 0x00 | | 0x00 | | | 见下文解释 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7 | 8 | | | 9 | | 10 | 11~m | m+1~n | n+1 |
| **WIFI配置** | 0xA5 | 0x01 | 0x02 | 同上 | 同上 | 状态 | 加密方式 | | | SSID长度 | | passwd长度 | SSID | passwd | 同上 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7~m | | | | | | | | | m+1 |
| **AIUI配置** | 0xA5 | 0x01 | 0x03 | 同上 | 同上 | AIUI配置 | | | | | | | | | 同上 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7~m | | | | | | | | | m+1 |
| **AIUI消息** | 0xA5 | 0x01 | 0x04 | 同上 | 同上 | AIUI消息（gzip压缩） | | | | | | | | | 同上 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7~m | | | | | | | | | m+1 |
| **主控消息** | 0xA5 | 0x01 | 0x05 | 同上 | 同上 | 主控消息 | | | | | | | | | 同上 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7~m | | | | | | | | | m+1 |
| **自定义消息** | 0xA5 | 0x01 | 0x2A | 同上 | 同上 | 自定义数据 | | | | | | | | | 同上 |
| 字节 | 0 | 1 | 2 | 3~4 | 5~6 | 7 | | 8 | 9 | | | 10 | | | 11 |
| **确认消息** | 0xA5 | 0x01 | 0xff | 同上 | 同上 | 0xA5 | | 0x00 | 0x00 | | | 0x00 | | | 同上 |

**消息长度：**

　　数据格式中3~4字节为消息数据长度，消息长度编码为小端模式，即第3字节存储低字节，第4字节存储高字节。如握手请求消息中消息数据有4字节，则消息长度为4，编码到3~4字节就是0x04 0x00

**消息ID：**

　　数据格式中5~6字节为消息ID，与消息长度类似，也是小端模式编码。可以使用消息ID过滤因超时重发导致的重复消息。两字节长度的消息ID取值0-65535，所以在实际使用中需要循环使用，具体实现可以参考Android平台上的源码实现。

**校检码：**

　　数据格式中每种数据类型的最后一个字节都是校检码，用于检验串口传输的正确性。其计算方式为除校检码字节外所有字节求和取反并加1。公式如下:

```ini
checkcode = ~sum(字节0+字节2+...+字节n) + 1
```text

**编码格式：**

　　消息中字符串类型的数据编码格式为UTF-8。

　　AIUI消息格式中的数据采用GZIP压缩格式，压缩前的编码格式也是UTF-8格式。

### 确认消息

确认消息是一个特殊的消息类型，它是对其他类型消息的确认，它的消息ID与其要确认的消息的ID相同。
如一个AIUI消息的消息ID为0x9527，那对应的确认消息的消息ID也应该是0x9527。

### WIFI配置

WIFI配置结果中，状态取值：

- 0：从机当前与路由连接

加密方式分为三类：

- 0：OPEN
- 1：WEP
- 2：WPA

### AIUI配置

AIUI配置的格式为JSON，content中包含配置文件内容，可配置字段参考[AIUI配置文件](https://aiui-doc.xf-yun.com/project-1/doc-13/#配置文件)内容，除AIUI配置文件中的内容外还可以通过launch\_demo配置是否启动AIUIProductDemo。

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
```text

### 注意：

AIUI只需配置一次，后面即使重启也会继续生效，AIUI配置生效需要重启服务，所以AIUI配置应尽可能只在首次启动无配置或配置修改的情况下使用。

配置项字段取值参见中[AIUI配置文件](https://aiui-doc.xf-yun.com/project-1/doc-13/#配置文件)部分说明

### 主控消息

主控消息是上位机发送给AIUI模块的消息，格式为JSON。
主控消息根据内部字段type的不同，控制AIUI的不同功能。

#### AIUI控制

type为aiui\_msg，发送AIUI控制消息:

```json
{
    "type": "aiui_msg",
    "content": {
        "msg_type": 8, //CMD_RESET_WAKEUP  重置AIUI唤醒状态
        "arg1": 0,
        "arg2": 0,
        "params": "",
        "data": "" //非必须，值为原数据的base64编码
    }
}
```text

### 注意：

各个字段取值具体说明参见[AIUIMessage类型](https://aiui-doc.xf-yun.com/project-1/doc-14/#aiuimessage)说明部分

#### 控制AIUI播放

type为voice，控制AIUI声音播放:

```json
{
    "type": "voice",
    "content": {
        "enable_voice":true/false  // 是否禁止AIUI声音播放
    }
}
```

#### 设置AIUI音量

type为voice，控制AIUI声音播放:

```json
{
    "type": "voice",
    "content": {
        "vol_value": 15  // 设置音量，范围7~15
    }
}
```text

#### WIFI状态查询

type为status，通过query字段查询不同状态:

```json
{
    "type": "status",
    "content": {
        "query": "wifi" // 查询AIUI WIFI状态信息
    }
}
```text

#### 音量查询

type为status，通过query字段查询不同状态:

```json
{
    "type": "status",
    "content": {
        "query": "volume" // 查询AIUI音量大小
    }
}
```text

#### 音频保存

type为save\_audio，控制AIUI保存原始音频，通过save\_len指定保存音频时长，单位为秒:

```json
{
    "type": "save_audio",
    "content": {
        "save_len": 10
    }
}
```

#### 文本合成

type为tts，发送文本让AIUI开始合成播放或者停止合成播放:

- 开始合成命令(parameters为可选参数):

  ```
  {
   "type": "tts",
   "content": {
       "action": "start",  //开始合成
       "text": "xxx",       //需要合成播放的文本(注意文本的编码格式要为utf-8)
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
       "action": "pause"  //停止合成
   }
  }
  ```
- 恢复合成命令:

  ```
  {
   "type": "tts",
   "content": {
       "action": "resume"  //停止合成
   }
  }
  ```
- 停止合成命令:

  ```
  {
   "type": "tts",
   "content": {
       "action": "stop"  //停止合成
   }
  }
  ```

  #### SmartConfig

type为smartcfg，控制AIUI模块smartconfig功能开关:

- 开始命令:

  ```
  {
   "type": "smartcfg",
   "content": {
       "cmd": "start",
       "timeout": 60 //接收smartconfig配置的超时时间
   }
  }
  ```
- 停止命令:

  ```
  {
   "type": "smartcfg",
   "content": {
       "cmd": "stop"
   }
  }
  ```

  #### AIUI结果过滤命令

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
```text

其中type\_filter根据AIUIEvent的eventType来过滤，具体取值请参考[AIUIEvent](https://aiui-doc.xf-yun.com/project-1/doc-14/#aiuievent)小节。select字段为允许发送的类型，unselect字段为不允许发送的类型。注意：取值类型为字符串类型，而不是int类型。如下为过滤唤醒事件示例：

```json
{
"type": "event_filter",
"content": {
    "type_filter" : {
        "select" : ["4"]  //结果事件对应取值为4
    }
}
}
```text

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
```text

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

### AIUI消息

AIUI消息是AIUI模块传递给上位机的消息，表示听写语义数据返回或者主控消息操作的结果。
原始内容格式为JSON，**但是为了传输的效率，实际消息内容采用了GZIP压缩格式**。

AIUI消息根据type字段的不同值解析数据。

#### WIFI状态

type为wifi\_status，代表WIFI状态查询返回或者当AIUI网络状态变化时主动通知，示例如下:

```json
{
    "type": "wifi_status",
    "content": {
        "connected": true/false,  //AIUI WIFI查询状态信息
        "ssid": "connected_ssid"  //当connected为true时，此字段表示当前连接的wifi名称
    }
}
```text

#### AIUI结果事件

type为aiui\_event，代表AIUI结果返回，总体结构示例：

```json
{
    "type": "aiui_event",
    "content": {
        "eventType":1,  //事件类型
        "arg1":0,       //参数1
        "arg2":0,       //参数2
        "info":{},      //描述信息
        "result":{}     //结果
    }
}
```java

### 注意：

具体字段参考[AIUIEvent类型](https://aiui-doc.xf-yun.com/project-1/doc-14/#aiuievent)说明部分。

#### 合成

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
       "eventType": 1,        //合成结束事件
       "error": ttsErrorCode  //0表示成功;发生错误时代表合成错误码
   }
  }
  ```

  ## 串口协议实现参考

  ### Android实现

根据[通信协议和通信格式](https://aiui-doc.xf-yun.com/project-1/doc-35/#aiui串口协议)，在Android平台进行了实现以供开发参考。如果上位机平台是Android平台，可以直接集成使用。

开发包中包含串口开发包下的UARTKit是AIUI串口协议实现的Library工程，UARTKitCtrDemo是运行在Android上位机上依赖UARTKit的Application工程，用于UARTKit接口使用的示例，AIUI中串口收发也是使用的UARTKit Library。

Android串口SDK架起了上位机与AIUIService交互的桥梁，通过收发AIUI消息，获取AIUI结果和控制AIUI的运行。

#### 权限

**串口通信需要应用有读写对应串口设备的权限（即对/dev/下的串口设备文件有rw权限）。**

#### 调用流程

调用主要接口类是UARTAgent。

在程序首次初始化的地方调用静态方法createAgent创建UARTAgent实例，传入EventListener参数用于接收串口事件，后面调用创建的UARTAgent实例的sendMessage方法发送串口消息，在程序结束前调用UARTAgent实例的destroy方法释放资源。

#### 接口说明

**UARTAgent**

包含如下接口:

```java
//创建UARTAgent
UARTAgent createAgent(String device, int speed, EventListener listener)

//发送串口消息
boolean sendMessage(MsgPacket reqPacket)

//销毁串口，释放资源
void destroy()
```java

**EventListener**

创建UARTAgent传入的listener，用于监听串口的状态和数据回调，定义如下:

```java
interface EventListener {
    void onEvent(UARTEvent event);
}
```

**UARTEvent**

UARTEvent即为串口事件，定义如下:

```python
class UARTEvent {
    int eventType; //串口事件类型
    Object data;   //串口事件数据
}
```java

**MsgPacket**

MsgPacket是构造发送给AIUI的消息的类型，可以通过PacketBuilder提供的静态工具方法很方便的构造：

- 构造AIUI配置请求数据包
   `MsgPacket.obtainAIUIConfPacket(String appid, String key, String sence, boolean launchDemo)`
- 构造获取WIFI状态请求数据包
   `MsgPacket.obtainWIFIStatusReqPacket()`
- 构造AIUI控制请求数据包
  `MsgPacket obtainAIUICtrPacket(int msgType, int arg1, int arg2, String params)`

更多消息类型的构造可以参考源码自行实现。

#### 代码示例

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
    }
});

//消息处理
private void processPacket(MsgPacket packet) {
    switch (packet.getMsgType()) {
        case MsgPacket.AIUI_PACKET_TYPE:
                Log.d(TAG, "recv aiui result" + new String(((AIUIPacket) packet).content));
                break;
        default:
                break;
    }
}

//发送AIUI配置信息
mAgent.sendMessage(PacketBuilder.obtainAIUIConfPacket("appid", "key", "scene", false));
```java

### 其他平台实现

Android平台上位机只需集成开发包中串口SDK UARTKit即可便捷地进行开发。若上位机是其他平台，可以先通过[AIUI串口历险记](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=17728)熟悉AIUI串口协议的一些具体内容，再参考[串口Android SDK的示例](https://aiui-doc.xf-yun.com/project-1/doc-35/#串口协议实现参考)熟悉处理流程。在Windows上也有分享的AIUI串口工具，参见[AIUI串口调试助手](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=26336)。

## 自定义消息

串口通信格式中定义了网络，配置，控制，接收几类消息，这些消息大部分格式是json文本，接收的AIUI消息的格式还是gzip压缩，对于性能较弱的机器（如单片机）来说，这些消息解析较慢。所以在串口通信格式中加入自定义数据类型，以扩展现有串口的适用性。

### 格式定义

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 分类 | 同步头 | 用户ID | 消息类型 | 消息长度 | 消息ID | 消息数据 | 校检码 |
| 自定义消息 | 0xA5 | 0x01 | 0x2A | 见下文解释 | 见下文解释 | 自定义消息数据 | 见下文解释 |
|

### 基本流程

自定义数据的基本工作流程：

① AIUI模块上开发者的Android应用发送含数据的特定广播，AIUI会把数据通过串口发送给上位机。

② 上位机也可以发送自定义数据给AIUI模块，AIUI模块上的开发者应用接收后进行处理即可。

对应上述流程，分别对应如下广播：

① `com.iflytek.aiui.devboard.action.SEND_CUSTOM_DATA`

② `com.iflytek.aiui.devboard.action.RECEIVE_CUSTOM_DATA`

流程示意如下：

![](./images/uart_user_define.png "null")

### 代码示例

下列代码演示功能：在AIUI模块中接收上位机发送的自定义消息后自动回复给上位机一串数据为`{1, 1, 2, 3, 5, 8}`的自定义消息。

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
    }
}
```text

在manifest中注册如下

```xml
<receiver android:name="com.example.uartcustomdata.CustomDataReceiver">
    <intent-filter>
        <action android:name="com.iflytek.aiui.devboard.action.RECEIVE_CUSTOM_DATA"/>
    </intent-filter>
</receiver>
```

## 常见问题

**Q: 怎么查看AIUI上串口消息的处理接收？**

**A:** 通过`adb logcat -s UART_Manager:*`（adb连接参照[调试](https://aiui-doc.xf-yun.com/project-1/doc-37/#adb调试)）查看AIUI串口的日志。

**Q: 串口消息构造后发送给AIUI，为什么没有执行对应操作（如发了合成命令，没有合成播放等）？**

**A:** 没有执行对应操作可能的原因分三种：

> 1. 消息格式构造问题
> 2. 消息ID重复
> 3. 消息内容构造问题

对于上述三种原因可以按如下方法依次排查：

> >
>
> - 如果收到了AIUI对消息的确认消息，那说明消息构造没问题，反之应该检查下消息构造的格式是否有问题。
> - 因为协议中[消息ID](https://aiui-doc.xf-yun.com/project-1/doc-35/#确认消息)的说明，AIUI会对消息ID与之前接受的200条消息ID进行比较，如果有相同则认为是因确认超时重发的消息，而进行过滤，直接返回对应的确认消息，不会对消息进行解析处理。
>
>   通过`adb logcat -s UART_Manager:*`（adb连接参照[调试](https://aiui-doc.xf-yun.com/project-1/doc-37/#adb调试)）查看AIUI串口的日志。 如果log中有:
>
>   ```
>    recv same data, send ack drop it !!!
>   ```
>
>   那说明消息ID与之前有重复，请检查消息ID的构造逻辑问题。
> - 消息内容的构造问题，请仔细对照[主控消息](https://aiui-doc.xf-yun.com/project-1/doc-35/#主控消息)内定义的消息内容格式，比如合成消息中的文本内容的编码格式要为utf-8。

**Q: 底板上有两个串口，AIUI使用了UART1，开发程序可以使用UART0吗？**

**A:** UART0是AIUI的调试串口，不能正常读写，所以UART0不能使用。如果对AIUI本身的串口功能有依赖，第三方应用如果需要读写串口发送自己的数据内容，可以考虑使用[串口自定义](https://aiui-doc.xf-yun.com/project-1/doc-35/#自定义数据)的功能。如果对AIUI本身的串口功能无依赖，AIUI软件内部关系中UARTService负责串口通信，所以将UARTService卸载即可独立读写串口（不推荐）。

**Q: 使用UARTKit SDK时设备初始化失败怎么办？**

**A:** 导致设备初始化失败的原因有两种，第一是设备打开失败，可能由于设备不存在、没有权限；第二是设备设置失败，因为不同上位机的串口配置不一样，UARTKit SDK的串口初始化设置仅在评估板上测试可用，所以需要开发者自己更改UARTKit SDK中设备初始化参数的代码，自行修改测试实现。

**Q: 使用UARTKit SDK串口功能不正常怎么办？**

**A:** 通过`adb logcat -s UART_Manager:*`查看上位机和AIUI模块的串口收发日志，确定收发不成功的问题点。比如一方有发送日志显示，但是另外一方无对应的接收日志，那可以通过将发送TX线通过USB转接线接到电脑上，用一般的串口查看助手，确认数据是不是已发送。可以用[AIUI串口调试助手](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=26336)测试确定是否是由AIUI数据发送问题。

**Q: 使用UARTKit SDK时日志中频繁出现DropHead，长时间不回调消息接收怎么办？**

**A:** 串口数据结构定义中定义了[同步头](https://aiui-doc.xf-yun.com/project-1/doc-35/#消息格式)，在底层进行数据接收中，会从数据流中匹配同步头，作为一条消息的数据开始标记，如果数据流中一直没有同步头，那就会一直打印drop head的日志。这种情况大部分的原因是上位机接收有误导致，可以打印具体接收的数据和定义的串口数据格式比较确定。可以用[AIUI串口调试助手](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=26336)测试确定是否是由AIUI数据发送问题。

**Q: 使用UARTKit SDK时底层打印接收日志，但是一直不回调消息接收怎么办？**

**A:** 如上Drop Head的问题，串口接收数据时在寻找到消息数据开始的同步头后，会根据其后的[长度信息](https://aiui-doc.xf-yun.com/project-1/doc-35/#消息格式)接收一定长度的数据，然后校验通过后向上传递，如果接收数据有误，导致长度信息解析过大，那后面所有正常的消息都会当作这条消息的数据一直接收，导致上层长时间没有消息回调接收，即使该消息接收完成，也会因为校验不通过直接丢弃。串口接收数据出错也是导致如上异常的原因，需要排查上位机的串口接收功能。如果只是在音乐、火车、新闻等数据量大的情况下有这个问题，可以通过[串口结果过滤](https://aiui-doc.xf-yun.com/project-1/doc-35/#aiui结果过滤命令)将大数据量的技能消息过滤，只在AIUI模块上处理，不传输到上位机。也可以在底层接收数据时，对解析接收长度做过滤，解析出超过限值的消息直接丢弃，AIUI压缩过后的数据量是6k以内。
