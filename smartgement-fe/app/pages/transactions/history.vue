<template>
  <div class="min-h-screen bg-white text-black font-sans">
    <!-- Navbar -->
    <AppNavbar>
      <template #page-title>
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">Transaction History</span>
      </template>
    </AppNavbar>
    
    <!-- Main Content -->
    <main class="max-w-7xl mx-auto p-4 md:p-8">
      <!-- Header Actions -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h2 class="text-4xl font-bold uppercase mb-1">Transactions</h2>
          <p class="text-gray-500 font-medium tracking-tight">View and manage your sales</p>
        </div>
        <div class="flex gap-3">
          <NuxtLink to="/transactions" class="bg-white text-black px-6 py-3 font-bold uppercase tracking-wider border-2 border-black hover:bg-gray-100 transition-colors">
            ← New Sale
          </NuxtLink>
          <button @click="showAIChat = true" class="bg-black text-white px-6 py-3 font-bold uppercase tracking-wider hover:bg-gray-800 transition-colors flex items-center gap-2">
            <span>🤖 AI Summary</span>
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="border-2 border-black p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-bold uppercase mb-2">Status</label>
            <select v-model="filters.status" class="w-full border-2 border-black px-4 py-2 font-mono">
              <option value="">All</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-bold uppercase mb-2">Payment</label>
            <select v-model="filters.paymentMethod" class="w-full border-2 border-black px-4 py-2 font-mono">
              <option value="">All</option>
              <option value="cash">Tunai</option>
              <option value="card">Kartu</option>
              <option value="ewallet">E-Wallet</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-bold uppercase mb-2">From Date</label>
            <input type="date" v-model="filters.dateFrom" class="w-full border-2 border-black px-4 py-2 font-mono" />
          </div>
          <div>
            <label class="block text-sm font-bold uppercase mb-2">To Date</label>
            <input type="date" v-model="filters.dateTo" class="w-full border-2 border-black px-4 py-2 font-mono" />
          </div>
        </div>
        <div class="flex gap-3 mt-4">
          <button @click="fetchTransactions" class="bg-black text-white px-6 py-2 font-bold uppercase text-sm hover:bg-gray-800">
            Apply Filters
          </button>
          <button @click="resetFilters" class="border-2 border-black px-6 py-2 font-bold uppercase text-sm hover:bg-gray-100">
            Reset
          </button>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Total Transactions</p>
          <p class="text-5xl font-bold font-mono">{{ stats.total }}</p>
        </div>
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Total Revenue</p>
          <p class="text-5xl font-bold font-mono">Rp{{ stats.revenue.toFixed(0) }}</p>
        </div>
        <div class="border-2 border-black p-6">
          <p class="text-sm font-bold uppercase text-gray-500 mb-2">Average Sale</p>
          <p class="text-5xl font-bold font-mono">Rp{{ stats.average.toFixed(0) }}</p>
        </div>
      </div>

      <!-- Transactions Table -->
      <div class="overflow-x-auto border-2 border-black">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-black text-white border-b-2 border-black">
              <th class="p-4 font-bold uppercase text-sm tracking-wider">ID</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Date</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Customer</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Payment</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider text-right">Amount</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider">Status</th>
              <th class="p-4 font-bold uppercase text-sm tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="border-b border-gray-200">
              <td colspan="7" class="p-8 text-center font-medium">Loading transactions...</td>
            </tr>
            <tr v-else-if="transactions.length === 0" class="border-b border-gray-200">
               <td colspan="7" class="p-8 text-center font-medium">No transactions found.</td>
            </tr>
            <tr v-for="transaction in transactions" :key="transaction.id" class="border-b border-gray-200 hover:bg-gray-50 transition-colors group">
              <td class="p-4 font-mono">#{{ transaction.id }}</td>
              <td class="p-4 font-mono text-sm">{{ formatDate(transaction.created_at) }}</td>
              <td class="p-4">{{ transaction.customer_name || 'Walk-in' }}</td>
              <td class="p-4">
                <span class="px-2 py-1 text-xs font-bold uppercase border border-black">
                  {{ getPaymentLabel(transaction.payment_method) }}
                </span>
              </td>
              <td class="p-4 text-right font-mono font-bold">Rp{{ transaction.total_amount.toLocaleString() }}</td>
              <td class="p-4">
                <span :class="getStatusClass(transaction.status)" class="px-2 py-1 text-xs font-bold uppercase">
                  {{ transaction.status }}
                </span>
              </td>
              <td class="p-4 text-right">
                <div class="flex justify-end gap-3 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="viewTransaction(transaction)" class="text-sm font-bold uppercase underline decoration-2 underline-offset-2 hover:text-gray-600">View</button>
                  <button v-if="transaction.status === 'completed'" @click="printReceipt(transaction)" class="text-sm font-bold uppercase underline decoration-2 underline-offset-2 hover:text-gray-600">Print</button>
                  <button v-if="transaction.status === 'completed'" @click="confirmCancel(transaction)" class="text-sm font-bold uppercase text-red-600 underline decoration-red-600 decoration-2 underline-offset-2 hover:text-red-800">Cancel</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.totalPages > 1" class="flex justify-center gap-2 mt-8">
        <button 
          @click="changePage(pagination.currentPage - 1)" 
          :disabled="pagination.currentPage === 1"
          class="px-4 py-2 border-2 border-black font-bold uppercase disabled:opacity-30 disabled:cursor-not-allowed hover:bg-black hover:text-white transition-colors"
        >
          ← Prev
        </button>
        <span class="px-4 py-2 border-2 border-black font-mono">
          {{ pagination.currentPage }} / {{ pagination.totalPages }}
        </span>
        <button 
          @click="changePage(pagination.currentPage + 1)" 
          :disabled="pagination.currentPage === pagination.totalPages"
          class="px-4 py-2 border-2 border-black font-bold uppercase disabled:opacity-30 disabled:cursor-not-allowed hover:bg-black hover:text-white transition-colors"
        >
          Next →
        </button>
      </div>
    </main>

    <!-- Transaction Detail Modal -->
    <TransactionDetailModal 
      v-if="selectedTransaction" 
      :transaction="selectedTransaction" 
      @close="selectedTransaction = null"
      @updated="onTransactionUpdated"
      @cancelled="onTransactionCancelled"
    />

    <!-- AI Chat Modal -->
    <div v-if="showAIChat" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4" @click="showAIChat = false">
      <div class="bg-white border-4 border-black w-full max-w-2xl max-h-[80vh] overflow-hidden" @click.stop>
        <div class="bg-black text-white p-4 flex justify-between items-center">
          <h3 class="font-bold uppercase">AI Transaction Summary</h3>
          <button @click="showAIChat = false" class="text-2xl hover:text-gray-300">×</button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[60vh]">
          <div class="mb-4">
            <p class="text-sm font-bold uppercase mb-2">Ask about your transactions:</p>
            <div class="flex gap-2">
              <input 
                v-model="aiQuery" 
                @keyup.enter="askAI"
                type="text" 
                placeholder="e.g., Ringkas transaksi hari ini"
                class="flex-1 border-2 border-black px-4 py-2 font-mono"
              />
              <button @click="askAI" :disabled="!aiQuery || aiLoading" class="bg-black text-white px-6 py-2 font-bold uppercase hover:bg-gray-800 disabled:opacity-50">
                {{ aiLoading ? 'Loading...' : 'Ask' }}
              </button>
            </div>
          </div>
          <div v-if="aiResponse" class="border-2 border-black p-4">
            <div class="prose prose-sm max-w-none whitespace-pre-wrap font-mono text-sm">{{ aiResponse }}</div>
          </div>
          <div v-if="!aiResponse && !aiLoading" class="text-center text-gray-500 py-8">
            <p class="font-bold uppercase mb-2">Try asking:</p>
            <div class="flex flex-col gap-2 mt-4">
              <button @click="aiQuery = 'Ringkas transaksi hari ini'" class="border-2 border-gray-300 px-4 py-2 hover:border-black">Ringkas transaksi hari ini</button>
              <button @click="aiQuery = 'Berapa total penjualan minggu ini?'" class="border-2 border-gray-300 px-4 py-2 hover:border-black">Berapa total penjualan minggu ini?</button>
              <button @click="aiQuery = 'Tampilkan tren penjualan'" class="border-2 border-gray-300 px-4 py-2 hover:border-black">Tampilkan tren penjualan</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

