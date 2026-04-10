<template>
  <div class="combo-display" :class="comboClass" :style="{ opacity: show ? 1 : 0 }">
    <div class="combo-content">
      <span class="combo-effect" aria-hidden="true">{{ comboEffect }}</span>
      <span class="combo-text">{{ comboLabel }}</span>
      <span class="combo-multiplier">×{{ multiplier }}x</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  combo: number
  show?: boolean
}>()

// 连击倍率配置
const comboConfig = [
  { min: 10, multiplier: 3.0, effect: '👑', label: '王者连击', class: 'combo-crown' },
  { min: 7, multiplier: 2.5, effect: '🔥🔥🔥', label: '烈焰连击', class: 'combo-inferno' },
  { min: 4, multiplier: 2.0, effect: '🔥🔥', label: '热手连击', class: 'combo-hot' },
  { min: 2, multiplier: 1.5, effect: '🔥', label: '小火连击', class: 'combo-fire' },
  { min: 1, multiplier: 1.0, effect: '', label: '继续加油', class: 'combo-normal' }
]

// 计算当前连击等级
const currentLevel = computed(() => {
  return comboConfig.find(level => props.combo >= level.min) || comboConfig[comboConfig.length - 1]
})

// 连击倍率
const multiplier = computed(() => currentLevel.value.multiplier)

// 连击特效图标
const comboEffect = computed(() => currentLevel.value.effect)

// 连击文字标签
const comboLabel = computed(() => {
  if (props.combo === 0) return '连击中断'
  return currentLevel.value.label
})

// 连击样式类
const comboClass = computed(() => [
  currentLevel.value.class,
  { 'combo-broken': props.combo === 0 }
])
</script>

<style scoped>
.combo-display {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 14px;
  transition: all 0.3s ease;
  pointer-events: none;
  user-select: none;
}

.combo-content {
  display: flex;
  align-items: center;
  gap: 8px;
  animation: combo-pulse 0.5s ease-in-out;
}

.combo-effect {
  font-size: 18px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.combo-text {
  white-space: nowrap;
}

.combo-multiplier {
  font-size: 16px;
  font-weight: 900;
}

/* 连击等级样式 */
.combo-normal {
  background: rgba(156, 163, 175, 0.9);
  color: white;
}

.combo-fire {
  background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);
  animation: combo-fire-glow 1.5s ease-in-out infinite;
}

.combo-hot {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(220, 38, 38, 0.5);
  animation: combo-hot-glow 1.2s ease-in-out infinite;
}

.combo-inferno {
  background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
  color: white;
  box-shadow: 0 4px 25px rgba(124, 58, 237, 0.6);
  animation: combo-inferno-glow 1s ease-in-out infinite;
}

.combo-crown {
  background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
  color: white;
  box-shadow: 0 4px 30px rgba(251, 191, 36, 0.7);
  animation: combo-crown-glow 0.8s ease-in-out infinite;
}

/* 连击中断样式 */
.combo-broken {
  background: rgba(107, 114, 128, 0.9);
  color: #fca5a5;
  animation: combo-shake 0.4s ease-in-out;
}

/* 动画效果 */
@keyframes combo-pulse {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes combo-fire-glow {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);
  }
  50% {
    box-shadow: 0 4px 25px rgba(249, 115, 22, 0.6);
  }
}

@keyframes combo-hot-glow {
  0%, 100% {
    box-shadow: 0 4px 20px rgba(220, 38, 38, 0.5);
  }
  50% {
    box-shadow: 0 4px 30px rgba(220, 38, 38, 0.7);
  }
}

@keyframes combo-inferno-glow {
  0%, 100% {
    box-shadow: 0 4px 25px rgba(124, 58, 237, 0.6);
    transform: translateX(-50%) scale(1);
  }
  50% {
    box-shadow: 0 4px 35px rgba(124, 58, 237, 0.8);
    transform: translateX(-50%) scale(1.02);
  }
}

@keyframes combo-crown-glow {
  0%, 100% {
    box-shadow: 0 4px 30px rgba(251, 191, 36, 0.7);
    transform: translateX(-50%) scale(1);
  }
  50% {
    box-shadow: 0 4px 45px rgba(251, 191, 36, 0.9);
    transform: translateX(-50%) scale(1.05);
  }
}

@keyframes combo-shake {
  0%, 100% {
    transform: translateX(-50%) translateX(0);
  }
  25% {
    transform: translateX(-50%) translateX(-5px);
  }
  75% {
    transform: translateX(-50%) translateX(5px);
  }
}
</style>
