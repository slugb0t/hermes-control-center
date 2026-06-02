<script setup lang="ts">
const pendingApproval = {
  session: 'Dashboard UI Migration',
  kind: 'Outbound message',
  risk: 'Sends a Discord reply on your behalf',
  requestedAt: 'Waiting for review',
  message: `I’m going to migrate the dashboard styling to Tailwind, keep the app mobile-first, preserve the full-width desktop layout, and verify the Nuxt build plus API tests before pushing.

This approval preview intentionally shows the complete text without truncation. Long messages should wrap naturally, preserve paragraph breaks, and remain readable before you approve, deny, or edit the request.`
}
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
          Approval cards must show the complete command, file diff, calendar event, or outbound message so you know exactly what Hermes is asking to do.
        </p>
      </div>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article class="col-span-8 rounded-[1.35rem] border border-amber-300/20 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <div class="mb-4 flex items-start justify-between gap-4 max-sm:block">
          <div>
            <p class="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-amber-200">Pending approval</p>
            <h2 class="text-base font-bold">{{ pendingApproval.kind }}</h2>
            <p class="mt-1 leading-relaxed text-zinc-400">Session: {{ pendingApproval.session }}</p>
          </div>
          <span class="inline-flex rounded-full border border-amber-300/30 bg-amber-300/10 px-3 py-1.5 text-sm font-bold text-amber-100 max-sm:mt-3">
            {{ pendingApproval.requestedAt }}
          </span>
        </div>

        <dl class="mb-4 grid gap-3 rounded-2xl border border-white/10 bg-white/[0.035] p-3.5 sm:grid-cols-2">
          <div>
            <dt class="text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">Risk</dt>
            <dd class="mt-1 text-zinc-200">{{ pendingApproval.risk }}</dd>
          </div>
          <div>
            <dt class="text-xs font-bold uppercase tracking-[0.12em] text-zinc-500">Display rule</dt>
            <dd class="mt-1 text-zinc-200">No truncation, no hidden text, readable wrapping.</dd>
          </div>
        </dl>

        <div>
          <h3 class="mb-2 text-sm font-bold text-zinc-200">Complete message</h3>
          <div class="rounded-2xl border border-white/10 bg-black/30 p-4 text-sm leading-relaxed text-zinc-100 shadow-inner">
            <p class="whitespace-pre-wrap break-words">{{ pendingApproval.message }}</p>
          </div>
        </div>

        <div class="mt-4 flex flex-wrap gap-2.5">
          <button class="rounded-2xl bg-linear-to-br from-emerald-500 to-cyan-500 px-3.5 py-3 font-bold text-white">
            Approve
          </button>
          <button class="rounded-2xl border border-white/10 bg-zinc-800/95 px-3.5 py-3 font-bold">
            Edit before sending
          </button>
          <button class="rounded-2xl border border-rose-300/25 bg-rose-400/10 px-3.5 py-3 font-bold text-rose-100">
            Deny
          </button>
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
