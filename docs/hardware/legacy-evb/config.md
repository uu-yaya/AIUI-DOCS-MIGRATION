---
title: 评估板参数配置
---

AIUIService在启动时会读取参数配置，根据配置初始化各个内部模块。

## 配置读取

AIUIService通过`android:authorities="com.iflytek.aiui.cfg.provider"`的ContentProvider读取配置，配置文件的格式和字段说明在[配置文件](/sdk-dev/basics/params)有详细的说明。

ControlService中实现的提供AIUI配置的ContentProvider简略代码如下:

```java
public class AIUIConfigProvider extends ContentProvider {
        private static final String TAG = "AIUIConfigProvider";

        @Override
        public Bundle call(String method, String arg, Bundle extras) {
                if ("readAIUICfg".equals(method)) {
                        //  /sdcard/AIUI/cfg/aiui.cfg配置文件由ControlService管理的，ControlService被卸载后，该配置文件就没用了
                        String config = ConfigUtil.readSdcardCfg(ServiceConstant.SDCARD_AIUI_CFG_PATH);
                        Bundle bundle = new Bundle();

                        bundle.putString("config", config);

                        return bundle;
                }

                return super.call(method, arg, extras);
        }
}
```

Manifest中注册信息如下source:

```xml
<!-- AIUI配置provider -->
<provider
    android:name="com.iflytek.aiui.devboard.controlservice.provider.AIUIConfigProvider"
    android:authorities="com.iflytek.aiui.cfg.provider"
    android:exported="true"
    android:multiprocess="false">
</provider>
```

如上的配置可以参考开发包中AIUIDemo中`AIUIConfigProvider.java`的实现。

评估板控制端ControlClient配置的appid和key就是通过tcp发送给ControlService，ControlService再通过如上的ContentProvider提供给AIUIService。

### 注意事项：

谁定义了配置的ContentProvider，就读取谁的配置。

ControlService和AIUIDemo都定义了相同的ContentProvider，这是不能同时安装的原因。

**ControlService:**

配置文件位于/sdcard/AIUI/cfg/aiui.cfg

**AIUIDemo:**

配置文件位于工程assets/cfg/aiui.cfg下

/sdcard/AIUI/cfg/aiui.cfg配置文件由ControlService管理，如果ControlServie被卸载后，这个配置文件就没用了。

## 配置文件

除了使用上节中提到的AIUIMessage和AIUIEvent来控制使用AIUI的功能外，还可以通过修改配置文件中的不同字段来控制AIUI的运作。

### 配置文件示例

AIUI的配置内容格式是json，配置了AIUI运行时各方面的参数：

```text
/* AIUI参数设置 */
{
    /* 语音云平台登录参数 */
    "login":{
            "appid":"xxxxxxxx",
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
    "tts":{
            "res_type":"assets",
            "res_path":"tts/common.jet;tts/mengmeng.jet",
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
            "xxxx": "xxx"  //自定义字段
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

#### 配置字段说明

公共参数说明：</SDK-dev/basics/params
录音参数如下：

|  |  |  |  |
| --- | --- | --- | --- |
| 参数类型 | | 参数名称 | |
| alsa | alsa录音参数 | sound\_card | **声卡设备号**    请根据实际情况设置，在使用麦克风阵列时必须  设置正确的设备号。 |
| card\_sample\_rate | **声卡采样率**    请根据实际情况设置，在使用麦克风阵列时必须  设置正确的采样率。 |

## 唤醒/合成配置

AIUI允许开发者通过修改本地配置文件或者云端语义技能的配置，改变AIUI默认反馈。

### 唤醒词配置

评估板默认唤醒词为*叮咚叮咚*，如想体验其他唤醒词效果，可以根据以下步骤进行更新：

①获取新资源。登录[AIUI应用管理](https://www.xfyun.cn/aiui/manage)，选择您的评估板应用，进入语音资源界面，制作并下载唤醒词资源。

②拷贝资源。将下载的资源拷贝到评估板，路径可自定义。

```bash
adb push xxxxxx.jet /sdcard/AIUI/ivw/xxxxxxxx.jet
```

③更新配置。AIUI首次启动后会自动在`/sdcard/AIUI/cfg/aiui.cfg`生成aiui.cfg文件， 使用adb命令将文件导出。

```bash
adb pull /sdcard/AIUI/cfg/aiui.cfg aiui.cfg
```

修改配置文件中资源路径，确保和拷贝的资源路径一致，示例如下:

```text
// 注：资源在sdcard中，res_type一定要写path；
// push资源前先确保目录已经创建；
// 阵列参数---唤醒词资源
"ivw":{
    "res_type":"path",
    "res_path":"/sdcard/AIUI/ivw/xxxxxxxx.jet"
}
```

### 注意：

资源在sdcard中，res\_type一定要写path；

修改完成后使用adb导入配置文件:

```bash
adb push aiui.cfg /sdcard/AIUI/cfg/aiui.cfg
```

④重启。使用adb命令重启系统：`adb shell reboot`，或者在手机端点击“同步配置”都可以让配置加载生效。

### 注意：

如需恢复默认配置，通过手机端ControlClient清空配置即可

### 发音人配置

评估板默认合成的发音人为*萌萌（mengmeng）*，如想体验其他发音人效果，可以根据以下步骤进行更新

①获取新资源。登录[AIUI应用管理](https://www.xfyun.cn/aiui/manage)，进入语音资源界面，下载您需要的发音人资源。

②拷贝资源。将下载的资源拷贝到评估板，路径可自定义。

```bash
adb push common.jet /sdcard/AIUI/tts/common.jet
adb push xxxxxxxx.jet /sdcard/AIUI/tts/xxxxxxxx.jet
```

③更新配置。AIUI首次启动后会自动在`/sdcard/AIUI/cfg/aiui.cfg`生成aiui.cfg文件， 使用adb命令将文件导出。

```bash
adb pull /sdcard/AIUI/cfg/aiui.cfg aiui.cfg
```

修改配置文件中资源路径，确保和拷贝的资源路径一致，示例如下：

```
// 注：资源在sdcard中，res_type一定要写path；
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

