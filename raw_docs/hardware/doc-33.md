---
title: 软件包说明
source_url: https://aiui-doc.xf-yun.com/project-1/doc-33/
---

## 概览

在官网下载的SDK包中包含很多资源，为了保障开发者能充分了解并使用它们，下面将分别介绍下它们的功能特点。

### bin目录

该目录下包含体验评估板语音交互能力所需的app以及更新app的批处理脚本。

|  |  |  |
| --- | --- | --- |
| 应用名称 | 安装载体 | 功能 |
| AIUILauncher | 评估板/核心板 | 系统级应用，安装时应push到/system/app/目录下，其主要功能是发送开机广播（开发者应用可监听此广播实现开机启动）、开机后拉起UARTService、ControlService、SmartConfigService服务。 |
| AIUIProductDemo | 评估板/核心板 | AIUI默认播报程序，包含完整的交互处理逻辑，如评估板的灯光控制、歌曲播报等。 |
| AIUIService | 评估板/核心板 | AIUI核心服务，包含语音唤醒、端点检测、离线命令词识别以及跟AIUI服务端通信等功能。 |
| ControlService | 评估板/核心板 | 评估板中给ControlClient提供服务的应用程序。 |
| SmartConfigService | 评估板/核心板 | 为评估板开启smartconfig配网的服务程序。 |
| UARTService | 评估板/核心板 | 负责串口通信的服务，作为上位机与评估板之间的通信入口。 |
| ControlClient | Android手机 | 运行在手机平台的应用，主要功能有：启动wifi配网、配置评估板授权信息以及负责手机端跟评估板之间的局域网通信。 |

AIUI评估板中关键应用关系图如下所示：

![](./images/kuangjia.png "null")

### doc目录

该目录下包含核心板数据手册与麦克风设计参考文档。

### lib目录

该目录下包含AIUIServiceKit.jar，开发者可在自己开发的评估板应用中集成该库，用来与AIUIService进行通信。详细使用可参考[AIUIServiceKit SDK](https://aiui-doc.xf-yun.com/project-1/doc-34/)。

### sample目录

该目录下包含ControlService、ControlClient、AIUIProductDemo、UARTService等应用的源码工程，开发者可在此基础上开发出更多样化的产品。

Demo工程下提供的AIUIDemo是为演示AIUI接口的基本调用方法，该Demo需要界面操作，安装在评估板或核心板中，可以使用TotalControl或vysor进行操作；AIUIDemo与AIUIProductDemo不能同时安装，二选一即可。AIUIDemo与ControlService也不能同时安装，原因参考[AIUI配置provider](https://aiui-doc.xf-yun.com/project-1/doc-13/#注意事项)。

UART工程下提供的UARTKit是Android平台下[AIUI串口协议](https://aiui-doc.xf-yun.com/project-1/doc-35/#aiui串口协议)的封装实现；UARTKitCtrDemo是上位机（Android平台）集成[AIUI串口协议](https://aiui-doc.xf-yun.com/project-1/doc-35/#aiui串口协议)的基本实现与调用方法演示程序，开发者可参考此代码实现上位机程序。

### SmartConfig目录

该目录下包含SmartConfig的示例Demo及集成文档。

### tools（其他工具）目录

该目录下包含在PC端使用adb工具对评估板进行配网的批处理脚本与获取msc日志的配置文件。

开发者在开发过程中遇到问题，如10120错误，可将msc.cfg放入/sdcard/msc/目录下，重启后复现问题，然后将/sdcard/msc/目录下的所有日志文件pull出来，发送给技术支持分析。
