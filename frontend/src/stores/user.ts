import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, getCurrentUser } from '@/api/auth'
import type { UserInfo } from '@/types/api'

/**
 * 检查 token 是否过期
 * @returns token 是否有效
 */
const checkTokenExpiration = (updateStore: () => void = () => {}): boolean => {
  const token = localStorage.getItem('token')
  const expiry = localStorage.getItem('token_expiry')

  if (!token) {
    return false
  }

  if (expiry && Date.now() > parseInt(expiry)) {
    // Token 已过期，同步清除 store 中的状态
    localStorage.removeItem('token')
    localStorage.removeItem('token_expiry')
    updateStore() // 同步更新 store
    return false
  }

  return true
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => {
    return !!token.value && checkTokenExpiration(() => {
      // Token 过期时同步更新 store
      token.value = ''
      userInfo.value = null
    })
  })
  const username = computed(() => userInfo.value?.username || '')
  const studentName = computed(() => userInfo.value?.studentName || '')
  const gradeLevel = computed(() => userInfo.value?.gradeLevel || 0)
  const avatarUrl = computed(() => userInfo.value?.avatarUrl)
  const currentLevel = computed(() => userInfo.value?.currentLevel || 1)
  const levelName = computed(() => userInfo.value?.levelName || '入门学徒')
  const currentExp = computed(() => userInfo.value?.currentExp || 0)
  const currentStreak = computed(() => userInfo.value?.currentStreak || 0)

  /**
   * 用户登录
   * @param username 用户名
   * @param password 密码
   * @returns 登录结果
   */
  const loginAction = async (username: string, password: string): Promise<void> => {
    const response = await login({ username, password })

    // 响应拦截器已经处理了 success 字段，这里直接获取数据
    // response 结构可能是 { token, user, expiresIn } 或 { data: { token, user, expiresIn } }
    const loginData = response.data || response

    if (loginData?.token) {
      token.value = loginData.token
      userInfo.value = loginData.user
      localStorage.setItem('token', loginData.token)

      // 存储 token 过期时间（默认 2 小时）
      const expiresIn = loginData.expiresIn || 7200
      localStorage.setItem('token_expiry', String(Date.now() + expiresIn * 1000))
    } else {
      throw new Error('登录响应格式错误')
    }
  }

  /**
   * 用户注册
   * @param data 注册参数
   * @returns 注册结果
   */
  const registerAction = async (data: {
    username: string
    password: string
    studentName: string
    gradeLevel: number
    phone?: string
  }): Promise<void> => {
    const response = await register(data)
    if (response.data) {
      token.value = response.data.token
      userInfo.value = response.data.user
      localStorage.setItem('token', token.value)
    }
  }

  /**
   * 获取用户信息
   */
  const fetchUserInfo = async (): Promise<void> => {
    if (!token.value || !checkTokenExpiration()) {
      return
    }

    try {
      const response = await getCurrentUser()
      if (response.data) {
        userInfo.value = response.data
      }
    } catch (error: unknown) {
      console.error('获取用户信息失败', error)
      logout()
    }
  }

  /**
   * 用户登出
   */
  const logout = (): void => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('token_expiry')
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    username,
    studentName,
    gradeLevel,
    avatarUrl,
    currentLevel,
    levelName,
    currentExp,
    currentStreak,
    loginAction,
    registerAction,
    fetchUserInfo,
    logout
  }
})