### 注意：

资源在sdcard中，res\_type一定要写path；

修改完成后使用adb导入配置文件:

```bash
adb push aiui.cfg /sdcard/AIUI/cfg/aiui.cfg
```

第四步：重启。使用adb命令重启系统：`adb shell reboot`，或者在手机端点击“同步配置”都可以让配置加载生效。

### 注意：

如需恢复默认配置，通过手机端ControlClient清空配置即可

**AIUI支持在线发音人，在线发音人下不需要指定资源路径，按如下配置即可：**

```
"tts":{
        "engine_type":"cloud",
        "voice_name":"xiaoyan"
}
```

#### 语速、音量及语调调节示例

```
"tts":{
    "res_type":"assets",
    "res_path":"tts/common.jet;tts/mengmeng.jet",
    "voice_name":"mengmeng"
    "speed": 50 //语速，不设置情况默认50 范围 0~100
    "volume": 50 //音量，不设置情况默认50 范围 0~100
    "pitch": 50 //语调，不设置情况默认50 范围 0~100
}
```

### 常见问题

**Q: 唤醒词替换后，无法唤醒**

**A:** 查看手机端的错误码信息并且AIUI模块开机后立即开始保存logcat日志3分钟，发送给技术支持分析。
​
**Q: 发音人替换后其他声音改变，但是唤醒后还是萌萌的声音**

**A:** 目前处理唤醒为了更好的体验效果，AIUIProductDemo播放的是录制好的音频，而不是合成的声音。所以换了合成资源，只会影响后面交互的合成播放。如需修改，可以通过修改开发包中开放的AIUIProductDemo中对应位置源码实现。

**Q: 替换配置文件后，开机后提示APPID未配置**

**A:** 如果SD卡下的aiui.cfg配置文件不是**UTF-8无BOM的JSON**格式，配置文件会被自动清空，导致开机后出现该提示。

**Q: 替换发音人，闲聊技能下某些回答不能播报，音乐天气等技能正常**

**A:** AIUI在闲聊的回答中带有情感标签，目前仅有萌萌的发音人支持[情感合成](/sdk-dev/features/tts)，所以替换不支持情感合成的发音人后，会导致不能播报的情况。

## 动态配置

AIUI支持运行过程中动态修改配置参数，并且实时生效。

### 切换场景

配置文件中的情景模式和后台应用定义的情景模式对应，在后台可以为不同情景模式配置不同语义技能、问答库，通过本地的配置文件或者动态设置使用的情景模式。

动态切换场景代码示例如下：

```java
String setParams = "{\"global\":{\"scene\":\"main\"}}"
AIUIMessage setMsg = new AIUIMessage(CMD_SET_PARAMS, 0 , 0, setParams, null);
mAgent.sendMessage(setMsg);
```

### 切换唤醒词

通过构造`CMD_SET_PARAMS`消息，params字段包含新唤醒词设置的json即可动态切换唤醒词，实时生效。代码示例如下：

```java
String ivwParams = "{\"ivw\":{\"res_type\":\"path\",\"res_path\":\"/sdcard/AIUI/ivw/ivw_resource.jet\"}}"
AIUIMessage setMsg = new AIUIMessage(CMD_SET_PARAMS, 0 , 0, ivwParams, null);
mAgent.sendMessage(setMsg);
```
