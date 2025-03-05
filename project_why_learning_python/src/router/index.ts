// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // 首頁路由
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      // About 頁面，透過程式碼分割懶加載
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      // 新增的 Why Learning Python 頁面路由
      path: '/why-learning-python',
      name: 'why-learning-python',
      component: () => import('../views/WhyLearningPython.vue'),
    },
  ],
})

export default router
