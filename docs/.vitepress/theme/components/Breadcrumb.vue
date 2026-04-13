<script setup>
import { useData, useRoute } from 'vitepress'
import { computed } from 'vue'

const { page, site } = useData()
const route = useRoute()

const crumbs = computed(() => {
  const path = route.path
  const parts = path.replace(/\.html$/, '').split('/').filter(Boolean)
  if (parts.length <= 1) return []

  const labels = {
    'platform-service': '平台服务',
    'app-config': '应用配置',
    'sdk-dev': 'SDK 开发',
    'api-dev': 'API 开发',
    'custom-biz': '自定义业务',
    'hardware': '硬件模组',
    'faq': '常见问题',
    'legal': '法律条款',
    'basics': '基础信息',
    'features': '功能特性',
    'classic-chain': '传统语义链路',
    'llm-chain': '通用大模型链路',
    'ultra-chain': '极速超拟人链路',
    'skill-studio': '技能工作室',
    'qa-library': '问答库',
    'protocols': '协议规范',
    'development': '技能开发',
    'rk3328-evb': 'RK3328 评估板',
    'rk3328-nr': 'RK3328 降噪板',
    'rk3588-mm': 'RK3588 多模态',
    'rk3588s-mm': 'RK3588S 多模态',
    'usb-audio': 'USB 声卡',
    'ac7911b': 'AC7911B',
    'zg803': 'ZG803',
    'legacy-evb': '旧评估板',
  }

  const items = []
  let href = '/'
  for (let i = 0; i < parts.length - 1; i++) {
    href += parts[i] + '/'
    items.push({
      text: labels[parts[i]] || parts[i],
      link: href,
    })
  }
  return items
})

const currentTitle = computed(() => page.value.title || '')
</script>

<template>
  <nav v-if="crumbs.length" class="breadcrumb">
    <span v-for="(crumb, i) in crumbs" :key="i">
      <a :href="crumb.link">{{ crumb.text }}</a>
      <span class="sep">&gt;</span>
    </span>
    <span class="current">{{ currentTitle }}</span>
  </nav>
</template>

<style scoped>
.breadcrumb {
  font-size: 13px;
  color: #9ca3af;
  margin-bottom: 8px;
  line-height: 1.4;
}
.breadcrumb a {
  color: #9ca3af;
  text-decoration: none;
}
.breadcrumb a:hover {
  color: #0050D8;
}
.sep {
  margin: 0 6px;
  color: #d1d5db;
}
.current {
  color: #6b7280;
}
.dark .breadcrumb { color: #6b7280; }
.dark .breadcrumb a { color: #6b7280; }
.dark .breadcrumb a:hover { color: #4D94FF; }
.dark .sep { color: #4b5563; }
.dark .current { color: #9ca3af; }
</style>
