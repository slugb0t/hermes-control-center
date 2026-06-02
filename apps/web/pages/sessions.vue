<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()
const apiBase = runtimeConfig.public.apiBase as string

interface SessionSummary {
  id: string
  title: string
  source: string
  model: string | null
  started_at: string | null
  last_activity_at: string | null
  message_count: number
  tool_call_count: number
  preview: string
}

const { data: sessions } = await useAsyncData<SessionSummary[]>('sessions-list', () => $fetch(`${apiBase}/sessions?limit=30`), { default: () => [] })
const formatTime = (value: string | null) => value ? new Date(value).toLocaleString() : 'unknown'
</script>

<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Sessions</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Conversation history.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Live read-only list from <code>~/.hermes/state.db</code>. Click a session to inspect recent messages and tool activity.
        </p>
      </div>
    </header>

    <div class="grid gap-4">
      <article
        v-for="session in sessions"
        :key="session.id"
        class="rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl"
      >
        <NuxtLink :to="`/sessions/${session.id}`" class="block">
          <div class="flex items-start justify-between gap-4 max-md:block">
            <div>
              <p class="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">{{ session.source }}</p>
              <h2 class="text-xl font-bold">{{ session.title }}</h2>
            </div>
            <div class="text-right text-sm text-zinc-400 max-md:mt-3 max-md:text-left">
              <p>{{ formatTime(session.last_activity_at) }}</p>
              <p>{{ session.model || 'unknown model' }}</p>
            </div>
          </div>
          <p class="mt-3 whitespace-pre-wrap break-words leading-relaxed text-zinc-300">{{ session.preview }}</p>
          <div class="mt-4 flex flex-wrap gap-2 text-sm text-zinc-400">
            <span class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1">{{ session.message_count }} messages</span>
            <span class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1">{{ session.tool_call_count }} tool calls</span>
            <span class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1">{{ session.id }}</span>
          </div>
        </NuxtLink>
      </article>
    </div>
  </section>
</template>
