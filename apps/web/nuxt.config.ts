export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  modules: ['@nuxtjs/google-fonts'],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'Hermes Control Center',
      meta: [
        { name: 'description', content: 'Mobile-friendly Mission Control dashboard for Hermes Agent.' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, viewport-fit=cover' },
        { name: 'theme-color', content: '#09090b' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
        { name: 'apple-mobile-web-app-title', content: 'Hermes' }
      ],
      link: [
        { rel: 'manifest', href: '/manifest.webmanifest' },
        { rel: 'icon', type: 'image/svg+xml', href: '/icon.svg' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.svg' }
      ]
    }
  },
  googleFonts: {
    families: {
      Inter: [400, 500, 600, 700]
    },
    display: 'swap'
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8787'
    }
  },
  typescript: {
    strict: true
  }
})
