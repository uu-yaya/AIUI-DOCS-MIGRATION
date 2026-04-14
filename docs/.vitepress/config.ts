import { defineConfig } from 'vitepress'
import sidebar from './sidebar.js'

export default defineConfig({
  title: 'AIUI 开发文档',
  description: '科大讯飞 AIUI 平台开发文档',
  lang: 'zh-CN',
  base: '/AIUI-DOCS-MIGRATION/',

  srcDir: '.',
  outDir: '../dist',

  themeConfig: {
    logo: false,
    siteTitle: 'AIUI 开发文档',

    nav: [
      { text: '快速开始', link: '/getting-started/' },
      { text: '开发教程', link: '/tutorials/' },
      {
        text: '开发接入',
        items: [
          { text: 'SDK 开发', link: '/sdk-dev/' },
          { text: 'API 开发', link: '/api-dev/' },
          { text: '参考文档', link: '/reference/' },
        ],
      },
      {
        text: '平台配置',
        items: [
          { text: '平台服务', link: '/platform-service/' },
          { text: '应用配置', link: '/app-config/' },
          { text: '自定义业务', link: '/custom-biz/' },
        ],
      },
      { text: '硬件模组', link: '/hardware/' },
      {
        text: '帮助',
        items: [
          { text: '常见问题', link: '/faq/' },
          { text: '故障排查', link: '/troubleshooting/' },
          { text: '联系方式', link: '/faq/contact' },
        ],
      },
      { text: '法律条款', link: '/legal/' },
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
