<template>
  <div class="min-h-screen bg-white text-black font-sans">
    <!-- Navbar -->
    <AppNavbar>
      <template #page-title>
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">Dashboard</span>
      </template>
    </AppNavbar>
    
    <!-- Main Content -->
    <main class="max-w-7xl mx-auto p-4 md:p-8">
      <!-- Header Actions -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h2 class="text-4xl font-bold uppercase mb-1">Products</h2>
          <p class="text-gray-500 font-medium tracking-tight">Manage your inventory</p>
        </div>
        <NuxtLink to="/products/create" class="bg-black text-white px-6 py-3 font-bold uppercase tracking-wider hover:bg-gray-800 transition-colors flex items-center gap-2">
          <span>+ Add Product</span>
        </NuxtLink>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Total Items</p>
          <p class="text-5xl font-bold font-mono">{{ products.length }}</p>
        </div>
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Nilai Valuasi</p>
          <p class="text-5xl font-bold font-mono">Rp{{ totalValue.toFixed(2) }}</p>
        </div>
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Low Stock</p>
          <p class="text-5xl font-bold font-mono">{{ lowStockCount }}</p>
        </div>
      </div>

      <!-- Products Table -->
      <div class="overflow-x-auto border-2 border-black">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-black text-white border-b-2 border-black">
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Name</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Category</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider text-right">Price</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider text-right">Stock</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="border-b border-gray-200">
              <td colspan="5" class="p-8 text-center font-medium">Loading inventory...</td>
            </tr>
            <tr v-else-if="products.length === 0" class="border-b border-gray-200">
               <td colspan="5" class="p-8 text-center font-medium">No products found. Add your first item.</td>
            </tr>
            <tr v-for="product in products" :key="product.id" class="border-b border-gray-200 hover:bg-gray-50 transition-colors group">
              <td class="p-4 font-semibold">{{ product.name }}</td>
              <td class="p-4 text-gray-600">{{ product.category || '-' }}</td>
              <td class="p-4 text-right font-mono">Rp{{ product.price.toFixed(2) }}</td>
              <td class="p-4 text-right font-mono">
                <span :class="{'text-red-600 font-bold': product.stock < 10}">{{ product.stock }}</span>
              </td>
              <td class="p-4 text-right">
                <div class="flex justify-end gap-3 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                    <NuxtLink :to="`/products/${product.id}`" class="text-sm font-bold uppercase underline decoration-2 underline-offset-2 hover:text-gray-600">Edit</NuxtLink>
                    <button @click="deleteProduct(product.id)" class="text-sm font-bold uppercase text-red-600 underline decoration-red-600 decoration-2 underline-offset-2 hover:text-red-800">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const router = useRouter()

const loading = ref(true)
const products = ref<any[]>([])

const totalValue = computed(() => {
    return products.value.reduce((acc, p) => acc + (p.price * p.stock), 0)
})

const lowStockCount = computed(() => {
    return products.value.filter(p => p.stock < 10).length
})

const fetchProducts = async () => {
    try {
        loading.value = true
        // Assuming API returns { data: [...products] } for success response wrapper
        // Backend returns: utils.SuccessResponse(c, "...", products) -> JSON { success: true, message: "...", data: products }
        const response: any = await api.get('/products')
        products.value = response.data || []
    } catch (error) {
        console.error('Failed to fetch products', error)
    } finally {
        loading.value = false
    }
}

const deleteProduct = async (id: number) => {
    if(!confirm('Are you sure you want to delete this product?')) return
    
    try {
        await api.delete(`/products/${id}`)
        products.value = products.value.filter(p => p.id !== id)
    } catch (error) {
        console.error('Failed to delete', error)
        alert('Failed to delete product')
    }
}

onMounted(() => {
    fetchProducts()
})

// Auth guard - if we had middleware we would use it, for now simple check
const { isAuthenticated } = useAuth()
if (!isAuthenticated.value) {
    router.push('/login')
}
</script>
