<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Sessions</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Conversation history.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Browse recent Hermes sessions, active runs, and session details once the API adapter is wired.
        </p>
      </div>
    </header>

    <div class="rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl">
      <h2 class="mb-2 text-base font-bold">Coming next</h2>
      <p class="leading-relaxed text-zinc-400">Session list, search, active session status, and transcript viewer.</p>
    </div>
  </section>
</template>
