import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analysis from '../views/Analysis.vue'
import Trading from '../views/Trading.vue'
import History from '../views/History.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: '实时仪表板',
      icon: 'speedometer2'
    }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis,
    meta: {
      title: '深度分析',
      icon: 'graph-up'
    }
  },
  {
    path: '/trading',
    name: 'Trading',
    component: Trading,
    meta: {
      title: '交易策略',
      icon: 'currency-exchange'
    }
  },
  {
    path: '/history',
    name: 'History',
    component: History,
    meta: {
      title: '历史数据',
      icon: 'clock-history'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      title: '系统设置',
      icon: 'gear'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫 - 更新页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '比特币分析'} - BTC Analysis Platform`
  next()
})

export default router