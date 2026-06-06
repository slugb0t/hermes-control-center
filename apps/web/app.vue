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
const isSidebarCollapsed = useState('sidebar-collapsed', () => false)
const isMobileNavOpen = useState('mobile-nav-open', () => false)
const layoutClass = computed(() => {
  if (isAuthRoute.value) return ''
  return isSidebarCollapsed.value ? 'md:grid md:grid-cols-[5.75rem_minmax(0,1fr)]' : 'md:grid md:grid-cols-[17rem_minmax(0,1fr)]'
})
const desktopLinkBase = computed(() => [
  navLinkBase,
  isSidebarCollapsed.value && 'justify-center px-2.5'
])

watch(() => route.path, () => {
  isMobileNavOpen.value = false
})
</script>

<template>
  <div :class="['min-h-screen overflow-x-hidden', layoutClass, !isAuthRoute && 'max-md:pb-[calc(7rem+env(safe-area-inset-bottom))]']">
    <aside
      v-if="!isAuthRoute"
      :class="[
        'sticky top-0 hidden h-dvh overflow-hidden border-r border-white/10 bg-[#050507]/70 p-5 backdrop-blur-2xl md:block',
        isSidebarCollapsed && 'p-3'
      ]"
      aria-label="Primary navigation"
    >
      <div :class="['mb-6 flex items-center justify-between gap-2', isSidebarCollapsed && 'flex-col']">
        <NuxtLink :class="['flex min-w-0 items-center gap-3', isSidebarCollapsed && 'justify-center']" to="/" :title="isSidebarCollapsed ? 'Hermes Control Center' : undefined">
        <span class="grid size-10 place-items-center rounded-2xl bg-linear-to-br from-violet-500 to-cyan-400 font-extrabold text-white">H</span>
        <span v-if="!isSidebarCollapsed">
          <strong>Hermes</strong>
          <small class="block text-xs text-zinc-400">Control Center</small>
        </span>
        </NuxtLink>
        <button
          class="grid size-9 shrink-0 place-items-center rounded-xl border border-white/10 bg-white/[0.035] text-zinc-400 transition hover:text-zinc-50"
          type="button"
          :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          @click="isSidebarCollapsed = !isSidebarCollapsed"
        >
          {{ isSidebarCollapsed ? '›' : '‹' }}
        </button>
      </div>

      <nav class="grid gap-1.5">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :class="[desktopLinkBase, route.path === item.to && navLinkActive]"
          :to="item.to"
          :title="isSidebarCollapsed ? item.label : undefined"
        >
          <span>{{ item.icon }}</span>
          <span v-if="!isSidebarCollapsed">{{ item.label }}</span>
        </NuxtLink>
      </nav>
    </aside>

    <main :class="['min-w-0', isAuthRoute ? '' : 'p-5 max-md:px-4 max-md:pb-[calc(7rem+env(safe-area-inset-bottom))] max-md:pt-[max(1rem,env(safe-area-inset-top))]']">
      <NuxtPage />
    </main>

    <button
      v-if="!isAuthRoute"
      type="button"
      class="fixed bottom-[calc(0.75rem+env(safe-area-inset-bottom))] right-3 z-30 grid size-12 place-items-center rounded-2xl border border-white/10 bg-zinc-950/92 text-lg text-zinc-200 shadow-[0_18px_80px_rgba(0,0,0,0.55)] backdrop-blur-2xl md:hidden"
      :aria-expanded="isMobileNavOpen"
      aria-controls="mobile-navigation"
      :aria-label="isMobileNavOpen ? 'Hide mobile navigation' : 'Show mobile navigation'"
      @click="isMobileNavOpen = !isMobileNavOpen"
    >
      {{ isMobileNavOpen ? '×' : '☰' }}
    </button>

    <nav
      v-if="!isAuthRoute"
      id="mobile-navigation"
      :class="[
        'fixed inset-x-3 bottom-[calc(4.25rem+env(safe-area-inset-bottom))] z-20 hidden grid-cols-5 gap-1 rounded-[1.4rem] border border-white/10 bg-zinc-950/90 p-2 shadow-[0_18px_80px_rgba(0,0,0,0.5)] backdrop-blur-2xl supports-[padding:max(0px)]:bottom-[max(4.25rem,env(safe-area-inset-bottom))]',
        isMobileNavOpen ? 'max-md:grid' : 'max-md:hidden'
      ]"
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
