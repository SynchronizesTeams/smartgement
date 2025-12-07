<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4" @click="$emit('close')">
    <div class="bg-white border-4 border-black w-full max-w-3xl max-h-[90vh] overflow-hidden" @click.stop>
      <!-- Header -->
      <div class="bg-black text-white p-4 flex justify-between items-center">
        <h3 class="font-bold uppercase">Transaction #{{ transaction.id }}</h3>
        <button @click="$emit('close')" class="text-2xl hover:text-gray-300">×</button>
      </div>

      <!-- Content -->
      <div class="p-6 overflow-y-auto max-h-[70vh]">
        <!-- Transaction Info Section -->
        <div class="border-2 border-black p-4 mb-6">
          <h4 class="font-bold uppercase mb-4">Transaction Info</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Date</p>
              <p class="font-mono">{{ formatDateTime(transaction.created_at) }}</p>
            </div>
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Status</p>
              <span :class="getStatusClass(transaction.status)" class="px-2 py-1 text-xs font-bold uppercase">
                {{ transaction.status }}
              </span>
            </div>
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Payment Method</p>
              <p>{{ getPaymentLabel(transaction.payment_method) }}</p>
            </div>
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Total Amount</p>
              <p class="font-mono font-bold text-lg">Rp{{ transaction.total_amount.toLocaleString() }}</p>
            </div>
          </div>
          
          <!-- Editable Fields -->
          <div v-if="!editing" class="mt-4 grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Customer</p>
              <p>{{ transaction.customer_name || 'Walk-in' }}</p>
            </div>
            <div>
              <p class="text-sm font-bold uppercase text-gray-500">Notes</p>
              <p>{{ transaction.notes || '-' }}</p>
            </div>
          </div>
          
          <!-- Edit Form -->
          <div v-else class="mt-4 space-y-4">
            <div>
              <label class="block text-sm font-bold uppercase mb-2">Customer Name</label>
              <input v-model="editForm.customer_name" type="text" class="w-full border-2 border-black px-4 py-2 font-mono" />
            </div>
            <div>
              <label class="block text-sm font-bold uppercase mb-2">Notes</label>
              <textarea v-model="editForm.notes" rows="3" class="w-full border-2 border-black px-4 py-2 font-mono"></textarea>
            </div>
          </div>
        </div>

        <!-- Items Section -->
        <div class="border-2 border-black mb-6">
          <div class="bg-black text-white p-3">
            <h4 class="font-bold uppercase">Items</h4>
          </div>
          <table class="w-full">
            <thead>
              <tr class="border-b-2 border-black bg-gray-100">
                <th class="p-3 text-left font-bold uppercase text-xs">Product</th>
                <th class="p-3 text-center font-bold uppercase text-xs">Qty</th>
                <th class="p-3 text-right font-bold uppercase text-xs">Price</th>
                <th class="p-3 text-right font-bold uppercase text-xs">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in transaction.items" :key="item.id" class="border-b border-gray-200">
                <td class="p-3">{{ item.product_name }}</td>
                <td class="p-3 text-center font-mono">{{ item.quantity }}</td>
                <td class="p-3 text-right font-mono">Rp{{ item.price.toLocaleString() }}</td>
                <td class="p-3 text-right font-mono font-bold">Rp{{ item.subtotal.toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Actions -->
      <div class="border-t-2 border-black p-4 bg-gray-50 flex justify-between">
        <div class="flex gap-3">
          <button v-if="!editing && transaction.status === 'completed'" @click="startEdit" class="bg-white border-2 border-black px-6 py-2 font-bold uppercase hover:bg-gray-100">
            Edit
          </button>
          <button v-if="editing" @click="cancelEdit" class="bg-white border-2 border-black px-6 py-2 font-bold uppercase hover:bg-gray-100">
            Cancel
          </button>
          <button v-if="editing" @click="saveEdit" :disabled="saving" class="bg-black text-white px-6 py-2 font-bold uppercase hover:bg-gray-800 disabled:opacity-50">
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
          <button @click="handlePrint" class="bg-white border-2 border-black px-6 py-2 font-bold uppercase hover:bg-gray-100 flex items-center gap-2">
            <Printer :size="16" /> Print
          </button>
        </div>
        <button v-if="transaction.status === 'completed'" @click="confirmCancel" class="bg-red-600 text-white px-6 py-2 font-bold uppercase hover:bg-red-700">
          Cancel Transaction
        </button>
      </div>

      <!-- Hidden Print Content -->
      <div id="receipt-print" class="hidden">
        <div class="p-8 font-mono text-sm" style="width: 320px; margin: 0 auto;">
          <!-- Store Header -->
          <div class="text-center mb-6 pb-4 border-b-2 border-dashed border-black">
            <h1 class="text-3xl font-bold mb-2 uppercase">{{ user?.username || 'TOKO SAYA' }}</h1>
            <p class="text-xs">STRUK PEMBELIAN</p>
            <p class="text-xs mt-1">================================</p>
          </div>
          
          <!-- Transaction Info -->
          <div class="mb-4 text-xs space-y-1">
            <div class="flex justify-between">
              <span>No. Transaksi</span>
              <span class="font-bold">#{{ transaction.id }}</span>
            </div>
            <div class="flex justify-between">
              <span>Tanggal</span>
              <span>{{ formatDateTime(transaction.created_at) }}</span>
            </div>
            <div class="flex justify-between">
              <span>Kasir</span>
              <span>{{ user?.username }}</span>
            </div>
          </div>

          <!-- Customer Info -->
          <div class="mb-4 pb-4 border-b border-dashed border-black">
            <div class="text-xs">
              <span class="font-bold">Nama Pembeli:</span> {{ transaction.customer_name || 'Walk-in Customer' }}
            </div>
          </div>
          
          <!-- Items Header -->
          <div class="mb-2">
            <p class="text-xs font-bold border-b-2 border-black pb-1">DETAIL BELANJA</p>
          </div>
          
          <!-- Items List -->
          <div class="mb-4 pb-4 border-b-2 border-black space-y-3">
            <div v-for="(item, idx) in transaction.items" :key="item.id" class="text-xs">
              <div class="flex justify-between font-bold mb-1">
                <span class="uppercase">{{ item.product_name }}</span>
              </div>
              <div class="flex justify-between text-gray-700">
                <span>  {{ item.quantity }} x Rp{{ item.price.toLocaleString() }}</span>
                <span class="font-bold">Rp{{ item.subtotal.toLocaleString() }}</span>
              </div>
              <div v-if="idx < transaction.items.length - 1" class="border-b border-dotted border-gray-400 mt-2"></div>
            </div>
          </div>
          
          <!-- Payment Summary -->
          <div class="mb-6 space-y-2">
            <div class="flex justify-between text-xs pb-2">
              <span>Metode Pembayaran</span>
              <span class="font-bold">{{ getPaymentLabel(transaction.payment_method) }}</span>
            </div>
            <div class="flex justify-between text-lg font-bold border-t-2 border-black pt-2">
              <span>TOTAL</span>
              <span>Rp{{ transaction.total_amount.toLocaleString() }}</span>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="text-center text-xs border-t-2 border-dashed border-black pt-4 space-y-2">
            <p class="font-bold text-base">TERIMA KASIH</p>
            <p>Barang yang sudah dibeli</p>
            <p>tidak dapat dikembalikan</p>
            <p class="mt-4 text-gray-600">{{ new Date().toLocaleDateString('id-ID') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Printer } from 'lucide-vue-next'

const props = defineProps<{
  transaction: any
}>()

const emit = defineEmits(['close', 'updated', 'cancelled'])

const api = useApi()
const { user } = useAuth()

const editing = ref(false)
const saving = ref(false)
const editForm = ref({
  customer_name: '',
  notes: ''
})

const startEdit = () => {
  editForm.value = {
    customer_name: props.transaction.customer_name || '',
    notes: props.transaction.notes || ''
  }
  editing.value = true
}

const cancelEdit = () => {
  editing.value = false
}

const saveEdit = async () => {
  try {
    saving.value = true
    await api.put(`/transactions/${props.transaction.id}`, editForm.value)
    editing.value = false
    emit('updated')
  } catch (error) {
    console.error('Failed to update transaction:', error)
    alert('Failed to update transaction')
  } finally {
    saving.value = false
  }
}

const confirmCancel = async () => {
  if (!confirm(`Cancel transaction #${props.transaction.id}? This will restore product stock.`)) return
  
  try {
    await api.delete(`/transactions/${props.transaction.id}`)
    emit('cancelled')
  } catch (error) {
    console.error('Failed to cancel transaction:', error)
    alert('Failed to cancel transaction')
  }
}

const handlePrint = () => {
  const printContent = document.getElementById('receipt-print')
  if (!printContent) return
  
  const printWindow = window.open('', '', 'width=400,height=600')
  if (!printWindow) return
  
  printWindow.document.write('<html><head><title>Receipt</title>')
  printWindow.document.write('<style>body { margin: 0; padding: 0; font-family: monospace; }</style>')
  printWindow.document.write('</head><body>')
  printWindow.document.write(printContent.innerHTML)
  printWindow.document.write('</body></html>')
  printWindow.document.close()
  printWindow.focus()
  setTimeout(() => {
    printWindow.print()
    printWindow.close()
  }, 250)
}

const formatDateTime = (dateString: string) => {
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

const getPaymentLabel = (method: string) => {
  const labels: Record<string, string> = {
    'cash': 'Tunai',
    'card': 'Kartu',
    'ewallet': 'E-Wallet'
  }
  return labels[method] || method
}

const getStatusClass = (status: string) => {
  if (status === 'completed') return 'bg-green-100 border border-green-600 text-green-800'
  if (status === 'cancelled') return 'bg-red-100 border border-red-600 text-red-800'
  return 'bg-gray-100 border border-gray-600'
}
</script>
