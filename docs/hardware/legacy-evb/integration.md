---
title: 集成方式
---

# 接入方式

AIUI 评估板提供了多种集成方式。在后期量产时，请[联系我们](/faq/contact)获取更完整的集成流程。

## 核心板模式

### 适用场景

适用于故事机、智能音箱等一些无屏交互的场景。

### 集成说明

开发者APP集成[AIUIServiceKit](/hardware/legacy-evb/aiui-service-kit)，运行在AIUI模块上，从AIUIService获取结果，进行解析处理，与评估板上AIUIProductDemo的效果类似，完整结构如下图所示：

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/3_access_service/access_evm/screenshot_1519544156229.png -->
![待补充：AIUI 评估板集成架构图01](/images/placeholder.svg)

具体集成方法请参见[AIUIServiceKit SDK](/hardware/legacy-evb/aiui-service-kit)，对AIUI核心板模块有任何疑问的可参考[`AIUI模块数据手册`](https://xfyun-doc.cn-bj.ufileos.com/1519542857029703/AIUI模块XFAI0801数据手册V0.3.pdf)。

### 开发者程序自启动

Android 4.4之后的版本，默认新安装未启动的程序处于Stopped状态，无法接受系统广播BOOT\_COMPLETE实现自启动，所以AIUI添加对第三方应用自启动的支持。

第三方应用只需要创建Receiver，按照如下的配置接收AIUI的广播即可:

```xml
<receiver android:name=".BootReceiver">
        <intent-filter>
                <action android:name="com.iflytek.aiuilauncher.action.BOOT_START"/>
        </intent-filter>
</receiver>
```

## 软核模式

软核模式和[核心板模式](/hardware/legacy-evb/integration)的软件结构是一样的，区别在于软核模式将AIUIService及其他Apk运行在开发者的硬件上（操作系统需要是Android）。

集成的时候AIUI只提供AIUI软件APK，所以称为软核模式。

### 适用场景

适用于硬件上需要灵活定制的场景。

### 集成说明

AIUI软核方案对开发者的硬件设计和录音都有一定的要求：

- 加密芯片

  AIUI只有在有加密芯片的硬件上才能正常运行，所以开发者的定制硬件上需要有加密芯片。
- 录音

  AIUI录音没有使用默认的录音机，而是系统定制中的Alsa(Advanced Linux
   Sound Architecture)录音机，
   开发者集成软核方案时可以选择自己录音通过AIUI ServiceKit
   SDK写入原始音频，也可以修改系统支持Alsa。

具体的要求和对接开发事项请[联系我们](/faq/contact)。

### 麦克风阵列方案迁移

如果采用了麦克风阵列的软核方案，那迁移到AIUI软核方案就十分简单，因为上面提到的加密芯片和录音的要求均已达到。

按以下步骤集成：

① 在开发集成评估时，将加密芯片替换为AIUI测试加密芯片，在测试完成量产时，再使用厂商特定AIUI加密芯片。

> 不同加密芯片需要联系商务提供特定版本的AIUIService apk。联系时请说明以下参数：
>
> - 几麦
> - 加密密钥挂载位置
> - 通道号是默认还是有其他需求

② 修改AIUI配置文件中的`alsa`参数下的`sound_card`和`sample_rate`参数为麦克风软核阵列方案确定的录音参数。

③ 开发集成参考[核心板模式](/hardware/legacy-evb/integration)。

## 上位机模式

### 适用场景

适用：上位机和AIUI模块通过串口通信，适用于有屏幕需求或硬件扩展需求（如机器人，智能家居等）。

### 集成说明

<!-- TODO: 需手动补充图片，原始 URL: https://aiui-file.cn-bj.ufileos.com/aiui-doc/3_access_service/access_evm/screenshot_1519546039919.png -->
![待补充：AIUI 评估板集成架构图02](/images/placeholder.svg)

如上图所示，为上位机模式的开发结构图，UARTService充当AIUIService和上位机之间的中介，一面负责将AIUI的结果通过串口发送给上位机，一面将上位机通过串口发送的指令发送到AIUI。

AIUIProductDemo是个可选的选项，因为如果在上位机上对结果进行解析播放，那么AIUI模块上的AIUIProductDemo的播报就不必要了。

具体集成方法请参见[串口SDK](/hardware/legacy-evb/serial-sdk)。
