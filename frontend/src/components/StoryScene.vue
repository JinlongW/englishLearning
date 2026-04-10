<template>
  <div class="story-scene">
    <!-- 场景插图 -->
    <div class="scene-image">
      <span class="emoji">{{ scene.image }}</span>
    </div>

    <!-- 场景标题 -->
    <h3 class="scene-title">{{ scene.title }}</h3>

    <!-- 角色对话区域 -->
    <div class="dialogue-area">
      <div
        v-for="(line, index) in scene.dialogue"
        :key="index"
        class="dialogue-bubble"
        :class="getSpeakerClass(line.speaker)"
      >
        <div class="speaker-name">{{ line.speaker }}</div>
        <div class="speech-bubble">
          <p class="dialogue-text">{{ line.text }}</p>
        </div>
      </div>
    </div>

    <!-- 语法点高亮区域 -->
    <div class="grammar-point">
      <div class="grammar-label">
        <span>💡</span> 语法小贴士
      </div>
      <p class="grammar-text">{{ highlightGrammarPoint(scene.grammarPoint) }}</p>
    </div>

    <!-- 播放按钮（预留音频功能） -->
    <button class="play-button" @click="handlePlay" title="播放音频">
      <span>▶️</span> 听对话
    </button>
  </div>
</template>

<script setup lang="ts">
import type { SceneDto } from '@/types/api'

interface Props {
  scene: SceneDto
}

defineProps<Props>()

// 根据说话者返回不同的样式类
const getSpeakerClass = (speaker: string): string => {
  const speakerLower = speaker.toLowerCase()
  if (speakerLower.includes('tom') || speakerLower.includes('boy') || speakerLower.includes('he')) {
    return 'speaker-boy'
  }
  if (speakerLower.includes('lily') || speakerLower.includes('girl') || speakerLower.includes('she')) {
    return 'speaker-girl'
  }
  return 'speaker-default'
}

// 高亮显示语法点中的关键词
const highlightGrammarPoint = (text: string): string => {
  // 简单实现：返回纯文本，后续可通过正则高亮动词变化等
  return text
}

// 播放音频处理（预留功能）
const handlePlay = () => {
  uni.showToast({
    title: '音频功能开发中',
    icon: 'none',
    duration: 2000
  })
  // TODO: 后续实现 TTS 或预录制音频播放
}
</script>

<style scoped>
.story-scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: linear-gradient(180deg, #f0f4ff 0%, #ffffff 100%);
  border-radius: 20px;
  min-height: 400px;
}

.scene-image {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.scene-image .emoji {
  font-size: 60px;
}

.scene-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
}

.dialogue-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.dialogue-bubble {
  display: flex;
  flex-direction: column;
  max-width: 85%;
}

.dialogue-bubble.speaker-boy {
  align-items: flex-start;
  align-self: flex-start;
}

.dialogue-bubble.speaker-girl {
  align-items: flex-end;
  align-self: flex-end;
}

.dialogue-bubble.speaker-default {
  align-items: flex-start;
}

.speaker-name {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
  font-weight: 600;
}

.speech-bubble {
  position: relative;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.6;
  max-width: 100%;
}

.dialogue-bubble.speaker-boy .speech-bubble,
.dialogue-bubble.speaker-default .speech-bubble {
  background: #e3f2fd;
  color: #1565c0;
  border-bottom-left-radius: 4px;
}

.dialogue-bubble.speaker-girl .speech-bubble {
  background: #fce4ec;
  color: #c2185b;
  border-bottom-right-radius: 4px;
}

.dialogue-text {
  margin: 0;
  word-wrap: break-word;
}

.grammar-point {
  width: 100%;
  background: #fff9e6;
  border: 2px solid #ffd54f;
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
}

.grammar-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #f57c00;
  font-weight: 600;
  margin-bottom: 8px;
}

.grammar-text {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.play-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.play-button:active {
  transform: scale(0.95);
}

.play-button span {
  font-size: 16px;
}
</style>
