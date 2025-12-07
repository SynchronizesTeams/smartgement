<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-4 max-w-[1400px] mx-auto h-[calc(100vh-2rem)]">
      <!-- Left: Product Selection -->
      <ProductGrid
        :products="products"
        v-model:searchQuery="searchQuery"
        @addToCart="addToCart"
      />

      <!-- Right: Cart & Checkout -->
      <CartPanel
        :cart="cart"
        v-model:customerName="customerName"
        v-model:paymentMethod="paymentMethod"
        :isProcessing="isProcessing"
        @checkout="processTransaction"
        @clearCart="clearCart"
        @increaseQuantity="increaseQuantity"
        @decreaseQuantity="decreaseQuantity"
        @removeFromCart="removeFromCart"
      />
    </div>

    <!-- Success Modal -->
    <SuccessModal
      :show="showSuccessModal"
      :transaction="lastTransaction"
      @close="closeSuccessModal"
      @print="printReceipt"
    />

    <!-- Print Receipt Modal -->
    <ReceiptModal
      :show="showPrintModal"
      :transaction="lastTransaction"
      :user="user"
      @close="closePrintModal"
    />
  </div>
</template>

<script setup lang="ts">
import ProductGrid from '~/components/transactions/ProductGrid.vue'
import CartPanel from '~/components/transactions/CartPanel.vue'
import SuccessModal from '~/components/transactions/SuccessModal.vue'
import ReceiptModal from '~/components/transactions/ReceiptModal.vue'

definePageMeta({
  middleware: 'auth'
})

const api = useApi()
const { user } = useAuth()

const searchQuery = ref('')
const products = ref<any[]>([])
const cart = ref<any[]>([])
const customerName = ref('')
const paymentMethod = ref('cash')
const isProcessing = ref(false)
const showSuccessModal = ref(false)
const showPrintModal = ref(false)
const lastTransaction = ref<any>(null)

const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data || []
  } catch (error) {
    // Silently handle error
  }
}

const addToCart = (product: any) => {
  if (product.stock === 0) return
  
  const existingItem = cart.value.find(item => item.product_id === product.id)
  
  if (existingItem) {
    if (existingItem.quantity < product.stock) {
      existingItem.quantity++
    }
  } else {
    cart.value.push({
      product_id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
      maxStock: product.stock
    })
  }
}

const increaseQuantity = (index: number) => {
  const item = cart.value[index]
  if (item.quantity < item.maxStock) {
    item.quantity++
  }
}

const decreaseQuantity = (index: number) => {
  const item = cart.value[index]
  if (item.quantity > 1) {
    item.quantity--
  }
}

const removeFromCart = (index: number) => {
  cart.value.splice(index, 1)
}

const clearCart = () => {
  cart.value = []
  customerName.value = ''
}

const processTransaction = async () => {
  if (cart.value.length === 0) return
  
  isProcessing.value = true
  
  try {
    const transactionData = {
      payment_method: paymentMethod.value,
      customer_name: customerName.value || 'Walk-in Customer',
      items: cart.value.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity
      }))
    }
    
    const response = await api.post('/transactions', transactionData)
    
    lastTransaction.value = response
    showSuccessModal.value = true
    
    clearCart()
    await fetchProducts()
  } catch (error: any) {
    alert('Transaksi gagal: ' + (error.data?.error || error.message || 'Terjadi kesalahan'))
  } finally {
    isProcessing.value = false
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
}

const printReceipt = () => {
  showSuccessModal.value = false
  showPrintModal.value = true
}

const closePrintModal = () => {
  showPrintModal.value = false
  lastTransaction.value = null
}

onMounted(() => {
  fetchProducts()
})
</script>
