<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()
const apiBase = runtimeConfig.public.apiBase as string

interface ApprovalSummary {
  id: string
  status: string
  message: string
}

const { data: approvals } = await useAsyncData<ApprovalSummary[]>('approvals-list', () => $fetch(`${apiBase}/approvals`), { default: () => [] })
</script>

<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Approvals</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Review the full request.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          This page is wired to the control API. Live Hermes approval bridging is still pending, so it currently shows bridge status instead of real approve/deny actions.
        </p>
      </div>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article class="col-span-8 rounded-[1.35rem] border border-amber-300/20 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <div v-for="approval in approvals" :key="approval.id" class="rounded-2xl border border-white/10 bg-white/[0.035] p-4">
          <p class="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-amber-200">{{ approval.status }}</p>
          <h2 class="mb-3 text-base font-bold">{{ approval.id }}</h2>
          <p class="whitespace-pre-wrap break-words leading-relaxed text-zinc-200">{{ approval.message }}</p>
        </div>
      </article>

      <aside class="col-span-4 rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <h2 class="mb-2 text-base font-bold">Safety rule</h2>
        <p class="leading-relaxed text-zinc-400">
          Notification previews can be compact, but the approval surface itself must expose the entire request and all decision-critical context before any approve button is reachable.
        </p>
        <ul class="mt-4 grid gap-3 text-sm text-zinc-300">
          <li class="rounded-2xl border border-white/10 bg-white/[0.035] p-3">Full outbound message text</li>
          <li class="rounded-2xl border border-white/10 bg-white/[0.035] p-3">Full command plus working directory</li>
          <li class="rounded-2xl border border-white/10 bg-white/[0.035] p-3">Full file path and diff preview</li>
          <li class="rounded-2xl border border-white/10 bg-white/[0.035] p-3">Calendar/event payload before save</li>
        </ul>
      </aside>
    </div>
  </section>
</template>
