import apiClient from './request'
import type { ApiResponse, GrammarDto, GrammarDetailDto, GrammarQuizResult, GrammarTreeNode } from '@/types/api'

/**
 * 获取语法课程列表
 * @param gradeUnitId 年级单元 ID
 * @returns 语法列表响应
 */
export const getGrammars = (
  gradeUnitId: string
): Promise<ApiResponse<GrammarDto[]>> => {
  return apiClient.get<never, ApiResponse<GrammarDto[]>>('/grammar', {
    params: { gradeUnitId }
  })
}

/**
 * 获取语法详情
 * @param id 语法 ID
 * @returns 语法详情响应
 */
export const getGrammarById = (id: string): Promise<ApiResponse<GrammarDetailDto>> => {
  return apiClient.get<never, ApiResponse<GrammarDetailDto>>(`/grammar/${id}`)
}

/**
 * 提交语法测验
 * @param id 语法 ID
 * @param answers 答案列表
 * @returns 测验结果
 */
export const submitGrammarQuiz = (
  id: string,
  answers: { questionId: string; userAnswer: string }[]
): Promise<ApiResponse<GrammarQuizResult>> => {
  return apiClient.post<{ answers: typeof answers }, ApiResponse<GrammarQuizResult>>(
    `/grammar/${id}/quiz`,
    { answers }
  )
}

/**
 * 获取语法知识树
 * @param grade 年级
 * @returns 语法树响应
 */
export const getGrammarTree = (
  grade: number
): Promise<ApiResponse<GrammarTreeNode[]>> => {
  return apiClient.get<never, ApiResponse<GrammarTreeNode[]>>('/grammar/tree', {
    params: { grade }
  })
}
