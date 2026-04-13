---
title: 技能
source_url: https://aiui-doc.xf-yun.com/project-1/doc-46/
---

用户可以给AIUI一些命令，比如创建待办事项列表、设置闹钟、播放歌曲或提供新闻。AlUI根据用户请求执行的任务称为“AlUI 技能”。基本上，AlUI技能是一个语音驱动的AIUI应用程序，旨在提供一种解决用户某一类交互需求的能力；针对确定的某一类需求，提供对话交互流程、结构化结果或知识回复、信源查询等相关内容。

技能的使用，除AIUI平台商店技能提供外，也支持开发者根据自有业务需求进行自定义开发，详见[自定义技能开发](https://aiui-doc.xf-yun.com/project-1/doc-56/ "自定义技能开发")说明。

下面以官方商店技能：**天气技能**为例进行说明，提供对话流程可以有：
**更多官方技能提供可以登陆[AIUI技能商店](https://aiui.xfyun.cn/store/all?chan=AIUI&way=menu "AIUI技能商店")了解。**

```text
用户：今天天气？
系统: 今天16摄氏度
用户：要带伞吗？
系统：不需要
```cpp

返回的结果内容：包含请求内容结构化理解（意图分类、槽位提取）、信源内容查询

```json
{
    "answer": {
        "text": "今天合肥市全天小雨，出门记得带伞，气温23℃ ~ 30℃，空气质量优，有西南风4-5级，有点热，适合穿短袖短裙等夏季清凉衣物。",
        "type": "T"
    },
    "category": "IFLYTEK.weather",
    "data": {
        "result": [
            {
                "airData": 18,
                "airQuality": "优",
                "city": "合肥市",
                "date": "2024-09-12",
                "dateLong": 1726070400,
                "date_for_voice": "今天",
                "extra": "",
                "humidity": "93%",
                "img": "http://cdn9002.iflyos.cn/osweathericon/07.png",
                "lastUpdateTime": "2024-09-12 15:00:08",
                "pm25": "11",
                "precipitation": "0.5mm",
                "sunRise": "2024-09-12 05:53:00",
                "sunSet": "2024-09-12 18:21:00",
                "temp": 26,
                "tempHigh": "30℃",
                "tempLow": "23℃",
                "tempRange": "23℃ ~ 30℃",
                "tempReal": "28℃",
                "visibility": "",
                "warning": "",
                "weather": "小雨",
                "weatherDescription": "有点热，适合穿短袖短裙等夏季清凉衣物。",
                "weatherDescription3": "23℃到32℃，今天有雨，后天有雨，风不大，气温较高，请尽量避免午后高温时段的户外活动。",
                "weatherDescription7": "23℃到33℃，今天有雨，后天到17号有雨，风不大，气温较高，请尽量避免午后高温时段的户外活动。",
                "weatherType": 7,
                "week": "周四",
                "wind": "西南风4-5级",
                "windLevel": 0
            },
            ……
        ]
    },
    "dialog_stat": "DataValid",
    "rc": 0,
    "save_history": true,
    "semantic": [
        {
            "intent": "QUERY",
            "slots": [
                {
                    "name": "queryType",
                    "value": "内容"
                },
                {
                    "name": "subfocus",
                    "value": "天气状态"
                },
                {
                    "name": "datetime",
                    "normValue": "{\"datetime\":\"2024-09-12\",\"suggestDatetime\":\"2024-09-12\"}",
                    "value": "今天"
                },
                {
                    "name": "location.type",
                    "normValue": "LOC_BASIC",
                    "value": "LOC_BASIC"
                },
                {
                    "name": "location.city",
                    "normValue": "合肥市",
                    "value": "合肥市"
                },
                {
                    "name": "location.cityAddr",
                    "normValue": "合肥",
                    "value": "合肥"
                }
            ]
        }
    ],
    "service": "weather",
    "shouldEndSession": "true",
    "sid": "atn05d0803c@dx00011a3de0f7a11100",
    "state": {
        "fg::weather::default::default": {
            "state": "default"
        }
    },
    "text": "合肥今天的天气",
    "used_state": {
        "state": "default",
        "state_key": "fg::weather::default::default"
    },
    "uuid": "atn05d0803c@dx00011a3de0f7a11100",
    "version": "207.0"
}
```
