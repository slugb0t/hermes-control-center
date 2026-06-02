<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()

const cards = [
  { label: 'Active sessions', value: '—', hint: 'Waiting for Hermes session adapter' },
  { label: 'Pending approvals', value: '—', hint: 'Approval bridge coming next' },
  { label: 'KB roots', value: '2', hint: 'kb-private and kb-shared' }
]

const activity = [
  { title: 'Control Center scaffold initialized', time: 'now', detail: 'Nuxt SPA/PWA shell is ready.' },
  { title: 'Hermes integration planned', time: 'next', detail: 'Wire API to Hermes sessions, tools, approvals, and logs.' },
  { title: 'Mobile home-screen ready', time: 'next', detail: 'PWA metadata included for iPhone Safari.' }
]
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <p class="eyebrow">Mission Control</p>
        <h1>Hermes, from anywhere.</h1>
        <p>
          A lightweight, mobile-friendly command center for watching sessions, approving actions,
          editing your KB, and keeping your calendar in flow.
        </p>
      </div>
      <span class="status-pill"><span class="status-dot" /> UI online</span>
    </header>

    <div class="grid">
      <article v-for="card in cards" :key="card.label" class="card span-4">
        <div class="metric">
          <span>{{ card.label }}</span>
          <strong>{{ card.value }}</strong>
        </div>
        <p>{{ card.hint }}</p>
      </article>

      <article class="card span-8">
        <h2>Live activity</h2>
        <ul class="activity-list">
          <li v-for="item in activity" :key="item.title" class="activity-item">
            <div>
              <strong>{{ item.title }}</strong>
              <p>{{ item.detail }}</p>
            </div>
            <small>{{ item.time }}</small>
          </li>
        </ul>
      </article>

      <article class="card span-4">
        <h2>Quick actions</h2>
        <p>These become real controls after the Hermes Control API is connected.</p>
        <div class="button-row">
          <NuxtLink class="button primary" to="/approvals">Review approvals</NuxtLink>
          <NuxtLink class="button" to="/kb">Open KB</NuxtLink>
        </div>
      </article>

      <article class="card span-12">
        <h2>API target</h2>
        <p><code>{{ runtimeConfig.public.apiBase }}</code></p>
      </article>
    </div>
  </section>
</template>
