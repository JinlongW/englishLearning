import apiClient from './request'
import type { ApiResponse, GradeTreeNode } from '@/types/api'

/**
 * 获取年级单元树
 * @returns 年级单元树响应
 */
export const getGradeUnitTree = (): Promise<ApiResponse<GradeTreeNode[]>> => {
  return apiClient.get<never, ApiResponse<GradeTreeNode[]>>('/gradeunit/tree')
}
