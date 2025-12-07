<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[1000]" @click="$emit('close')">
    <div class="bg-white p-8 rounded text-center max-w-md w-[90%]" @click.stop>
      <div class="w-20 h-20 bg-green-500 text-white rounded-full flex items-center justify-center text-5xl mx-auto mb-4">✓</div>
      <h2 class="mb-4">Transaksi Berhasil!</h2>
      <p class="text-3xl font-bold mb-2">Rp{{ transaction?.total_amount?.toLocaleString() }}</p>
      <p class="text-gray-600 mb-6">ID: #{{ transaction?.id }}</p>
      
      <div class="flex gap-3 justify-center">
        <button @click="$emit('print')" class="px-6 py-3 bg-white border-2 border-black rounded font-bold uppercase hover:bg-gray-100 flex items-center gap-2">
          <Printer :size="16" /> Cetak Struk
        </button>
        <button @click="$emit('close')" class="px-6 py-3 bg-black text-white rounded font-bold uppercase hover:bg-gray-800">OK</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Printer } from 'lucide-vue-next'

interface Transaction {
  id: number
  total_amount: number
}

defineProps<{
  show: boolean
  transaction: Transaction | null
}>()

defineEmits<{
  close: []
  print: []
}>()
</script>
