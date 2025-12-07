<template>
  <div class="cashier-container">
    <div class="cashier-layout">
      <!-- Left: Product Selection -->
      <div class="products-panel">
        <div class="panel-header">
          <h2>Produk</h2>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari produk..."
            class="search-input"
          />
        </div>
        
        <div class="products-grid">
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            @click="addToCart(product)"
            class="product-card"
            :class="{ 'out-of-stock': product.stock === 0 }"
          >
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="product-price">Rp{{ product.price.toLocaleString() }}</p>
              <p class="product-stock">Stok: {{ product.stock }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Cart & Checkout -->
      <div class="cart-panel">
        <div class="panel-header">
          <h2>Keranjang</h2>
          <button @click="clearCart" class="btn-secondary-sm" v-if="cart.length > 0">
            Bersihkan
          </button>
        </div>

        <div class="cart-items">
          <div v-if="cart.length === 0" class="empty-cart">
            <p>Keranjang kosong</p>
          </div>

          <div v-for="(item, index) in cart" :key="index" class="cart-item">
            <div class="item-info">
              <h4>{{ item.name }}</h4>
              <p class="item-price">Rp{{ item.price.toLocaleString() }}</p>
            </div>
            <div class="item-controls">
              <button @click="decreaseQuantity(index)" class="qty-btn">-</button>
              <span class="qty">{{ item.quantity }}</span>
              <button @click="increaseQuantity(index)" class="qty-btn">+</button>
              <button @click="removeFromCart(index)" class="remove-btn">×</button>
            </div>
            <div class="item-subtotal">
              Rp{{ (item.price * item.quantity).toLocaleString() }}
            </div>
          </div>
        </div>

        <div class="cart-summary">
          <div class="summary-row">
            <span>Subtotal</span>
            <span class="amount">Rp{{ calculateTotal().toLocaleString() }}</span>
          </div>
          <div class="summary-row total">
            <span>Total</span>
            <span class="amount">Rp{{ calculateTotal().toLocaleString() }}</span>
          </div>
        </div>

        <div class="checkout-section">
          <div class="form-group">
            <label>Nama Pelanggan (Opsional)</label>
            <input v-model="customerName" type="text" placeholder="Nama pelanggan" />
          </div>

          <div class="form-group">
            <label>Metode Pembayaran</label>
            <select v-model="paymentMethod">
              <option value="cash">Tunai</option>
              <option value="card">Kartu</option>
              <option value="ewallet">E-Wallet</option>
            </select>
          </div>

          <button
            @click="processTransaction"
            :disabled="cart.length === 0 || isProcessing"
            class="btn-checkout"
          >
            {{ isProcessing ? 'Memproses...' : 'Bayar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="closeSuccessModal">
      <div class="modal-content" @click.stop>
        <div class="success-icon">✓</div>
        <h2>Transaksi Berhasil!</h2>
        <p class="transaction-total">Rp{{ lastTransaction?.total_amount.toLocaleString() }}</p>
        <p class="transaction-id">ID: #{{ lastTransaction?.id }}</p>
        <button @click="closeSuccessModal" class="btn-primary">OK</button>
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

const searchQuery = ref('')
const products = ref<any[]>([])
const cart = ref<any[]>([])
const customerName = ref('')
const paymentMethod = ref('cash')
const isProcessing = ref(false)
const showSuccessModal = ref(false)
const lastTransaction = ref<any>(null)

// Fetch products
const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data || []
  } catch (error) {
    console.error('Failed to fetch products:', error)
  }
}

// Filtered products based on search
const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value
  
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(p => 
    p.name.toLowerCase().includes(query) ||
    p.category?.toLowerCase().includes(query)
  )
})

// Add product to cart
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

// Increase quantity
const increaseQuantity = (index: number) => {
  const item = cart.value[index]
  if (item.quantity < item.maxStock) {
    item.quantity++
  }
}

// Decrease quantity
const decreaseQuantity = (index: number) => {
  const item = cart.value[index]
  if (item.quantity > 1) {
    item.quantity--
  }
}

// Remove from cart
const removeFromCart = (index: number) => {
  cart.value.splice(index, 1)
}

// Clear cart
const clearCart = () => {
  cart.value = []
  customerName.value = ''
}

// Calculate total
const calculateTotal = () => {
  return cart.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
}

