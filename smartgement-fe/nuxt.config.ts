export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  future: {
    compatibilityVersion: 4
  },

  modules: ['@nuxtjs/tailwindcss'], // <--- WAJIB ADA

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      script: [
        {
          src: 'https://www.google.com/recaptcha/api.js',
          async: true,
          defer: true
        }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8080/api',
      aiBase: process.env.NUXT_PUBLIC_AI_BASE || 'http://localhost:8000',
      recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY || ''
    }
  }
})
