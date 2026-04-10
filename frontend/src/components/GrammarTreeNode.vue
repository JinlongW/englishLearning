<template>
  <div class="tree-node">
    <div
      class="node-content"
      :class="[node.status, `level-${node.level}`]"
      @click="handleClick"
    >
      <div class="node-icon">
        <span v-if="node.status === 'completed'">✅</span>
        <span v-else-if="node.status === 'learning'">📖</span>
        <span v-else-if="node.status === 'available'">🔓</span>
        <span v-else>🔒</span>
      </div>
      <div class="node-info">
        <div class="node-header">
          <h4>{{ node.title }}</h4>
          <span class="category-tag">{{ getCategoryLabel(node.category) }}</span>
        </div>
        <p class="node-description">{{ node.description }}</p>
        <div class="node-meta">
          <span class="level-badge">L{{ node.level }}</span>
        </div>
      </div>
      <div class="node-arrow">›</div>
    </div>

    <!-- 递归渲染子节点 -->
    <div v-if="node.children.length > 0" class="node-children">
      <tree-node
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        @click-node="handleChildClick"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { GrammarTreeNode } from '@/types/api'

interface Props {
  node: GrammarTreeNode
}

const props = defineProps<Props>()

const emit = defineEmits<{
  clickNode: [node: GrammarTreeNode]
}>()

// 分类标签映射
const categoryLabels: Record<string, string> = {
  tense: '时态',
  voice: '语态',
  clause: '从句',
  word: '词汇',
  sentence: '句型'
}

const getCategoryLabel = (category: string): string => {
  return categoryLabels[category] || category
}

const handleClick = () => {
  emit('clickNode', props.node)
}

const handleChildClick = (child: GrammarTreeNode) => {
  emit('clickNode', child)
}
</script>

<style scoped>
.tree-node {
  margin-left: 0;
}

.node-content {
  background: white;
  border-radius: 12px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 4px solid transparent;
}

.node-content:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.node-content.completed {
  border-left-color: #52c41a;
  background: #f6ffed;
}

.node-content.learning {
  border-left-color: #1890ff;
  background: #e6f7ff;
}

.node-content.available {
  border-left-color: #faad14;
  background: #fffbe6;
}

.node-content.locked {
  border-left-color: #d9d9d9;
  opacity: 0.7;
}

.node-icon {
  font-size: 28px;
  flex-shrink: 0;
}

.node-info {
  flex: 1;
  min-width: 0;
}

.node-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.node-header h4 {
  color: #333;
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.category-tag {
  flex-shrink: 0;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  background: #f0f0f0;
  color: #666;
}

.node-content.completed .category-tag {
  background: #f6ffed;
  color: #52c41a;
}

.node-content.learning .category-tag {
  background: #e6f7ff;
  color: #1890ff;
}

.node-content.available .category-tag {
  background: #fffbe6;
  color: #faad14;
}

.node-description {
  color: #666;
  font-size: 12px;
  margin: 0 0 6px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.node-meta {
  display: flex;
  gap: 8px;
}

.level-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.node-arrow {
  font-size: 20px;
  color: #ccc;
  flex-shrink: 0;
}

.node-children {
  margin-left: 20px;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