const api = useApi()
const { user } = useAuth()

const loading = ref(true)
const transactions = ref<any[]>([])
const selectedTransaction = ref<any>(null)
const showAIChat = ref(false)
const aiQuery = ref('')
const aiResponse = ref('')
const aiLoading = ref(false)

const filters = ref({
  status: '',
  paymentMethod: '',
  dateFrom: '',
  dateTo: ''
})

const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  limit: 20,
  total: 0
})

const stats = computed(() => {
  const completed = transactions.value.filter(t => t.status === 'completed')
  const revenue = completed.reduce((sum, t) => sum + t.total_amount, 0)
  return {
    total: transactions.value.length,
    revenue: revenue,
    average: completed.length > 0 ? revenue / completed.length : 0
  }
})

const fetchTransactions = async () => {
  try {
    loading.value = true
    const offset = (pagination.value.currentPage - 1) * pagination.value.limit
    
    const params: any = {
      limit: pagination.value.limit,
      offset: offset
    }
    
    // Add filters to params if set
    // Note: backend may need additional filter support
    
    const response: any = await api.get('/transactions', { params })
    transactions.value = response.data || []
    pagination.value.total = response.total || 0
    pagination.value.totalPages = Math.ceil((response.total || 0) / pagination.value.limit)
  } catch (error) {
    console.error('Failed to fetch transactions', error)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    status: '',
    paymentMethod: '',
    dateFrom: '',
    dateTo: ''
  }
  pagination.value.currentPage = 1
  fetchTransactions()
}

