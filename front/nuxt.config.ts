// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxt/ui"],
  compatibilityDate: "2024-12-13",
  runtimeConfig: {
    public: {
      // Make sure to match the .env variable name (minus the prefix)
      API_URL: process.env.NUXT_PUBLIC_API_URL || "error",
    },
  },
});
