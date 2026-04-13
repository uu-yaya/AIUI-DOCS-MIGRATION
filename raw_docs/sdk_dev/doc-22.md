---
title: 语音唤醒
source_url: https://aiui-doc.xf-yun.com/project-1/doc-22/
---

语音唤醒能力概述

AIUI SDK配合唤醒SDK，配置语音唤醒能力后，用户语音说出唤醒词后，AIUI SDK进入“working”状态，处理并响应用户后续的语音指令。

本文档主要介绍单麦系统录音语音唤醒集成方式，如开发者是多麦阵列+降噪CAE+AIUI一体使用，可联系AIUI技术同事咨询。

[**- 1.集成步骤>>>点击跳转**](#集成步骤)
[**- 2.自定义唤醒词更换>>>点击跳转**](#自定义唤醒词更换)

## 集成步骤

### 1.1. aiui参数配置

在aiui参数配置文件（aiui.cfg）中开启语音唤醒配置，主要涉及三个部分：

- `speech` 下配置语音唤醒开关
- `ivw` 下配置需加载的唤醒库和唤醒参数配置文件
- `recorder` 下配置录音音频通道

```text
// 语音业务流程控制
"speech":{
    "wakeup_mode":"vtn" //开启唤醒
}
//唤醒参数配置
"ivw":{
    "mic_type": "mic1", //唤醒库加载，建议取值和麦克类型保持一致，例Android系统当前取值代表加载 libvtn_mic1.so
    "res_type":"path",
    "res_path":"/sdcard/AIUI/ivw/vtn/vtn.ini"
},
//音频通道设置，默认唤醒固定设置
"recorder":{
    "channel_count": 1,
    "channel_filter": "0,-1"
},
```java

### 1.2. 唤醒参数配置文件说明

如上节所述，在aiui配置文件唤醒参数`ivw`中需配置唤醒参数配置文件`vtn.ini`，该文件主要需要修改两点：

- `appid` 这是唤醒装机量鉴权appid信息，建议与aiui.cfg中appid取值保持一致
- `res_path` 这是唤醒词资源路径

```ini
[auth]
appid=xxx

[cae]
cae_enable = 1
input_audio_unit = 2

[ivw]
#唤醒功能, 0（关闭，默认），1（开启）
ivw_enable = 1

#唤醒资源文件路径
res_path=/sdcard/AIUI/ivw/vtn/res.bin
```java

### 1.3. SDK调用

温馨提示

AIUI SDK集成开发前，需要确保唤醒参数配置文件`vtn.ini`和唤醒词资源文件`res.bin`已复制或拷贝到对应的设置路径下。

**资源文件拷贝**

- 将`ivw`下示例唤醒配置`vtn.ini`和示例唤醒资源`res.bin`(唤醒词小飞小飞）拷贝到对应的目录文件下。
  Android示例：

  ```
  FileUtil.copyAssetFolder("ivw", "/sdcard/AIUI/ivw");
  ```

**接口调用**：创建AIUIAgent，根据SDK配置的录音方式，发送不同的事件：

- `系统录音`：发送`CMD_START_RECORD`消息，即开始录音，设备进入待唤醒状态。
- `外部录音`：外部音频流通过`CMD_WRITE`事件写入，设备进入待唤醒状态。

```java
//创建AIUIAgent
mAIUIAgent = AIUIAgent.createAgent( this, getAIUIParams(), mAIUIListener );
//开始录音 - 系统录音
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0 ,0, "data_type=audio,sample_rate=16000", null);
mAIUIAgent.sendMessage(msg);

// 外部音频写入 - 外部录音
byte[] audio = xxx;     // 外部录音获取的音频流
String params = "data_type=audio,sample_rate=16000";
AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_WRITE, 0, 0, params, audio);
mAIUIAgent.sendMessage(msg);
```

- 此时喊唤醒词`小飞小飞`，SDK抛出唤醒事件（`EVENT_WAKEUP`)，进入识别状态，响应后面的语音指令。

**回调事件**：

```java
    private final AIUIListener mAIUIListener = new AIUIListener() {
        @Override
        public void onEvent(AIUIEvent event) {
            switch (event.eventType) {
                //唤醒事件
                case AIUIConstant.EVENT_WAKEUP: {
                    String info = event.info;
                    Log.i(TAG, "on EVENT_WAKEUP: " + info);
                    if(info != null &&  !info.isEmpty()){
                            JSONObject jsInfo = new JSONObject(info);
                            String ivwResult = jsInfo.getString("ivw_result");
                            JSONObject ivwInfo = new JSONObject(ivwResult);
                            String keyword = ivwInfo.getString("keyword");
                            Log.i("本次唤醒为：" + keyword);
                    }
                }
                break;
```text

**结果解析**：

```json
{
    "angle": 0,
    "beam": 0,
    "ivw_result": {
        "angle": 0,//唤醒角度
        "beam": 0,//波束
        "start_ms": 255370//唤醒音频开始时间点，用于切分音频做声源定位，开发者无需关注
        "end_ms": 256390,//唤醒音频结束时间点，用于切分音频做声源定位，开发者无需关注
        "keyword": "xiao3 fei1 xiao3 fei1",//唤醒词
        "physical": 0,
        "power": 0,//音频能量大小，特殊版本才有
        "score": 1072//唤醒得分，score>唤醒阈值才会唤醒

    },
    "type": 3
}
```cpp

## 自定义唤醒词更换

AIUI SDK默认提供的语音唤醒能力，支持开发者免费自定义更换，AIUI平台自定义唤醒词打包说明如下：

- 唤醒词打包服务能力免费
- 不限制资源下载次数
- 仅支持中文唤醒词打包
- 默认单个唤醒词资源最多包含3个唤醒词

温馨提示

此处生成的唤醒资源为浅定制版本，如果需要更好的唤醒效果，可联系商务进行唤醒词的深定制训练。

**操作步骤如下**：

① 登录 https:/aiui.xfyun.cn/ 创建应用或选择已创建的应用，进入应用配置页面。

② 点击 资源下载 -> 配置唤醒词 -> 选择 3.17.7 引擎版本 下载 。页面弹窗的“温馨提示”可直接忽略。

③ 解压下载的资源压缩包，获取其中的`res.bin`按照集成示例中的步骤替换对应路径的文件即可。

![](/media/202508/2025-08-21_172339_1146090.940921879392558.png "null")
