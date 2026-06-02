<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Sessions</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Conversation history.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Browse recent Hermes sessions, active runs, and session details once the API adapter is wired. Approval requests should appear inline in the relevant session timeline.
        </p>
      </div>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article class="col-span-7 rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <h2 class="mb-2 text-base font-bold">Coming next</h2>
        <p class="leading-relaxed text-zinc-400">Session list, search, active session status, and transcript viewer.</p>
      </article>

      <article class="col-span-5 rounded-[1.35rem] border border-amber-300/20 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <p class="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-amber-200">Inline approvals</p>
        <h2 class="mb-2 text-base font-bold">Approvals belong in context</h2>
        <p class="leading-relaxed text-zinc-400">
          When a session blocks on approval, the timeline card should show the full request text, command, or diff without cutting it off, then offer approve/deny/edit actions.
        </p>
      </article>
    </div>
  </section>
</template>
