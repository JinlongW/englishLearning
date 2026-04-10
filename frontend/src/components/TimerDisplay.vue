<template>
  <div class="timer-display" :class="{ 'warning': isWarning }">
    <div class="timer-circle">
      <svg class="progress-ring" width="60" height="60">
        <!-- 背景圆环 -->
        <circle
          class="progress-ring__circle-bg"
          stroke="#e0e0e0"
          stroke-width="4"
          fill="transparent"
          r="26"
          cx="30"
          cy="30"
        />
        <!-- 进度圆环 -->
        <circle
          class="progress-ring__circle"
          :stroke="circleColor"
          stroke-width="4"
          fill="transparent"
          r="26"
          cx="30"
          cy="30"
          :style="circleStyle"
        />
      </svg>
      <div class="timer-text">
        <span :class="{ 'warning-text': isWarning }">{{ displayTime }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps<{
  totalTime?: number // 总时间（秒），默认 30 秒
  isRunning?: boolean // 是否正在计时
}>()

const emit = defineEmits<{
  (e: 'timeout'): void // 时间到事件
  (e: 'tick', timeLeft: number): void // 每秒计时事件
}>()

const totalTime = props.totalTime ?? 30
const timeLeft = ref(totalTime)
const timerInterval = ref<number | null>(null)

// 计算显示时间
const displayTime = computed(() => {
  return Math.ceil(timeLeft.value).toString()
})

// 根据剩余时间计算颜色（绿 -> 黄 -> 红）
const circleColor = computed(() => {
  const percentage = timeLeft.value / totalTime
  if (percentage > 0.5) {
    // 绿色 (16-30 秒)
    return '#4ade80'
  } else if (percentage > 0.3) {
    // 黄色 (9-15 秒)
    return '#fbbf24'
  } else {
    // 红色 (0-8 秒)
    return '#ef4444'
  }
})

// 最后 5 秒进入警告状态
const isWarning = computed(() => timeLeft.value <= 5)

// 计算圆环样式（虚线圆环进度）
const circleStyle = computed(() => {
  const circumference = 2 * Math.PI * 26
  const offset = circumference - (timeLeft.value / totalTime) * circumference
  return {
    strokeDasharray: `${circumference} ${circumference}`,
    strokeDashoffset: offset.toString(),
    transition: 'stroke-dashoffset 0.1s linear, stroke 0.3s ease'
  }
})

// 开始计时
const start = () => {
  stop()
  timeLeft.value = totalTime
  if (props.isRunning !== false) {
    timerInterval.value = window.setInterval(() => {
      timeLeft.value -= 0.1
      emit('tick', Math.ceil(timeLeft.value))

      if (timeLeft.value <= 0) {
        stop()
        emit('timeout')
      }
    }, 100)
  }
}

// 停止计时
const stop = () => {
  if (timerInterval.value !== null) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

// 重置计时器
const reset = () => {
  stop()
  timeLeft.value = totalTime
}

// 暴露方法给父组件
defineExpose({
  start,
  stop,
  reset,
  timeLeft
})

// 监听 isRunning 变化
watch(() => props.isRunning, (newVal) => {
  if (newVal) {
    start()
  } else {
    stop()
  }
}, { immediate: true })

onUnmounted(() => {
  stop()
})
</script>

<style scoped>
.timer-display {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.timer-circle {
  position: relative;
  width: 60px;
  height: 60px;
}

.progress-ring {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

.progress-ring__circle {
  stroke-linecap: round;
}

.progress-ring__circle-bg {
  stroke-linecap: round;
}

.timer-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.warning-text {
  color: #ef4444;
  animation: pulse 0.5s ease-in-out infinite alternate;
}

.timer-display.warning {
  animation: shake 0.5s ease-in-out infinite;
}

@keyframes pulse {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-3px);
  }
  75% {
    transform: translateX(3px);
  }
}
</style>
