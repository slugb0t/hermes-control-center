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
  status: 'idle' | 'running' | 'waiting' | 'failed' | string
  started_at: string | null
  last_activity_at: string | null
  message_count: number
  tool_call_count: number
  preview: string
  messages: MessageSummary[]
}

interface MarkdownSegment {
  type: 'text' | 'code'
  text: string
  html?: string
  language?: string
}

interface ToolCallPreview {
  name: string
  arguments: string
}

interface CodeBlockPreview {
  label: string
  language: string
  text: string
}

const { data: session, pending, error, refresh } = await useAsyncData<SessionDetail>(`session-${sessionId}`, () => $fetch(`${apiBase}/sessions/${sessionId}?message_limit=80`))
const formatTime = (value: string | null | undefined) => value ? new Date(value).toLocaleString() : 'unknown'
const shortSessionId = computed(() => session.value?.id ? `${session.value.id.slice(0, 8)}…` : '—')
const expandedMessages = ref<Set<number>>(new Set())
const expandedTools = ref<Set<number>>(new Set())
const roleFilter = ref<'all' | 'user' | 'assistant' | 'tool'>('all')
const copiedKey = ref<string | null>(null)
const latestAnchor = ref<HTMLElement | null>(null)
const isSidebarCollapsed = useState('sidebar-collapsed', () => false)
const previewLength = 1600

