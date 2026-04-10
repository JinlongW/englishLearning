<template>
  <div class="story-learning-container">
    <header class="header">
      <div class="back-btn" @click="goBack">
        <span>‹</span> 返回
      </div>
      <h1>情景学习</h1>
      <div class="header-spacer"></div>
    </header>

    <main class="main-content">
      <!-- 课程标题 -->
      <div class="lesson-title-card">
        <h2>{{ lessonTitle }}</h2>
        <p>通过动画场景学习语法知识</p>
      </div>

      <!-- 场景滑动区域 -->
      <div class="scenes-container">
        <div
          ref="scenesContainerRef"
          class="scenes-wrapper"
          @touchstart="handleTouchStart"
          @touchmove="handleTouchMove"
          @touchend="handleTouchEnd"
        >
          <div
            v-for="(scene, index) in scenes"
            :key="scene.id || index"
            class="scene-item"
            :class="{ active: index === currentIndex }"
          >
            <!-- 场景序号指示器 -->
            <div class="scene-indicator">
              <span>{{ index + 1 }} / {{ scenes.length }}</span>
            </div>

            <!-- 情景组件 -->
            <StoryScene :scene="scene" />
          </div>
        </div>
      </div>

      <!-- 底部导航提示 -->
      <div class="navigation-hint">
        <span class="hint-icon">👆</span>
        <span>左右滑动切换场景</span>
      </div>

      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>

      <!-- 完成按钮 -->
      <button
        v-if="currentIndex === scenes.length - 1"
        class="complete-btn"
        @click="handleComplete"
      >
        ✨ 完成学习
      </button>

      <!-- 场景切换按钮（可选） -->
      <div class="scene-nav-buttons">
        <button
          v-if="currentIndex > 0"
          class="nav-btn prev"
          @click="prevScene"
        >
          ‹ 上一个
        </button>
        <button
          v-if="currentIndex < scenes.length - 1"
          class="nav-btn next"
          @click="nextScene"
        >
          下一个 ›
        </button>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { SceneDto } from '@/types/api'
import StoryScene from '@/components/StoryScene.vue'
import BottomNav from '@/components/BottomNav.vue'

const route = useRoute()
const router = useRouter()

const lessonTitle = ref('Tom 的日常')
const scenes = ref<SceneDto[]>([
  {
    title: '早晨上学',
    image: '🏫',
    dialogue: [
      { speaker: 'Tom', text: 'I go to school every day.' },
      { speaker: 'Lily', text: 'She goes to school at 8:00.' }
    ],
    grammarPoint: '一般现在时表示习惯性动作，第三人称单数动词加 -s'
  },
  {
    title: '午饭时间',
    image: '🍽️',
    dialogue: [
      { speaker: 'Tom', text: 'We eat lunch at 12:00.' },
      { speaker: 'Lily', text: 'He eats an apple every day.' }
    ],
    grammarPoint: '主语是复数时动词用原形，主语是第三人称单数时动词加 -s'
  },
  {
    title: '放学后',
    image: '⚽',
    dialogue: [
      { speaker: 'Tom', text: 'They play football after school.' },
      { speaker: 'Lily', text: 'She plays basketball on weekends.' }
    ],
    grammarPoint: '表示经常性、习惯性的动作或客观事实用一般现在时'
  }
])

const currentIndex = ref(0)
const scenesContainerRef = ref<HTMLElement | null>(null)

// 触摸滑动相关
const touchStartX = ref(0)
const touchMoveDistance = ref(0)
const isSwiping = ref(false)

// 进度百分比
const progressPercent = computed(() => {
  return ((currentIndex.value + 1) / scenes.value.length) * 100
})

// 处理触摸开始
const handleTouchStart = (event: TouchEvent) => {
  touchStartX.value = event.touches[0].clientX
  isSwiping.value = true
  touchMoveDistance.value = 0
}

// 处理触摸移动
const handleTouchMove = (event: TouchEvent) => {
  if (!isSwiping.value) return
  touchMoveDistance.value = event.touches[0].clientX - touchStartX.value
}

// 处理触摸结束
const handleTouchEnd = () => {
  isSwiping.value = false
  const threshold = 50 // 滑动阈值（像素）

  if (touchMoveDistance.value > threshold) {
    // 向右滑动 - 上一个
    if (currentIndex.value > 0) {
      currentIndex.value--
    }
  } else if (touchMoveDistance.value < -threshold) {
    // 向左滑动 - 下一个
    if (currentIndex.value < scenes.value.length - 1) {
      currentIndex.value++
    }
  }
  touchMoveDistance.value = 0
}

// 上一个场景
const prevScene = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

// 下一个场景
const nextScene = () => {
  if (currentIndex.value < scenes.value.length - 1) {
    currentIndex.value++
  }
}

// 返回
const goBack = () => {
  router.back()
}

// 完成学习
const handleComplete = () => {
  // 显示完成提示
  uni.showModal({
    title: '🎉 学习完成！',
    content: `你已完成 "${lessonTitle.value}" 的学习，获得 10 积分！`,
    showCancel: false,
    confirmText: '继续学习',
    success: () => {
      // TODO: 调用 API 记录学习进度和积分
      // 返回语法详情页
      router.back()
    }
  })
}

onMounted(() => {
  // 可以从路由参数获取课程 ID 和标题
  const title = route.query.title as string
  if (title) {
    lessonTitle.value = title
  }
})
</script>

<style scoped>
.story-learning-container {
  min-height: 100vh;
  padding-bottom: 70px;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 15px 20px;
  color: white;
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.back-btn span {
  font-size: 20px;
}

.header h1 {
  margin: 0;
  font-size: 18px;
}

.header-spacer {
  flex: 1;
}

.main-content {
  padding: 20px;
}

.lesson-title-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.lesson-title-card h2 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 20px;
}

.lesson-title-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.scenes-container {
  overflow: hidden;
  margin-bottom: 15px;
}

.scenes-wrapper {
  display: flex;
  transition: transform 0.3s ease-out;
}

.scene-item {
  min-width: 100%;
  transition: opacity 0.3s;
}

.scene-indicator {
  text-align: center;
  padding: 8px;
  font-size: 12px;
  color: #999;
}

.navigation-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #999;
  font-size: 13px;
  margin-bottom: 15px;
}

.hint-icon {
  animation: swipe-hint 1.5s infinite;
}

@keyframes swipe-hint {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(5px); }
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
  border-radius: 10px;
}

.complete-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  margin-bottom: 15px;
}

.complete-btn:active {
  transform: scale(0.95);
}

.scene-nav-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.nav-btn {
  padding: 12px 24px;
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-btn:active {
  background: #667eea;
  color: white;
}
</style>
