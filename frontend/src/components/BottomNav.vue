<template>
  <nav class="bottom-nav">
    <router-link
      v-for="route in routes"
      :key="route.path"
      :to="route.path"
      class="nav-item"
      :class="{ active: isActive(route.path) }"
    >
      <span class="nav-icon">{{ route.icon }}</span>
      <span>{{ route.name }}</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

interface NavRoute {
  path: string
  icon: string
  name: string
}

const route = useRoute()

const routes: NavRoute[] = [
  { path: '/', icon: '🏠', name: '首页' },
  { path: '/words', icon: '🔤', name: '单词' },
  { path: '/smart-review', icon: '🧠', name: '复习' },
  { path: '/challenge', icon: '⚔️', name: '挑战' },
  { path: '/profile', icon: '👤', name: '我的' }
]

const isActive = (path: string): boolean => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #999;
  font-size: 12px;
  gap: 4px;
  transition: color 0.2s;
}

.nav-item.active {
  color: #667eea;
}

.nav-item.active .nav-icon {
  filter: drop-shadow(0 2px 4px rgba(102, 126, 234, 0.3));
}

.nav-icon {
  font-size: 24px;
}
</style>
