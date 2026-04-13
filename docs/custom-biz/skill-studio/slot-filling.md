---
title: 填槽对话
---

**目录**

1. 多轮对话
    1.1. 意图内多轮对话（填槽对话）
    1.2. 意图间多轮对话
2. 填槽对话概念
3. 图示
4. 示例
5. 系统配置与云函数的相互配合
6. 注意事项

## 多轮对话

多轮对话分为**意图内多轮对话**、**意图间多轮对话**。

### 1.1. 意图内多轮对话（填槽对话）

填槽对话：信息不完整，引导用户补充

示例

- 用户：我要订闹钟
- 系统：您要订几点的闹钟 （填槽对话：追问语句）
- 用户：明早六点

### 1.2. 意图间多轮对话

示例

- 用户：订1间房
- 系统：预约成功，请问还需要一份早餐吗？
- 用户：来3份
- 系统：预定成功

上述示例包含「定房间」和「定早餐」2个意图。意图间的多轮对话，需要开发者自己实现，具体参考技能云函数。

## 填槽对话概念

1. 槽值和追问语句
   例如订闹钟技能，槽值是时间（time），是必须信息。
   缺少必须信息会触发追问：**您要订几点的闹钟**
2. 槽位确认
   槽位可设置为需用户确认。请谨慎使用，避免繁琐。示例：

- 用户：订2间房
- 系统：是2间房吗？ （槽位确认）

3. 意图确认
   意图可设置为需用户确认，例如在购物技能中，当用户选购完商品后，你可以要求对意图进行确认，“你购买了一副墨镜，确认下单吗？”。

## 图示

填槽对话流程图：

- 如果使用 Delegate（托管）或者关闭云函数，系统会依次遍历每一个环节（每次请求都是从第一个环节开始遍历）。当系统发现该环节被开发者在平台上标记为**必选**或者**开启**，且该环节的值为 **null** 或者 **none**，就会触发该环节，否则会跳过该环节直至流程结束。
- 如果开发者调用了ElicitSlotDirective（槽追问）、ConfirmSlotDirective（槽位确认）、ConfirmIntentDirective（意图确认），则以开发者指定的环节为准。

<!-- TODO: 需手动补充图片，原始 URL: http://aiui-file.cn-bj.ufileos.com/aiui-doc/4_skill_develop/2_reference/tcdh.png -->
![待补充：填槽对话流程图](/images/placeholder.svg)

## 示例

以”订票”技能举例，飞机票（buyPlaneTicket）意图的语义槽分别是fromCity（出发城市）、toCity（到达城市）、time（出发时间），其中 fromCity 通过 GPS 信息获取，toCity和time为用户必须回答的槽位。

示例对话：
槽追问

- 用户：买一张周三的飞机票
- 系统：你想到哪个城市？

  ```
  {
  "name": "buyPlaneTicket",
  "confirmationStatus": "NONE"
  "slots": [
    {
      "name": "fromCity",
      "value": "",//开发者通过获取 GPS 信息，通过代码填写为合肥
      "confirmationStatus": "NONE"
    },
    {
      "name": "toCity",
      "value": "",
      "confirmationStatus": "NONE"
    },
    {
      "name": "time",
      "value": "周三",★★★
      "confirmationStatus": "NONE"
    }
  ],
  }
  ```

槽确认

- 用户：我想去北京
- 系统：你确认目的地是北京吗 （ 槽位确认 ）

```json
{
  "name": "buyPlaneTicket",
  "slots": [
    {
      "name": "fromCity",
      "value": "合肥",
      "confirmationStatus": "NONE"
    },
    {
      "name": "toCity",
      "value": "北京",★★★
      "confirmationStatus": "NONE"
    },
    {
      "name": "time",
      "value": "周三",
      "confirmationStatus": "NONE"
    }
  ],
  "confirmationStatus": "NONE"
}
```

意图确认

- 用户：确认
- 系统：好的，周三从合肥去北京的机票确认下单吗 （ 意图确认 ）

```json
{
  "name": "buyPlaneTicket",
  "slots": [
    {
      "name": "fromCity",
      "value": "合肥",
      "confirmationStatus": "NONE"
    },
    {
      "name": "toCity",
      "value": "北京",
      "confirmationStatus": "CONFIRMED"
    },
    {
      "name": "time",
      "value": "周三",
      "confirmationStatus": "NONE"
    }
  ],
  "confirmationStatus": "NONE"
}
```

填槽对话结束

- 用户：确认下单
- 系统：好的，已下单 （填槽对话结束）

```json
{

  "name": "buyPlaneTicket",
  "slots": [
    {
      "name": "fromCity",
      "value": "",
      "confirmationStatus": "NONE"
    },
    {
      "name": "toCity",
      "value": "北京",
      "confirmationStatus": "CONFIRMED"
    },
    {
      "name": "time",
      "value": "周三",
      "confirmationStatus": "NONE"
    }
  ],
  "confirmationStatus": "CONFIRMED"
}
```

## 系统配置与云函数的相互配合

假如我们现在拥有一个快递查询 API，99%的快递单号，可以自动判断快递公司，1%的快递单号需人工选择。以查快递技能举例，我们应当把 express\_number 和 express\_company 勾选为必选槽（如下图）

![](/media/202407/2024-07-09_165650_1768140.6362392210097515.png "null")

实际使用中云函数中的**伪代码**如下：

```
if(express_number.value==null){
    if(express_company.value==null){
        //如果用户没有标明快递公司，则使用自动识别
        express_company.value="自动识别"
    }
    //如果快递单号为空，因为在平台上配置了必选槽，可以直接托管给系统
    //此时使用ElicitSlotDirective效果相同
    DelegateDirective()
    return
}

// 调用 API 获取快递信息
express_result = express_api(express_number.value)

if(express_result=='无法自动判断快递公司'){
    // 如果无法自动判断快递公司，使用ElicitSlot追问用户
    ElicitSlotDirective(express_company,'请问你的快递公司是什么')

}else{
    // 可以自动判断快递公司，直接播报查询结果给用户
    speak(express_result)
}
```

## 注意事项

填槽对话只是准确理解需求的一个技术手段，但不鼓励设计过多的多轮对话。

反例

- 用户：清华大学的录取分数线是多少
- 系统：请问你想查询的省份是哪一个？
- 用户：安徽
- 系统：请问你是文科还是理科？
- 用户：理科
- 系统：请问你想查询哪一年的分数？
- 用户：2017年
- 系统：请问你想查询的是提前批还是本科一批？
- 用户：本科一批
- 系统：2017年清华大学在安徽的本科一批理科投档线是670分

正例

- 用户：清华大学的录取分数线是多少
- 系统：清华大学2017年在安徽的本科一批投档线是理科670分、文科648分。你还可以问我往年和提前批的分数线。

开发者可以通过GPS 获取设备位置，默认返回最近一年的分数，多数情况下用户想要知道的是本科一批的信息，文科理科分数线可以同时返回，在返回了关键信息后，提醒用户可以通过进一步的对话，获取更多信息。
