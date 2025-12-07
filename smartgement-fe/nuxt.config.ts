export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },

  future: {
    compatibilityVersion: 4,
  },

  modules: ["@nuxtjs/tailwindcss", "@nuxt/icon"], // <--- WAJIB ADA

  css: ["~/assets/css/main.css"],

  app: {
    head: {
      script: [
        {
          src: "https://www.google.com/recaptcha/api.js",
          async: true,
          defer: true,
        },
      ],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE,
      aiBase: process.env.NUXT_PUBLIC_AI_BASE,
      recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY,
    },
  },
});
