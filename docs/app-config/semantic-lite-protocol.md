---
title: 语义精简协议介绍
---

精简协议概述

精简协议简化了标准语义协议。适用于低算力设备。

标准协议缺陷：1.不同技能的result字段不同，设备端解析不便

       2.有n个技能就需要解析n个service

       3.RTOS设备的内存不足以解析完整协议

## 精简协议内容

精简协议规整了媒资类和播报类技能，其中媒资类技能指的是需要从data.result字段中拿到播放的url进行播放，而播报类技能则指的是只需要播报answer内容的技能。

### 1.1. 媒资类技能的协议修改点

- 新增service\_pkg字段，表示技能的精简协议类型，将官方媒资类技能统一打包，通过 service\_pkg=”media”标识；客户端只需要判断该字段即可对媒资类技能统一处理；
- 针对媒资类技能，data.result字段只保留4个：

|  |  |  |
| --- | --- | --- |
| **字段** | **类型** | **说明** |
| itemid | String | 资源ID |
| uni\_url | String | 资源地址 |
| duration | String | 资源播放持续时间 |
| name | String | 资源名称 |

- 针对媒资类技能，data.result数组长度缩减到5条。

### 1.2. 播报类技能的协议修改点

- 新增service\_pkg字段，表示技能的精简协议类型，将播报类技能统一打包，通过 service\_pkg=”broadcast”标识；客户端只需要判断该字段即可对播报类技能统一处理；
- 播报类技能，data.result数组中不再返回数据。

### 1.3. 建议客户端对于精简协议的处理流程

![](/media/202508/2025-08-26_104544_4249630.5081075964548062.png)

## 精简协议技能列表

### 2.1. 媒资类技能列表

|  |  |  |
| --- | --- | --- |
| **service** | **中文名** | **类型** |
| AIUI.audioBook | 有声书 | 媒资类 |
| AIUI.Bible | 圣经 | 媒资类 |
| AIUI.chCultivation | 儿童兴趣培养 | 媒资类 |
| AIUI.chDevelopment | 儿童学堂 | 媒资类 |
| AIUI.chLiterature | 国学 | 媒资类 |
| AIUI.chSong | 儿歌 | 媒资类 |
| AIUI.meditationTime | 冥想时刻 | 媒资类 |
| AIUI.ocularGym | 眼保健操 | 媒资类 |
| AIUI.sleepWell | 好好睡觉 | 媒资类 |
| AIUI.smarter | 越听越聪明 | 媒资类 |
| AIUI.whiteNoise | 白噪音 | 媒资类 |
| animalCries | 动物叫声 | 媒资类 |
| crossTalk | 相声小品 | 媒资类 |
| drama | 戏曲 | 媒资类 |
| englishEveryday | 英语每日一句 | 媒资类 |
| health | 健康讲座 | 媒资类 |
| history | 历史 | 媒资类 |
| KLLI3.studyPinYin | 我想学拼音 | 媒资类 |
| LEIQIAO.funnyPassage | 搞笑段子 | 媒资类 |
| LEIQIAO.openClass | 公开课 | 媒资类 |
| LEIQIAO.speech | 名人演讲 | 媒资类 |
| musicX | 音乐 | 媒资类 |
| musicX\_dialect | 音乐方言版 | 媒资类 |
| news | 新闻 | 媒资类 |
| novel | 有声小说 | 媒资类 |
| radio | 广播电台 | 媒资类 |
| story | 故事 | 媒资类 |
| storyTelling | 评书 | 媒资类 |

### 2.2. 播报类技能列表

|  |  |  |
| --- | --- | --- |
| **service** | **中文名** | **类型** |
| KLLI3.FamilyNames | 百家姓 | 播报类 |
| baike | 百科 | 播报类 |
| AIUI.2bd672cefd | 猜数字 | 播报类 |
| lottery | 彩票 | 播报类 |
| cookbook | 菜谱 | 播报类 |
| AIUI.e09af9377o | 成语接龙 | 播报类 |
| wordsDictionary | 词典 | 播报类 |
| AIUI.unitConversion | 单位换算 | 播报类 |
| translation | 翻译 | 播报类 |
| college | 高校查询 | 播报类 |
| AIUI.collegeScore | 高校分数线 | 播报类 |
| KLLI3.powerScaler | 功率换算 | 播报类 |
| stock | 股票 | 播报类 |
| LEIQIAO.cityOfPro | 国内城市查询 | 播报类 |
| AIUI.forex | 汇率 | 播报类 |
| AIUI.f65cf38453 | 会说话的小鹦鹉 | 播报类 |
| AIUI.calc | 计算器 | 播报类 |
| LEIQIAO.relationShip | 家族关系神器 | 播报类 |
| holiday | 假期安排 | 播报类 |
| AIUI.cd756aff0p | 剪刀石头布 | 播报类 |
| petrolPrice | 今日油价 | 播报类 |
| KLLI3.numberScaler | 进制转换 | 播报类 |
| AIUI.famousQuotes | 经典名句 | 播报类 |
| LEIQIAO.timesTable | 九九乘法表 | 播报类 |
| AIUI.85beebdd4t | 口算挑战 | 播报类 |
| garbageClassify | 垃圾分类 | 播报类 |
| LEIQIAO.historyToday | 历史上的今天 | 播报类 |
| AIUI.b1ed7474c9 | 谜语 | 播报类 |
| AIUI.20aafd8b1r | 脑筋急转弯 | 播报类 |
| AIUI.ac140b7894 | 抛硬币 | 播报类 |
| carNumber | 汽车尾号限行 | 播报类 |
| chineseZodiac | 生肖运势 | 播报类 |
| ZUOMX.queryCapital | 省会查询 | 播报类 |
| poetry | 诗词 | 播报类 |
| AIUI.179c5b26by | 诗词挑战 | 播报类 |
| datetimePro | 时间日期查询 | 播报类 |
| AIUI.WorldCup | 世界杯 | 播报类 |
| KLLI3.captialInfo | 首都查询 | 播报类 |
| LEIQIAO.BMI | 体重指数查询 | 播报类 |
| weather | 天气 | 播报类 |
| weather\_dialect | 天气方言版 | 播报类 |
| AIUI.114c02b04p | 跳数字 | 播报类 |
| calendar | 万年历 | 播报类 |
| joke | 笑话 | 播报类 |
| AIUI.virusSearch | 新冠疫情查询 | 播报类 |
| constellation | 星座 | 播报类 |
| dream | 周公解梦 | 播报类 |
| EGO.healthKnowledge | 健康知识 | 播报类 |
| EGO.foodsCalorie | 食物热量 | 播报类 |
