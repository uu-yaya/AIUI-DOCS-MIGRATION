import { defineConfig } from 'vitepress'
import sidebar from './sidebar.js'

export default defineConfig({
  title: 'AIUI 开发文档',
  description: '科大讯飞 AIUI 平台开发文档',
  lang: 'zh-CN',

  // docs/ 作为根目录，不需要额外 srcDir
  srcDir: '.',
  outDir: '../dist',

  themeConfig: {
    logo: '/images/placeholder.svg',
    siteTitle: 'AIUI 开发文档',

    nav: [
      { text: '快速开始', link: '/getting-started/introduction' },
      { text: '开发教程', link: '/tutorials/create-app' },
      {
        text: '参考',
        items: [
          { text: 'API 参考', link: '/reference/api/rapid/auth' },
          { text: '应用配置参考', link: '/reference/app-config/basic' },
          { text: 'SDK 参考', link: '/reference/sdk/' },
          { text: '技能协议', link: '/reference/protocols/' },
          { text: '错误码', link: '/reference/error-codes' },
          { text: '发音人列表', link: '/reference/tts-voices' },
          { text: '术语表', link: '/glossary' },
        ],
      },
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
      { text: '故障排查', link: '/troubleshooting/' },
      { text: '法律条款', link: '/legal/' },
      { text: '联系方式', link: '/faq/contact' },
    ],

    sidebar,

    socialLinks: [
      { icon: 'github', link: 'https://github.com' },
    ],

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
