---
title: SDK 状态说明
description: AIUI SDK 的三种运行状态及状态转换机制说明
---

## SDK 状态

AIUI SDK 有 3 种状态：

**STATE_IDLE：** 未开启状态，此时只能进行 start（开启服务）操作。

**STATE_READY：** 就绪状态，不处理数据，需要语音唤醒或者发送 CMD_WAKEUP 手动唤醒。

**STATE_WORKING：** 工作状态，可以处理数据。

## 状态转换说明

AIUI SDK 三种状态之间的转化流程如下：

- AIUIAgent 创建时，是 `idle` 状态；
- 发送 CMD_START 消息后是 `ready` 状态；
- 发送唤醒消息后是 `working` 状态，此时可语音或文本与 AIUI 交互。

更详细状态转换说明如下图所示：

![SDK 状态转换图](/media/202506/2025-06-10_165957_3200100.4926176772522235.png)

| 操作名称 | 说明 |
| --- | --- |
| start | 向 SDK 发送 CMD_START 消息。 |
| stop | 向 SDK 发送 CMD_STOP 消息。 |
| wakeup | 语音唤醒或手动发送唤醒指令 CMD_WAKEUP。 |
| reset_wakeup | 发送 CMD_RESET_WAKEUP 消息。 |
| sleep | 休眠，当一段时间内无有效交互（语义）发生。 |
| re_wakeup | 在 STATE_WORKING 状态下，再次说出唤醒词，或者向 SDK 发送 CMD_WAKEUP 消息。 |

## SDK 状态与事件关联

### 打开和关闭

:::tip 提示
通用 AIUI SDK 接入时开发者可以不用关心这两个消息事件，SDK 初始化后默认就启动了 AIUI 服务。
:::

- `CMD_START` -- 启动 AIUI 服务（SDK 初始化自动调用）
- `CMD_STOP` -- 停止 AIUI 服务，此时不能唤醒

### 唤醒和休眠

语音唤醒或者发送 `CMD_WAKEUP` 消息进入工作状态。如果连续一段时间（[配置文件](/sdk-dev/basics/params/)中 `interact_timeout` 参数）无**有效交互**就会进入就绪状态，或者发送 `CMD_RESET_WAKEUP` 消息。

:::info 有效交互
有效交互：交互请求有技能语义结果，结果中 rc 字段的值为 0 或 3。
:::

### 延迟休眠

持续一段时间无**有效交互**，AIUI 就会休眠（[配置文件](/sdk-dev/basics/params/)的 `interact_timeout` 可配置）。

**有效交互**：交互的结果有语义结果，`rc` 字段的值为 0 或 3。

1. AIUI 平台关闭语义理解就没有语义结果，是无效交互。
2. 第三方后处理结果中的语义难以辨别，是无效交互。

收到语义结果后 5 秒内发送 `CMD_RESULT_VALIDATION_ACK`，设置这次结果为有效交互。

## SDK 回调解析说明

Android 示例代码如下，开发者可以通过 AIUI SDK 状态事件来判断当前是否可以进行对话交互。

```java
private final AIUIListener mAIUIListener = new AIUIListener() {
    @Override
    public void onEvent(AIUIEvent event) {
        Log.i(TAG, "onEvent, eventType=" + event.eventType);

        switch (event.eventType) {

            case AIUIConstant.EVENT_STATE: {    // 状态事件
                int state = event.arg1;

                if (AIUIConstant.STATE_IDLE == state) {
                    // 闲置状态，AIUI 未开启
                    showTip("STATE_IDLE");
                } else if (AIUIConstant.STATE_READY == state) {
                    // AIUI 已就绪，等待唤醒
                    showTip("STATE_READY");
                } else if (AIUIConstant.STATE_WORKING == state) {
                    // AIUI 工作中，可进行交互
                    showTip("STATE_WORKING");
                }
            }
            break;
        }
    }
};
```

## 交互历史

AIUI 云端服务默认会存储交互历史，在后续对话中根据上下文信息可以做更好的回复。

- **传统语义链路**

  AIUI 服务存储 5 轮对话历史，仅技能语义服务加载使用。例：先问"合肥今天的天气"，再问"明天呢"，结合交互历史，AIUI 技能语义会回答合肥明天的天气。

  在传统链路下，AIUI SDK 交互支持用户配置交互历史使用方式，对于**清除历史**方式，详见[配置](/sdk-dev/basics/params/)中 `clean_dialog_history` 字段取值说明。

  - `auto:` 休眠后自动清除历史。
  - `user:` 用户发送 `CMD_CLEAN_DIALOG_HISTORY` 手动清除历史。

  ```java
  // 手动清除交互历史
  AIUIMessage cleanMessage = new AIUIMessage(AIUIConstant.CMD_CLEAN_DIALOG_HISTORY, 0, 0, "", null);
  mAIUIAgent.sendMessage(cleanMessage);
  ```

- **通用大模型链路**

  AIUI 云端服务存储 2 轮对话历史（用户原始 query 和回复 answer），服务链路中语义规整、技能语义、文档问答、大模型回复等模块会加载使用，根据历史信息输出更准确的结果。例如在语义规整模块上，先问"合肥今天的天气"，再问"明天呢"，会规整用户请求为："合肥明天的天气"。

- **极速超拟人链路**

  和通用大模型链路基本流程保持一致，区别在于极速超拟人链路云端存储 10 轮对话历史（用户原始 query 和回复 answer）。影响服务链路中语义规整、技能语义、文档问答、大模型回复等模块结果输出。
