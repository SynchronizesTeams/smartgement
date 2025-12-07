<template>
  <div class="min-h-screen flex items-center justify-center bg-white text-black p-4 font-sans">
    <div class="w-full max-w-md border-2 border-black p-8 bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold uppercase tracking-tighter mb-2">Register</h1>
        <p class="text-gray-600 font-medium">Create your Smartgement account</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
           <label for="name" class="block text-sm font-bold uppercase mb-2">Full Name</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50 focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="Enter your name"
              required
            />
        </div>

        <div>
            <label for="email" class="block text-sm font-bold uppercase mb-2">Email</label>
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
            <label for="password" class="block text-sm font-bold uppercase mb-2">Password</label>
             <input
              id="password"
              v-model="form.password"
              type="password"
              class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50 focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="Create a password"
              required
            />
        </div>

        <div>
            <label for="confirmPassword" class="block text-sm font-bold uppercase mb-2">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50 focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
              placeholder="Confirm your password"
              required
            />
        </div>

        <div v-if="error" class="bg-red-50 border-2 border-red-500 text-red-700 p-3 text-sm font-bold text-center">
          {{ error }}
        </div>

        <!-- reCAPTCHA v2 Widget -->
        <div class="flex justify-center">
          <div id="recaptcha-register" class="g-recaptcha"></div>
        </div>

        <button 
            type="submit" 
            class="w-full bg-black text-white font-bold uppercase py-4 hover:bg-gray-800 transition-transform active:translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="loading"
        >
            {{ loading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>

      <div class="mt-8 text-center border-t-2 border-gray-100 pt-6">
        <p class="font-medium text-gray-600">Already have an account? <NuxtLink to="/login" class="text-black font-bold uppercase underline decoration-2 underline-offset-2 hover:bg-black hover:text-white px-1">Login here</NuxtLink></p>
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

const config = useRuntimeConfig()
const recaptchaSiteKey = config.public.recaptchaSiteKey

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const recaptchaWidgetId = ref<number | null>(null)
const recaptchaReady = ref(false)

const { register } = useAuth()

// Initialize reCAPTCHA when component is mounted
onMounted(() => {
  // Wait for reCAPTCHA script to load
  const checkRecaptcha = setInterval(() => {
    if (window.grecaptcha && window.grecaptcha.render) {
      clearInterval(checkRecaptcha)
      
      // Wait a bit more for DOM to be ready
      setTimeout(() => {
        try {
          const widgetId = window.grecaptcha.render('recaptcha-register', {
            'sitekey': recaptchaSiteKey,
            'callback': () => {
              recaptchaReady.value = true
            }
          })
          recaptchaWidgetId.value = widgetId
        } catch (e) {
          console.error('reCAPTCHA render error:', e)
          error.value = 'Failed to load reCAPTCHA. Please refresh the page.'
        }
      }, 500)
    }
  }, 100)

  // Cleanup after 15 seconds if not loaded
  setTimeout(() => {
    clearInterval(checkRecaptcha)
    if (recaptchaWidgetId.value === null) {
      error.value = 'reCAPTCHA failed to load. Please check your internet connection.'
    }
  }, 15000)
})

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  try {
    if (!form.name || !form.email || !form.password || !form.confirmPassword) {
      error.value = 'Please fill in all fields'
      loading.value = false
      return
    }
    
    if (form.password !== form.confirmPassword) {
      error.value = 'Passwords do not match'
      loading.value = false
      return
    }
    
    if (form.password.length < 6) {
      error.value = 'Password must be at least 6 characters'
      loading.value = false
      return
    }

    // Check if reCAPTCHA is loaded
    if (recaptchaWidgetId.value === null) {
      error.value = 'reCAPTCHA not loaded. Please refresh the page.'
      loading.value = false
      return
    }

    // Get reCAPTCHA token using widget ID
    const recaptchaToken = window.grecaptcha.getResponse(recaptchaWidgetId.value)
    if (!recaptchaToken) {
      error.value = 'Please complete the reCAPTCHA verification'
      loading.value = false
      return
    }
    
    await register({
        username: form.email, 
        password: form.password,
        recaptcha_token: recaptchaToken
    })
    
  } catch (err: any) {
    error.value = err?.data?.error || 'Registration failed. Please try again.'
    // Reset reCAPTCHA on error
    if (window.grecaptcha && recaptchaWidgetId.value !== null) {
      window.grecaptcha.reset(recaptchaWidgetId.value)
    }
  } finally {
    loading.value = false
  }
}
</script>
