import apiClient from './request'
import type { ApiResponse, PageResponse, Word } from '@/types/api'

/**
 * 获取单词列表
 * @param gradeUnitId 年级单元 ID
 * @param page 页码
 * @param pageSize 每页数量（默认 100，确保加载整个单元的所有单词）
 * @returns 单词列表响应
 */
export const getWords = (
  gradeUnitId: string,
  page = 1,
  pageSize = 100
): Promise<ApiResponse<PageResponse<Word>>> => {
  return apiClient.get<never, ApiResponse<PageResponse<Word>>>('/word', {
    params: { gradeUnitId, page, pageSize }
  })
}

/**
 * 获取单词详情
 * @param id 单词 ID
 * @returns 单词详情响应
 */
export const getWord = (id: string): Promise<ApiResponse<Word>> => {
  return apiClient.get<never, ApiResponse<Word>>(`/word/${id}`)
}

/**
 * 获取单词详情（别名）
 * @param id 单词 ID
 * @returns 单词详情响应
 */
export const getWordById = (id: string): Promise<ApiResponse<Word>> => {
  return apiClient.get<never, ApiResponse<Word>>(`/word/${id}`)
}

/**
 * 更新单词学习进度
 * @param id 单词 ID
 * @param score 分数
 * @param status 状态
 * @returns 更新响应
 */
export const updateWordProgress = (
  id: string,
  score: number,
  status: string
): Promise<ApiResponse<Word>> => {
  return apiClient.post<{ score: number; status: string }, ApiResponse<Word>>(
    `/word/${id}/progress`,
    { score, status }
  )
}

/**
 * 获取需要复习的单词列表（艾宾浩斯智能复习）
 * @param limit 数量限制
 * @returns 复习单词列表
 */
export const getWordsDueForReview = (limit = 20): Promise<ApiResponse<{ id: string; wordText: string; meaningCn: string; reviewCount: number; nextReviewAt: string; isUrgent: boolean }[]>> => {
  return apiClient.get<never, ApiResponse<{ id: string; wordText: string; meaningCn: string; reviewCount: number; nextReviewAt: string; isUrgent: boolean }[]>>('/word/review/due', {
    params: { limit }
  })
}

/**
 * 获取一周复习计划
 * @returns 复习计划列表
 */
export const getReviewSchedule = (): Promise<ApiResponse<{ date: string; wordCount: number; previewWords: string[] }[]>> => {
  return apiClient.get<never, ApiResponse<{ date: string; wordCount: number; previewWords: string[] }[]>>('/word/review/schedule')
}
