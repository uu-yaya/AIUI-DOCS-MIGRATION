import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Breadcrumb from './components/Breadcrumb.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-before': () => h(Breadcrumb),
    })
  },
}
