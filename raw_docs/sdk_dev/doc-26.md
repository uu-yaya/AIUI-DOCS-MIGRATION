---
title: 离线识别
source_url: https://aiui-doc.xf-yun.com/project-1/doc-26/
---

概述

离线识别能力就是依赖本地识别引擎做语音数据处理，支持离线识别、离线命令词。
离线不依赖网络服务，但是效果比在线服务差。

[**- 1、集成说明>>>点击跳转**](#集成说明)
[**- 2、结果解析>>>点击跳转**](#结果解析)
[**- 3、进阶使用>>>点击跳转**](#进阶使用)

## 集成说明

### 1.1. 获取SDK

AIUI平台应用下下载的通用SDK开发包，默认仅支持在线语音交互能力【唤醒除外】，需要支持离线语音识别SDK，需要联系讯飞商务申请，申请方式有：

- 方式1：邮件联系[技术支持](mailto:aiui_support@iflytek.com)说明需求，并提供有效信息
  - 公司名称
  - 联系人方式
  - 产品需求描述
  - AIUI应用appid信息
- 方式2：添加AIUI QQ交流群（575396706）联系讯飞技术同事咨询。

获取支持离线识别能力SDK后，AIUI输出的资源包中，一般包含两部分：

- 开启了离线能力的SDK原始库
- 绑定appid的离线引擎资源

### 1.2. 参数配置

温馨提示

当(esr.engine\_type)离线识别交互模式未指定开启离线命令词能力时，preloads字段要丢弃掉，否则引擎加载将直接报错。

`aiui.cfg`中增加离线识别相关配置：

```
    "speech":{
        "intent_engine_type":"local"
    },

    "esr":{
        "engine_type": "wfst_fsa",
        "pgs_enable": "1",
        "res_type":"assets",
        "res_path":"esr/common.jet",
        "preloads": [
            {
                "id": 0,
                "res_type": "assets",
                "res_path": "esr/contact.jet"
            }
        ]
    },
```

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **模块名称** | | **模块说明** | | |
| **模块名称** | **模块说明** | **参数名称** | **是否必传** | **参数和取值说明** |
| **speech** | 业务相关参数 | intent\_engine\_type | 是 | **语音交互模式** cloud：纯在线语音交互 local：纯离线语音交互 mixed：离在线混合交互【并行模式，返回最快的有效结果】 pipe：优先离线，无有效结果时在请求在线【串行模式】 parallel：离在线混合交互【并行模式，返回全部结果，需SDK版本 6.6.0001.0040版本以上】 |
| **esr** | 离线识别参数 | engine\_type | 是 | **离线识别交互模式** wfst：离线听写模式 wfst\_fsa：离线听写+离线命令词匹配模式  fsa：离线命令词匹配模式 |
| pgs\_enable | 否 | **离线听写流式识别模式** 1：开启 0：关闭（默认） |
| res\_type | 是 | **离线识别资源加载方式** assets：assets资源（apk工程的assets文件） path：path资源（sdcard文件） |
| res\_path | 是 | **离线识别资源文件路径** 使用识别离线识别时必须设置。 |
| preloads | 否 | **离线语法文件加载** 当开启离线命令词能力时才需要配置。 json数组格式，支持多个离线语法文件加载，语法id取值不可重复 |

**重点字段说明**：

- `intent_engine_type`
  控制音频到语义结果的解析方式，取值有：

  - 纯在线处理模式：cloud

  ![](/media/202508/2025-08-20_175422_1468520.26469913463450956.png "null")

  - 纯离线模式：local

  ![](/media/202508/2025-08-20_175404_5128600.1555309231411286.png "null")

  - 离在线并行模式：mixed、parallel

  ![](/media/202508/2025-08-20_172110_5668490.7803748544271709.png "null")

  - 离在线串行模式：pipe

  ![](/media/202508/2025-08-21_092250_5054990.3964926097062822.png "null")

- `preloads`
  配置初始化时默认编译加载的离线语法资源，初始化时默认编译加载的离线语法资源。可以配置多条预加载的资源，在每一条配置中需要声明编译加载语法ID和语法文件路径。
  - 当设置 wfst 纯离线听写模式时，不需要配置该能力项
  - 语法文件支持动态修改。具体见下发使用说明

如上配置之后，SDK在识别时就会按照配置的离线语法进行离线命令词识别，并通过`EVENT_RESULT`返回离线结果，结果数据示例请参见`离线结果`一节的说明。

### 1.3. 离线语法文件编辑

上述章节中提到，当`esr.engine_type`取值模式开启了离线命令词能力【`wfst_fsa` 或 `fsa`】，`preloads`字段将需要配置离线语法文件。

离线命令语法是使用 FSA 描述的语法，对交互话术进行句式拆解，构建句式。

示例离线语法如下，对应的交互句式为： {action}{contact}[{phoneType}]

- [] 代表非必选项

```text
#FSA 1.0;

0    1    <action>
1    2    <contact>
2    3    -
2    3    <phoneType>
;

<action>:拨打|呼叫|打电话给;
<contact>:张三|李四;
<phoneType>:移动号码|家庭号码|单位号码;
```cpp

**格式说明**：

- 以`#`开头的行表示注释行；
- 以`<>`表示slot槽定义，冒号后面是slot的值定义。slot的即可以在语法文件中定义，也可以通过下面章节介绍的方式进行更新；
- 以`-`表示当前网络定义所绑定的槽位属于`非必填项`；
- 以数字开头行表示句式网络定义，上面示例语法网络定义可视化表示如下：

![](/media/202508/2025-08-21_093644_9451880.12186235797019251.png "null")

只要识别的内容能命中定义的网络，SDK就会返回离线命令词结果。比如说法`打电话给张三`会命中0 -> 1(action)和1 -> 2(contact)句式网络定义，那就返回如下离线命令词结果：

```json
{
        "ws": [
            {
                "slot": "action",
                "w": "打电话给"
            },
            {
                "slot": "contact",
                "w": "张三"
            },
            {
                "slot": "",
                "w": "。"
            }
        ]
    }
```text

### 注意：

编写语法文件时，数字与数字间隔处理，需要使用换行符，不可使用空格。

![](/media/202508/2025-08-26_092927_8313420.31543500029372507.png "null")

## 结果解析

根据配置文件中esr的`engine_type`配置，离线解析时会返回**离线流式听写、离线听写，离线命令词结果**这几类结果类型的组合。

- 离线流式听写和离线听写结果
  可以用作识别时的识别过程显示
- 离线命令词结果中包含识别命中离线语法定义的句式结果
  可以用作解析交互的意图。例如`engine_type`是`wfst_fsa`且`pgs_enable`处于开启状态，那一次交互会返回**多次离线流式识别结果 + 一次离线识别结果 + 一次离线命令词结果**。

### 2.1. 离线流式听写结果(esr\_pgs)

配置 `engine_type`取值为`wfst_fsa`且`esr.pgs_enable` 取值为`1`后，监听AIUI SDK回调EVENT\_RESULT事件

- `event.info`结果格式示例

  ```
  {
    "data": [
        {
            "params": {
                "sub": "esr_pgs"
            },
            "content": [
                {
                    "dte": "utf8",
                    "dtf": "json",
                    "cnt_id": "0"
                }
            ]
        }
    ]
  }
  ```
- 解析获取明文result

  ```
  {
    "text": {
        "content": "点一"
    }
  }
  ```

### 2.2. 离线听写结果(esr\_iat)

- `event.info`结果格式示例

  ```
  {
      "data": [
          {
              "params": {
                  "sub": "esr_iat"
              },
              "content": [
                  {
                      "dte": "utf8",
                      "dtf": "json",
                      "cnt_id": "0"
                  }
              ]
          }
      ]
  }
  ```

- 解析获取明文result

  ```
  {
      "text": {
          "bg": "-1",
          "ed": "-1",
          "sc": "26982",
          "ws": [
              {
                  "boundary": "68",
                  "pinyin": "xia4",
                  "sc": "0",
                  "slot": "",
                  "w": "下"
              },
              {
                  "boundary": "76",
                  "pinyin": "yi1",
                  "sc": "0",
                  "slot": "",
                  "w": "一"
              },
              {
                  "boundary": "116",
                  "pinyin": "ye4",
                  "sc": "0",
                  "slot": "",
                  "w": "页"
              },
              {
                  "sc": "0",
                  "slot": null,
                  "w": "。"
              }
          ]
      }
  }
  ```

### 2.3. 离线命令词结果(esr\_fsa)

配置 `esr.engine_type`取值为`wfst_fsa`或`fsa`后，监听AIUI SDK回调EVENT\_RESULT事件。当交互匹配的离线语法文件句式时，返回`esr_fsa`类型结果。解析说明如下：

- `event.info`结果格式示例

  ```
  {
      "data": [
          {
              "params": {
                  "sub": "esr_fsa"
              },
              "content": [
                  {
                      "dte": "utf8",
                      "dtf": "json",
                      "cnt_id": "0"
                  }
              ]
          }
      ]
  }
  ```

- 解析获取明文result

  ```
  {
          "bg": "-1",
          "ed": "-1",
          "sc": "30267",
          "ws": [
              {
                  "boundary": "92",
                  "pinyin": "dian3yi1shou3",
                  "sc": "0",
                  "slot": "play",
                  "w": "点一首"
              },
              {
                  "boundary": "144",
                  "pinyin": "liu2de2hua2",
                  "sc": "0",
                  "slot": "singer",
                  "w": "刘德华"
              },
              {
                  "boundary": "156",
                  "pinyin": "de4",
                  "sc": "0",
                  "slot": "de",
                  "w": "的"
              },
              {
                  "boundary": "200",
                  "pinyin": "ge1",
                  "sc": "0",
                  "slot": "musicSuf",
                  "w": "歌"
              },
              {
                  "sc": "0",
                  "slot": null,
                  "w": "。"
              }
          ]
      }
  ```

## 进阶使用

AIUI离线识别(ESR)开始离线命令词后，关于离线语法配置支持多种加载方式，主要分：

- 静态参数配置
  - 语法文件直接全量配置
  - 语法文件指定槽位更新
- 动态参数设置
  - 使用动态参数更新方式更新离线语法文件槽位取值

### 3.1. 静态参数配置更新槽位

当编写的语法文件中涉及的槽位需要依赖设备或用户做不同取值，例如上面`contact`的slot，我需要更新成我们设备上对应的联系人，那我们可以在配置中为`preloads`资源增加如下的配置：

温馨提示

该方式需要在AIUI SDK初始化前先构建好需要更新的槽位指定的内容文件。如下示例中的 contact\_update.jet 文件取值。

```
"esr":{
    "engine_type": "wfst_fsa",
    "pgs_enable": "1",
    "res_type":"assets",
    "res_path":"esr/common.jet",
    "preloads": [
            {
                "id": 0,
                "res_type": "assets",
                "res_path": "esr/contact.jet",
                "update_slots": [
                    {
                        "slot": "contact",
                        "res_type": "assets",
                        "res_path": "esr/contact_update.jet"
                    }
                ]
            },
     ]
}
```text

上述示例中，代表加载的`contact.jet`离线语法文件中`contact`槽位取值依赖`contact_update.jet`文件中实际取值。

### 注意：

contact\_update.jet离线槽位取值文件编写方式，说明如下：

文件中直接填写槽位取值

用 | 分割每个词条

```java
王二|张海洋
```java

如上的配置加载完成后，我们直接说`打电话给张海洋`就可以如上面一样返回命中的`esr_fsa`结果

### 3.2. 动态参数设置更新槽位

离线识别配置离线命令词能力，除配置文件静态参数直接指定槽位更新，也支持在AIUI程序运行中进行通过动态参数设置来更新需要的槽位取值。

温馨提示

离线语法动态参数设置前提，都需要AIUI SDK处于working工作状态下进行。

#### 3.2.1. 离线语法编译

**代码示例**

```java
String grammarContent = FucUtil.readAssetsFile(this, "esr/contact.jet","utf-8");
AIUIMessage buildMessage = new AIUIMessage(AIUIConstant.CMD_BUILD_GRAMMAR, 1, 0, grammarContent, null);
```

**参数说明**

- `arg1`字段指明编译语法的ID，后面更新语法槽时通过指定相同的语法ID来更新这个语法文件中槽,对应aiui.cfg中preloads下的id取值。 ；
- `arg2`字段指明是否禁用语法编译自动加载下次识别生效，取值如下：
  - `1` ：只编译语法，编译完成后不自动加载生效（可以通过后面的`CMD_LOAD_GRAMMAR`手动加载编译好的语法）
  - `0`  ：编译语法后自动加载生效
- `params`字段指明编译的语法内容。

**结果回调**
编译结果及下面操作都会通过`EVENT_CMD_RETURN`返回，示例处理如下：

```java
    //AIUI事件监听器
    private AIUIListener mAIUIListener = new AIUIListener() {

        @Override
        public void onEvent(AIUIEvent event) {
            switch (event.eventType) {
                /**
                 * arg1 表示操作的CMD
                 * arg2 表示操作成功(0)失败(错误码)
                 * info 结果信息
                 */
                case AIUIConstant.EVENT_CMD_RETURN: {
                    switch (event.arg1) {
                        case AIUIConstant.CMD_BUILD_GRAMMAR:
                        case AIUIConstant.CMD_UPDATE_LOCAL_LEXICON: {
                            Log.d(TAG, "arg1 " + event.arg1 + " ret " + event.arg2 + " info " + event.info);
                        }
                    }
                }
                break;

                default:
                    break;
            }
        }

    };
```java

#### 3.2.2. 离线语法槽位更新

**代码示例**

```java
String updateContent = String.format("{\"name\": \"%s\", \"content\": \"%s\"}", "contact", "黄莺莺|窦唯|鲍家街四十三号");
AIUIMessage updateMessage = new AIUIMessage(AIUIConstant.CMD_UPDATE_LOCAL_LEXICON, 1, 0, updateContent,null);
```text

**参数说明**

- `arg1`字段指明槽更新目标的语法ID，语法ID需要之前通过`CMD_BUILD_GRAMMAR`完成编译的离线语法ID一致。
- `arg2`字段指明槽更新内容模式是否为追加，取值如下：
  - 0 替换（replace）模式，更新的内容会替换当前槽内容；
  - 1 追加（append）模式，更新的内容会追加到当前槽内容的后面。
- `params` 字段指明槽位更新的内容。

#### 3.2.3. 离线语法加载

**代码示例**

```
AIUIMessage loadMessage = new AIUIMessage(AIUIConstant.CMD_LOAD_GRAMMAR, 1, 0, "", null);
```text

**参数说明**

- `arg1`字段指明需要加载的语法ID，语法ID需要之前通过`CMD_BUILD_GRAMMAR`完成编译的离线语法ID一致。

#### 3.2.4. 离线语法卸载

**代码示例**

```
AIUIMessage loadMessage = new AIUIMessage(AIUIConstant.CMD_UNLOAD_GRAMMAR, 1, 0, "", null)；
```text

**参数说明**

- `arg1`字段指明需要卸载的语法ID，语法ID需要之前通过`CMD_BUILD_GRAMMAR`或`CMD_LOAD_GRAMMAR`完成的离线语法ID一致。
