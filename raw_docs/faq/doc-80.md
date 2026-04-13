---
title: AIUI常见问题
source_url: https://aiui-doc.xf-yun.com/project-1/doc-80/
---

# 常见问题

- 交互次数计量方式

  > 以单次会话发送结束帧后，云端有正常结果下发（异常不消耗次数）算一次会话。单次会话不区分下发结果和类别，例如应用配置 识别+语义+合成 能力，那么一次音频请求，下发的识别、语义、合成结果，算一次交互。
- 每次交互用什么来标记会话

  > 语义结果有个sid=“xxxx”的字符串，sid就是该路会话的唯一标记。遇到问题时请提供sid给讯飞排查。
- AIUI支持方言和多语种的识别和语义理解吗？

  > 关于方言和多语种识别：AIUI目前支持的语种包括中文和英文，中文普通话、粤语和四川话识别。其他语种需要提交工单进行商务申请。
  > 关于多语种语义理解：AIUI的官方开放技能（音乐、天气等）不支持英文语义理解，但是开发者可以通过开发自定义技能实现英文语义理解。英文技能不支持模糊匹配。
- 麦克风阵列和aiui评估板的区别

  > AIUI评估板（量产板）包含麦克风阵列。麦克风阵列是前端声学解决方案，输出唤醒信号和处理好的单路音频。
- 在国外能使用AIUI吗？

  > 可以,国外比国内响应慢一点。
- AIUI支持离线识别吗？

  > AIUI 本身不具备离线识别和语义理解的能力，但是支持和离线命令词能力混合使用。用户编写离线命令词abnf脚本并集成客户端SDK可以实现离线命令词识别，具体用法参考文档离线命令词使用
  > 有一点需要注意，离线识别更适用于命令词（上一首、下一首）等短小的命令词。当开发者语料非常复杂时编写的abnf会相对复杂，adbnf脚本开发请参考[abnf语法开发指南](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=7595)
- 单麦、双麦克风阵列可以用AIUI方案吗？

  > 麦克风只是前端拾音方案，AIUI SDK 本身不具备降噪能力，接受单路音频。如需降噪方案可以选择讯飞麦克风阵列或者 AIUI 评估板（量产板）
- 识别热词的生效时间

  > 应用级热词生效<60分钟、用户级热词生效<10分钟，所见即可说的资源立刻生效。
- 麦克风阵列输出的音频是什么？

  > 麦克风阵列把6路音频送进算法引擎，做声源定位，降噪，确定唤醒方向后，把处理后的音频输出，最后输出是16k/16bit,双声道数据。但由于两个声道数据完全一致，本质上是单声道数据。
- CMD\_WAKEUP之后不能立即CMD\_SYNC

  > CMD\_WAKEUP之后等状态变化后就可以同步数据了
- ARM，MIPS 架构如何下载 SDK

  > 因为开发板的编译器过多，我们无法编译全部架构的 SDK，讯飞提供付费的交叉编译服务。
  > 目前AIUI平台做服务升级,一家客户可提供免费2次交叉编译打包支持,如超过次数，则需要对接AIUI平台商务，基于项目合作获取更多支持。
  > 可邮件联系我们[aiui\_support@iflytek.com](mailto:aiui_support@iflytek.com) 或开发者QQ交流群中进行申请。

- 内容开小差 RC3

  > 请求信源有问题、URL的访问问题可能包括网络访问问题，播放格式支持问题，还有https证书过期。
- 诗歌对答中出现的K0\K3 是为了什么

  > 这个标签是为了做提高合成效果做的合成的标记，开发者可以通过正则表达式自行过滤。
- AIUI SDK linux、windows、ios、android 是否都支持语音和文本语义

  > 是的
- windows 支持8k音频么

  > 只支持16k
- AIUI 的收费标准？

  > 应用含500次/天的测试量；正式量产提高限制可以发送邮件至[aiui\_support@iflytek.com](mailto:aiui_support@iflytek.com)咨询合作。
- 多轮对话多久退出

  > 服务端保存最长120s
- 在aiui中可以手动清除交互历史，想在多轮对话结束后清除交互历史，那语义json中判断多轮交互的结束的依据是什么？

  > AIUI支持多轮对话，如在问合肥今天的天气怎么样之后，再询问明天呢，AIUI会结合上一句询问合肥今天天气的历史，就会回答合肥明天的天气。
  > AIUI默认在休眠后唤醒会清除交互历史，在STATE\_WORKING状态下唤醒，则不会清除交互历史。
  > AIUI清除历史的方式是可配置的，默认为auto即是上面描述的模式。当配置成user值后，用户可以通过发送CMD\_CLEAN\_DIALOG\_HISTORY在任何时候手动清除交互的历史。
  > 即使在上面两种情况下，客户端没有主动清除交互历史，服务端保存用户交互历史的时间也是有限的，当用户交互超过5轮后，服务端也会将交互历史清空。
