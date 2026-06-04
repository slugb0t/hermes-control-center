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
  content_truncated?: boolean
  tool_calls?: string | null
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
const expandedMessages = ref<Set<number>>(new Set())
const previewLength = 1200
const hasExpandableContent = (message: MessageSummary) => message.content_truncated || message.content.length > previewLength
const isExpanded = (message: MessageSummary) => expandedMessages.value.has(message.id)
const visibleContent = (message: MessageSummary) => {
  if (!hasExpandableContent(message) || isExpanded(message)) return message.content
  return `${message.content.slice(0, previewLength).trimEnd()}…`
}
const toggleMessage = (message: MessageSummary) => {
  const next = new Set(expandedMessages.value)
  if (next.has(message.id)) next.delete(message.id)
  else next.add(message.id)
  expandedMessages.value = next
}
const tryFormatStructuredContent = (content: string) => {
  const trimmed = content.trim()
  if (!trimmed || !['{', '['].includes(trimmed[0] || '')) return content
  try {
    return JSON.stringify(JSON.parse(trimmed), null, 2)
  } catch {
    return content
  }
}
const isStructuredContent = (message: MessageSummary) => message.role === 'tool' || /^[\s]*[\[{]/.test(message.content)
const formattedContent = (message: MessageSummary) => tryFormatStructuredContent(visibleContent(message))
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
        <div class="space-y-3">
          <pre
            v-if="message.content && isStructuredContent(message)"
            class="overflow-x-auto rounded-2xl border border-white/10 bg-black/35 p-3 font-mono text-[0.72rem] leading-5 text-zinc-200 [overflow-wrap:normal] [white-space:pre-wrap] max-sm:text-[0.68rem]"
          ><code>{{ formattedContent(message) }}</code></pre>
          <p v-else-if="message.content" class="whitespace-pre-wrap break-words text-sm leading-relaxed text-zinc-200 max-sm:text-[0.82rem] max-sm:leading-6">{{ visibleContent(message) }}</p>
          <p v-else class="rounded-2xl border border-white/10 bg-white/[0.025] px-3 py-2 text-sm italic text-zinc-500">No visible assistant text was recorded for this message.</p>
          <button
            v-if="hasExpandableContent(message)"
            type="button"
            class="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-bold text-zinc-200 transition hover:border-cyan-300/30 hover:text-cyan-100"
            @click="toggleMessage(message)"
          >
            {{ isExpanded(message) ? 'Show less' : 'Show full message' }}
          </button>
        </div>
      </article>
    </div>
  </section>
</template>
