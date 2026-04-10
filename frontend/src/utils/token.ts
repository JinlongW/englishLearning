/**
 * Token 管理工具
 */

const TOKEN_KEY = 'token'
const TOKEN_EXPIRY_KEY = 'token_expiry'

/**
 * 保存 token 和过期时间
 */
export const setToken = (token: string, expiresInMs: number): void => {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(TOKEN_EXPIRY_KEY, (Date.now() + expiresInMs).toString())
}

/**
 * 获取 token
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * 检查 token 是否有效
 */
export const isTokenValid = (): boolean => {
  const token = getToken()
  const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY)

  if (!token || !expiry) return false

  const expiryTime = parseInt(expiry, 10)
  if (Number.isNaN(expiryTime)) return false

  return Date.now() < expiryTime
}

/**
 * 清除 token
 */
export const clearToken = (): void => {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(TOKEN_EXPIRY_KEY)
}

/**
 * 获取过期时间（毫秒）
 */
export const getTokenExpiry = (): number | null => {
  const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY)
  if (!expiry) return null
  return parseInt(expiry, 10)
}
