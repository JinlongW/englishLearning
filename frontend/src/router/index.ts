import { createRouter, createWebHistory } from 'vue-router'
import 'vue-router'
import { isTokenValid, clearToken } from '@/utils/token'

// 扩展 Vue Router 类型定义
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    title?: string
  }
}

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false, title: '注册' }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true, title: '首页' }
  },
  {
    path: '/words',
    name: 'Words',
    component: () => import('@/views/Words.vue'),
    meta: { requiresAuth: true, title: '学单词' }
  },
  {
    path: '/word/:id',
    name: 'WordDetail',
    component: () => import('@/views/WordDetail.vue'),
    meta: { requiresAuth: true, title: '单词详情' }
  },
  {
    path: '/grammar/tree',
    name: 'GrammarTree',
    component: () => import('@/views/GrammarTree.vue'),
    meta: { requiresAuth: true, title: '语法知识图谱' }
  },
  {
    path: '/grammar',
    name: 'Grammar',
    component: () => import('@/views/Grammar.vue'),
    meta: { requiresAuth: true, title: '学语法' }
  },
  {
    path: '/grammar/:id',
    name: 'GrammarDetail',
    component: () => import('@/views/GrammarDetail.vue'),
    meta: { requiresAuth: true, title: '语法课程' }
  },
  {
    path: '/grammar/:id/quiz',
    name: 'GrammarQuiz',
    component: () => import('@/views/GrammarQuiz.vue'),
    meta: { requiresAuth: true, title: '语法测验' }
  },
  {
    path: '/grammar/story-learning',
    name: 'StoryLearning',
    component: () => import('@/views/StoryLearning.vue'),
    meta: { requiresAuth: true, title: '情景学习' }
  },
  {
    path: '/challenge',
    name: 'Challenge',
    component: () => import('@/views/Challenge.vue'),
    meta: { requiresAuth: true, title: '每日挑战' }
  },
  {
    path: '/challenge/answer',
    name: 'ChallengeAnswer',
    component: () => import('@/views/ChallengeAnswer.vue'),
    meta: { requiresAuth: true, title: '挑战答题' }
  },
  {
    path: '/wrong-questions',
    name: 'WrongQuestions',
    component: () => import('@/views/WrongQuestions.vue'),
    meta: { requiresAuth: true, title: '错题本' }
  },
  {
    path: '/wrong-questions/review',
    name: 'WrongQuestionReview',
    component: () => import('@/views/WrongQuestionReview.vue'),
    meta: { requiresAuth: true, title: '错题复习' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true, title: '我的' }
  },
  {
    path: '/smart-review',
    name: 'SmartReview',
    component: () => import('@/views/SmartReview.vue'),
    meta: { requiresAuth: true, title: '智能复习' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 英语学习工具`
  }

  const token = localStorage.getItem('token')
  const tokenExpiry = localStorage.getItem('token_expiry')

  // 检查 token 是否过期或无效
  if (!isTokenValid()) {
    if (token || tokenExpiry) {
      // 清除无效的 token
      clearToken()
    }
    if (to.meta.requiresAuth) {
      next('/login')
      return
    }
  }

  // 已登录用户访问登录/注册页时重定向到首页
  if (isTokenValid() && (to.path === '/login' || to.path === '/register')) {
    next('/')
    return
  }

  // 其他情况正常放行
  next()
})

export default router
