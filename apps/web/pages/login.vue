<script setup lang="ts">
definePageMeta({
  layout: false
})

const route = useRoute()
const { loggedIn, fetch } = useUserSession()

const username = ref('slugb0t')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

watchEffect(() => {
  if (loggedIn.value) {
    navigateTo(typeof route.query.redirect === 'string' ? route.query.redirect : '/')
  }
})

const submit = async () => {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: {
        username: username.value,
        password: password.value
      }
    })

    await fetch()
    await navigateTo(typeof route.query.redirect === 'string' ? route.query.redirect : '/')
  } catch {
    errorMessage.value = 'Invalid username or password.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="grid min-h-screen place-items-center bg-[#050507] px-4 py-10 text-zinc-50">
    <form
      class="w-full max-w-sm rounded-[2rem] border border-white/10 bg-white/[0.04] p-6 shadow-[0_24px_120px_rgba(0,0,0,0.55)] backdrop-blur-2xl"
      @submit.prevent="submit"
    >
      <div class="mb-6 text-center">
        <div class="mx-auto mb-4 grid size-14 place-items-center rounded-2xl bg-linear-to-br from-violet-500 to-cyan-400 text-xl font-extrabold text-white">H</div>
        <h1 class="text-2xl font-black tracking-tight">Hermes Control Center</h1>
        <p class="mt-2 text-sm text-zinc-400">Sign in to your private dashboard.</p>
      </div>

      <label class="mb-4 block">
        <span class="mb-1.5 block text-sm font-semibold text-zinc-300">Username</span>
        <input
          v-model="username"
          class="w-full rounded-2xl border border-white/10 bg-zinc-950 px-4 py-3 text-zinc-50 outline-none transition focus:border-violet-400"
          autocomplete="username"
          name="username"
          required
          type="text"
        >
      </label>

      <label class="mb-4 block">
        <span class="mb-1.5 block text-sm font-semibold text-zinc-300">Password</span>
        <input
          v-model="password"
          class="w-full rounded-2xl border border-white/10 bg-zinc-950 px-4 py-3 text-zinc-50 outline-none transition focus:border-violet-400"
          autocomplete="current-password"
          autofocus
          name="password"
          required
          type="password"
        >
      </label>

      <p v-if="errorMessage" class="mb-4 rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ errorMessage }}
      </p>

      <button
        class="w-full rounded-2xl bg-violet-500 px-4 py-3 font-bold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="isSubmitting"
        type="submit"
      >
        {{ isSubmitting ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
  </main>
</template>