// Process transaction
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
    
    console.log('Sending transaction:', transactionData)
    
    // Use api composable (includes auth headers)
    const response = await api.post('/transactions', transactionData)
    
    console.log('Transaction response:', response)
    
    lastTransaction.value = response
    showSuccessModal.value = true
    
    // Clear cart and refresh products
    clearCart()
    await fetchProducts()
  } catch (error: any) {
    console.error('Transaction failed:', error)
    alert('Transaksi gagal: ' + (error.data?.error || error.message || 'Terjadi kesalahan'))
  } finally {
    isProcessing.value = false
  }
}

// Close success modal
const closeSuccessModal = () => {
  showSuccessModal.value = false
  lastTransaction.value = null
}

// Load products on mount
onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.cashier-container {
  min-height: 100vh;
  background-color: var(--color-gray-100);
  padding: var(--spacing-md);
}

.cashier-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-md);
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 2rem);
}

.products-panel,
.cart-panel {
  background: var(--color-white);
  border: var(--border-width) solid var(--color-gray-300);
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: var(--spacing-md);
  border-bottom: var(--border-width) solid var(--color-gray-300);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2 {
  font-size: var(--font-size-xl);
  margin: 0;
}

.search-input {
  padding: var(--spacing-sm);
  border: var(--border-width) solid var(--color-gray-400);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  width: 250px;
}

.products-grid {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-md);
  align-content: start;
}

.product-card {
  border: var(--border-width) solid var(--color-gray-300);
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.product-card:hover:not(.out-of-stock) {
  border-color: var(--color-black);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.product-card.out-of-stock {
  opacity: 0.5;
  cursor: not-allowed;
}

.product-info h3 {
  font-size: var(--font-size-base);
  margin-bottom: var(--spacing-xs);
}

.product-price {
  font-size: var(--font-size-lg);
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.product-stock {
  font-size: var(--font-size-sm);
  color: var(--color-gray-600);
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

.empty-cart {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-gray-500);
}

.cart-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  border: var(--border-width) solid var(--color-gray-300);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-sm);
}

.item-info h4 {
  font-size: var(--font-size-base);
  margin-bottom: var(--spacing-xs);
}

.item-price {
  font-size: var(--font-size-sm);
  color: var(--color-gray-600);
}

.item-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  grid-column: 1 / -1;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: var(--border-width) solid var(--color-gray-400);
  background: var(--color-white);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-btn:hover {
  background: var(--color-gray-100);
}

.qty {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
}

.remove-btn {
  margin-left: auto;
  width: 32px;
  height: 32px;
  border: var(--border-width) solid var(--color-gray-400);
  background: var(--color-white);
  color: var(--color-gray-600);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 24px;
  line-height: 1;
}

.remove-btn:hover {
  background: var(--color-gray-900);
  color: var(--color-white);
  border-color: var(--color-black);
}

.item-subtotal {
  grid-column: 1 / -1;
  text-align: right;
  font-weight: 600;
  font-size: var(--font-size-lg);
}

.cart-summary {
  padding: var(--spacing-md);
  border-top: var(--border-width) solid var(--color-gray-300);
  border-bottom: var(--border-width) solid var(--color-gray-300);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
}

.summary-row.total {
  font-size: var(--font-size-xl);
  font-weight: 700;
  margin-top: var(--spacing-sm);
  padding-top: var(--spacing-sm);
  border-top: 2px solid var(--color-black);
}

.checkout-section {
  padding: var(--spacing-md);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  font-size: var(--font-size-sm);
}

.form-group input,
.form-group select {
  width: 100%;
  padding: var(--spacing-sm);
  border: var(--border-width) solid var(--color-gray-400);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
}

.btn-checkout {
  width: 100%;
  padding: var(--spacing-md);
  background: var(--color-black);
  color: var(--color-white);
  border: none;
  border-radius: var(--border-radius);
  font-size: var(--font-size-lg);
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.btn-checkout:hover:not(:disabled) {
  background: var(--color-gray-800);
}

.btn-checkout:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary-sm {
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--color-white);
  border: var(--border-width) solid var(--color-black);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
}

.btn-secondary-sm:hover {
  background: var(--color-gray-100);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #4CAF50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin: 0 auto var(--spacing-md);
}

.modal-content h2 {
  margin-bottom: var(--spacing-md);
}

.transaction-total {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.transaction-id {
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-lg);
}

/* Responsive */
@media (max-width: 1024px) {
  .cashier-layout {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .products-panel {
    order: 2;
  }
  
  .cart-panel {
    order: 1;
  }
}
</style>
