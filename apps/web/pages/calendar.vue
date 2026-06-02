<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Calendar</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Your time, visible.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Read, discuss, create, and edit events through Hermes. Deletes require explicit confirmation.
        </p>
      </div>
    </header>

    <div class="rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl">
      <h2 class="mb-2 text-base font-bold">Agenda-first mobile view</h2>
      <p class="leading-relaxed text-zinc-400">Mobile will prioritize today/upcoming agenda, while desktop can add week and month views.</p>
    </div>
  </section>
</template>
