<template>
  <div class="bg-white border border-gray-300 rounded flex flex-col overflow-hidden">
    <div class="p-4 border-b border-gray-300 flex justify-between items-center">
      <h2 class="text-xl m-0">Produk</h2>
      <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', ($event.target as HTMLInputElement).value)"
        type="text"
        placeholder="Cari produk..."
        class="p-2 border border-gray-400 rounded text-base w-64"
      />
    </div>
    
    <div class="flex-1 overflow-y-auto p-4 grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-4 content-start">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        @click="$emit('addToCart', product)"
        class="border border-gray-300 rounded p-4 cursor-pointer transition-all hover:border-black hover:shadow-md"
        :class="{ 'opacity-50 cursor-not-allowed': product.stock === 0 }"
      >
        <div>
          <h3 class="text-base mb-1">{{ product.name }}</h3>
          <p class="text-lg font-semibold mb-1">Rp{{ product.price.toLocaleString() }}</p>
          <p class="text-sm text-gray-600">Stok: {{ product.stock }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Product {
  id: number
  name: string
  price: number
  stock: number
  category?: string
}

const props = defineProps<{
  products: Product[]
  searchQuery: string
}>()

defineEmits<{
  'update:searchQuery': [value: string]
  addToCart: [product: Product]
}>()

const filteredProducts = computed(() => {
  if (!props.searchQuery) return props.products
  
  const query = props.searchQuery.toLowerCase()
  return props.products.filter(p => 
    p.name.toLowerCase().includes(query) ||
    p.category?.toLowerCase().includes(query)
  )
})
</script>
