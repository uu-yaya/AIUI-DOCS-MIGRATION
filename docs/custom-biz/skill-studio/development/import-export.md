---
title: 技能导入导出
---

## 批量导出

### 1.1. 导出技能

对某一个技能进行批量导出操作。你可以导出后进行本地修改，修改完成后导入进行覆盖，也可以导出后再导入另一个技能，达到技能复制的目的。

### 1.2. 导出实体

对某一个实体的所有词条和别名进行导出操作。你可以导出后进行本地修改，修改完成后导入进行覆盖，也可以导出后再导入另一个实体，达到实体复制的目的。

## 技能导入

### 2.1. 文件包说明

1. 上传.zip文件即可导入技能。导入的.zip包中包含一个`config.json`文件，和意图文件`意图英文名.json`
2. 上传后，系统会对上传的文件进行校验。请确保：.zip文件包中，所有json文件都在一个文件目录下，不包含多余的文件夹。
   1. `意图英文名.json`文件中不存在重复的语料。

### 2.2. `config.json`说明

`config.json`已升级为v2.1版本，请注意导入时将`version`字段修改为`2.1`。

2.1版本与2.0版本除版本号外，其他信息未做修改。

#### 2.3. 示例

```json
{
    "version": "2.1",//本次更新
    "intents": {
            "queryWeather": {
      "chineseName": "查询",
      "entranceIntent": true,
      "confirmation": {
          "required": true,
          "prompts": [
              "确认查询吗",
              "确定吗"
          ]
      },
      "assistWords": {
          "how": "IFLYTEK.Modal",
          "please": "IFLYTEK.Please"
      },
      "slots": {
          "city": {
              "order": 1,
              "entity": "IFLYTEK.ChinaCity",
              "elicitation": {
                  "required": true,
                  "prompts": [
                      "您想问哪个城市",
                      "哪个城市"
                  ]
              }
          },
          "time": {
              "order": 2,
              "entity": "IFLYTEK.Datetime",
              "elicitation": {
                  "required": false
              }
          }
      },
            "intent2的英文名": {
                //intent2的信息
            }
    }
}
{
    "version": "2.0",//保持不变
    "intents": {

    }
}
```

#### 2.3.1. 字段说明

| 字段 | 说明 | 数据类型 | 是否必需 |
| --- | --- | --- | --- |
| version | 导入的协议版本，当前取值：2.1。 | String | 是 |
| intents | 该技能下的所有意图信息。 | Object | 是 |
| intent[i] | 该技能下的某一个意图的信息，技能下至少有一个意图。该字段取值为意图的英文名。 | Object | 是 |
| intent[i].chineseName | 该意图的中文名，若该字段留空，则将取值为意图英文名 | String | 是 |
| intent[i].entranceIntent | 该意图为入口意图。取值：true（入口意图），false（对话意图）。 请注意，在商店技能中，所有意图均为对话意图，导入时该字段将不会被处理 | Boolean | 否 |
| intent[i].confirmation | 该意图的意图确认信息。 | Object | 是 |
| intent[i].confirmation. required | 该意图是否需要确认。取值：false（不需要确认），true（需要确认） | Boolean | 是 |
| intent[i].confirmation. prompts | 进行意图确认时的确认话术，这是一个string的list | List | 是 |
| intent[i].assistWords | 该意图的语料中包含的辅助词。若意图没有辅助词，该字段留空。 | Map | 是 |
| intent[i].assistWords.\* | 辅助词的key-value键值对。格式为：`"key": "辅助词英文名"` 若使用的是官方辅助词，则需要带上`IFLYTEK.`的前缀。 若使用的是自定义辅助词，则填写自定义实体的英文名。 |  |  |
| intent[i].slots | 该意图的语料中包含的词槽。若意图没有词槽，该字段留空。 | Map | 是 |
| intent[i].slots.\*slots[i] | 该意图的语料中包含的某一个词槽信息。 | Object | 否 |
| intent[i].slots.\*slots[i]. order | 该词槽的顺序 | Integer | 是 |
| intent[i].slots.\*slots[i]. entity | 该词槽对应的实体的英文名。 若使用的是官方实体，则需要带上`IFLYTEK.`的前缀。 若使用的是自定义实体，则填写自定义实体的英文名。 | String | 是 |
| intent[i].slots.\*slots[i]. elicitation | 该词槽的追问信息 | Object | 是 |
| intent[i].slots.\*slots[i]. elicitation.required | 该词槽是否必须，若词槽必填，当用户语料中缺少该槽时，将会进行追问。取值：true(必填槽)，false（非必填槽） | Boolean | 是 |
| intent[i].slots.\*slots[i]. elicitation.prompts | 必填槽缺槽时的追问话术 | List | 是 |

#### 2.3.2. 请确保

1. `intent[i]`的取值为意图的英文名，在.zip文件夹中有对应的意图存在。
2. `config.json`文件中的意图信息，与`意图英文名.json`的意图信息完全相等，不存在多于或少于的情况。
3. `config.json`文件中包含的实体、辅助词信息，与语料文件中引用的实体、辅助词信息一致，不存在多于或少于的情况。

### 2.4. `意图英文名.json`说明

`config.json`版本为2.0时，意图文件为`.txt`格式，2.1升级为`.json`格式，后续将支持更多字段。

#### 示例

```json
[
    {
        "text": "{time}{city}天气怎么样"
    },
    {
        "text": "{今天:time}{广州:city}热不热"
    },
    {
        "text": "天气怎么样"
    }
]
```

#### 2.4.2. 字段说明

整个文件为一个List，每一句语料为一个Object，每个Object中可能包含以下字段

| 字段 | 说明 | 类型 | 是否必需 |
| --- | --- | --- | --- |
| text | 语料文本。 | String | 是 |

#### 2.4.3. 语料写法

语料的3种写法：

1. 模板：{time}{city}天气怎么样。其中花括号中的内容为词槽。
2. 贴弧：{今天:time}{广州:city}热不热。其中花括号中为显示的文本`今天`和对应的词槽`time`。
3. 纯文本：今天广州热不热。

模板写法支持**可选符**。
{}代表词槽
[ ]代表可选，语料不包含可选内容也能命中。例：呼叫张三[的电话|的手机]

- 呼叫张三
- 呼叫张三的电话
- 呼叫张三的手机

( )代表必选，语料必须包含才能命中。例如：(呼叫|联系)张三

- 呼叫张三
- 联系张三

::: warning 注意
一句语料至多有5个中括号和小括号。
:::

仅「模版语料」支持可选符写法\*\*

## 实体导入

实体导入可选择批量覆盖和批量追加。支持excel、txt格式

### 3.1. excel格式

#### 3.1.1. 示例

| 词条名 | 别名 |  |  |  |
| --- | --- | --- | --- | --- |
| 北京 | 帝都 | 首都 | 京城 | 皇城 |
| 合肥 | 霸都 | 安徽省省会 | 安徽省会 |  |

#### 3.1.2. 说明

在excel的第一列填写词条名，后面的列中填写该词条名对应的别名。

### 3.2. txt格式

#### 3.2.1. 示例

```text
北京
帝都        北京
首都        北京
合肥
霸都        合肥
安徽省省会   合肥
庐州        合肥
```

#### 3.2.2. 说明

在txt的第一行填写词条名，回车后填写别名。别名TAB符分隔后填写对应的词条名。
