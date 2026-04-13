---
title: 合成能力使用
---

概述

本文档主要介绍在**传统语义交互链路**下使用API协议进行主动合成服务调用说明。

## 调用说明

温馨提示

传统语义链路**仅支持普通发音人合成调用。**

### 确认参数

普通类发音人除部分免费外，其它发音人需要联系讯飞商务授权，具体发音人信息见[发音人列表](/sdk-dev/voice-list "发音人列表")。

示例普通发音人：小娟

- vcn：**x2\_xiaojuan**

情景模式固定取值：

- scene：**IFLYTEK.TTS（语音合成）**

### 请求构建

`构建请求参数`如下：

```json
{
    "auth_id": "1fdd930f9f995fbc5ebb48e971b791bc",
    "volume": "50",
    "tts_aue": "raw",
    "data_type": "text",
    "scene": "IFLYTEK.tts",
    "vcn": "x2_xiaojuan"
}
```

## 示例代码

下面提供文本合成调用示例：

点击查看python代码

```python
from ws4py.client.threadedclient import WebSocketClient
import base64
import hashlib
import json
import time
import uuid

base_url = "ws://wsapi.xfyun.cn/v1/aiui"
# 在 https://aiui.xfyun.cn/ 新建Webapi应用，并关闭IP白名单限制
app_id = "XX"
api_key = "XXXX"

#数据类型，（text、audio）
data_type = "text";

#场景（默认main、main_box、单合成IFLYTEK.tts）
scene = "IFLYTEK.tts";

#发送的文本
text_msg = "床前明月光，疑是地上霜。";

file_path = r"weather.pcm" #用户自己收集

# 结束标识
end_tag = "--end--"

class WsapiClient(WebSocketClient):
    def opened(self):
        pass

    def closed(self, code, reason=None):
        if code == 1000:
            print("连接正常关闭")
        else:
            print("连接异常关闭，code：" + str(code) + " ，reason：" + str(reason))

    def received_message(self, m):
        s = json.loads(str(m))

        if s['action'] == "started":

            if(scene == "IFLYTEK.tts"):
                self.send(text_msg.encode("utf-8"))
            else :
                if(data_type == "text"):
                    self.send(text_msg.encode("utf-8"))
                if(data_type == "audio"):
                    file_object = open(file_path, 'rb')
                    try:
                        while True:
                            # 每40ms发送1280个字节数据
                            chunk = file_object.read(1280)
                            if not chunk:
                                break
                            self.send(chunk)

                            time.sleep(0.04)
                    finally:
                        file_object.close()

            # 数据发送结束之后发送结束标识
            self.send(bytes(end_tag.encode("utf-8")))
            print("发送结束标识")

        elif s['action'] == "result":
            data = s['data']
            if data['sub'] == "iat":
                print("user: ", data["text"])
            elif data['sub'] == "nlp":
                intent = data['intent']
                if intent['rc'] == 0:
                    print("server: ", intent['answer']['text'])
                else:
                    print("我没有理解你说的话啊")
            elif data['sub'] == "tts":
                # TODO 播报pcm音频
                print("tts: " + base64.b64decode(data['content']).decode())
        else:
            print(s)

def get_auth_id():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return hashlib.md5(":".join([mac[e:e + 2] for e in range(0, 11, 2)]).encode("utf-8")).hexdigest()

if __name__ == '__main__':
    try:
        # 构造握手参数
        curTime = int(time.time())

        auth_id = get_auth_id()

        param_iat = """{{
            "auth_id": "{0}",
            "result_level": "plain",
            "data_type": "audio",
            "aue": "raw",
            "scene": "main_box",
            "sample_rate": "16000",
            "ver_type": "monitor",
            "close_delay": "200",
            "tts_res_type": "url",
            "context": "{{\\\"sdk_support\\\":[\\\"iat\\\",\\\"nlp\\\",\\\"tts\\\"]}}"
        }}"""

        param_text = """{{
            "auth_id": "{0}",
            "result_level": "plain",
            "data_type": "text",
            "scene": "main_box",
            "ver_type": "monitor",
            "close_delay": "200",
            "tts_res_type": "url",
            "context": "{{\\\"sdk_support\\\":[\\\"iat\\\",\\\"nlp\\\",\\\"tts\\\"]}}"
        }}"""

        param_tts = """{{
            "auth_id": "{0}",
            "data_type": "text",
            "vcn": "x2_xiaojuan",
            "scene": "IFLYTEK.tts",
            "tts_aue": "raw"
        }}"""
        param = ""
        if(scene == 'IFLYTEK.tts'):
            param = param_tts.format(auth_id).encode(encoding="utf-8")
        else:
            if(data_type == 'text'):
                param = param_text.format(auth_id).encode(encoding="utf-8")
            if(data_type == 'audio'):
                param = param_iat.format(auth_id).encode(encoding="utf-8")

        paramBase64 = base64.b64encode(param).decode()
        checkSumPre = api_key + str(curTime) + paramBase64
        checksum = hashlib.md5(checkSumPre.encode("utf-8")).hexdigest()
        connParam = "?appid=" + app_id + "&checksum=" + checksum + "&param=" + paramBase64 + "&curtime=" + str(
            curTime) + "&signtype=md5"

        ws = WsapiClient(base_url + connParam, protocols=['chat'], headers=[("Origin", "https://wsapi.xfyun.cn")])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        pass
```
