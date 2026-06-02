<template>
  <section class="w-full">
    <header class="mb-5 flex items-start justify-between gap-4 max-md:block">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-cyan-300">Settings</p>
        <h1 class="mb-2 text-[clamp(2rem,6vw,4.5rem)] font-bold leading-[0.95] tracking-[-0.07em]">
          Control plane.
        </h1>
        <p class="max-w-3xl leading-relaxed text-zinc-400">
          Configure connection status, allowed roots, auth, and deployment details. Secrets remain backend-only.
        </p>
      </div>
    </header>

    <div class="rounded-[1.35rem] border border-white/10 bg-zinc-900/80 p-4 shadow-[0_18px_80px_rgba(0,0,0,0.24)] backdrop-blur-xl">
      <h2 class="mb-2 text-base font-bold">Secure defaults</h2>
      <p class="leading-relaxed text-zinc-400">
        Private network access, HttpOnly cookie auth, CSRF protection, file allowlists, and audit logging are planned before privileged writes.
      </p>
    </div>
  </section>
</template>
