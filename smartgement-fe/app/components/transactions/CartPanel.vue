<template>
  <div class="bg-white border border-gray-300 rounded flex flex-col overflow-hidden">
    <div class="p-4 border-b border-gray-300 flex justify-between items-center">
      <h2 class="text-xl m-0">Keranjang</h2>
      <div class="flex gap-2">
        <NuxtLink to="/history" class="px-2 py-1 bg-white border border-black rounded cursor-pointer text-sm hover:bg-gray-100 flex items-center gap-1 no-underline text-black">
          <History :size="14" /> Riwayat
        </NuxtLink>
        <button @click="$emit('clearCart')" class="px-2 py-1 bg-white border border-black rounded cursor-pointer text-sm hover:bg-gray-100" v-if="cart.length > 0">
          Bersihkan
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto p-4">
      <div v-if="cart.length === 0" class="text-center p-8 text-gray-500">
        <p>Keranjang kosong</p>
      </div>

      <div v-for="(item, index) in cart" :key="index" class="grid grid-cols-[1fr_auto] gap-2 p-2 border border-gray-300 rounded mb-2">
        <div>
          <h4 class="text-base mb-1">{{ item.name }}</h4>
          <p class="text-sm text-gray-600">Rp{{ item.price.toLocaleString() }}</p>
        </div>
        <div class="flex items-center gap-1 col-span-2">
          <button @click="$emit('decreaseQuantity', index)" class="w-8 h-8 border border-gray-400 bg-white rounded cursor-pointer text-lg flex items-center justify-center hover:bg-gray-100">-</button>
          <span class="min-w-[40px] text-center font-semibold">{{ item.quantity }}</span>
          <button @click="$emit('increaseQuantity', index)" class="w-8 h-8 border border-gray-400 bg-white rounded cursor-pointer text-lg flex items-center justify-center hover:bg-gray-100">+</button>
          <button @click="$emit('removeFromCart', index)" class="ml-auto w-8 h-8 border border-gray-400 bg-white text-gray-600 rounded cursor-pointer text-2xl leading-none hover:bg-gray-900 hover:text-white hover:border-black">×</button>
        </div>
        <div class="col-span-2 text-right font-semibold text-lg">
          Rp{{ (item.price * item.quantity).toLocaleString() }}
        </div>
      </div>
    </div>

    <div class="p-4 border-t border-b border-gray-300">
      <div class="flex justify-between mb-2">
        <span>Subtotal</span>
        <span class="font-mono">Rp{{ total.toLocaleString() }}</span>
      </div>
      <div class="flex justify-between font-semibold text-xl mt-2 pt-2 border-t-2 border-black">
        <span>Total</span>
        <span class="font-mono">Rp{{ total.toLocaleString() }}</span>
      </div>
    </div>

    <div class="p-4">
      <div class="mb-4">
        <label class="block font-semibold mb-1 text-sm">Nama Pelanggan (Opsional)</label>
        <input 
          :value="customerName" 
          @input="$emit('update:customerName', ($event.target as HTMLInputElement).value)"
          type="text" 
          placeholder="Nama pelanggan" 
          class="w-full p-2 border border-gray-400 rounded text-base"
        />
      </div>

      <div class="mb-4">
        <label class="block font-semibold mb-1 text-sm">Metode Pembayaran</label>
        <select 
          :value="paymentMethod" 
          @change="$emit('update:paymentMethod', ($event.target as HTMLSelectElement).value)"
          class="w-full p-2 border border-gray-400 rounded text-base"
        >
          <option value="cash">Tunai</option>
          <option value="card">Kartu</option>
          <option value="ewallet">E-Wallet</option>
        </select>
      </div>

      <button
        @click="$emit('checkout')"
        :disabled="cart.length === 0 || isProcessing"
        class="w-full p-4 bg-black text-white border-none rounded text-lg font-semibold cursor-pointer transition-colors hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ isProcessing ? 'Memproses...' : 'Bayar' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { History } from 'lucide-vue-next'

interface CartItem {
  product_id: number
  name: string
  price: number
  quantity: number
  maxStock: number
}

const props = defineProps<{
  cart: CartItem[]
  customerName: string
  paymentMethod: string
  isProcessing: boolean
}>()

defineEmits<{
  'update:customerName': [value: string]
  'update:paymentMethod': [value: string]
  checkout: []
  clearCart: []
  increaseQuantity: [index: number]
  decreaseQuantity: [index: number]
  removeFromCart: [index: number]
}>()

const total = computed(() => {
  return props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})
</script>
