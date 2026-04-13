---
title: 流式识别
source_url: https://aiui-doc.xf-yun.com/project-1/doc-28/
---

概述

流式识别是语音识别引擎的一种结果输出方式，开启后识别引擎将实时返回引擎处理的结果，实现边说边返回识别结果的效果。
![图标](/media/202212/2022-12-31_150858_5697510.13813317141714532.gif)

[**- 1、开启方法>>>点击跳转**](#开启方法)
[**- 2、结果解析说明>>>点击跳转**](#结果解析说明)

## 开启方法

在AIUI应用的`语音识别配置`项下勾选`progressive 流式识别`选项，及代表开启了流式识别能力。

![](/media/202508/2025-08-20_154653_6893550.46462539284416615.png "null")

## 结果解析说明

开始流式识别配置后，AIUI SDK监听回调`EVENT_RESULT`事件，解析 sub=iat：

- 示例识别结果：`给13856901234充100元话费`
- 回调获取iat结果展示
  - sn：当前的结果id
  - ls：是否为最后一条结果
  - pgs：结果处理字段，apd（追加结果），rpl（替换结果）
  - rg：替换范围

```json
{"sn":1,"ls":false,"bg":0,"ed":0,"pgs":"apd","ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]}]}
{"sn":2,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,1],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"1385"}]}]}
{"sn":3,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,2],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"13856"}]}]}
{"sn":4,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,3],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"138569"}]}]}
......
{"sn":21,"ls":false,"bg":0,"ed":0,"pgs":"rpl","rg":[1,20],"ws":[{"bg":0,"cw":[{"sc":0.00,"w":"给"}]},{"bg":0,"cw":[{"sc":0.00,"w":"13856901234"}]},{"bg":0,"cw":[{"sc":0.00,"w":"充"}]},{"bg":0,"cw":[{"sc":0.00,"w":"100"}]},{"bg":0,"cw":[{"sc":0.00,"w":"元"}]},{"bg":0,"cw":[{"sc":0.00,"w":"话费"}]}]}
{"sn":22,"ls":true,"bg":0,"ed":0,"pgs":"apd","ws":[{"bg":0,"cw":[{"sc":0.00,"w":"。"}]}]}
```java

- 解析示例代码

```java
    //AIUI事件监听器
    private AIUIListener mAIUIListener = new AIUIListener() {

        @Override
        public void onEvent(AIUIEvent event) {
            switch (event.eventType) {
                case AIUIConstant.EVENT_RESULT: {
                    //结果事件
                    Log.i( TAG,  "on event: "+ event.eventType );
                    try {
                        JSONObject bizParamJson = new JSONObject(event.info);
                        JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
                        JSONObject params = data.getJSONObject("params");
                        JSONObject content = data.getJSONArray("content").getJSONObject(0);
                        String sub = params.optString("sub");
                        if (content.has("cnt_id")) {
                            String cnt_id = content.getString("cnt_id");
                            if ("iat".equals(sub)) {
                                JSONObject cntJson = new JSONObject(new String(event.data.getByteArray(cnt_id), "utf-8"));
                                JSONObject result = cntJson.optJSONObject("intent");
                                if(result.length() < 2){
                                    return;
                                }
                                updateIATPGS(cntJson);
                            }
                        }
                    } catch (Throwable e) {
                        e.printStackTrace();
                    }

                } break;

                default:
                    break;
            }
        }
    };

    // 处理听写PGS的队列
    private String[] mIATPGSStack = new String[50];

    private void updateIATPGS(JSONObject cntJson) {
        JSONObject text = cntJson.optJSONObject("text");
        // 解析拼接此次听写结果
        StringBuilder iatText = new StringBuilder();
        JSONArray words = text.optJSONArray("ws");
        boolean lastResult = text.optBoolean("ls");
        for(int index = 0; index < words.length(); index++) {
            JSONArray charWord = words.optJSONObject(index).optJSONArray("cw");
            for(int cIndex = 0; cIndex < charWord.length(); cIndex++) {
                iatText.append(charWord.optJSONObject(cIndex).opt("w"));
            }
        }
        String voiceIAT = "";
        String pgsMode = text.optString("pgs");
        //非PGS模式结果
        if (TextUtils.isEmpty(pgsMode)) {
        } else {
            int serialNumber = text.optInt("sn");
            mIATPGSStack[serialNumber] = iatText.toString();
            //pgs结果两种模式rpl和apd模式（替换和追加模式）
            if("rpl".equals(pgsMode)) {
                //根据replace指定的range，清空stack中对应位置值
                JSONArray replaceRange = text.optJSONArray("rg");
                try {
                    int start = replaceRange.getInt(0);
                    int end = replaceRange.getInt(1);
                    for(int index = start; index <= end; index++) {
                        mIATPGSStack[index] = null;
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            StringBuilder PGSResult = new StringBuilder();
            //汇总stack经过操作后的剩余的有效结果信息
            for(int index = 0; index < mIATPGSStack.length; index++) {
                if(TextUtils.isEmpty(mIATPGSStack[index])) continue;

                if(!TextUtils.isEmpty(PGSResult.toString())) PGSResult.append("\n");
                PGSResult.append(mIATPGSStack[index]);
                //如果是最后一条听写结果，则清空stack便于下次使用
                if(lastResult) {
                    mIATPGSStack[index] = null;
                }
            }
            voiceIAT = PGSResult.toString();
            mNlpText.setText(voiceIAT);
        }
    }
```
