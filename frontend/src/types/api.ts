// API 响应基础接口
export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// 分页响应接口
export interface PageResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

// 用户信息接口
export interface UserInfo {
  id: string
  username: string
  studentName: string
  gradeLevel: number
  levelName: string
  currentLevel: number
  currentExp: number
  currentStreak: number
}

// 登录响应接口
export interface LoginResponse {
  token: string
  user: UserInfo
  expiresIn?: number
}

// 单词接口
export interface Word {
  id: string
  wordText: string
  phoneticUk: string
  phoneticUs: string
  audioUrl?: string
  meaningCn: string
  partOfSpeech?: string
  exampleEn?: string
  exampleCn?: string
  imageUrl?: string
  status: string
  score?: number
  progress?: number
}

// 语法课程接口
export interface GrammarLesson {
  id: string
  title: string
  description: string
  duration: number
  status: 'locked' | 'learning' | 'completed'
  score?: number
}

// 每日挑战接口
export interface DailyChallenge {
  id: string
  date: string
  totalQuestions: number
  correctCount: number
  progress: number
  isCompleted: boolean
}

// 错题接口
export interface WrongQuestion {
  id: string
  text: string
  type: string
  status: 'new' | 'reviewing' | 'mastered'
  lastReviewDate: string
  reviewCount: number
}

// 错题详情响应接口（包含完整题目信息）
export interface WrongQuestionDetailResponse {
  id: string
  questionId: string
  questionText: string
  questionType: string
  difficulty: number
  options: QuestionOption[]
  correctAnswer: string
  analysis: string
  reviewStatus: 'new' | 'reviewing' | 'mastered'
  reviewCount: number
  lastReviewDate: string
  nextReviewAt: string | null
}

// 题目选项接口
export interface QuestionOption {
  id: string
  optionKey: string
  optionContent: string
  imageUrl?: string
  audioUrl?: string
}

// 题目详情响应接口
export interface QuestionDetailResponse {
  id: string
  questionType: string
  difficulty: number
  questionStem: string
  stemAudioUrl?: string
  options: QuestionOption[]
  questionOrder?: number
}

// 答案提交结果响应
export interface AnswerResult {
  isCorrect: boolean
  correctAnswer: string
  analysis: string
  pointsEarned: number
  expEarned: number
  levelUp: boolean
}

// 挑战题目结果接口
export interface ChallengeQuestionResult {
  questionId: string
  questionStem: string
  userAnswer: string
  correctAnswer: string
  isCorrect: boolean
  timeUsedSeconds: number
  speedBonus: number
  analysis?: string
}

// 挑战结果响应接口
export interface ChallengeResult {
  id: string
  totalQuestions: number
  correctCount: number
  score: number
  timeUsedSeconds: number
  pointsEarned: number
  coinsEarned: number
  questionResults: ChallengeQuestionResult[]
}

// 每日挑战 DTO
export interface DailyChallengeDto {
  id?: string
  date: string
  status: string
  isCompleted: boolean
  totalQuestions: number
  correctCount: number
  score: number
  pointsEarned: number
  coinsEarned: number
}

// 语法课程详情 DTO
export interface GrammarDetailDto {
  id: string
  title: string
  contentType: string
  durationSeconds?: number
  sortOrder: number
  passingScore: number
  status: string
  score?: number
  contentJson?: string
  quizJson?: string
}

// 情景对话条目
export interface SceneDialogue {
  speaker: string
  text: string
}

// 情景学习场景 DTO
export interface SceneDto {
  title: string
  image: string
  dialogue: SceneDialogue[]
  grammarPoint: string
}

// 带情景的语法详情 DTO
export interface GrammarDetailWithScenesDto extends GrammarDetailDto {
  scenes?: SceneDto[]
}

// 徽章信息 DTO
export interface BadgeDto {
  id: string
  badgeCode: string
  badgeName: string
  badgeIcon?: string
  badgeType: string
  description: string
  earnedAt?: string
  isEarned: boolean
  isNew: boolean
}

// 学习统计响应
export interface LearningSummary {
  totalLearningDays: number
  currentStreak: number
  maxStreak: number
  wordsLearned: number
  grammarsCompleted: number
  challengesCompleted: number
  wrongQuestionCount: number
  totalPoints: number
  totalCoins: number
  currentLevel: number
  levelName: string
}

// 共同答案提交接口 - 可重用
export interface AnswerSubmission {
  userAnswer: string
  timeUsedSeconds: number
}

// 语法测验结果响应
export interface GrammarQuizResult {
  score: number
  isPassed: boolean
  correctCount: number
  totalCount: number
  pointsEarned: number
}

// 年级单元树节点接口
export interface GradeUnitTreeNode {
  id: string
  label: string
  grade: number
  semester: string
  unitNo: number
  wordCount: number
  learnedWordCount: number
  status: 'not_started' | 'learning' | 'completed'
}

// 年级树节点接口
export interface GradeTreeNode {
  grade: number
  label: string
  semester: string
  units: GradeUnitTreeNode[]
}

// 语法知识树节点接口
export interface GrammarTreeNode {
  id: string
  title: string
  description: string
  level: number
  category: string
  status: 'locked' | 'available' | 'learning' | 'completed'
  prerequisiteId?: string
  children: GrammarTreeNode[]
}
