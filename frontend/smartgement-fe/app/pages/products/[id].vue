<template>
  <div class="min-h-screen bg-white text-black font-sans">
    <nav class="border-b-2 border-black p-4 flex justify-between items-center bg-white sticky top-0 z-10">
      <div class="flex items-center gap-4">
        <h1 class="text-2xl font-bold uppercase tracking-tighter">Smartgement</h1>
        <NuxtLink to="/dashboard" class="text-sm font-bold uppercase hover:underline decoration-2 underline-offset-4">Dashboard</NuxtLink>
        <span class="text-gray-400">/</span>
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">Edit Product</span>
      </div>
    </nav>

    <main class="max-w-3xl mx-auto p-4 md:p-8">
      <div v-if="loadingData" class="text-center p-12">
        <p class="font-bold uppercase animate-pulse">Loading product details...</p>
      </div>

      <div v-else class="border-2 border-black p-6 md:p-8">
         <div class="flex justify-between items-center mb-8">
            <h2 class="text-3xl font-bold uppercase">Edit Product</h2>
            <button @click="deleteProduct" class="text-red-600 font-bold uppercase text-sm hover:underline decoration-2 underline-offset-2">Delete Item</button>
         </div>
         
         <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Name -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Product Name</label>
                <input v-model="form.name" type="text" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" required />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Price -->
                <div>
                   <label class="block text-sm font-bold uppercase mb-2">Price ($)</label>
                   <input v-model.number="form.price" type="number" step="0.01" class="w-full border-2 border-black p-3 font-mono font-medium focus:outline-none focus:bg-gray-50" required />
                </div>
                <!-- Stock -->
                <div>
                   <label class="block text-sm font-bold uppercase mb-2">Stock</label>
                   <input v-model.number="form.stock" type="number" class="w-full border-2 border-black p-3 font-mono font-medium focus:outline-none focus:bg-gray-50" required />
                </div>
            </div>

            <!-- Category -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Category</label>
                <input v-model="form.category" type="text" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50" />
            </div>

            <!-- Description -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Description</label>
                <textarea v-model="form.description" rows="4" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50"></textarea>
            </div>

             <!-- Ingredients -->
            <div>
                <label class="block text-sm font-bold uppercase mb-2">Ingredients</label>
                <textarea v-model="form.ingredients" rows="2" class="w-full border-2 border-black p-3 font-medium focus:outline-none focus:bg-gray-50"></textarea>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t-2 border-black mt-8">
                <NuxtLink to="/dashboard" class="px-6 py-3 font-bold uppercase hover:bg-gray-100 transition-colors">Cancel</NuxtLink>
                <button type="submit" :disabled="saving" class="bg-black text-white px-8 py-3 font-bold uppercase hover:bg-gray-800 transition-colors disabled:opacity-50">
                    {{ saving ? 'Saving...' : 'Update Product' }}
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
const route = useRoute()
const router = useRouter()
const { isAuthenticated } = useAuth()

const loadingData = ref(true)
const saving = ref(false)
const error = ref('')
const productId = route.params.id

const form = reactive({
    name: '',
    price: 0,
    stock: 0,
    category: '',
    description: '',
    ingredients: ''
})

// Auth Guard
if (!isAuthenticated.value) {
    router.push('/login')
}

const fetchProduct = async () => {
    try {
        loadingData.value = true
        const response: any = await api.get(`/products/${productId}`)
        const data = response.data
        
        form.name = data.name
        form.price = data.price
        form.stock = data.stock
        form.category = data.category
        form.description = data.description
        form.ingredients = data.ingredients
    } catch (err) {
        console.error(err)
        alert('Failed to load product')
        router.push('/dashboard')
    } finally {
        loadingData.value = false
    }
}

const handleSubmit = async () => {
    saving.value = true
    error.value = ''

    try {
        await api.put(`/products/${productId}`, form)
        router.push('/dashboard')
    } catch (err: any) {
        console.error(err)
        error.value = err?.data?.error || 'Failed to update product'
    } finally {
        saving.value = false
    }
}

const deleteProduct = async () => {
    if(!confirm('Are you sure you want to delete this product? This cannot be undone.')) return
    
    try {
        await api.delete(`/products/${productId}`)
        router.push('/dashboard')
    } catch (error) {
        console.error('Failed to delete', error)
        alert('Failed to delete product')
    }
}

onMounted(() => {
    fetchProduct()
})
</script>