- AIUI中使用唤醒功能需要单独集成MSC中的VoiceWakeUper吗？

  > 不需要了。为了方便开发者可以快速在AIUI中集成语音唤醒功能，AIUI SDK内部封装了语音唤醒的调用逻辑，实现了动态调用。开发者只需将唤醒词和下载的SDK（libmsc.so或msc.dll）放置到相应位置然后进行配置便可以体验唤醒功能。具体使用方法参考语音唤醒功能
- AIUI 支持自己录音写入SDK吗？

  > 支持。AIUI SDK不仅支持SDK内部录音（Android平台内部封装了系统录音机），还支持外部音频写入。外部音频写入适用于开发者有自己的音频采集方式，只需将采集的音频不断写入SDK内部即可。不同音频采集可以通过参数配置来实现
- 调用AIUI的SDK时，CMD\_START\_RECORD只支持Android，那么我要在Linux和Windows下如何录音？

  > Linux平台和Windows平台SDK录音在不同的发行版本上略有不同，SDK内部很难设计出一套兼容各个版本的内部录音机。因此我们在Unbuntu和Win7上分别使用 Alsa 和 Wavein 实现了音频采集并将源码开放。
  >
  > [LINUX平台ALSA录音+AIUI SDK实现语音交互方案分享](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38759&extra=)
  >
  > [Windows平台Wavein录音+AIUI SDK实现语音交互方案分享](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38837&extra=)
- AIUI支持一直保持唤醒状态吗？

  > 不支持。当距离最后一次有效语义结果（字段rc不为4）超过设置的时间时，AIUI将进入休眠状态，用户想要再次交互必须重新唤醒。超时休眠时间设置范围是 [10000,180000) ms,设置方式参考参数设置
- continues和oneshot交互模式有什么不同？

  > continues适用于一次唤醒多次交互的方式；oneshot支持一次唤醒一次交互的方式。在有麦克风阵列的移动端continues交互模式体验更加方便，在需要按住按钮说话的移动端oneshot交互模式更加适用。开发者可以根据自己的产品特性和功能进行甄选。
- continues 和 oneshot模式支持音频一直写入吗？

  > 无论是 continues 还是oneshot，云端支持每次1min持续音频写入，开发者不能持续不断的向云端写入音频。
- Android移动端想通过蓝牙耳机录音录音跟AIUI交互怎么办？

  > 开发者在集成AIUI 移动版SDK时会有这样的需求，蓝牙耳机连接手机，音频从蓝牙耳机而不是手机自带麦克风送入AIUI SDK。80%的Android手机连接蓝牙耳机后音频通道会自动切换，开发者不需要关心底层具体实现，使用AIUI的CMD\_START\_RECORD就可以正常捕获音频。但观察我们的开发者，的确存在某些蓝牙耳机连接手机后无法正常获取音频。针对这种情况，我们建议开发者采用外部录音的方式与AIUI进行交互。所谓外部录音，即我们不通过CMD\_START\_RECORD开启SDK 内部录音方式，而是通过自己的方案采集到16k 16bit音频后通过CMD\_WRITE的方式写入AIUI进行交互。这两种方式都不复杂，甚至采用外部录音的方式可能在某些订制设备上具备更好的扩展性和移植性。
- 蓝牙耳机连接手机设备后无法采集到录音数据是怎么回事？

  > 有时开发者会发现，手机连接蓝牙耳机后，音频无法通过耳机传到手机上。造成这个问题的根本原因是android系统的录音通道没有切换，我们不去深究录音通道没有切换的具体原因，因为这与蓝牙设备和Android固件订制版本比较多有关。但我们有必要跟科普一下蓝牙连接的两种思路：A2DP及SCO。A2DP是一种单向的高品质音频数据传输链路，通常用于播放立体声音乐；而SCO则是一种双向的音频数据的传输链路，该链路只支持8K及16K单声道的音频数据，只能用于普通语音的传输。两者的主要区别是：A2DP只能播放，默认是打开的，而SCO既能录音也能播放，默认是关闭的。既然要录音肯定要打开sco，因此识别前调用上面的代码就可以通过蓝牙耳机录音了，录完记得要关闭。

`开启SCO`

```
AudioManager mAudioManager = (AudioManager)getSystemService(Context.AUDIO_SERVICE);

mAudioManager.setBluetoothScoOn(true);
mAudioManager.startBluetoothSco();
```

`关闭SCO`

```
mAudioManager.setBluetoothScoOn(false);
mAudioManager.stopBluetoothSco();
```

- XCode里 include string file not found
  > 由于AIUIProcessor.mm中使用到了include string 这是C++/C所有的特性，在iOS中如果使用该特性需将文件后缀名改为.mm

- AIUI点击开始录音和停止录音，可以在那里拿到录得内容?

  > 移动版本现在不支持抛出16k音频。