const changePage = (page: number) => {
  pagination.value.currentPage = page
  fetchTransactions()
}

const viewTransaction = (transaction: any) => {
  selectedTransaction.value = transaction
}

const confirmCancel = async (transaction: any) => {
  if (!confirm(`Cancel transaction #${transaction.id}? This will restore product stock.`)) return
  
  try {
    await api.delete(`/transactions/${transaction.id}`)
    await fetchTransactions()
  } catch (error) {
    console.error('Failed to cancel transaction', error)
    alert('Failed to cancel transaction')
  }
}

const printReceipt = (transaction: any) => {
  selectedTransaction.value = transaction
  // Will open modal with print option
  nextTick(() => {
    // Trigger print functionality from modal
  })
}

const onTransactionUpdated = () => {
  selectedTransaction.value = null
  fetchTransactions()
}

const onTransactionCancelled = () => {
  selectedTransaction.value = null
  fetchTransactions()
}

// AI Functions
const askAI = async () => {
  if (!aiQuery.value.trim()) return
  
  try {
    aiLoading.value = true
    aiResponse.value = ''
    
    const chatResponse = await fetch(`${useRuntimeConfig().public.aiBase}/chatbot/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        merchant_id: user.value?.id?.toString(),
        message: aiQuery.value,
        conversation_history: []
      })
    })
    
    const data = await chatResponse.json()
    aiResponse.value = data.response || 'No response from AI'
  } catch (error) {
    console.error('AI request failed:', error)
    aiResponse.value = 'Failed to get AI response. Please try again.'
  } finally {
    aiLoading.value = false
  }
}

// Utility Functions
const formatDate = (dateString: string) => {
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

// Load transactions on mount
onMounted(() => {
  fetchTransactions()
})
</script>
