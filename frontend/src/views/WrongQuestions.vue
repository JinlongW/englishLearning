<template>
  <div class="wrong-questions-container">
    <header class="header">
      <h1>错题本</h1>
      <p>温故而知新，消灭错题！</p>
    </header>

    <main class="main-content">
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-value">{{ totalWrong }}</div>
          <div class="stat-label">总错题</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ needReview }}</div>
          <div class="stat-label">待复习</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ mastered }}</div>
          <div class="stat-label">已掌握</div>
        </div>
      </div>

      <!-- 筛选标签 -->
      <div class="filter-tabs">
        <button
          :class="{ active: filter === 'all' }"
          @click="filter = 'all'"
        >
          全部
        </button>
        <button
          :class="{ active: filter === 'review' }"
          @click="filter = 'review'"
        >
          待复习
        </button>
        <button
          :class="{ active: filter === 'mastered' }"
          @click="filter = 'mastered'"
        >
          已掌握
        </button>
      </div>

      <!-- 错题列表 -->
      <div class="question-list" v-if="questions.length > 0">
        <div
          v-for="q in questions"
          :key="q.id"
          class="question-card"
          @click="reviewQuestion(q)"
        >
          <div class="question-content">
            <div class="question-text">{{ q.text }}</div>
            <div class="question-meta">
              <span class="question-type">{{ q.type }}</span>
              <span class="question-date">{{ q.lastReviewDate }}</span>
            </div>
          </div>
          <div class="question-status" :class="q.status">
            {{ q.status === 'new' ? '新题' : q.status === 'reviewing' ? '复习中' : '已掌握' }}
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🎉</div>
        <p>太棒了！目前没有错题！</p>
      </div>

      <!-- 复习按钮 -->
      <button v-if="needReview > 0" class="review-btn" @click="startReview">
        开始复习 ({{ needReview }} 题)
      </button>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getWrongQuestions } from '@/api/wrong-question'
import type { WrongQuestionDetailResponse } from '@/types/api'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()

const filter = ref<'all' | 'review' | 'mastered'>('all')
const loading = ref(false)

const totalWrong = ref(0)
const needReview = ref(0)
const mastered = ref(0)
const questions = ref<WrongQuestionDetailResponse[]>([])

const loadWrongQuestions = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const status = filter.value === 'all' ? null : filter.value
    const res = await getWrongQuestions(1, 100, status)
    questions.value = res.items || []

    // 统计
    totalWrong.value = res.total || 0
    needReview.value = questions.value.filter(q => q.reviewStatus !== 'mastered').length
    mastered.value = questions.value.filter(q => q.reviewStatus === 'mastered').length
  } catch (error) {
    console.error('加载错题失败', error)
    const errorMessage = error instanceof Error ? error.message : '加载失败，请稍后重试'
    uni.showToast({
      title: errorMessage,
      icon: 'none',
      duration: 3000
    })
  } finally {
    loading.value = false
  }
}

const startReview = async () => {
  try {
    const res = await getWrongQuestions(1, 10, 'review')
    if (res.items && res.items.length > 0) {
      // 获取待复习题目 ID 列表
      const questionIds = res.items.map(q => q.id).join(',')

      // 跳转到复习页面
      router.push({
        path: '/wrong-questions/review',
        query: { ids: questionIds }
      })
    } else {
      uni.showToast({
        title: '当前没有需要复习的题目',
        icon: 'none'
      })
    }
  } catch (error) {
    console.error('加载复习题目失败', error)
    uni.showToast({
      title: '加载失败，请稍后重试',
      icon: 'none'
    })
  }
}

const reviewQuestion = (q: WrongQuestionDetailResponse) => {
  // 跳转到单个题目的复习页面
  router.push({
    path: '/wrong-questions/review',
    query: { ids: q.id }
  })
}

onMounted(() => {
  loadWrongQuestions()
})

// 当筛选变化时重新加载
watch(filter, () => {
  loadWrongQuestions()
})
</script>

<style scoped>
.wrong-questions-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  padding: 20px;
  color: white;
}

.header h1 {
  margin-bottom: 5px;
}

.header p {
  opacity: 0.9;
  font-size: 14px;
}

.main-content {
  padding: 20px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #4facfe;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.filter-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-tabs button {
  flex: 1;
  padding: 10px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tabs button.active {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border-color: transparent;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.question-card {
  background: white;
  border-radius: 15px;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s;
}

.question-card:hover {
  transform: translateX(5px);
}

.question-content {
  flex: 1;
}

.question-text {
  color: #333;
  margin-bottom: 10px;
  font-size: 15px;
}

.question-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
}

.question-type,
.question-date {
  background: #f5f7fa;
  padding: 3px 8px;
  border-radius: 5px;
}

.question-status {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.question-status.new {
  background: #ffe4e6;
  color: #f43f5e;
}

.question-status.reviewing {
  background: #fef3c7;
  color: #f59e0b;
}

.question-status.mastered {
  background: #dcfce7;
  color: #22c55e;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 15px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 15px;
}

.review-btn {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  padding: 15px 40px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 5px 20px rgba(79, 172, 254, 0.4);
  cursor: pointer;
}
</style>
