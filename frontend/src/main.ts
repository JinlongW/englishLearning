import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 添加 uni-app polyfill (用于浏览器环境)
if (typeof window !== 'undefined' && !(window as any).uni) {
  (window as any).uni = {
    showLoading: (options: { title?: string; mask?: boolean }) => {
      console.log('[uni.showLoading]', options.title)
      // 可以在这里添加自定义 loading 逻辑
    },
    hideLoading: () => {
      console.log('[uni.hideLoading]')
    },
    showToast: (options: { title?: string; icon?: string; duration?: number }) => {
      console.log('[uni.showToast]', options.title)
      alert(options.title)
    },
    showSuccess: (title: string) => {
      alert(title)
    },
    navigateBack: () => {
      window.history.back()
    },
    navigateTo: (options: { url: string }) => {
      window.location.href = options.url
    },
    redirectTo: (options: { url: string }) => {
      window.location.replace(options.url)
    },
    reLaunch: (options: { url: string }) => {
      window.location.href = options.url
    },
    switchTab: (options: { url: string }) => {
      window.location.href = options.url
    }
  }
}

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
