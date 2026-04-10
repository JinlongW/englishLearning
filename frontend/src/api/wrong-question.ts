import apiClient from './request'
import type { ApiResponse, PageResponse, WrongQuestionDetailResponse } from '@/types/api'

/**
 * 获取错题列表
 * @param page 页码
 * @param pageSize 每页数量
 * @param status 状态筛选 (null = 全部)
 * @returns 错题分页列表
 */
export const getWrongQuestions = (
  page = 1,
  pageSize = 20,
  status?: string | null
): Promise<ApiResponse<PageResponse<WrongQuestionDetailResponse>>> => {
  return apiClient.get<never, ApiResponse<PageResponse<WrongQuestionDetailResponse>>>('/wrong-question', {
    params: { page, pageSize, status }
  })
}

/**
 * 获取待复习题目
 * @param limit 数量限制
 * @returns 复习题目列表
 */
export const getReviewQuestions = (limit = 10): Promise<ApiResponse<any[]>> => {
  return apiClient.get<never, ApiResponse<any[]>>('/wrong-question/review', {
    params: { limit }
  })
}

/**
 * 复习错题
 * @param wrongQuestionId 错题 ID
 * @param userAnswer 用户答案
 * @returns 复习结果
 */
export const reviewWrongQuestion = (
  wrongQuestionId: string,
  userAnswer: string
): Promise<ApiResponse<{ reviewCount: number; nextReviewAt: string | null; reviewStatus: string; isMastered: boolean }>> => {
  return apiClient.post<{ userAnswer: string }, ApiResponse<any>>(
    `/wrong-question/${wrongQuestionId}/review`,
    { userAnswer }
  )
}

/**
 * 标记为已掌握
 * @param wrongQuestionId 错题 ID
 * @returns 操作结果
 */
export const markWrongQuestionAsMastered = (
  wrongQuestionId: string
): Promise<ApiResponse<void>> => {
  return apiClient.post<never, ApiResponse<void>>(
    `/wrong-question/${wrongQuestionId}/master`
  )
}

/**
 * 提交复习答案
 * @param id 错题 ID
 * @param userAnswer 用户答案
 * @param isCorrect 是否正确
 * @returns 复习结果
 */
export const submitReview = (
  id: string,
  userAnswer: string,
  isCorrect: boolean
): Promise<ApiResponse<any>> => {
  return apiClient.post(`/wrong-question/${id}/review`, { userAnswer, isCorrect })
}
