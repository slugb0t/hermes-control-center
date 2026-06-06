<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()
const apiBase = runtimeConfig.public.apiBase as string

interface SystemStatus {
  hermes_connected: boolean
  live_updates: string
  allowed_roots: string[]
  state_db: string | null
  session_count: number
  active_session_count: number
  latest_activity_at: string | null
}

interface SessionSummary {
  id: string
  title: string
  source: string
  model: string | null
  last_activity_at: string | null
  message_count: number
  tool_call_count: number
  preview: string
}

interface MessageSummary {
  id: number
  session_id: string
  role: string
  tool_name: string | null
  timestamp: string | null
  content: string
}

const { data: status } = await useAsyncData<SystemStatus>('dashboard-status', () => $fetch(`${apiBase}/status`))
const { data: sessions } = await useAsyncData<SessionSummary[]>('dashboard-sessions', () => $fetch(`${apiBase}/sessions?limit=3`), { default: () => [] })
const { data: activity } = await useAsyncData<MessageSummary[]>('dashboard-activity', () => $fetch(`${apiBase}/activity?limit=5`), { default: () => [] })

const cardClass = 'rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl'

const metrics = computed(() => [
  { label: 'Hermes connected', value: status.value?.hermes_connected ? 'Yes' : 'No', hint: status.value?.state_db || 'State database not available' },
  { label: 'Sessions', value: status.value?.session_count?.toString() ?? '—', hint: `${status.value?.active_session_count ?? 0} active/open sessions` },
  { label: 'KB roots', value: status.value?.allowed_roots?.length?.toString() ?? '—', hint: status.value?.allowed_roots?.join(', ') || 'No roots configured' }
])

const formatTime = (value: string | null) => value ? new Date(value).toLocaleString() : 'unknown'
</script>

<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Mission Control</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Hermes, from anywhere.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Live read-only preview of the Hermes VPS state: sessions, recent activity, active counts, and configured KB roots.
        </p>
      </div>
      <span
        class="inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm font-bold"
        :class="status?.hermes_connected ? 'border-emerald-400/30 bg-emerald-400/10 text-emerald-200' : 'border-rose-400/30 bg-rose-400/10 text-rose-200'"
      >
        <span class="size-2 rounded-full" :class="status?.hermes_connected ? 'bg-emerald-400 shadow-[0_0_18px_#34d399]' : 'bg-rose-400'" />
        {{ status?.hermes_connected ? 'Hermes connected' : 'Hermes offline' }}
      </span>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article v-for="card in metrics" :key="card.label" :class="[cardClass, 'col-span-4 max-md:col-span-1']">
        <div class="flex items-baseline justify-between gap-4">
          <span>{{ card.label }}</span>
          <strong class="text-3xl">{{ card.value }}</strong>
        </div>
        <p class="mt-2 break-words leading-relaxed text-zinc-400">{{ card.hint }}</p>
      </article>

      <article :class="[cardClass, 'col-span-7 min-w-0 overflow-hidden max-md:col-span-1']">
        <div class="mb-4 flex items-center justify-between gap-3">
          <h2 class="text-base font-bold">Recent sessions</h2>
          <NuxtLink class="text-sm font-bold text-cyan-300" to="/sessions">View all</NuxtLink>
        </div>
        <ul class="grid gap-3">
          <li v-for="session in sessions" :key="session.id" class="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035] p-3.5">
            <NuxtLink :to="`/sessions/${session.id}`" class="block">
              <div class="flex items-start justify-between gap-3 max-sm:block">
                <strong>{{ session.title }}</strong>
                <small class="text-zinc-400">{{ formatTime(session.last_activity_at) }}</small>
              </div>
              <p class="mt-2 whitespace-pre-wrap break-words text-sm leading-relaxed text-zinc-400 [overflow-wrap:anywhere]">{{ session.preview }}</p>
              <p class="mt-2 text-xs uppercase tracking-[0.12em] text-zinc-500 [overflow-wrap:anywhere]">
                {{ session.source }} · {{ session.message_count }} messages · {{ session.tool_call_count }} tools
              </p>
            </NuxtLink>
          </li>
        </ul>
      </article>

      <article :class="[cardClass, 'col-span-5 min-w-0 overflow-hidden max-md:col-span-1']">
        <h2 class="mb-4 text-base font-bold">Recent activity</h2>
        <ul class="grid gap-3">
          <li v-for="item in activity" :key="item.id" class="min-w-0 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.035] p-3.5">
            <div class="mb-2 flex items-center justify-between gap-3">
              <span class="text-xs font-bold uppercase tracking-[0.12em] text-cyan-300">{{ item.tool_name || item.role }}</span>
              <small class="text-zinc-500">{{ formatTime(item.timestamp) }}</small>
            </div>
            <p class="whitespace-pre-wrap break-words text-sm leading-relaxed text-zinc-300 [overflow-wrap:anywhere]">{{ item.content }}</p>
          </li>
        </ul>
      </article>

      <article :class="[cardClass, 'col-span-12 max-md:col-span-1']">
        <h2 class="mb-2 text-base font-bold">API target</h2>
        <p class="break-words leading-relaxed text-zinc-400"><code>{{ apiBase }}</code></p>
      </article>
    </div>
  </section>
</template>
