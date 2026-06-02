<script setup lang="ts">
const route = useRoute()

const navItems = [
  { label: 'Home', to: '/', icon: '⌂' },
  { label: 'Sessions', to: '/sessions', icon: '✦' },
  { label: 'Approvals', to: '/approvals', icon: '✓' },
  { label: 'KB', to: '/kb', icon: '◇' },
  { label: 'Calendar', to: '/calendar', icon: '◷' },
  { label: 'Settings', to: '/settings', icon: '⚙' }
]
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar" aria-label="Primary navigation">
      <NuxtLink class="brand" to="/">
        <span class="brand-mark">H</span>
        <span>
          <strong>Hermes</strong>
          <small>Control Center</small>
        </span>
      </NuxtLink>

      <nav class="nav-list">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          class="nav-link"
          :class="{ active: route.path === item.to }"
          :to="item.to"
        >
          <span>{{ item.icon }}</span>
          {{ item.label }}
        </NuxtLink>
      </nav>
    </aside>

    <main class="main-panel">
      <NuxtPage />
    </main>

    <nav class="bottom-nav" aria-label="Mobile navigation">
      <NuxtLink
        v-for="item in navItems.slice(0, 5)"
        :key="item.to"
        class="bottom-nav-link"
        :class="{ active: route.path === item.to }"
        :to="item.to"
      >
        <span>{{ item.icon }}</span>
        <small>{{ item.label }}</small>
      </NuxtLink>
    </nav>
  </div>
</template>
