<template>
  <div class="smart-review-container">
    <header class="header">
      <h1>智能复习</h1>
      <p class="subtitle">基于艾宾浩斯记忆曲线</p>
    </header>

    <main class="main-content">
      <!-- 今日复习概览 -->
      <section class="today-summary">
        <div class="summary-card">
          <div class="summary-icon">📅</div>
          <div class="summary-content">
            <div class="summary-title">今日待复习</div>
            <div class="summary-count">{{ todayCount }}</div>
            <div class="summary-urgent" v-if="urgentCount > 0">
              <span class="urgent-badge">{{ urgentCount }} 个即将遗忘</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 一键开始复习 -->
      <section class="start-section">
        <button class="start-btn" @click="startReview" :disabled="todayCount === 0 || starting">
          <span class="btn-icon">🎯</span>
          <span>{{ starting ? '加载中...' : '一键开始复习' }}</span>
        </button>
      </section>

      <!-- 今日待复习单词列表 -->
      <section class="words-section" v-if="reviewWords.length > 0">
        <h2>今日待复习单词</h2>
        <div class="words-list">
          <div
            v-for="word in reviewWords"
            :key="word.id"
            class="word-item"
            :class="{ urgent: word.isUrgent }"
          >
            <div class="word-info">
              <div class="word-text">{{ word.wordText }}</div>
              <div class="word-meaning">{{ word.meaningCn }}</div>
              <div class="word-meta">
                <span class="review-count">已复习 {{ word.reviewCount }} 次</span>
                <span class="next-review" :class="{ overdue: word.isUrgent }">
                  {{ formatReviewTime(word.nextReviewAt) }}
                </span>
              </div>
            </div>
            <div class="word-status">
              <span v-if="word.isUrgent" class="urgent-tag">紧急</span>
              <span v-else class="normal-tag">待复习</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 空状态 -->
      <div v-if="!loading && reviewWords.length === 0" class="empty-state">
        <div class="empty-icon">🎉</div>
        <p>太棒了！没有需要复习的单词</p>
        <p class="empty-hint">继续学习新单词，稍后再来检查</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner">📚</div>
        <p>加载复习计划中...</p>
      </div>

      <!-- 本周复习计划 -->
      <section class="schedule-section" v-if="weeklySchedule.length > 0">
        <h2>本周复习计划</h2>
        <ReviewSchedule :schedule="weeklySchedule" />
      </section>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/request'
import BottomNav from '@/components/BottomNav.vue'
import ReviewSchedule from '@/components/ReviewSchedule.vue'

interface WordReviewDto {
  id: string
  wordText: string
  meaningCn: string
  reviewCount: number
  nextReviewAt: string
  isUrgent: boolean
}

interface ReviewScheduleDto {
  date: string
  wordCount: number
  previewWords: string[]
}

const loading = ref(false)
const starting = ref(false)
const reviewWords = ref<WordReviewDto[]>([])
const weeklySchedule = ref<ReviewScheduleDto[]>([])

const todayCount = ref(0)
const urgentCount = ref(0)

// 格式化复习时间
const formatReviewTime = (reviewTime: string): string => {
  const now = new Date()
  const reviewDate = new Date(reviewTime)
  const diffMs = reviewDate.getTime() - now.getTime()
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffMinutes < 0) {
    return `已过期 ${Math.abs(diffMinutes)} 分钟`
  } else if (diffMinutes < 60) {
    return `${diffMinutes} 分钟后`
  } else if (diffHours < 24) {
    return `${diffHours} 小时后`
  } else {
    return `${diffDays} 天后`
  }
}

// 加载复习单词
const loadReviewWords = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const result = await apiClient.get<never, { data: WordReviewDto[] }>('/word/review/due')
    reviewWords.value = result.data || []
    todayCount.value = reviewWords.value.length
    urgentCount.value = reviewWords.value.filter(w => w.isUrgent).length
  } catch (error) {
    console.error('加载复习单词失败', error)
    uni.showToast({ title: '加载失败，请重试', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// 加载周计划
const loadWeeklySchedule = async () => {
  try {
    const result = await apiClient.get<never, { data: ReviewScheduleDto[] }>('/word/review/schedule')
    weeklySchedule.value = result.data || []
  } catch (error) {
    console.error('加载周计划失败', error)
  }
}

// 开始复习
const startReview = async () => {
  if (starting.value || reviewWords.value.length === 0) return

  starting.value = true
  try {
    // 跳转到复习模式（可以复用 WordDetail 或创建专门的复习页）
    // 这里先简单提示，后续可以创建专门的复习页面
    uni.showToast({
      title: `开始复习 ${reviewWords.value.length} 个单词`,
      icon: 'none',
      duration: 2000
    })
    // TODO: 导航到复习页面
  } catch (error) {
    console.error('开始复习失败', error)
    uni.showToast({ title: '启动失败，请重试', icon: 'none' })
  } finally {
    starting.value = false
  }
}

onMounted(() => {
  loadReviewWords()
  loadWeeklySchedule()
})
</script>

<style scoped>
.smart-review-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.header h1 {
  margin-bottom: 5px;
  font-size: 24px;
}

.header .subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.main-content {
  padding: 20px;
}

.today-summary {
  margin-bottom: 20px;
}

.summary-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.summary-icon {
  font-size: 48px;
}

.summary-content {
  flex: 1;
}

.summary-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.summary-count {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.summary-urgent {
  display: flex;
  align-items: center;
  gap: 8px;
}

.urgent-badge {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.start-section {
  margin-bottom: 25px;
}

.start-btn {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.start-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 24px;
}

.words-section h2 {
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.words-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 25px;
}

.word-item {
  background: white;
  border-radius: 12px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.word-item.urgent {
  border-left: 4px solid #f87171;
}

.word-item:hover {
  transform: translateY(-2px);
}

.word-info {
  flex: 1;
}

.word-text {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.word-meaning {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.word-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.review-count {
  background: #f0f4ff;
  padding: 2px 8px;
  border-radius: 10px;
  color: #667eea;
}

.next-review {
  color: #999;
}

.next-review.overdue {
  color: #f87171;
  font-weight: 500;
}

.word-status {
  display: flex;
  gap: 8px;
}

.urgent-tag {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.normal-tag {
  background: #e0e7ff;
  color: #667eea;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.schedule-section {
  margin-top: 25px;
}

.schedule-section h2 {
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  margin-bottom: 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 15px;
}

.empty-state p {
  color: #666;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: #999;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
}

.loading-spinner {
  font-size: 60px;
  margin-bottom: 15px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
