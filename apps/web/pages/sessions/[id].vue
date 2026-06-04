<script setup lang="ts">
const route = useRoute()
const runtimeConfig = useRuntimeConfig()
const apiBase = runtimeConfig.public.apiBase as string
const sessionId = route.params.id as string

interface MessageSummary {
  id: number
  session_id: string
  role: string
  tool_name: string | null
  timestamp: string | null
  content: string
}

interface SessionDetail {
  id: string
  title: string
  source: string
  model: string | null
  started_at: string | null
  last_activity_at: string | null
  message_count: number
  tool_call_count: number
  preview: string
  messages: MessageSummary[]
}

const { data: session } = await useAsyncData<SessionDetail>(`session-${sessionId}`, () => $fetch(`${apiBase}/sessions/${sessionId}?message_limit=40`))
const formatTime = (value: string | null | undefined) => value ? new Date(value).toLocaleString() : 'unknown'
const shortSessionId = computed(() => session.value?.id ? `${session.value.id.slice(0, 8)}…` : '—')
const roleClass = (role: string) => {
  if (role === 'user') return 'border-cyan-300/20 bg-cyan-300/10 text-cyan-100'
  if (role === 'tool') return 'border-amber-300/20 bg-amber-300/10 text-amber-100'
  return 'border-violet-300/20 bg-violet-300/10 text-violet-100'
}
</script>

<template>
  <section class="w-full">
    <header class="mb-4 flex min-w-0 items-start justify-between gap-4 max-md:block">
      <div class="min-w-0">
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300 max-sm:text-[0.7rem]">Session detail</p>
        <h1 class="mb-3 max-w-5xl text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.98] tracking-[-0.06em] text-balance max-sm:text-[clamp(1.65rem,9vw,2.55rem)] max-sm:tracking-[-0.045em]">
          {{ session?.title || 'Loading session…' }}
        </h1>
        <div class="flex max-w-3xl flex-wrap gap-2 text-xs text-zinc-400 sm:text-sm">
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ shortSessionId }}</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.source || 'unknown source' }}</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.message_count ?? '—' }} messages</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.tool_call_count ?? '—' }} tools</span>
        </div>
      </div>
      <NuxtLink class="mt-1 inline-flex shrink-0 rounded-2xl border border-white/10 bg-zinc-800/95 px-3.5 py-3 font-bold max-md:mt-4 max-sm:w-full max-sm:justify-center max-sm:py-2.5 max-sm:text-sm" to="/sessions">
        Back to sessions
      </NuxtLink>
    </header>

    <div class="grid gap-4">
      <article
        v-for="message in session?.messages || []"
        :key="message.id"
        class="min-w-0 overflow-hidden rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-sm:rounded-[1.1rem] max-sm:p-3"
      >
        <div class="mb-3 flex items-center justify-between gap-3 max-sm:block">
          <span class="inline-flex rounded-full border px-3 py-1 text-xs font-bold uppercase tracking-[0.12em]" :class="roleClass(message.role)">
            {{ message.tool_name || message.role }}
          </span>
          <small class="text-zinc-500 max-sm:mt-2 max-sm:block">{{ formatTime(message.timestamp) }}</small>
        </div>
        <p class="max-h-[34rem] overflow-auto whitespace-pre-wrap break-words text-sm leading-relaxed text-zinc-200 max-sm:text-[0.82rem] max-sm:leading-6">{{ message.content }}</p>
      </article>
    </div>
  </section>
</template>
