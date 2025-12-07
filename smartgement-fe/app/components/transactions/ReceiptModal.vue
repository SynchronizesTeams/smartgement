<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[1000]" @click="$emit('close')">
    <div class="bg-white p-8 rounded text-center max-w-md w-[90%]" @click.stop>
      <div id="receipt-content" class="font-mono text-sm" style="width: 320px; margin: 0 auto;">
        <!-- Store Header -->
        <div class="text-center mb-6 pb-4 border-b-2 border-dashed border-black">
          <h1 class="text-xl font-bold mb-2 uppercase">{{ user?.username || 'TOKO' }}</h1>
          <p>STRUK PEMBAYARAN</p>
        </div>
        
        <!-- Transaction Info -->
        <div class="mb-4 space-y-1">
          <div class="flex justify-between">
            <span>No. Transaksi:</span>
            <span>#{{ transaction?.id }}</span>
          </div>
          <div class="flex justify-between">
            <span>Tanggal:</span>
            <span>{{ formatDateTime(transaction?.created_at) }}</span>
          </div>
          <div class="flex justify-between">
            <span>Kasir:</span>
            <span>{{ user?.username }}</span>
          </div>
          <div class="flex justify-between">
            <span>Pelanggan:</span>
            <span>{{ transaction?.customer_name || 'Walk-in' }}</span>
          </div>
        </div>

        <!-- Items -->
        <div class="my-4 border-t border-b border-black py-2">
          <div v-for="item in transaction?.items" :key="item.id" class="mb-2">
            <div class="flex justify-between font-semibold">
              <span>{{ item.product_name }}</span>
              <span>Rp{{ item.subtotal.toLocaleString() }}</span>
            </div>
            <div class="text-xs text-gray-600">
              {{ item.quantity }} x Rp{{ item.price.toLocaleString() }}
            </div>
          </div>
        </div>

        <!-- Total -->
        <div class="mb-6">
          <div class="flex justify-between text-lg font-bold">
            <span>TOTAL:</span>
            <span>Rp{{ transaction?.total_amount?.toLocaleString() }}</span>
          </div>
          <div class="text-xs">
            Metode: {{ getPaymentMethodLabel(transaction?.payment_method) }}
          </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-xs border-t-2 border-dashed border-black pt-4">
          <p class="font-bold">TERIMA KASIH</p>
          <p>Barang yang sudah dibeli tidak dapat dikembalikan</p>
        </div>
      </div>

      <!-- Print Buttons -->
      <div class="flex gap-3 justify-center mt-6">
        <button @click="handlePrint" class="px-6 py-3 bg-white border-2 border-black rounded font-bold uppercase hover:bg-gray-100 flex items-center gap-2">
          <Printer :size="16" /> Print
        </button>
        <button @click="$emit('close')" class="px-6 py-3 bg-gray-200 border-2 border-black rounded font-bold uppercase hover:bg-gray-300">Tutup</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Printer } from 'lucide-vue-next'

interface TransactionItem {
  id: number
  product_name: string
  price: number
  quantity: number
  subtotal: number
}

interface Transaction {
  id: number
  total_amount: number
  created_at: string
  customer_name: string
  payment_method: string
  items: TransactionItem[]
}

interface User {
  username: string
}

defineProps<{
  show: boolean
  transaction: Transaction | null
  user: User | null
}>()

const emit = defineEmits<{
  close: []
}>()

const handlePrint = () => {
  window.print()
}

const formatDateTime = (dateString: string | undefined) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('id-ID', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getPaymentMethodLabel = (method: string | undefined) => {
  if (!method) return '-'
  const labels: Record<string, string> = {
    'cash': 'Tunai',
    'card': 'Kartu',
    'ewallet': 'E-Wallet'
  }
  return labels[method] || method
}
</script>

<style scoped>
@media print {
  body * {
    visibility: hidden;
  }
  #receipt-content, #receipt-content * {
    visibility: visible;
  }
  #receipt-content {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>