- TTS保存合成音频的方法是什么？

  > 集成MSC中SpeechSynthesizer进行语音合成时保存合成后的音频采用以下方式:

```
mTTS.setParams(SpeechConstant.AUDIO_FORMAT, "wav");
mTTS.setParams(SpeechConstant.TTS_AUDIO_PATH,"mnt/sdcard/tts/xxx.wav");
```

- 英文识别选择优先阿拉伯数字，没有效果？

  > 英文识别目前不支持平台勾选的数字优先,后期会进行优化。
- 用云函数自定义技能的话，怎么接入第三方的信源？

  > 参考如下代码

```javascript
var http = require('http');

if ("wordIntroduce" == eventName) {
    wordIntroduceHandler();
} else {
    response.speak("请说出你想查询的词汇。");
}

function wordIntroduceHandler(){
    let word = getSlotValue(event.request.slots, "word")
    if (word == null || word == "" || word == undefined) {
        response.speak("请说出你想查询的词汇。");
    }
    let url = 'http://www.xxx.cn/demo?name=' + encodeURIComponent(word);
    doHttpGet(url, function(data){
        if(data.rc == '0' && data.total != "0"){
            let info = data.result[0];
            let result = {
                morfei_name: info.name,
                morfei_img: info.img,
                morfei_description: info.description
            }
            response.speak(info.description,result);
        }else{
            response.speak("词典还没收录此条数据。");
        }

    })
}

function getSlotValue(semanticSlots, slotName) {
    for (let i in semanticSlots) {
        slot = semanticSlots[i];
        if (slotName == slot.name) {
            return slot.normValue;
        }
    }
    return null;
}

function doHttpGet(url,callback) {
    http.get(url, function (res) {
        res.setEncoding('utf8');
        var chunks = '';
        res.on('data', function (chunk) {
            chunks += chunk;
        });
        res.on('end', function () {
            callback(JSON.parse(chunks));
        });
    }).on('error', function (e) {
        defaultErrorAnswer();
    }).setTimeout(800, function () {
        defaultErrorAnswer();
    });
}
```text

- 如何使用开放技能上传动态实体实现打电话技能？

  > AIUI为开发者提供了打电话开放技能，但是联系人数据需要开发者或用户上传，开发者可以参考此篇帖子进行开发。[使用AIUI实现打电话功能教程](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38705&extra=)
- aiui.log日志怎么保存？

  > AIUI评估板中的日志名称为msc.log（不久后会改为aiui.log），移动手机版为aiui.log。对于评估板和Android手机开发者，需要将msc.cfg文件push到sdcard/msc/目录下；对于iOS开发者，则需要将msc.cfg放到沙盒中，操作流程参考[iOS平台aiui.log日志保存教程](http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38695&extra=)

- 自定义问答选择情感合成后语音不合成是什么原因？

  > AIUI在闲聊的回答中会情感标签，目前仅有萌萌的发音人支持情感合成，所以替换不支持情感合成的发音人后，会导致不能播报的情况。
- AIUI支持8k音频吗？

  > SDK只支持 16k 16bit音频，WebAPI支持 8k和16k音频识别。

- telephone技能data/result字段出现fuzzy\_score、fuzzy\_type字段
  出现该字段表示该条数据是通过模糊匹配得出，开发者无需特殊关注。

- 移动端设备在语音合成时偶尔发生因为识别到自己的声音而答非所问是什么原因？

  > 移动端设备不像AIUI评估板等智能硬件一样具备麦克风阵列，SDK内部无法集成降噪、回声消除、声源定位等算法。如果是持续交互模式（一次唤醒、持续交互）下语音合成是比较容易被麦克风吸收识别的。解决这个问题，我们我们推荐使用oneshot交互模式（一次唤醒一次交互）或者智能硬件解决方案。
- 在某些应用场景下一些专业领域词汇的识别率稍低怎么办？

  > 针对您的应用（产品）中出现的专有词汇，可以通过上传热词的方式来提高识别率。例如“燕京啤酒”在通用领域可能会被识别成“眼睛啤酒”，但是当您上传了热词后，识别成功率会大概率提升。热词可以直接在我的应用中进行上传配置，生效时间是10~60分钟。
- 应用配置了后处理，但是在平台“快速体验界面”体验没有反应怎么办？

  > 快速体验不支持调试后处理业务，您可以使用客户端SDK进行调试。
- aiui问答库支持用API导入吗？

  > 不支持，目前问答库只能通过平台上通过进行配置，在平台上进行配置比较方便快捷。
- 我的应用和技能都不支持删除吗？

  > 是的，目前我的应用和技能暂时不支持删除，不过我们正在进行产品设计和规划，具体支持时间以平台通知为准，欢迎大家关注AIUI开放平台。
- 自定义问答库支持英文吗？

  > 不支持。
