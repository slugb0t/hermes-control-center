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

const cardClass = 'rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl'
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
          A lightweight, mobile-friendly command center for watching sessions, approving actions,
          editing your KB, and keeping your calendar in flow.
        </p>
      </div>
      <span class="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1.5 text-sm font-bold text-emerald-200">
        <span class="size-2 rounded-full bg-emerald-400 shadow-[0_0_18px_#34d399]" /> UI online
      </span>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article v-for="card in cards" :key="card.label" :class="[cardClass, 'col-span-4 max-md:col-span-1']">
        <div class="flex items-baseline justify-between gap-4">
          <span>{{ card.label }}</span>
          <strong class="text-3xl">{{ card.value }}</strong>
        </div>
        <p class="mt-2 leading-relaxed text-zinc-400">{{ card.hint }}</p>
      </article>

      <article :class="[cardClass, 'col-span-8 max-md:col-span-1']">
        <h2 class="mb-4 text-base font-bold">Live activity</h2>
        <ul class="grid gap-3">
          <li v-for="item in activity" :key="item.title" class="flex justify-between gap-3 rounded-2xl border border-white/10 bg-white/[0.035] p-3.5">
            <div>
              <strong>{{ item.title }}</strong>
              <p class="mt-1 leading-relaxed text-zinc-400">{{ item.detail }}</p>
            </div>
            <small class="text-zinc-400">{{ item.time }}</small>
          </li>
        </ul>
      </article>

      <article :class="[cardClass, 'col-span-4 max-md:col-span-1']">
        <h2 class="mb-2 text-base font-bold">Quick actions</h2>
        <p class="leading-relaxed text-zinc-400">These become real controls after the Hermes Control API is connected.</p>
        <div class="mt-4 flex flex-wrap gap-2.5">
          <NuxtLink class="rounded-2xl bg-linear-to-br from-violet-500 to-indigo-500 px-3.5 py-3 font-bold text-white" to="/approvals">
            Review approvals
          </NuxtLink>
          <NuxtLink class="rounded-2xl border border-white/10 bg-zinc-800/95 px-3.5 py-3 font-bold" to="/kb">
            Open KB
          </NuxtLink>
        </div>
      </article>

      <article :class="[cardClass, 'col-span-12 max-md:col-span-1']">
        <h2 class="mb-2 text-base font-bold">API target</h2>
        <p class="leading-relaxed text-zinc-400"><code>{{ runtimeConfig.public.apiBase }}</code></p>
      </article>
    </div>
  </section>
</template>
