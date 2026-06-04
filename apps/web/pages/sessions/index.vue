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

interface SessionFilters {
  sources: string[]
  models: string[]
}

const sort = ref('recent')
const source = ref('all')
const model = ref('all')
const tools = ref('all')
const query = ref('')
const limit = ref(50)

const sessionsUrl = computed(() => {
  const params = new URLSearchParams({
    limit: String(limit.value),
    sort: sort.value,
    tools: tools.value,
  })
  if (source.value !== 'all') params.set('source', source.value)
  if (model.value !== 'all') params.set('model', model.value)
  if (query.value.trim()) params.set('query', query.value.trim())
  return `${apiBase}/sessions?${params.toString()}`
})

const { data: sessions, pending, refresh } = await useAsyncData<SessionSummary[]>('sessions-list', () => $fetch(sessionsUrl.value), {
  default: () => [],
  watch: [sessionsUrl],
})
const { data: filters } = await useAsyncData<SessionFilters>('session-filters', () => $fetch(`${apiBase}/sessions/filters`), {
  default: () => ({ sources: [], models: [] }),
})
const formatTime = (value: string | null) => value ? new Date(value).toLocaleString() : 'unknown'
const sourceOptions = computed(() => ['all', ...(filters.value?.sources || [])])
const modelOptions = computed(() => ['all', ...(filters.value?.models || [])])
const resetFilters = () => {
  sort.value = 'recent'
  source.value = 'all'
  model.value = 'all'
  tools.value = 'all'
  query.value = ''
}
</script>

<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div class="min-w-0">
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Sessions</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em] max-sm:text-[clamp(2rem,11vw,3rem)] max-sm:tracking-[-0.055em]">
          Conversation history.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400 max-sm:text-sm">
          Live read-only list from <code>~/.hermes/state.db</code>. Filter by recency, source, model, tools, or search text.
        </p>
      </div>
    </header>

    <section class="mb-5 rounded-[1.35rem] border border-white/10 bg-zinc-950/55 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.2)] backdrop-blur-xl max-sm:rounded-[1.1rem] max-sm:p-3">
      <div class="grid gap-3 md:grid-cols-[1.5fr_1fr_1fr]">
        <label class="block text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
          Search
          <input
            v-model="query"
            class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm normal-case tracking-normal text-zinc-100 outline-none transition placeholder:text-zinc-600 focus:border-cyan-300/40"
            placeholder="Title, id, or message text"
            type="search"
          >
        </label>
        <label class="block text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
          Sort
          <select v-model="sort" class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm normal-case tracking-normal text-zinc-100 outline-none focus:border-cyan-300/40">
            <option value="recent">Most recently active</option>
            <option value="newest">Newest started</option>
            <option value="oldest">Oldest started</option>
            <option value="most-messages">Most messages</option>
            <option value="most-tools">Most tool calls</option>
          </select>
        </label>
        <label class="block text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
          Tools
          <select v-model="tools" class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm normal-case tracking-normal text-zinc-100 outline-none focus:border-cyan-300/40">
            <option value="all">All sessions</option>
            <option value="with-tools">With tools</option>
            <option value="no-tools">No tools</option>
          </select>
        </label>
      </div>
      <div class="mt-3 grid gap-3 md:grid-cols-[1fr_1fr_auto]">
        <label class="block text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
          Source
          <select v-model="source" class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm normal-case tracking-normal text-zinc-100 outline-none focus:border-cyan-300/40">
            <option v-for="option in sourceOptions" :key="option" :value="option">{{ option === 'all' ? 'All sources' : option }}</option>
          </select>
        </label>
        <label class="block text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
          Model
          <select v-model="model" class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-3 py-2.5 text-sm normal-case tracking-normal text-zinc-100 outline-none focus:border-cyan-300/40">
            <option v-for="option in modelOptions" :key="option" :value="option">{{ option === 'all' ? 'All models' : option }}</option>
          </select>
        </label>
        <div class="flex items-end gap-2 max-md:pt-1">
          <button class="rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-bold text-zinc-200 transition hover:border-cyan-300/30 hover:text-cyan-100" type="button" @click="refresh()">
            Refresh
          </button>
          <button class="rounded-2xl border border-white/10 bg-black/20 px-4 py-2.5 text-sm font-bold text-zinc-400 transition hover:text-zinc-100" type="button" @click="resetFilters">
            Reset
          </button>
        </div>
      </div>
    </section>

    <div class="mb-3 flex items-center justify-between text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">
      <span>{{ sessions.length }} sessions</span>
      <span v-if="pending" class="text-cyan-300">Loading…</span>
    </div>

    <div class="grid gap-4">
      <article
        v-for="session in sessions"
        :key="session.id"
        class="min-w-0 rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-sm:rounded-[1.1rem] max-sm:p-3.5"
      >
        <NuxtLink :to="`/sessions/${session.id}`" class="block">
          <div class="flex items-start justify-between gap-4 max-md:block">
            <div class="min-w-0">
              <p class="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">{{ session.source }}</p>
              <h2 class="break-words text-xl font-bold leading-tight max-sm:text-lg">{{ session.title }}</h2>
            </div>
            <div class="shrink-0 text-right text-sm text-zinc-400 max-md:mt-3 max-md:text-left max-sm:text-xs">
              <p>{{ formatTime(session.last_activity_at) }}</p>
              <p>{{ session.model || 'unknown model' }}</p>
            </div>
          </div>
          <p class="mt-3 line-clamp-5 whitespace-pre-wrap break-words leading-relaxed text-zinc-300 max-sm:text-sm">{{ session.preview }}</p>
          <div class="mt-4 flex flex-wrap gap-2 text-sm text-zinc-400">
            <span class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1">{{ session.message_count }} messages</span>
            <span class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1">{{ session.tool_call_count }} tool calls</span>
            <span class="max-w-full truncate rounded-full border border-white/10 bg-white/[0.035] px-3 py-1 max-sm:max-w-44">{{ session.id }}</span>
          </div>
        </NuxtLink>
      </article>
    </div>
  </section>
</template>
