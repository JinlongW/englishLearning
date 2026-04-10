import apiClient from './request'
import type { ApiResponse, QuestionDetailResponse } from '@/types/api'

/**
 * 获取挑战题目列表
 * @param challengeId 挑战 ID
 * @returns 题目列表
 */
export const getChallengeQuestions = (challengeId: string): Promise<QuestionDetailResponse[]> => {
  return apiClient.get<never, QuestionDetailResponse[]>(`/challenge/${challengeId}/questions`)
}

/**
 * 提交挑战答案
 * @param challengeId 挑战 ID
 * @param questionId 题目 ID
 * @param userAnswer 用户答案
 * @param isCorrect 是否正确
 * @param timeUsedSeconds 用时秒数
 * @returns 答案结果
 */
export const submitChallengeAnswer = (
  challengeId: string,
  questionId: string,
  userAnswer: string,
  isCorrect: boolean,
  timeUsedSeconds: number
): Promise<ApiResponse<{
  isCorrect: boolean
  correctAnswer: string
  pointsEarned: number
}>> => {
  return apiClient.post<
    { userAnswer: string; isCorrect: boolean; timeUsedSeconds: number },
    ApiResponse<{
      isCorrect: boolean
      correctAnswer: string
      pointsEarned: number
    }>
  >(
    `/challenge/${challengeId}/question/${questionId}/answer`,
    { userAnswer, isCorrect, timeUsedSeconds }
  )
}
