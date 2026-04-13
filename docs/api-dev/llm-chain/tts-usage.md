---
title: 合成能力使用
---

::: info 概述
本文档主要介绍在**通用大模型交互链路**下使用API协议进行主动合成服务调用说明。

合成类型主要包括：
:::

## 调用说明

温馨提示

通用大模型不支持流式文本合成，如果有需要的话，建议创建新应用对接极速超拟人协议

### 通用合成

**该合成类型指的是使用`普通发音人`进行文本合成，合成文本需`一帧发送完毕`。**

#### 确认参数

普通类发音人除部分免费外，其它发音人需要联系讯飞商务授权，具体发音人信息见[发音人列表](/sdk-dev/voice-list "发音人列表")。

示例普通发音人：小娟

- vcn：**x2\_xiaojuan**

情景模式固定取值：

- scene：**IFLYTEK.TTS（语音合成）**

#### 请求构建

`构建请求`如下：

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.tts"        // 文本合成类请求固定取值（注意超拟人合成时取值方式）
    },
    "parameter": {
        "tts": {
            "vcn": "x2_xiaojuan",                // 普通发音人取值
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",        // 待合成文本：需经过base64编码
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

### 超拟人合成

**该合成类型指的是使用`超拟人发音人`进行文本合成，合成文本需`一帧发送完毕`。**

#### 确认参数

在通用大模型链路下，所有超拟人都免费开放开发者使用。各超拟人发音人信息见[发音人列表](/sdk-dev/voice-list "发音人列表")。

温馨提示

在通用大模型链路下进行主动超拟人合成时，需要注意情景模式取值（**scene：IFLYTEK.hts**）

示例超拟人发音人：聆小琪

- vcn：**x4\_lingxiaoqi\_oral**

情景模式固定取值：

- scene：**IFLYTEK.hts**

#### 请求构建

`构建请求`如下：

```json
{
    "header": {
        "sn": "1234567890",
        "appid": "a44e0f36",
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.hts"                    // 超拟人合成固定传值
    },
    "parameter": {
        "tts": {
            "vcn": "x4_lingxiaoqi_oral",        // 超拟人发音人取值
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",        // 待合成文本：需经过base64编码
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

### 声音复刻合成

温馨提示

在通用大模型链路中，声音复刻仅支持全文本整体合成，不支持流式合成。如需使用流式合成，需要升级使用极速超拟人服务。

#### 确认参数

声音复刻合成类请求，首先需要开发者按照`声音复刻API`注册获取资源id（`res_id`），资源注册详见[4.2.4 声音复刻API](/api-dev/llm-chain/voice-clone-api "4.2.4 声音复刻API")文档说明。

声音复刻合成参数示例：

- vcn：
  - **x5\_clone** // 声音复刻v4版本资源使用时，固定取值
  - **x6\_clone** // 声音复刻omni\_v版本资源使用时，固定取值
- res\_id：**fsdfwee234324** // 创建的资源id
- scene：**IFLYTEK.TTS（语音合成）** // 固定取值

#### 请求构建

`构建请求`如下：

```json
{
    "header": {
        "sn": "1234567890",                    // 与资源注册sn保持一致
        "appid": "a44e0f36",                // 与资源注册appid保持一致
        "stmid": "text-1",
        "status": 3,
        "scene": "IFLYTEK.tts"
    },
    "parameter": {
        "tts": {
            "vcn": "x5_clone",                    // 声音复刻合成固定传值
            "res_id": "fsdfwee234324",            // 声音复刻资源id
            "tts": {
                "channels": 1,
                "sample_rate": 16000,
                "bit_depth": 16,
                "encoding": "raw"
            }
        }
    },
    "payload": {
        "text": {
            "compress": "raw",
            "format": "plain",
            "text": "5omT55S16K+d57uZ5byg5LiJ",        // 待合成文本：需经过base64编码
            "encoding": "utf8",
            "status": 3
        }
    }
}
```

## 示例代码

下面提供`声音复刻类调用示例`，其他合成按照协议说明修改 `scene` 和 `vcn` 取值即可。

点击查看python代码

```python
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import time
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket

## 修改应用应用配置后直接执行即可

# 请求地址
url = "wss://aiui.xf-yun.com/v2/aiint/ws"

appid = "xxx"
api_key = "xxx"
api_secret = "xxx"

# 场景
scene = "IFLYTEK.tts"
# scene = "main_box"

# 请求类型用来设置文本请求还是音频请求，text/audio
data_type = 'text'

# 音频请求上传的音频文件路径：示例
audio_path = "D:/weather.pcm"

# 请求文本
question = "今天晚上吃点啥好呢，是酱香饼还是麻酱拌凉皮"

# 每帧音频数据大小，单位字节
chuncked_size = 1024

audio_save_fp = open('D:\save_hts_audio.pcm', mode='wb+')

class AIUIV2WsClient(object):
    # 初始化
    def __init__(self):
        self.handshake = self.assemble_auth_url(url)

    # 生成握手url
    def assemble_auth_url(self, base_url):
        host = urlparse(base_url).netloc
        path = urlparse(base_url).path
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        print(signature_origin)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        print('get authorization_origin:', authorization_origin)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "host": host,
            "date": date,
            "authorization": authorization,
        }
        # 拼接鉴权参数，生成url
        url = base_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

    def on_open(self, ws):
        # 连接建立成功后开始发送数据
        print("### ws connect open")
        thread.start_new_thread(self.run, ())

    def run(self):
        if data_type == "text":
            self.text_req()
        if data_type == "audio":
            self.audio_req()

    def text_req(self):
         req = self.genTextReq(question, 3)
         self.ws.send(req)

    def audio_req(self):
        f = open(audio_path, 'rb')
        try:
            f.seek(0, 2)
            eof = f.tell()
            f.seek(0, 0)

            first = True
            status = 0
            while True:
                d = f.read(frame_size)
                if not d:
                    break

                if first and f.tell() >= eof:
                    # 一帧传完
                    status = 3
                elif f.tell() >= eof:
                    # 尾帧
                    status = 2
                elif not first:
                    # 中间帧
                    status = 1

                req = self.genAudioReq(d, status)
                first = False
                self.ws.send(req)
                # 发送间隔40毫秒
                time.sleep(0.04)
        finally:
            f.close()

    def genTextReq(self, data, status):
        aiui_data = {
            "header": {
                "sn":"1234567891",
                "app_id": appid,
                "stmid": "text-1",
                "status": status,
                "scene": scene
            },
            "parameter": {
                "nlp": {
                    "nlp": {
                        "compress": "raw",
                        "format": "json",
                        "encoding": "utf8"
                    },
                    # 动态实体
                    "sub_scene": "cbm_v45",
                    "new_session": True
                },
                "tts": {
                    "vcn": "x5_clone",
                    "res_id": "fsdfwee234324",
                    "tts": {
                        "channels": 1,
                        "sample_rate": 16000,
                        "bit_depth": 16,
                        "encoding": "raw"
                    }
                }
            },
            "payload": {
                "text": {
                    "compress": "raw",
                    "format": "plain",
                    "text": base64.b64encode(data.encode('utf-8')).decode('utf-8'),
                    "encoding": "utf8",
                    "status": status
                }
            }
        }
        return json.dumps(aiui_data)

    def genAudioReq(self, data, status):
        # 构造pcm音频请求参数
        aiui_data = {
            "header": {
                "appid": appid,
                "sn": sn,
                "stmid": "audio-1",
                "status": status,
                "scene": scene
            },
            "parameter": {
                "nlp": {
                    "nlp": {
                        "compress": "raw",
                        "format": "json",
                        "encoding": "utf8"
                    },
                    "sub_scene": "cbm_v45",
                    "new_session": True
                }
            },
            "payload": {
                "audio": {
                    "encoding": "raw",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16,
                    "status": status,
                    "audio": base64.b64encode(data).decode(),
                }
            }
        }
        return json.dumps(aiui_data)

    # 收到websocket消息的处理
    def on_message(self, ws, message):
        data = json.loads(message)

        # print('原始结果:', message)
        header = data['header']
        code = header['code']
        # 结果解析
        if code != 0:
            print('请求错误:', code, json.dumps(data, ensure_ascii=False))
            ws.close()
        if 'nlp' in message:
            nlp_json = data['payload']['nlp']
            nlp_text_bs64 = nlp_json['text']
            nlp_text = base64.b64decode(nlp_text_bs64).decode('utf-8')
            nlp_all = json.dumps(data,indent=2)
            # print("--------nlp--------\n" , nlp_all)
            # print("语义结果：",nlp_text,"--------nlp--------\n")
        if 'tts' in message:
            tts_all = json.dumps(data,indent=2)
            print("--------hts_all--------\n",tts_all,"\n--------hts_all_all--------\n")
            tts_audio =  data['payload']['tts']['audio']
            tts_content = base64.b64decode(tts_audio)
            audio_save_fp.write(tts_content)

        if 'status' in header and header['status'] == 2:
            # 接受最后一帧结果，关闭连接
            ws.close()

    def on_error(self, ws, error):
        print("### connection error: " + error)
        ws.close()

    def on_close(self, ws, close_status_code, close_msg):
        print("### connection is closed ###, cloce code:" + str(close_status_code))

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.handshake,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

if __name__ == "__main__":

    client = AIUIV2WsClient()
    client.start()
```
