---
title: 声纹管理 API
---

## 服务介绍

温馨提示

1、本服务使用前需先联系讯飞商务获取授权或发送邮件到 aiui\_support@iflytek.com 提交申请。

2、接口调用前，指定的设备（SN）需要先调用AIUI服务完成设备激活。

3、每个设备（SN）默认限制最多添加10个成员，每个成员最多可以注册3个声纹。

本服务文档主要介绍声纹识别相关服务接口，主要接口如下：
**成员控制相关接口**

- 成员添加
- 成员查询
- 成员编辑
- 成员删除

**声纹相关接口**

- 声纹注册
- 声纹查询
- 声纹更新
- 声纹删除
- 声纹检索

## 接口说明

### 请求地址

> `http[s]://aiui.xf-yun.com`

### 接口鉴权

具体鉴权参数构建见[鉴权文档](/api-dev/llm-chain/auth "大模型API服务鉴权")说明。

### 注意：

鉴权的时间戳有时效性，建议每次请求鉴权时都实时的获取最新时间戳，生成鉴权参数

## 功能接口

### 3.1. 成员添加

成员与设备（sn）绑定，每个设备最多可以添加10个成员。当前成员包含属性：年龄性别。

- METHOD: POST
- PATH: /v3/aiint/members
- Content-Type: application/json
- 请求示例：

  ```
  {
      "AppID": "test",
      "sn": "test-sn",
      "member_id": "ifly-001",
      "name": "小飞",
      "age_sex": "child",
      "desc": "可爱的小飞飞"
  }
  ```
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | member\_id | string | 成员标识，不超过32位，用户自行保证appid, sn下唯一；不传默认生成32位uuid（纯小写） | 否 | ifly-001 |
  | name | string | 成员名称，不超过16个字符，不支持特殊符号，同一个sn下面的name不能重复 | 是 | 小飞 |
  | age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |
  | desc | string | 描述，不超过32个字符，不支持特殊符号 | 否 | - |
