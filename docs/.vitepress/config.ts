import { defineConfig } from 'vitepress'
import sidebar from './sidebar.js'

export default defineConfig({
  title: 'AIUI 文档',
  description: '科大讯飞 AIUI 全链路人机交互平台开发文档',
  lang: 'zh-CN',
  appearance: true,

  srcDir: '.',
  outDir: '../dist',

  head: [
    ['link', { rel: 'icon', href: '/logo.svg', type: 'image/svg+xml' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '文档中心',

    nav: [
      { text: '平台服务', link: '/platform-service/' },
      { text: '应用配置', link: '/app-config/' },
      {
        text: '开发接入',
        items: [
          { text: 'SDK 开发', link: '/sdk-dev/' },
          { text: 'API 开发', link: '/api-dev/' },
        ],
      },
      { text: '自定义业务', link: '/custom-biz/' },
      { text: '硬件模组', link: '/hardware/' },
      { text: '常见问题', link: '/faq/' },
      { text: '法律条款', link: '/legal/' },
      { text: '联系方式', link: '/faq/contact' },
    ],

    sidebar,

    search: {
      provider: 'local',
    },

    footer: {
      message: '科大讯飞 AIUI 开放平台',
      copyright: 'Copyright © 2024 科大讯飞股份有限公司',
    },

    outline: {
      label: '本页目录',
      level: [2, 3],
    },

    docFooter: {
      prev: '上一页',
      next: '下一页',
    },

    lastUpdated: {
      text: '最后更新',
    },
  },

  markdown: {
    lineNumbers: true,
  },
})
