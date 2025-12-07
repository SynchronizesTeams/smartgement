<template>
  <div class="login-page">
    <!-- Back to Home -->
    <NuxtLink to="/" class="back-home"> ← Back to Home </NuxtLink>

    <div
      class="min-h-screen flex items-center justify-center bg-white text-black p-4 font-sans"
    >
      <div
        class="w-full max-w-md border-2 border-black p-8 bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
      >
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold uppercase tracking-tighter mb-2">
            Login
          </h1>
          <p class="text-gray-600 font-medium">Welcome back to Smartgement</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-bold uppercase mb-2"
              >Email</label
            >
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50 focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="Enter your email"
              required
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-bold uppercase mb-2"
              >Password</label
            >
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50 focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="Enter your password"
              required
            />
          </div>

          <div
            v-if="error"
            class="bg-red-50 border-2 border-red-500 text-red-700 p-3 text-sm font-bold text-center"
          >
            {{ error }}
          </div>

          <!-- reCAPTCHA v2 Widget -->
          <div class="flex justify-center">
            <div id="recaptcha-login" class="g-recaptcha"></div>
          </div>

          <button
            type="submit"
            class="w-full bg-black text-white font-bold uppercase py-4 hover:bg-gray-800 transition-transform active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="loading"
          >
            {{ loading ? "Logging in..." : "Login" }}
          </button>
        </form>

        <div class="mt-8 text-center border-t-2 border-gray-100 pt-6">
          <p class="font-medium text-gray-600">
            Don't have an account?
            <NuxtLink
              to="/register"
              class="text-black font-bold uppercase underline decoration-2 underline-offset-2 hover:bg-black hover:text-white px-1"
              >Register here</NuxtLink
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
declare global {
  interface Window {
    grecaptcha: any;
  }
}

const config = useRuntimeConfig();
const recaptchaSiteKey = config.public.recaptchaSiteKey;

const form = reactive({
  email: "",
  password: "",
});

const loading = ref(false);
const error = ref("");
const recaptchaWidgetId = ref<number | null>(null);
const recaptchaReady = ref(false);

const { login } = useAuth();

// Initialize reCAPTCHA when component is mounted
onMounted(() => {
  // Wait for reCAPTCHA script to load
  const checkRecaptcha = setInterval(() => {
    if (window.grecaptcha && window.grecaptcha.render) {
      clearInterval(checkRecaptcha);

      // Wait a bit more for DOM to be ready
      setTimeout(() => {
        try {
          const widgetId = window.grecaptcha.render("recaptcha-login", {
            sitekey: recaptchaSiteKey,
            callback: () => {
              recaptchaReady.value = true;
            },
          });
          recaptchaWidgetId.value = widgetId;
        } catch (e) {
          console.error("reCAPTCHA render error:", e);
          error.value = "Failed to load reCAPTCHA. Please refresh the page.";
        }
      }, 500);
    }
  }, 100);

  // Cleanup after 15 seconds if not loaded
  setTimeout(() => {
    clearInterval(checkRecaptcha);
    if (recaptchaWidgetId.value === null) {
      error.value =
        "reCAPTCHA failed to load. Please check your internet connection.";
    }
  }, 15000);
});

const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    if (!form.email || !form.password) {
      error.value = "Please fill in all fields";
      loading.value = false;
      return;
    }

    // Check if reCAPTCHA is loaded
    if (recaptchaWidgetId.value === null) {
      error.value = "reCAPTCHA not loaded. Please refresh the page.";
      loading.value = false;
      return;
    }

    // Get reCAPTCHA token using widget ID
    const recaptchaToken = window.grecaptcha.getResponse(
      recaptchaWidgetId.value
    );
    if (!recaptchaToken) {
      error.value = "Please complete the reCAPTCHA verification";
      loading.value = false;
      return;
    }

    await login({
      username: form.email,
      password: form.password,
      recaptcha_token: recaptchaToken,
    });
  } catch (err: any) {
    error.value =
      err?.data?.error || "Login failed. Please verify your credentials.";
    // Reset reCAPTCHA on error
    if (window.grecaptcha && recaptchaWidgetId.value !== null) {
      window.grecaptcha.reset(recaptchaWidgetId.value);
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  animation: fadeIn 0.5s ease-out;
}

.back-home {
  position: fixed;
  top: var(--spacing-lg);
  left: var(--spacing-lg);
  padding: var(--spacing-sm) var(--spacing-md);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--color-black);
  text-decoration: none;
  border: 2px solid var(--color-black);
  background-color: var(--color-white);
  transition: all var(--transition-base);
  z-index: 10;
}

.back-home:hover {
  background-color: var(--color-black);
  color: var(--color-white);
  transform: translateX(-4px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .back-home {
    top: var(--spacing-sm);
    left: var(--spacing-sm);
    font-size: 0.75rem;
    padding: var(--spacing-xs) var(--spacing-sm);
  }
}
</style>
