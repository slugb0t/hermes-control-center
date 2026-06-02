<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Knowledge Base</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Syncthing notes.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Browse and edit Markdown in kb-private and kb-shared through allowlisted API roots.
        </p>
      </div>
    </header>

    <div class="grid grid-cols-12 gap-4 max-md:grid-cols-1">
      <article class="col-span-6 rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <h2 class="mb-2 text-base font-bold">kb-private</h2>
        <p class="leading-relaxed text-zinc-400">Private notes and work documents. Editing will be audit-logged.</p>
      </article>
      <article class="col-span-6 rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl max-md:col-span-1">
        <h2 class="mb-2 text-base font-bold">kb-shared</h2>
        <p class="leading-relaxed text-zinc-400">Shared knowledge base folder. File actions will stay path-constrained.</p>
      </article>
    </div>
  </section>
</template>
