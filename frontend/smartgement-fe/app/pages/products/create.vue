<template>
  <div class="min-h-screen bg-white text-black font-sans">
    <!-- Navbar -->
    <nav class="border-b-2 border-black p-4 flex justify-between items-center bg-white sticky top-0 z-10">
      <div class="flex items-center gap-4">
        <h1 class="text-2xl font-bold uppercase tracking-tighter">Smartgement</h1>
        <NuxtLink to="/dashboard" class="text-sm font-bold uppercase hover:underline decoration-2 underline-offset-4">Dashboard</NuxtLink>
        <span class="text-gray-400">/</span>
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">New Product</span>
      </div>
    </nav>

    <main class="max-w-3xl mx-auto p-4 md:p-8">
      <div class="border-2 border-black p-6 md:p-8">
         <h2 class="text-3xl font-bold uppercase mb-8">Add New Product</h2>
         
         <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Name -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Product Name</label>
                <input v-model="form.name" type="text" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" placeholder="E.g. Vintage Camera Lens" required />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Price -->
                <div>
                   <label class="block text-sm font-bold uppercase mb-2">Price ($)</label>
                   <input v-model.number="form.price" type="number" step="0.01" class="w-full border-2 border-black p-3 font-mono font-medium focus:outline-none focus:bg-gray-50" placeholder="0.00" required />
                </div>
                <!-- Stock -->
                <div>
                   <label class="block text-sm font-bold uppercase mb-2">Stock</label>
                   <input v-model.number="form.stock" type="number" class="w-full border-2 border-black p-3 font-mono font-medium focus:outline-none focus:bg-gray-50" placeholder="0" required />
                </div>
            </div>

            <!-- Category -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Category (Optional)</label>
                <input v-model="form.category" type="text" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" placeholder="E.g. Electronics" />
            </div>

            <!-- Description -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Description (Optional)</label>
                <textarea v-model="form.description" rows="4" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" placeholder="Product details..."></textarea>
            </div>

             <!-- Ingredients (Optional) -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Ingredients (Optional)</label>
                <textarea v-model="form.ingredients" rows="2" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" placeholder="Comma separated ingredients..."></textarea>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t-2 border-black mt-8">
                <NuxtLink to="/dashboard" class="px-6 py-3 font-bold uppercase hover:bg-gray-100 transition-colors">Cancel</NuxtLink>
                <button type="submit" :disabled="loading" class="bg-black text-white px-8 py-3 font-bold uppercase hover:bg-gray-800 transition-colors disabled:opacity-50">
                    {{ loading ? 'Saving...' : 'Save Product' }}
                </button>
            </div>
            
            <p v-if="error" class="text-red-600 font-bold text-center mt-4">{{ error }}</p>
         </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const router = useRouter()
const { isAuthenticated } = useAuth()

const loading = ref(false)
const error = ref('')

const form = reactive({
    name: '',
    price: null,
    stock: 0,
    category: '',
    description: '',
    ingredients: ''
})

// Auth Guard
if (!isAuthenticated.value) {
    router.push('/login')
}

const handleSubmit = async () => {
    loading.value = true
    error.value = ''

    try {
        await api.post('/products', form)
        router.push('/dashboard')
    } catch (err: any) {
        console.error(err)
        error.value = err?.data?.error || 'Failed to create product'
    } finally {
        loading.value = false
    }
}
</script>