- `返回值`示例:

  ```
  {
      "sid": "acm00680001@dx191bbe967b5c444992",
      "code": 0,
      "msg": "success",
      "data": null
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |

### 3.2. 成员查询

全量返回指定设备下面的成员信息

- METHOD: GET
- PATH: /v3/aiint/members?AppID={AppID}&sn={sn}
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备唯一标识,取值长度不超过32位 | 是 | test-sn |
- `返回值`示例:

  ```
  {
      "sid": "acm00680001@dx191bbe967b5c444992",
      "code": 0,
      "msg": "success",
      "data": [
          {
              "AppID": "test",
              "sn": "test-sn",
              "member_id": "ifly-001",
              "name": "小飞",
              "age_sex": "child",
              "desc": "可爱的小飞飞"
          }
      ]
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | []object | 返回数据 | 否 | - |
  | data[i].AppID | string | 应用id | 是 | 5c8b403a |
  | data[i].sn | string | 设备唯一编号 | 是 | - |
  | data[i].member\_id | string | 成员标识 | 是 | ifly-001 |
  | data[i].name | string | 成员名称 | 是 | - |
  | data[i].age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |

### 3.3. 成员编辑

更新指定成员信息

- METHOD: PUT
- PATH: /v3/aiint/members
- Content-Type: application/json
- 请求体示例：

  ```
  {
      "AppID": "test",
      "sn": "test-sn",
      "member_id": "ifly-001",
      "name": "小飞",
      "age_sex": "child",
      "desc": "可爱的小飞飞"
  }
  ```
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | member\_id | string | 成员标识，不超过32位，用户自行保证appid, sn下唯一；不传默认生成32位uuid（纯小写） | 否 | ifly-001 |
  | name | string | 成员名称，不超过16个字符，不支持特殊符号，同一个sn下面的name不能重复 | 是 | 小飞 |
  | age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |
  | desc | string | 描述，不超过32个字符，不支持特殊符号 | 否 | - |
- `返回值`示例:

  ```
  {
      "sid": "acm00680001@dx191bbe967b5c444992",
      "code": 0,
      "msg": "success",
      "data": null
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |

### 3.4. 成员删除

删除指定成员及其声纹数据

- METHOD: DELETE
- PATH: /v3/aiint/members
- Content-Type: application/json
- 请求体示例：

  ```
  {
      "AppID": "test",
      "sn": "test-sn",
      "member_id": "ifly-001"
  }
  ```
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | member\_id | string | 成员标识，不超过32位，用户自行保证appid, sn下唯一；不传默认生成32位uuid（纯小写） | 是 | ifly-001 |

- `返回值`示例:

  ```
  {
      "sid": "acm00680001@dx191bbe967b5c444992",
      "code": 0,
      "msg": "success",
      "data": null
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |

### 3.5. 声纹注册

第一次添加声纹时后台创建声纹库，没有传成员id时默认生成一个新的成员，根据声纹检测结果生成成员信息

- METHOD: POST
- PATH: /v3/aiint/vpr/features
- Content-Type: multipart/form-data
- HTTP 请求示例：

  ```
  POST /v3/aiint/vpr/features HTTP/1.1
  Host: 127.0.0.1:9996
  Content-Length: xxx
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="AppID"

  5c8b403a
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="sn"

  12334454543dfsdfsf
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="data"; filename="/D:/文件/TTS（语音合成）/2-正常音色文件-zzy.pcm"
  Content-Type: <Content-Type header here>

  (data)
  ------WebKitFormBoundary7MA4YWxkTrZu0gW--
  ```
- `表单参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | member\_id | string | 成员标识，不超过32位，用户自行保证appid, sn下唯一；不传默认生成32位uuid（纯小写） | 否 | ifly-001 |
  | data | file | 音频文件，只支持音频格式：pcm 16k 16bit 单通道，时常不少于1秒，不超过2分钟 | 是 | - |
  | feature\_info | string | 描述，不超过32个字符，不支持特殊符号 | 否 | 小飞飞近场 |

- `返回值`示例:

  ```
  {
      "sid": "acm00010034@dx191749d8e5d0001562",
      "code": 0,
      "msg": "success",
      "data": {
          "feature_id": "fsdfwee234324",
          "member_id": "4b37ccbb6679c34389176ed5bc920196",
          "age_sex": "child"
      }
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |
  | data.feature\_id | string | 声纹特征id | 是 | fsdfwee234324 |
  | data.member\_id | string | 成员id | 是 | 3 |
  | data.age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |

### 3.6. 声纹查询

查询指定sn下的成员声纹信息

- METHOD: GET
- PATH: /v3/aiint/vpr/features?AppID={AppID}&sn={sn}&member\_id={member\_id}
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备唯一标识,取值长度不超过32位 | 是 | test-sn |
  | member\_id | string | 成员id标识 | 否 | ifly-001 |

- `返回值`示例:

  ```
  {
      "sid": "acm00680001@dx191bbe967b5c444992",
      "code": 0,
      "msg": "success",
      "data": [
          {
              "AppID": "5c8b403a",
              "sn": "test-sn",
              "member_id": "ifly-001",
              "name": "小飞",
              "age_sex": "child",
              "desc": "可爱的小飞飞",
              "features": [
                  {
                      "feature_id": "w23ddfw3",
                      "merge_cnt": 1,
                      "feature_info": "近场"
                  },
                  {
                      "feature_id": "w23ddfw4",
                      "merge_cnt": 1,
                      "feature_info": "远场"
                  }
              ]
          }
      ]
  }
  ```
- `返回值参数字段`说明：

| 参数名 | 类型 | 说明 | 必需 | 示例 |
| --- | --- | --- | --- | --- |
| sid | string | 请求标识 | 是 | - |
| code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
| msg | string | 描述 | 是 | - |
| data | []object | 返回数据 | 否 | - |
| data[i].AppID | string | 应用id | 是 | 5c8b403a |
| data[i].sn | string | 设备唯一编号 | 是 | - |
| data[i].member\_id | string | 成员标识 | 是 | ifly-001 |
| data[i].name | string | 成员名称 | 是 | - |
| data[i].age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |
| data[i].desc | string | 描述，不超过32个字符，不支持特殊符号 | 否 | - |
| data[i].features | []object | 成员注册的声纹 | 否 | - |
| data[i].features[j].feature\_id | string | 声纹id | 是 | - |
| data[i].features[j].merge\_cnt | int | 声纹特征合并更新次数，初始值：1，调用更新声纹特征接口并且cover=false时加1 | 是 | - |
| data[i].features[j].feature\_info | string | 特征信息，不超过32个字符，不支持特殊符号 | 否 | - |

### 3.7. 声纹更新

更新指定id的声纹特征，可以选择直接覆盖或者与原有特征进行合并更新

- METHOD: PUT
- PATH: /v3/aiint/vpr/features
- Content-Type: multipart/form-data
- HTTP 请求示例：

  ```
  POST /v3/aiint/vpr/features HTTP/1.1
  Host: 127.0.0.1:9996
  Content-Length: xxx
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="AppID"

  5c8b403a
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="sn"

  12334454543dfsdfsf

  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="feature_id"

  njecjooy194
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="cover"

  false
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="data"; filename="/D:/文件/TTS（语音合成）/2-正常音色文件-zzy.pcm"
  Content-Type: <Content-Type header here>

  (data)
  ------WebKitFormBoundary7MA4YWxkTrZu0gW--
  ```
- `表单参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | feature\_id | string | 特征id，注册接口返回 | 是 | fsdfwee234324 |
  | cover | string | 是否覆盖原有特征：true 覆盖、false 与原有特征进行合并更新；默认：true | 否 | true |
  | data | file | 音频文件，只支持音频格式：pcm 16k 16bit 单通道，时常不少于1秒，不超过2分钟 | 是 | - |
  | feature\_info | string | 描述，不超过32个字符，不支持特殊符号 | 否 | 小飞飞近场 |

- `返回值`示例:

  ```
  {
      "sid": "acm00010034@dx191749d8e5d0001562",
      "code": 0,
      "msg": "success",
      "data": {
          "feature_id": "fsdfwee234324",
          "merge_cnt": 2,
          "member_id": "fily-001",
          "age_sex": "child"
      }
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |
  | data.feature\_id | string | 声纹特征id | 是 | fsdfwee234324 |
  | data.merge\_cnt | int | 声纹特征合并更新次数，创建的新声纹为1，调用更新声纹特征接口并且cover=false时加1 | 是 | 2 |
  | data.member\_id | string | 成员id | 是 | 3 |
  | data.age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |

### 3.8. 声纹删除

指定声纹id进行删除

- METHOD: DELETE
- PATH: /v3/aiint/vpr/features
- Content-Type: application/json
- 请求体示例：

  ```
  {
      "AppID": "5c8b403a",
      "sn": "test-sn",
      "feature_id": "fsdfwee234324"
  }
  ```
- `请求参数`说明

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | AppID | string | 应用id | 是 | 5c8b403a |
  | sn | string | 设备(用户)唯一标识，长度不超过32位。对应急速交互API接口中的sn参数 | 是 | - |
  | feature\_id | string | 声纹特征id | 是 | fsdfwee234324 |

- `返回值`示例:

  ```
  {
      "sid": "acm00010034@dx191749d8e5d0001562",
      "code": 0,
      "msg": "success",
      "data": {
          "feature_id": "fsdfwee234324",
          "member_id": "4b37ccbb6679c34389176ed5bc920196",
          "age_sex": "child"
      }
  }
  ```
- `返回值参数字段`说明：

### 3.9. 声纹检索

检索出指定设备声纹库中与当前上传的音频匹配的声纹信息，用于效果验证

- METHOD: POST
- PATH: /v3/aiint/vpr/searchFea
- Content-Type: multipart/form-data
- HTTP 请求示例：

  ```
  POST /v3/aiint/vpr/features HTTP/1.1
  Host: 127.0.0.1:9996
  Content-Length: xxx
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="AppID"

  5c8b403a
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="sn"

  12334454543dfsdfsf
  ------WebKitFormBoundary7MA4YWxkTrZu0gW
  Content-Disposition: form-data; name="data"; filename="/D:/文件/TTS（语音合成）/2-正常音色文件-zzy.pcm"
  Content-Type: <Content-Type header here>

  (data)
  ------WebKitFormBoundary7MA4YWxkTrZu0gW--
  ```

- `返回值`示例:

  ```
  {
      "sid": "acr005c0001@dx19a4333de9f0001992",
      "code": 0,
      "msg": "success",
      "data": [
          {
              "member": {
                  "AppID": "test",
                  "sn": "test-sn",
                  "member_id": "ifly-001",
                  "name": "小飞",
                  "age_sex": "child",
                  "desc": "可爱的小飞飞",
              },
              "feature_id": "fhptu9n1kl4",
              "score": 1
              "age": "youth",
              "gender": "male",
          }
      ]
  }
  ```
- `返回值参数字段`说明：

  | 参数名 | 类型 | 说明 | 必需 | 示例 |
  | --- | --- | --- | --- | --- |
  | sid | string | 请求标识 | 是 | - |
  | code | int | 状态码，0 成功，非0表示请求处理失败 | 是 | 0 |
  | msg | string | 描述 | 是 | - |
  | data | object | 返回数据 | 否 | - |
  | data[i].member | object | 匹配到的成员 | 是 | - |
  | data[i].member.AppID | string | 应用id | 是 | 5c8b403a |
  | data[i].member.sn | string | 设备唯一编号 | 是 | - |
  | data[i].member.member\_id | string | 成员标识 | 是 | ifly-001 |
  | data[i].member.name | string | 成员名称 | 是 | - |
  | data[i].member.age\_sex | string | 性别年龄：child 儿童、male 青年男、female 青年女、oldmale 老年男、oldfemale 老年女 | 否 | child |
  | data[i].member.desc | string | 描述，不超过32个字符，不支持特殊符号 | 否 | - |
  | data[i].feature\_id | string | 声纹特征id | 是 | fhptu9n1kl4 |
  | data[i].score | float | 相似度得分 0~1，精确到小 数点后两位 | 是 | 0.6 |
  | data[i].age | string | 年龄（仅参考）：child 儿童、youth 年轻人、old 老年人、unknown (出错 时返回) | 是 | youth |
  | data[i].gender | string | 性别（仅参考）：male 成年男、female 成年女、child儿童、unknown (出错 时返回) | 是 | male |

## 链路使用

### 功能开启

在AIUI极速交互类应用中，需要识别结果中包含声纹识别结果，除了先注册声纹外，还需要选择最新的 大模型识别引擎，并在AIUI应用下开启声纹能力。如下图：

温馨提示

AIUI语义模型配置下的个性化设置项，同声纹注册能力一样需要授权，通过授权后应用才会展示

![](/media/202601/2026-01-05_154626_5217740.8901393786789986.png)
![](/media/202601/2026-01-05_144040_4363450.5354565358372473.png)

### 结果解析

集成[AIUI极速交互协议API](/api-dev/ultra-chain/interact-api) 进行音频对话请求，参数配置（AppID、sn）与声纹注册信息一致后，在识别结束帧结果中，解析 extra 字段取值。相关示例结果如下：

- 匹配到声纹结果

  ```
  {
    "payload": {
        "IAT（语音识别）": {
            "compress": "raw",
            "format": "plain",
            "text": "{\"extra\":{\"feature_id\":\"99ijf7om8zs\",\"score\":0.51},\"text\":{\"sn\":1,\"ls\":true,\"bg\":0,\"ed\":0,\"rg\":null,\"VAD（端点检测）\":null,\"voice\":null,\"pgs\":\"\",\"rst\":\"\",\"sign\":\"\",\"ws\":[{\"bg\":0,\"cw\":[{\"sc\":0,\"w\":\"今天是什么日子\",\"ph\":\"\",\"ng\":\"\",\"wb\":0,\"wc\":0,\"we\":0,\"wp\":\"\"}]}]}}",
            "encoding": "utf8",
            "seq": 1,
            "status": 2
        }
    },
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "audio-1",
        "sid": "xgo000d9722@dx19b8cd02fb70001822",
        "status": 1
    }
  }
  ```
- 未匹配到声纹结果

  ```
  {
    "payload": {
        "IAT（语音识别）": {
            "compress": "raw",
            "format": "plain",
            "text": "{\"extra\":{},\"text\":{\"sn\":1,\"ls\":true,\"bg\":0,\"ed\":0,\"rg\":null,\"VAD（端点检测）\":null,\"voice\":null,\"pgs\":\"\",\"rst\":\"\",\"sign\":\"\",\"ws\":[{\"bg\":0,\"cw\":[{\"sc\":0,\"w\":\"今天星期几\",\"ph\":\"\",\"ng\":\"\",\"wb\":0,\"wc\":0,\"we\":0,\"wp\":\"\"}]}]}}",
            "encoding": "utf8",
            "seq": 1,
            "status": 2
        }
    },
    "header": {
        "code": 0,
        "message": "success",
        "stmid": "audio-1",
        "sid": "xgo000e72f9@dx19b8ce808060001822",
        "status": 1
    }
  }
  ```
