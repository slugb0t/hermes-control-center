<script setup lang="ts">
const route = useRoute()

const navItems = [
  { label: 'Home', to: '/', icon: '⌂' },
  { label: 'Sessions', to: '/sessions', icon: '✦' },
  { label: 'Approvals', to: '/approvals', icon: '✓' },
  { label: 'KB', to: '/kb', icon: '◇' },
  { label: 'Calendar', to: '/calendar', icon: '◷' },
  { label: 'Settings', to: '/settings', icon: '⚙' }
]

const navLinkBase = 'flex items-center gap-2.5 rounded-[0.9rem] px-3.5 py-3 text-zinc-400 transition hover:bg-violet-500/15 hover:text-zinc-50'
const navLinkActive = 'bg-violet-500/15 text-zinc-50'
const bottomLinkBase = 'grid min-h-14 place-items-center gap-0.5 rounded-2xl text-lg text-zinc-400 transition'
const bottomLinkActive = 'bg-violet-500/15 text-zinc-50'
const isAuthRoute = computed(() => route.path === '/login')
</script>

<template>
  <div :class="['min-h-screen overflow-x-hidden', !isAuthRoute && 'md:grid md:grid-cols-[17rem_minmax(0,1fr)] max-md:pb-[calc(7rem+env(safe-area-inset-bottom))]']">
    <aside
      v-if="!isAuthRoute"
      class="sticky top-0 hidden h-screen border-r border-white/10 bg-[#050507]/70 p-5 backdrop-blur-2xl md:block"
      aria-label="Primary navigation"
    >
      <NuxtLink class="mb-6 flex items-center gap-3" to="/">
        <span class="grid size-10 place-items-center rounded-2xl bg-linear-to-br from-violet-500 to-cyan-400 font-extrabold text-white">H</span>
        <span>
          <strong>Hermes</strong>
          <small class="block text-xs text-zinc-400">Control Center</small>
        </span>
      </NuxtLink>

      <nav class="grid gap-1.5">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :class="[navLinkBase, route.path === item.to && navLinkActive]"
          :to="item.to"
        >
          <span>{{ item.icon }}</span>
          {{ item.label }}
        </NuxtLink>
      </nav>
    </aside>

    <main :class="['min-w-0', isAuthRoute ? '' : 'p-5 max-md:px-4 max-md:pb-[calc(7rem+env(safe-area-inset-bottom))] max-md:pt-[max(1rem,env(safe-area-inset-top))]']">
      <NuxtPage />
    </main>

    <nav
      v-if="!isAuthRoute"
      class="fixed inset-x-3 bottom-[calc(0.75rem+env(safe-area-inset-bottom))] z-20 hidden grid-cols-5 gap-1 rounded-[1.4rem] border border-white/10 bg-zinc-950/90 p-2 shadow-[0_18px_80px_rgba(0,0,0,0.5)] backdrop-blur-2xl supports-[padding:max(0px)]:bottom-[max(0.75rem,env(safe-area-inset-bottom))] max-md:grid"
      aria-label="Mobile navigation"
    >
      <NuxtLink
        v-for="item in navItems.slice(0, 5)"
        :key="item.to"
        :class="[bottomLinkBase, route.path === item.to && bottomLinkActive]"
        :to="item.to"
      >
        <span>{{ item.icon }}</span>
        <small class="text-[0.65rem]">{{ item.label }}</small>
      </NuxtLink>
    </nav>
  </div>
</template>
