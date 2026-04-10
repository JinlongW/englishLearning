import apiClient from './request'
import type { ApiResponse } from '@/types/api'
import type { DailyChallengeDto, QuestionDetailResponse, ChallengeResult } from '@/types/api'

/**
 * 获取今日挑战状态
 * @returns 今日挑战状态
 */
export const getTodayChallenge = (): Promise<ApiResponse<DailyChallengeDto>> => {
  return apiClient.get<never, ApiResponse<DailyChallengeDto>>('/challenge/today')
}

/**
 * 开始新挑战
 * @returns 挑战 ID 和题目列表
 */
export const startChallenge = (): Promise<ApiResponse<{ challengeId: string; questions: QuestionDetailResponse[] }>> => {
  return apiClient.post<never, ApiResponse<{ challengeId: string; questions: QuestionDetailResponse[] }>>('/challenge/start')
}

/**
 * 提交挑战结果
 * @param challengeId 挑战 ID
 * @param answers 答案列表
 * @param timeUsedSeconds 用时秒数
 * @returns 挑战结果
 */
export const submitChallenge = (
  challengeId: string,
  answers: { questionId: string; userAnswer: string; isCorrect: boolean; timeUsedSeconds: number }[],
  timeUsedSeconds: number
): Promise<ApiResponse<ChallengeResult>> => {
  return apiClient.post<{ answers: typeof answers; timeUsedSeconds: number }, ApiResponse<ChallengeResult>>(
    `/challenge/${challengeId}/submit`,
    { answers, timeUsedSeconds }
  )
}
