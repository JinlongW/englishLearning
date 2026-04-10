<template>
  <div class="review-schedule">
    <div class="schedule-grid">
      <div
        v-for="(day, index) in scheduleData"
        :key="day.date"
        class="schedule-day"
        :class="{ today: day.isToday, hasWords: day.wordCount > 0 }"
      >
        <div class="day-header">
          <span class="day-name">{{ day.dayName }}</span>
          <span class="day-date">{{ day.month }}/{{ day.day }}</span>
        </div>

        <div class="day-content">
          <!-- 进度条可视化 -->
          <div class="progress-container">
            <div
              class="progress-bar"
              :style="{
                height: getBarHeight(day.wordCount) + 'px',
                background: getBarColor(day.wordCount, day.isToday)
              }"
            ></div>
          </div>

          <!-- 单词数量 -->
          <div class="word-count" :class="{ large: day.wordCount >= 10 }">
            {{ day.wordCount }}
          </div>

          <!-- 预览单词 -->
          <div v-if="day.previewWords.length > 0" class="word-preview">
            <span
              v-for="(word, idx) in day.previewWords"
              :key="idx"
              class="preview-tag"
            >
              {{ word }}
            </span>
          </div>

          <!-- 空状态 -->
          <div v-if="day.wordCount === 0" class="no-words">
            <span>✓</span>
            <span class="no-words-text">无复习</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface ReviewScheduleDto {
  date: string
  wordCount: number
  previewWords: string[]
}

const props = defineProps<{
  schedule: ReviewScheduleDto[]
}>()

const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

// 处理日程数据
const scheduleData = computed(() => {
  return props.schedule.map(item => {
    const date = new Date(item.date)
    const today = new Date()
    const isToday = date.toDateString() === today.toDateString()

    return {
      date: item.date,
      dayName: dayNames[date.getDay()],
      month: date.getMonth() + 1,
      day: date.getDate(),
      wordCount: item.wordCount,
      previewWords: item.previewWords,
      isToday
    }
  })
})

// 获取进度条高度（最大 60px）
const getBarHeight = (wordCount: number): number => {
  if (wordCount === 0) return 4
  return Math.min(60, 8 + wordCount * 4)
}

// 获取进度条颜色
const getBarColor = (wordCount: number, isToday: boolean): string => {
  if (wordCount === 0) return '#e2e8f0'
  if (isToday) return 'linear-gradient(180deg, #667eea 0%, #764ba2 100%)'
  if (wordCount >= 10) return 'linear-gradient(180deg, #f87171 0%, #ef4444 100%)'
  return 'linear-gradient(180deg, #4ade80 0%, #22c55e 100%)'
}
</script>

<style scoped>
.review-schedule {
  background: white;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.schedule-day {
  background: #f8fafc;
  border-radius: 12px;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.schedule-day.today {
  background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
  border-color: #667eea;
}

.schedule-day.hasWords {
  cursor: pointer;
}

.schedule-day.hasWords:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.day-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.day-name {
  font-size: 11px;
  color: #666;
  font-weight: 500;
}

.schedule-day.today .day-name {
  color: #667eea;
  font-weight: 600;
}

.day-date {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.day-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.progress-container {
  width: 100%;
  height: 60px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.progress-bar {
  width: 8px;
  border-radius: 4px;
  transition: height 0.3s, background 0.3s;
  min-height: 4px;
}

.word-count {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  min-height: 24px;
}

.word-count.large {
  color: #f87171;
}

.schedule-day.today .word-count {
  color: #667eea;
}

.word-preview {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  justify-content: center;
}

.preview-tag {
  background: #e0e7ff;
  color: #667eea;
  font-size: 9px;
  padding: 2px 4px;
  border-radius: 4px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-words {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: #4ade80;
}

.no-words span:first-child {
  font-size: 16px;
  font-weight: bold;
}

.no-words-text {
  font-size: 10px;
  color: #999;
}
</style>
