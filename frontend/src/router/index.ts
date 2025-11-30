import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AppLayout from '../layouts/AppLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'
import { useAuth } from '../composables/useAuth'
import { config } from '../config'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'login',
        component: () => import('../views/LoginView.vue'),
      },
    ],
  },
  {
    path: '/login-callback',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'login-callback',
        component: () => import('../views/LoginCallbackView.vue'),
      },
    ],
  },
  {
    path: '/app',
    component: AppLayout,
    meta: { requiresAuth: false },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
      },
      {
        path: 'items',
        name: 'items',
        component: () => import('../views/ItemsListView.vue'),
      },
      {
        path: 'burn-config',
        name: 'burn-config',
        component: () => import('../views/BurnConfigurationView.vue'),
      },
      {
        path: 'burn-results',
        name: 'burn-results',
        component: () => import('../views/BurnResultsView.vue'),
      },
    ],
  },
  {
    path: '/components',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'components',
        component: () => import('../views/ComponentsShowcaseView.vue'),
      },
    ],
  },
  {
    path: '/charts',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'charts',
        component: () => import('../views/ChartsShowcaseView.vue'),
      },
    ],
  },
  {
    path: '/',
    name: 'landing',
    component: () => import('../views/LandingView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const { isAuthenticated } = useAuth()

  if (requiresAuth && !isAuthenticated.value) {
    if (config.cognitoLoginUrl) {
      window.location.href = config.cognitoLoginUrl
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
