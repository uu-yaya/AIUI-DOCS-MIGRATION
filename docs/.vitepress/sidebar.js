// 自动生成，勿手动编辑（由 scripts/build.py 生成）
export default {
  "/getting-started/": [
    {
      text: "快速开始",
      items: [
        { text: "AIUI 平台介绍", link: "/getting-started/introduction" },
        { text: "选择接入路径", link: "/getting-started/choose-your-path" },
        { text: "极速超拟人体验", link: "/getting-started/hello-world-rapid" },
        { text: "大模型链路体验", link: "/getting-started/hello-world-llm" },
        { text: "传统语义链路体验", link: "/getting-started/hello-world-traditional" },
      ],
    },
  ],
  "/tutorials/": [
    {
      text: "开发教程",
      items: [
        { text: "创建你的第一个 AIUI 应用", link: "/tutorials/create-app" },
        { text: "Android SDK 集成教程", link: "/tutorials/sdk-android" },
        { text: "iOS SDK 集成教程", link: "/tutorials/sdk-ios" },
        { text: "Windows/Linux SDK 集成教程", link: "/tutorials/sdk-windows-linux" },
        { text: "WebSocket API 接入教程", link: "/tutorials/api-integration" },
        { text: "自定义技能开发", link: "/tutorials/custom-skill" },
        { text: "问答库开发", link: "/tutorials/qa-library" },
        { text: "技能后处理与 Webhook 开发", link: "/tutorials/webhook" },
        { text: "智能体开发教程", link: "/tutorials/agent-dev" },
        { text: "声音复刻教程", link: "/tutorials/voice-clone" },
        { text: "三方大模型配置教程", link: "/tutorials/third-party-llm" },
        { text: "极速超拟人新特性教程", link: "/tutorials/new-features" },
      ],
    },
  ],
  "/reference/": [
    {
      text: "API 参考 — 极速超拟人链路",
      collapsed: false,
      items: [
        { text: "服务鉴权", link: "/reference/api/rapid/auth" },
        { text: "交互 API", link: "/reference/api/rapid/interaction" },
        { text: "个性化 API", link: "/reference/api/rapid/personalization" },
        { text: "合成能力", link: "/reference/api/rapid/tts" },
        { text: "声音复刻 API", link: "/reference/api/rapid/voice-clone" },
        { text: "声纹管理 API", link: "/reference/api/rapid/voiceprint" },
      ],
    },
    {
      text: "API 参考 — 通用大模型链路",
      collapsed: false,
      items: [
        { text: "服务鉴权", link: "/reference/api/llm/auth" },
        { text: "交互 API", link: "/reference/api/llm/interaction" },
        { text: "个性化 API", link: "/reference/api/llm/personalization" },
        { text: "合成能力", link: "/reference/api/llm/tts" },
        { text: "声音复刻 API", link: "/reference/api/llm/voice-clone" },
      ],
    },
    {
      text: "API 参考 — 传统语义链路",
      collapsed: false,
      items: [
        { text: "服务鉴权", link: "/reference/api/traditional/auth" },
        { text: "交互 API", link: "/reference/api/traditional/interaction" },
        { text: "个性化 API", link: "/reference/api/traditional/personalization" },
        { text: "合成能力", link: "/reference/api/traditional/tts" },
      ],
    },
    {
      text: "应用配置参考",
      collapsed: false,
      items: [
        { text: "基础配置", link: "/reference/app-config/basic" },
        { text: "语义模型配置", link: "/reference/app-config/semantic-model" },
        { text: "回复角色配置", link: "/reference/app-config/reply-role" },
        { text: "语音识别配置", link: "/reference/app-config/speech-recognition" },
        { text: "语音合成配置", link: "/reference/app-config/tts" },
        { text: "星火大模型配置", link: "/reference/app-config/spark-llm" },
        { text: "三方大模型配置", link: "/reference/app-config/third-party-llm" },
        { text: "应用后处理配置", link: "/reference/app-config/post-processing" },
        { text: "全双工配置", link: "/reference/app-config/full-duplex" },
        { text: "表情标签配置", link: "/reference/app-config/emotion-tag" },
        { text: "长时记忆配置", link: "/reference/app-config/long-term-memory" },
        { text: "声纹识别配置", link: "/reference/app-config/voiceprint" },
      ],
    },
    {
      text: "SDK 参考",
      collapsed: false,
      items: [
        { text: "SDK 基础信息", link: "/reference/sdk/" },
        {
          text: "接口说明",
          collapsed: true,
          items: [
            { text: "概述", link: "/reference/sdk/interfaces/" },
            { text: "Android", link: "/reference/sdk/interfaces/android" },
            { text: "iOS", link: "/reference/sdk/interfaces/ios" },
            { text: "Windows / Linux", link: "/reference/sdk/interfaces/windows-linux" },
          ],
        },
        {
          text: "参数配置",
          collapsed: true,
          items: [
            { text: "概述", link: "/reference/sdk/params/" },
            { text: "Android", link: "/reference/sdk/params/android" },
            { text: "iOS / Windows / Linux", link: "/reference/sdk/params/ios-windows-linux" },
          ],
        },
        { text: "消息事件", link: "/reference/sdk/events" },
        { text: "SDK 状态", link: "/reference/sdk/states" },
        {
          text: "数据发送",
          collapsed: true,
          items: [
            { text: "概述", link: "/reference/sdk/data-sending/" },
            { text: "Android", link: "/reference/sdk/data-sending/android" },
            { text: "iOS / Windows / Linux", link: "/reference/sdk/data-sending/ios-windows-linux" },
          ],
        },
        {
          text: "回调解析",
          collapsed: true,
          items: [
            { text: "概述", link: "/reference/sdk/callbacks/" },
            { text: "Android", link: "/reference/sdk/callbacks/android" },
            { text: "iOS / Windows / Linux", link: "/reference/sdk/callbacks/ios-windows-linux" },
          ],
        },
        { text: "交互结果协议", link: "/reference/sdk/result-protocol" },
      ],
    },
    {
      text: "技能协议",
      collapsed: false,
      items: [
        { text: "技能协议概述", link: "/reference/protocols/" },
        { text: "语义协议", link: "/reference/protocols/semantic-protocol" },
        { text: "标准请求", link: "/reference/protocols/post-process-request" },
        { text: "请求校验", link: "/reference/protocols/post-process-verify" },
        { text: "Request v2.1", link: "/reference/protocols/post-process-request-v21" },
        { text: "Response v2.1", link: "/reference/protocols/post-process-response-v21" },
        { text: "资源限制", link: "/reference/protocols/resource-limits" },
      ],
    },
    {
      text: "其他参考",
      collapsed: false,
      items: [
        { text: "错误码列表", link: "/reference/error-codes" },
        { text: "发音人列表", link: "/reference/tts-voices" },
        { text: "术语表", link: "/glossary" },
      ],
    },
  ],
  "/troubleshooting/": [
    {
      text: "故障排查",
      items: [
        { text: "故障排查", link: "/troubleshooting/" },
      ],
    },
  ],
  "/platform-service/": [
    {
      text: "AIUI 平台服务",
      items: [
        { text: "概述", link: "/platform-service/" },
        { text: "平台介绍", link: "/platform-service/overview" },
        { text: "应用介绍", link: "/platform-service/app-intro" },
        { text: "服务链路介绍", link: "/platform-service/service-chain" },
        { text: "平台能力概述", link: "/platform-service/capabilities" },
        { text: "快速体验", link: "/platform-service/quickstart" },
      ],
    },
  ],
  "/app-config/": [
    {
      text: "AIUI 应用配置",
      items: [
        { text: "概述", link: "/app-config/" },
        { text: "应用发布", link: "/app-config/publish" },
        { text: "语义精简协议", link: "/app-config/semantic-lite-protocol" },
        { text: "基础配置", link: "/app-config/basic-config" },
        { text: "语义模型配置", link: "/app-config/semantic-model" },
        { text: "回复角色配置", link: "/app-config/reply-role" },
        { text: "语音识别配置", link: "/app-config/asr-config" },
        { text: "结构化语义配置", link: "/app-config/structured-semantic" },
        { text: "星火大模型配置", link: "/app-config/spark-llm" },
        { text: "语音合成配置", link: "/app-config/tts-config" },
        { text: "应用后处理配置", link: "/app-config/post-process" },
        { text: "三方大模型配置", link: "/app-config/third-party-llm" },
        { text: "全双工配置", link: "/app-config/full-duplex" },
        { text: "表情标签配置", link: "/app-config/emotion-tags" },
        { text: "长时记忆配置", link: "/app-config/long-memory" },
        { text: "声纹识别配置", link: "/app-config/voiceprint" },
      ],
    },
  ],
  "/sdk-dev/": [
    {
      text: "SDK 开发",
      collapsed: false,
      items: [
        { text: "概述", link: "/sdk-dev/" },
        { text: "接入流程", link: "/sdk-dev/quickstart" },
        { text: "错误码", link: "/sdk-dev/error-codes" },
        { text: "发音人列表", link: "/sdk-dev/voice-list" },
      ],
    },
    {
      text: "SDK 基础",
      collapsed: false,
      items: [
        { text: "基础信息", link: "/sdk-dev/basics/" },
        {
          text: "接口说明",
          collapsed: true,
          items: [
            { text: "概述", link: "/sdk-dev/basics/interfaces/" },
            { text: "Android", link: "/sdk-dev/basics/interfaces/android" },
            { text: "iOS", link: "/sdk-dev/basics/interfaces/ios" },
            { text: "Windows / Linux", link: "/sdk-dev/basics/interfaces/windows-linux" },
          ],
        },
        {
          text: "参数配置",
          collapsed: true,
          items: [
            { text: "概述", link: "/sdk-dev/basics/params/" },
            { text: "Android", link: "/sdk-dev/basics/params/android" },
            { text: "iOS / Windows / Linux", link: "/sdk-dev/basics/params/ios-windows-linux" },
          ],
        },
        { text: "消息事件", link: "/sdk-dev/basics/events" },
        { text: "SDK 状态", link: "/sdk-dev/basics/states" },
        {
          text: "数据发送",
          collapsed: true,
          items: [
            { text: "概述", link: "/sdk-dev/basics/data-sending/" },
            { text: "Android", link: "/sdk-dev/basics/data-sending/android" },
            { text: "iOS / Windows / Linux", link: "/sdk-dev/basics/data-sending/ios-windows-linux" },
          ],
        },
        {
          text: "回调解析",
          collapsed: true,
          items: [
            { text: "概述", link: "/sdk-dev/basics/callbacks/" },
            { text: "Android", link: "/sdk-dev/basics/callbacks/android" },
            { text: "iOS / Windows / Linux", link: "/sdk-dev/basics/callbacks/ios-windows-linux" },
          ],
        },
        { text: "交互结果协议", link: "/sdk-dev/basics/result-protocol" },
      ],
    },
    {
      text: "SDK 能力",
      collapsed: false,
      items: [
        { text: "基础能力", link: "/sdk-dev/features/" },
        { text: "流式识别", link: "/sdk-dev/features/streaming-asr" },
        { text: "离线识别", link: "/sdk-dev/features/offline-asr" },
        { text: "语音唤醒", link: "/sdk-dev/features/wakeword" },
        { text: "语音合成", link: "/sdk-dev/features/tts" },
        { text: "用户个性化", link: "/sdk-dev/features/personalization" },
        { text: "自定义参数", link: "/sdk-dev/features/custom-params" },
      ],
    },
    {
      text: "SDK 链路接入",
      collapsed: false,
      items: [
        { text: "传统语义链路", link: "/sdk-dev/classic-chain/" },
        { text: "链路配置", link: "/sdk-dev/classic-chain/config" },
        { text: "个性化数据", link: "/sdk-dev/classic-chain/personalization" },
        { text: "通用大模型链路", link: "/sdk-dev/llm-chain/" },
        { text: "链路配置", link: "/sdk-dev/llm-chain/config" },
        { text: "个性化数据", link: "/sdk-dev/llm-chain/personalization" },
        { text: "超拟人合成", link: "/sdk-dev/llm-chain/ultra-tts" },
        { text: "声音复刻", link: "/sdk-dev/llm-chain/voice-clone" },
        { text: "极速超拟人链路", link: "/sdk-dev/ultra-chain/" },
        { text: "链路配置", link: "/sdk-dev/ultra-chain/config" },
        { text: "个性化数据", link: "/sdk-dev/ultra-chain/personalization" },
        { text: "流式合成", link: "/sdk-dev/ultra-chain/streaming-tts" },
        { text: "声音复刻", link: "/sdk-dev/ultra-chain/voice-clone" },
        { text: "RTOS 接入", link: "/sdk-dev/ultra-chain/rtos" },
      ],
    },
  ],
  "/api-dev/": [
    {
      text: "AIUI API 开发",
      items: [
        { text: "概述", link: "/api-dev/" },
        { text: "传统语义链路", link: "/api-dev/classic-chain/" },
        { text: "交互 API", link: "/api-dev/classic-chain/interact-api" },
        { text: "个性化 API", link: "/api-dev/classic-chain/personalization-api" },
        { text: "合成能力", link: "/api-dev/classic-chain/tts-usage" },
        { text: "通用大模型链路", link: "/api-dev/llm-chain/" },
        { text: "服务鉴权", link: "/api-dev/llm-chain/auth" },
        { text: "交互 API", link: "/api-dev/llm-chain/interact-api" },
        { text: "个性化 API", link: "/api-dev/llm-chain/personalization-api" },
        { text: "声音复刻 API", link: "/api-dev/llm-chain/voice-clone-api" },
        { text: "合成能力", link: "/api-dev/llm-chain/tts-usage" },
        { text: "极速超拟人链路", link: "/api-dev/ultra-chain/" },
        { text: "服务鉴权", link: "/api-dev/ultra-chain/auth" },
        { text: "交互 API", link: "/api-dev/ultra-chain/interact-api" },
        { text: "个性化 API", link: "/api-dev/ultra-chain/personalization-api" },
        { text: "声音复刻 API", link: "/api-dev/ultra-chain/voice-clone-api" },
        { text: "合成能力", link: "/api-dev/ultra-chain/tts-usage" },
        { text: "声纹管理 API", link: "/api-dev/ultra-chain/voiceprint-api" },
      ],
    },
  ],
  "/custom-biz/": [
    {
      text: "自定义业务",
      collapsed: false,
      items: [
        { text: "概述", link: "/custom-biz/" },
      ],
    },
    {
      text: "设备人设开发",
      collapsed: false,
      items: [
        { text: "概述", link: "/custom-biz/device-persona/" },
        { text: "配置指南", link: "/custom-biz/device-persona/guide" },
      ],
    },
    {
      text: "技能工作室",
      collapsed: false,
      items: [
        { text: "技能工作室概述", link: "/custom-biz/skill-studio/overview" },
        { text: "名词解析", link: "/custom-biz/skill-studio/glossary" },
        { text: "技能", link: "/custom-biz/skill-studio/skills" },
        { text: "意图和语料", link: "/custom-biz/skill-studio/intents" },
        { text: "实体", link: "/custom-biz/skill-studio/entities" },
        { text: "动态实体", link: "/custom-biz/skill-studio/dynamic-entities" },
        { text: "模糊匹配", link: "/custom-biz/skill-studio/fuzzy-match" },
        { text: "填槽对话", link: "/custom-biz/skill-studio/slot-filling" },
        {
          text: "技能设计规范",
          collapsed: true,
          items: [
            { text: "概述", link: "/custom-biz/skill-studio/design-guide" },
            { text: "语音技能设计规范", link: "/custom-biz/skill-studio/voice-design-guide" },
            { text: "审核规范", link: "/custom-biz/skill-studio/review-guide" },
            { text: "图标规范", link: "/custom-biz/skill-studio/icon-guide" },
          ],
        },
      ],
    },
    {
      text: "技能开发",
      collapsed: false,
      items: [
        { text: "概述", link: "/custom-biz/skill-studio/development/" },
        { text: "创建技能", link: "/custom-biz/skill-studio/development/create" },
        { text: "意图配置", link: "/custom-biz/skill-studio/development/intent-config" },
        { text: "技能测试", link: "/custom-biz/skill-studio/development/testing" },
        { text: "技能发布", link: "/custom-biz/skill-studio/development/publish" },
        { text: "技能后处理", link: "/custom-biz/skill-studio/development/post-process" },
        { text: "导入导出", link: "/custom-biz/skill-studio/development/import-export" },
        { text: "云函数 API v2.1", link: "/custom-biz/skill-studio/cloud-function-api-v21" },
        { text: "云函数 API v2.0", link: "/custom-biz/skill-studio/cloud-function-api-v20" },
        { text: "智能体开发", link: "/custom-biz/skill-studio/agent-dev" },
        { text: "智能体对接", link: "/custom-biz/skill-studio/agent-integration" },
      ],
    },
    {
      text: "问答库",
      collapsed: false,
      items: [
        { text: "概述", link: "/custom-biz/qa-library/" },
        { text: "语句问答", link: "/custom-biz/qa-library/sentence-qa" },
        { text: "关键词问答", link: "/custom-biz/qa-library/keyword-qa" },
        { text: "文档问答", link: "/custom-biz/qa-library/document-qa" },
      ],
    },
    {
      text: "技能协议",
      collapsed: false,
      items: [
        { text: "技能协议", link: "/custom-biz/protocols/" },
        { text: "语义协议", link: "/custom-biz/protocols/semantic-protocol" },
        { text: "标准请求", link: "/custom-biz/protocols/post-process-request" },
        { text: "请求校验", link: "/custom-biz/protocols/post-process-verify" },
        { text: "Request v2.1", link: "/custom-biz/protocols/post-process-request-v21" },
        { text: "Response v2.1", link: "/custom-biz/protocols/post-process-response-v21" },
        { text: "资源限制", link: "/custom-biz/protocols/resource-limits" },
      ],
    },
  ],
  "/hardware/": [
    {
      text: "硬件模组",
      collapsed: false,
      items: [
        { text: "概述", link: "/hardware/" },
      ],
    },
    {
      text: "USB 声卡套件",
      collapsed: false,
      items: [
        { text: "USB 声卡套件", link: "/hardware/usb-audio/" },
        { text: "产品白皮书", link: "/hardware/usb-audio/whitepaper" },
        { text: "使用指南", link: "/hardware/usb-audio/guide" },
      ],
    },
    {
      text: "RK3328 降噪板",
      collapsed: false,
      items: [
        { text: "RK3328 降噪板", link: "/hardware/rk3328-nr/" },
        { text: "产品白皮书", link: "/hardware/rk3328-nr/whitepaper" },
        { text: "使用手册", link: "/hardware/rk3328-nr/manual" },
        { text: "规格书", link: "/hardware/rk3328-nr/specs" },
        { text: "协议手册", link: "/hardware/rk3328-nr/protocol" },
      ],
    },
    {
      text: "RK3328 评估板",
      collapsed: false,
      items: [
        { text: "RK3328 评估板", link: "/hardware/rk3328-evb/" },
        { text: "产品白皮书", link: "/hardware/rk3328-evb/whitepaper" },
        { text: "使用手册", link: "/hardware/rk3328-evb/manual" },
        { text: "规格书", link: "/hardware/rk3328-evb/specs" },
        { text: "开发手册", link: "/hardware/rk3328-evb/dev-guide" },
      ],
    },
    {
      text: "RK3588S 多模态",
      collapsed: false,
      items: [
        { text: "RK3588S 多模态套件", link: "/hardware/rk3588s-mm/" },
        { text: "产品白皮书", link: "/hardware/rk3588s-mm/whitepaper" },
        { text: "使用手册", link: "/hardware/rk3588s-mm/manual" },
        { text: "规格书", link: "/hardware/rk3588s-mm/specs" },
      ],
    },
    {
      text: "RK3588 多模态",
      collapsed: false,
      items: [
        { text: "RK3588 多模态套件", link: "/hardware/rk3588-mm/" },
        { text: "产品规格书", link: "/hardware/rk3588-mm/specs" },
        { text: "使用手册", link: "/hardware/rk3588-mm/manual" },
        { text: "视频传输协议", link: "/hardware/rk3588-mm/video-protocol" },
        { text: "语义传输协议", link: "/hardware/rk3588-mm/semantic-protocol" },
        { text: "音频传输协议", link: "/hardware/rk3588-mm/audio-protocol" },
        { text: "消息事件", link: "/hardware/rk3588-mm/message-events" },
      ],
    },
    {
      text: "AC7911B",
      collapsed: false,
      items: [
        { text: "AC7911B 套件", link: "/hardware/ac7911b/" },
        { text: "产品白皮书", link: "/hardware/ac7911b/whitepaper" },
        { text: "快速体验", link: "/hardware/ac7911b/quickstart" },
      ],
    },
    {
      text: "ZG803",
      collapsed: false,
      items: [
        { text: "ZG803 套件", link: "/hardware/zg803/" },
        { text: "产品白皮书", link: "/hardware/zg803/whitepaper" },
      ],
    },
    {
      text: "旧版评估板",
      collapsed: false,
      items: [
        { text: "旧版评估板", link: "/hardware/legacy-evb/" },
        { text: "集成方式", link: "/hardware/legacy-evb/integration" },
        { text: "软件包说明", link: "/hardware/legacy-evb/packages" },
        { text: "AIUIServiceKit", link: "/hardware/legacy-evb/aiui-service-kit" },
        { text: "串口 SDK", link: "/hardware/legacy-evb/serial-sdk" },
        { text: "参数配置", link: "/hardware/legacy-evb/config" },
        { text: "调试升级", link: "/hardware/legacy-evb/debug-upgrade" },
      ],
    },
  ],
  "/faq/": [
    {
      text: "常见问题",
      items: [
        { text: "常见问题", link: "/faq/" },
        { text: "AIUI 常见问题", link: "/faq/aiui-faq" },
        { text: "评估板常见问题", link: "/faq/evb-faq" },
        { text: "动态实体常见问题", link: "/faq/dynamic-entity-faq" },
        { text: "联系方式", link: "/faq/contact" },
      ],
    },
  ],
  "/legal/": [
    {
      text: "服务条款",
      collapsed: false,
      items: [
        { text: "概述", link: "/legal/" },
      ],
    },
    {
      text: "平台协议",
      collapsed: false,
      items: [
        { text: "平台服务协议", link: "/legal/aiui-platform-tos" },
        { text: "平台隐私政策", link: "/legal/aiui-platform-privacy" },
      ],
    },
    {
      text: "小飞在家",
      collapsed: false,
      items: [
        { text: "小飞用户协议", link: "/legal/xiaofei-tos" },
        { text: "小飞隐私政策", link: "/legal/xiaofei-privacy" },
        { text: "开源许可", link: "/legal/xiaofei-oss-license" },
      ],
    },
    {
      text: "讯飞账号",
      collapsed: false,
      items: [
        { text: "账号隐私政策", link: "/legal/xfyun-account-privacy" },
        { text: "账号用户协议", link: "/legal/xfyun-account-tos" },
      ],
    },
    {
      text: "带屏音箱",
      collapsed: false,
      items: [
        { text: "音箱用户协议", link: "/legal/xfyun-speaker-tos" },
        { text: "音箱隐私政策", link: "/legal/xfyun-speaker-privacy" },
      ],
    },
    {
      text: "SDK 协议",
      collapsed: false,
      items: [
        { text: "SDK 隐私政策", link: "/legal/aiui-sdk-privacy" },
        { text: "SDK 合规说明", link: "/legal/aiui-sdk-compliance" },
      ],
    },
  ],
}
