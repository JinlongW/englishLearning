import apiClient from './request'
import type { ApiResponse, LoginResponse, UserInfo } from '@/types/api'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  studentName: string
  gradeLevel: number
  phone?: string
}

/**
 * 用户登录
 * @param data 登录参数
 * @returns 登录响应，包含 token 和用户信息
 */
export const login = (data: LoginParams): Promise<ApiResponse<LoginResponse>> => {
  return apiClient.post<LoginParams, ApiResponse<LoginResponse>>('/auth/login', data)
}

/**
 * 用户注册
 * @param data 注册参数
 * @returns 注册响应
 */
export const register = (data: RegisterParams): Promise<ApiResponse<LoginResponse>> => {
  return apiClient.post<RegisterParams, ApiResponse<LoginResponse>>('/auth/register', data)
}

/**
 * 获取当前登录用户信息
 * @returns 用户信息
 */
export const getCurrentUser = (): Promise<ApiResponse<UserInfo>> => {
  return apiClient.get<never, ApiResponse<UserInfo>>('/auth/me')
}