const messages = computed(() => session.value?.messages || [])
const filteredMessages = computed(() => {
  if (roleFilter.value === 'all') return messages.value
  return messages.value.filter((message) => message.role === roleFilter.value)
})
const availableRoles = computed(() => {
  const roles = new Set(messages.value.map((message) => message.role))
  return [
    { value: 'all', label: 'All', count: messages.value.length },
    { value: 'user', label: 'User', count: messages.value.filter((message) => message.role === 'user').length, hidden: !roles.has('user') },
    { value: 'assistant', label: 'Assistant', count: messages.value.filter((message) => message.role === 'assistant').length, hidden: !roles.has('assistant') },
    { value: 'tool', label: 'Tools', count: messages.value.filter((message) => message.role === 'tool').length, hidden: !roles.has('tool') },
  ].filter((item) => !item.hidden)
})
const latestMessage = computed(() => messages.value.at(-1))
const statusMeta = computed(() => getSessionStatusMeta(session.value?.status))
const statusLabel = computed(() => statusMeta.value.label)
const statusClass = computed(() => statusMeta.value.badgeClass)
const statusDotClass = computed(() => statusMeta.value.dotClass)

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
const isToolExpanded = (message: MessageSummary) => expandedTools.value.has(message.id)
const toggleTool = (message: MessageSummary) => {
  const next = new Set(expandedTools.value)
  if (next.has(message.id)) next.delete(message.id)
  else next.add(message.id)
  expandedTools.value = next
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
const escapeHtml = (content: string) => content
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/\"/g, '&quot;')

const renderInlineMarkdown = (content: string) => escapeHtml(content)
  .replace(/`([^`]+)`/g, '<code class="rounded-md border border-white/10 bg-black/35 px-1.5 py-0.5 font-mono text-[0.86em] text-cyan-100">$1</code>')
  .replace(/\*\*([^*]+)\*\*/g, '<strong class="font-bold text-zinc-50">$1</strong>')
  .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a class="text-cyan-200 underline decoration-cyan-200/30 underline-offset-4 hover:text-cyan-100" href="$2" target="_blank" rel="noreferrer">$1</a>')

const renderMarkdown = (content: string) => {
  const lines = content.split('\n')
  const html: string[] = []
  let listItems: string[] = []
  let paragraph: string[] = []

  const flushParagraph = () => {
    if (!paragraph.length) return
    html.push(`<p>${renderInlineMarkdown(paragraph.join(' '))}</p>`)
    paragraph = []
  }
  const flushList = () => {
    if (!listItems.length) return
    html.push(`<ul>${listItems.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join('')}</ul>`)
    listItems = []
  }

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      flushParagraph()
      flushList()
      continue
    }
    const heading = /^(#{1,3})\s+(.+)$/.exec(trimmed)
    if (heading) {
      flushParagraph()
      flushList()
      const level = heading[1].length
      html.push(`<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`)
      continue
    }
    const bullet = /^[-*]\s+(.+)$/.exec(trimmed)
    if (bullet) {
      flushParagraph()
      listItems.push(bullet[1])
      continue
    }
    flushList()
    paragraph.push(trimmed)
  }
  flushParagraph()
  flushList()
  return html.join('')
}

const markdownSegments = (message: MessageSummary): MarkdownSegment[] => {
  const content = visibleContent(message)
  if (!content) return []
  if (isStructuredContent(message)) return [{ type: 'code', text: formattedContent(message), language: message.tool_name || 'json' }]
  const segments: MarkdownSegment[] = []
  const fencePattern = /```([^\n`]*)\n([\s\S]*?)```/g
  let cursor = 0
  for (const match of content.matchAll(fencePattern)) {
    const index = match.index || 0
    if (index > cursor) {
      const text = content.slice(cursor, index).trim()
      segments.push({ type: 'text', text, html: renderMarkdown(text) })
    }
    segments.push({ type: 'code', language: match[1]?.trim() || 'text', text: match[2]?.trimEnd() || '' })
    cursor = index + match[0].length
  }
  if (cursor < content.length) {
    const text = content.slice(cursor).trim()
    segments.push({ type: 'text', text, html: renderMarkdown(text) })
  }
  return segments.filter((segment) => segment.text)
}

const parseToolCalls = (message: MessageSummary): ToolCallPreview[] => {
  if (!message.tool_calls) return []
  try {
    const parsed = JSON.parse(message.tool_calls)
    const calls = Array.isArray(parsed) ? parsed : [parsed]
    return calls.map((call) => {
      const fn = call?.function || {}
      const name = fn.name || call?.name || call?.type || message.tool_name || 'tool'
      const args = fn.arguments || call?.arguments || ''
      return { name, arguments: tryFormatStructuredContent(String(args)) }
    })
  } catch {
    return [{ name: message.tool_name || 'tool', arguments: message.tool_calls }]
  }
}
const toolCallsByMessageId = computed(() => new Map(messages.value.map((message) => [message.id, parseToolCalls(message)])))
const toolCallsFor = (message: MessageSummary) => toolCallsByMessageId.value.get(message.id) || []
const tryParseObject = (value: string): Record<string, unknown> | null => {
  try {
    const parsed = JSON.parse(value)
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed as Record<string, unknown> : null
  } catch {
    return null
  }
}
const codeBlocksForToolCall = (call: ToolCallPreview): CodeBlockPreview[] => {
  const args = tryParseObject(call.arguments)
  if (!args) return [{ label: 'arguments', language: 'json', text: call.arguments || 'No arguments recorded.' }]

  if (call.name === 'terminal' || 'command' in args) {
    const blocks: CodeBlockPreview[] = []
    if (args.command) blocks.push({ label: 'command', language: 'bash', text: String(args.command) })
    const options = Object.fromEntries(Object.entries(args).filter(([key]) => key !== 'command'))
    if (Object.keys(options).length) blocks.push({ label: 'options', language: 'json', text: JSON.stringify(options, null, 2) })
    return blocks.length ? blocks : [{ label: 'arguments', language: 'json', text: JSON.stringify(args, null, 2) }]
  }

  return [{ label: 'arguments', language: 'json', text: JSON.stringify(args, null, 2) }]
}
const hasVisibleBody = (message: MessageSummary) => Boolean(message.content && !message.tool_calls)
const roleClass = (role: string) => {
  if (role === 'user') return 'border-cyan-300/20 bg-cyan-300/10 text-cyan-100'
  if (role === 'tool') return 'border-amber-300/20 bg-amber-300/10 text-amber-100'
  return 'border-violet-300/20 bg-violet-300/10 text-violet-100'
}
const messageShellClass = (role: string) => {
  if (role === 'user') return 'border-cyan-300/10 bg-cyan-950/20'
  if (role === 'tool') return 'border-amber-300/10 bg-amber-950/15'
  return 'border-white/10 bg-zinc-900/80'
}
const copyText = async (key: string, text: string) => {
  if (!text || !import.meta.client || !navigator.clipboard?.writeText) return
  try {
    await navigator.clipboard.writeText(text)
    copiedKey.value = key
    window.setTimeout(() => {
      if (copiedKey.value === key) copiedKey.value = null
    }, 1600)
  } catch {
    // Clipboard writes can fail on HTTP origins, older browsers, or denied permissions.
  }
}
const jumpToLatest = () => latestAnchor.value?.scrollIntoView({ behavior: 'smooth', block: 'end' })
const composerSidebarClass = computed(() => isSidebarCollapsed.value ? 'md:left-[5.75rem]' : 'md:left-[17rem]')
</script>

<template>
  <section class="w-full pb-36 max-md:pb-64 max-sm:pb-72">
    <header class="mb-4 flex min-w-0 items-start justify-between gap-4 max-md:block">
      <div class="min-w-0">
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300 max-sm:text-[0.7rem]">Session workspace</p>
        <h1 class="mb-3 max-w-5xl text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.98] tracking-[-0.06em] text-balance max-sm:text-[clamp(1.65rem,9vw,2.55rem)] max-sm:tracking-[-0.045em]">
          {{ session?.title || 'Loading session…' }}
        </h1>
        <div class="flex max-w-4xl flex-wrap gap-2 text-xs text-zinc-400 sm:text-sm">
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ shortSessionId }}</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.source || 'unknown source' }}</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.message_count ?? '—' }} messages</span>
          <span class="rounded-full border border-white/10 bg-white/[0.035] px-2.5 py-1">{{ session?.tool_call_count ?? '—' }} tools</span>
          <span class="inline-flex items-center gap-2 rounded-full border px-2.5 py-1 font-bold" :class="statusClass">
            <span class="size-1.5 rounded-full" :class="statusDotClass" />
            {{ statusLabel }}
          </span>
        </div>
      </div>
      <div class="mt-1 flex shrink-0 gap-2 max-md:mt-4 max-sm:grid max-sm:grid-cols-2">
        <button class="inline-flex rounded-2xl border border-white/10 bg-zinc-800/95 px-3.5 py-3 font-bold max-sm:justify-center max-sm:py-2.5 max-sm:text-sm" type="button" @click="refresh()">
          Refresh
        </button>
        <NuxtLink class="inline-flex rounded-2xl border border-white/10 bg-zinc-800/95 px-3.5 py-3 font-bold max-sm:justify-center max-sm:py-2.5 max-sm:text-sm" to="/sessions">
          Back
        </NuxtLink>
      </div>
    </header>

    <section class="sticky top-3 z-10 mb-4 rounded-[1.2rem] border border-white/10 bg-zinc-950/80 p-3 shadow-[0_18px_80px_rgba(0,0,0,0.26)] backdrop-blur-2xl max-sm:static">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="item in availableRoles"
            :key="item.value"
            type="button"
            :class="[
              'rounded-full border px-3 py-1.5 text-xs font-bold transition',
              roleFilter === item.value ? 'border-cyan-300/40 bg-cyan-300/10 text-cyan-100' : 'border-white/10 bg-white/[0.035] text-zinc-400 hover:text-zinc-100'
            ]"
            @click="roleFilter = item.value as typeof roleFilter"
          >
            {{ item.label }} · {{ item.count }}
          </button>
        </div>
        <button class="rounded-full border border-white/10 bg-white/[0.035] px-3 py-1.5 text-xs font-bold text-zinc-300 transition hover:text-cyan-100" type="button" @click="jumpToLatest">
          Jump to latest
        </button>
      </div>
    </section>

    <div v-if="pending" class="rounded-[1.35rem] border border-white/10 bg-zinc-900/70 p-6 text-zinc-400">
      Loading session messages…
    </div>
    <div v-else-if="error" class="rounded-[1.35rem] border border-rose-300/20 bg-rose-950/20 p-6 text-rose-100">
      Could not load this session. Try refreshing or go back to the sessions list.
    </div>
    <div v-else-if="!filteredMessages.length" class="rounded-[1.35rem] border border-white/10 bg-zinc-900/70 p-6 text-zinc-400">
      No messages match this filter yet.
    </div>

    <div v-else class="grid gap-4">
      <article
        v-for="message in filteredMessages"
        :key="message.id"
        class="group min-w-0 overflow-hidden rounded-[1.35rem] border p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-sm:rounded-[1.1rem] max-sm:p-3"
        :class="messageShellClass(message.role)"
      >
        <div class="mb-3 flex items-center justify-between gap-3 max-sm:block">
          <div class="flex min-w-0 flex-wrap items-center gap-2">
            <span class="inline-flex rounded-full border px-3 py-1 text-xs font-bold uppercase tracking-[0.12em]" :class="roleClass(message.role)">
              {{ message.tool_name || message.role }}
            </span>
            <span v-if="message.tool_calls" class="rounded-full border border-amber-300/20 bg-amber-300/10 px-2.5 py-1 text-xs font-bold text-amber-100">
              tool request
            </span>
          </div>
          <small class="text-zinc-500 max-sm:mt-2 max-sm:block">{{ formatTime(message.timestamp) }}</small>
        </div>

        <div v-if="toolCallsFor(message).length" class="mb-3 rounded-2xl border border-amber-300/15 bg-black/25 p-3">
          <button class="flex w-full items-center justify-between gap-3 text-left text-xs font-bold uppercase tracking-[0.12em] text-amber-100" type="button" @click="toggleTool(message)">
            <span>{{ toolCallsFor(message).length }} tool call{{ toolCallsFor(message).length === 1 ? '' : 's' }}</span>
            <span>{{ isToolExpanded(message) ? 'Collapse' : 'Expand' }}</span>
          </button>
          <div v-if="isToolExpanded(message)" class="mt-3 grid gap-3">
            <div v-for="(call, callIndex) in toolCallsFor(message)" :key="`${message.id}-${callIndex}`" class="rounded-xl border border-white/10 bg-black/25 p-3">
              <div class="mb-2 flex items-center justify-between gap-3">
                <strong class="text-sm text-amber-100">{{ call.name }}</strong>
                <button class="rounded-full border border-white/10 px-2 py-1 text-[0.68rem] font-bold text-zinc-400 hover:text-zinc-100" type="button" @click="copyText(`tool-${message.id}-${callIndex}`, call.arguments)">
                  {{ copiedKey === `tool-${message.id}-${callIndex}` ? 'Copied' : 'Copy args' }}
                </button>
              </div>
              <div class="grid gap-2">
                <div v-for="block in codeBlocksForToolCall(call)" :key="`${message.id}-${callIndex}-${block.label}`" class="overflow-hidden rounded-xl border border-white/10 bg-black/35">
                  <div class="flex items-center justify-between border-b border-white/10 px-3 py-2 text-[0.68rem] font-bold uppercase tracking-[0.12em] text-zinc-500">
                    <span>{{ block.label }} · {{ block.language }}</span>
                    <button class="text-zinc-400 hover:text-cyan-100" type="button" @click="copyText(`tool-${message.id}-${callIndex}-${block.label}`, block.text)">
                      {{ copiedKey === `tool-${message.id}-${callIndex}-${block.label}` ? 'Copied' : 'Copy' }}
                    </button>
                  </div>
                  <pre class="overflow-x-auto p-3 font-mono text-[0.72rem] leading-5 text-zinc-200 [overflow-wrap:normal] [white-space:pre-wrap] max-sm:text-[0.68rem]"><code>{{ block.text }}</code></pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="hasVisibleBody(message)" class="space-y-3">
          <template v-for="(segment, index) in markdownSegments(message)" :key="`${message.id}-${index}`">
            <div v-if="segment.type === 'code'" class="overflow-hidden rounded-2xl border border-white/10 bg-black/35">
              <div class="flex items-center justify-between border-b border-white/10 px-3 py-2 text-[0.68rem] font-bold uppercase tracking-[0.12em] text-zinc-500">
                <span>{{ segment.language || 'code' }}</span>
                <button class="text-zinc-400 hover:text-cyan-100" type="button" @click="copyText(`code-${message.id}-${index}`, segment.text)">
                  {{ copiedKey === `code-${message.id}-${index}` ? 'Copied' : 'Copy' }}
                </button>
              </div>
              <pre class="overflow-x-auto p-3 font-mono text-[0.72rem] leading-5 text-zinc-200 [overflow-wrap:normal] [white-space:pre-wrap] max-sm:text-[0.68rem]"><code>{{ segment.text }}</code></pre>
            </div>
            <div v-else class="message-markdown text-sm leading-relaxed text-zinc-200 max-sm:text-[0.82rem] max-sm:leading-6" v-html="segment.html || renderMarkdown(segment.text)" />
          </template>
          <p v-if="!message.content && !message.tool_calls" class="rounded-2xl border border-white/10 bg-white/[0.025] px-3 py-2 text-sm italic text-zinc-500">No visible text was recorded for this message.</p>
          <div class="flex flex-wrap gap-2">
            <button
              v-if="message.content"
              type="button"
              class="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-bold text-zinc-400 transition hover:border-cyan-300/30 hover:text-cyan-100"
              @click="copyText(`message-${message.id}`, message.content)"
            >
              {{ copiedKey === `message-${message.id}` ? 'Copied' : 'Copy message' }}
            </button>
            <button
              v-if="hasExpandableContent(message)"
              type="button"
              class="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-bold text-zinc-200 transition hover:border-cyan-300/30 hover:text-cyan-100"
              @click="toggleMessage(message)"
            >
              {{ isExpanded(message) ? 'Show less' : 'Show full message' }}
            </button>
          </div>
        </div>
      </article>
      <div ref="latestAnchor" aria-hidden="true" />
    </div>

    <form :class="['fixed inset-x-0 bottom-[calc(6.25rem+env(safe-area-inset-bottom))] z-30 border-t border-white/10 bg-zinc-950/92 px-4 py-3 shadow-[0_-18px_80px_rgba(0,0,0,0.45)] backdrop-blur-2xl md:bottom-0', composerSidebarClass]" @submit.prevent>
      <div class="mx-auto flex max-w-5xl items-end gap-2 max-sm:gap-1.5">
        <label class="sr-only" for="session-composer">Message Hermes</label>
        <textarea
          id="session-composer"
          class="min-h-12 flex-1 resize-none rounded-2xl border border-white/10 bg-black/35 px-4 py-3 text-sm text-zinc-300 outline-none placeholder:text-zinc-600 focus:border-cyan-300/35 max-sm:max-h-28 max-sm:min-h-11"
          disabled
          placeholder="Composer preview — message sending arrives in the next phase"
          rows="1"
        />
        <button class="min-h-12 rounded-2xl border border-white/10 bg-white/[0.04] px-4 text-sm font-bold text-zinc-500 max-sm:px-3" disabled type="submit">
          Send
        </button>
      </div>
      <p class="mx-auto mt-2 max-w-5xl text-xs text-zinc-600 max-sm:text-[0.68rem]">
        Phase 1 preview: timeline, filters, readable tools, and composer shell. Gateway sending comes next.
      </p>
    </form>
  </section>
</template>

<style scoped>
.message-markdown :deep(p) {
  margin-bottom: 0.85rem;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.message-markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.message-markdown :deep(h1),
.message-markdown :deep(h2),
.message-markdown :deep(h3) {
  margin: 1.1rem 0 0.55rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: rgb(244 244 245);
}

.message-markdown :deep(h1:first-child),
.message-markdown :deep(h2:first-child),
.message-markdown :deep(h3:first-child) {
  margin-top: 0;
}

.message-markdown :deep(h1) {
  font-size: 1.35rem;
}

.message-markdown :deep(h2) {
  font-size: 1.12rem;
}

.message-markdown :deep(h3) {
  font-size: 1rem;
}

.message-markdown :deep(ul) {
  margin: 0.5rem 0 0.85rem 1.15rem;
  list-style: disc;
}

.message-markdown :deep(li) {
  margin: 0.25rem 0;
  padding-left: 0.1rem;
}
</style>
