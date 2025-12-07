<template>
  <div class="dashboard-page">
    <!-- Navbar -->
    <AppNavbar>
      <template #page-title>
        <span
          class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase"
          >Dashboard</span
        >
      </template>
    </AppNavbar>

    <!-- Main Content -->
    <main class="dashboard-content">
      <!-- Header Actions -->
      <div class="page-header">
        <div class="header-text">
          <h2 class="page-title">Products</h2>
          <p class="page-subtitle">Manage your inventory</p>
        </div>
        <NuxtLink to="/products/create" class="btn-add-product">
          <span class="btn-icon">+</span>
          <span>Add Product</span>
        </NuxtLink>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <StatCard
          label="Total Items"
          :value="products.length"
          icon="lucide:package"
          :animated="true"
        />
        <StatCard
          label="Total Value"
          :value="totalValue"
          icon="lucide:dollar-sign"
          prefix="Rp"
          :animated="true"
        />
        <StatCard
          label="Low Stock"
          :value="lowStockCount"
          icon="lucide:alert-triangle"
          :trend="
            lowStockCount > 0
              ? `${lowStockCount} items need restock`
              : 'All good!'
          "
          :trend-direction="lowStockCount > 0 ? 'down' : 'up'"
          :animated="true"
        />
      </div>

      <!-- Search and Filter -->
      <div class="search-section">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search products..."
          class="search-input"
        />
      </div>

      <!-- Products Table -->
      <div class="table-container">
        <table class="products-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th class="text-right">Price</th>
              <th class="text-right">Stock</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="loading-cell">
                <div class="loading-spinner"></div>
                Loading inventory...
              </td>
            </tr>
            <tr v-else-if="filteredProducts.length === 0">
              <td colspan="5" class="empty-cell">
                <div class="empty-state">
                  <div class="empty-icon">📦</div>
                  <p class="empty-text">
                    {{ searchQuery ? "No products found" : "No products yet" }}
                  </p>
                  <NuxtLink
                    v-if="!searchQuery"
                    to="/products/create"
                    class="empty-cta"
                  >
                    Add your first product
                  </NuxtLink>
                </div>
              </td>
            </tr>
            <tr
              v-for="product in filteredProducts"
              :key="product.id"
              class="product-row"
            >
              <td class="product-name">{{ product.name }}</td>
              <td class="product-category">{{ product.category || "-" }}</td>
              <td class="product-price">Rp{{ product.price.toFixed(2) }}</td>
              <td class="product-stock">
                <span :class="{ 'low-stock': product.stock < 10 }">
                  {{ product.stock }}
                </span>
              </td>
              <td class="product-actions">
                <div class="action-buttons">
                  <NuxtLink
                    :to="`/products/${product.id}`"
                    class="btn-action btn-edit"
                  >
                    Edit
                  </NuxtLink>
                  <button
                    @click="deleteProduct(product.id)"
                    class="btn-action btn-delete"
                  >
                    Delete
                  </button>
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
const api = useApi();
const router = useRouter();

const loading = ref(true);
const products = ref<any[]>([]);
const searchQuery = ref("");

const totalValue = computed(() => {
  return products.value.reduce((acc, p) => acc + p.price * p.stock, 0);
});

const lowStockCount = computed(() => {
  return products.value.filter((p) => p.stock < 10).length;
});

const filteredProducts = computed(() => {
  if (!searchQuery.value) return products.value;

  const query = searchQuery.value.toLowerCase();
  return products.value.filter(
    (p) =>
      p.name.toLowerCase().includes(query) ||
      (p.category && p.category.toLowerCase().includes(query))
  );
});

const fetchProducts = async () => {
  try {
    loading.value = true;
    // Assuming API returns { data: [...products] } for success response wrapper
    // Backend returns: utils.SuccessResponse(c, "...", products) -> JSON { success: true, message: "...", data: products }
    const response: any = await api.get("/products");
    products.value = response.data || [];
  } catch (error) {
    console.error("Failed to fetch products", error);
  } finally {
    loading.value = false;
  }
};

const deleteProduct = async (id: number) => {
  if (!confirm("Are you sure you want to delete this product?")) return;

  try {
    await api.delete(`/products/${id}`);
    products.value = products.value.filter((p) => p.id !== id);
  } catch (error) {
    console.error("Failed to delete", error);
    alert("Failed to delete product");
  }
};

onMounted(() => {
  fetchProducts();
});

// Auth guard - if we had middleware we would use it, for now simple check
const { isAuthenticated } = useAuth();
if (!isAuthenticated.value) {
  router.push("/login");
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background-color: var(--color-white);
  animation: fadeIn 0.4s ease-out;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
  gap: var(--spacing-md);
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  margin-bottom: var(--spacing-xs);
  line-height: 1;
}

.page-subtitle {
  color: var(--color-gray-600);
  font-weight: 600;
  font-size: var(--font-size-lg);
}

.btn-add-product {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  background-color: var(--color-black);
  color: var(--color-white);
  text-decoration: none;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.875rem;
  transition: all var(--transition-base);
  border: 2px solid var(--color-black);
}

.btn-add-product:hover {
  background-color: var(--color-white);
  color: var(--color-black);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.search-section {
  margin-bottom: var(--spacing-lg);
}

.search-input {
  width: 100%;
  max-width: 500px;
  padding: var(--spacing-md);
  font-size: var(--font-size-base);
  font-family: var(--font-family);
  border: 2px solid var(--color-gray-400);
  background-color: var(--color-white);
  transition: all var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-black);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-container {
  overflow-x: auto;
  border: 2px solid var(--color-black);
  background-color: var(--color-white);
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table thead {
  background-color: var(--color-black);
  color: var(--color-white);
}

.products-table th {
  padding: var(--spacing-md);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-align: left;
}

.products-table th.text-right {
  text-align: right;
}

.products-table tbody tr {
  border-bottom: 1px solid var(--color-gray-300);
  transition: background-color var(--transition-fast);
}

.products-table tbody tr:hover {
  background-color: var(--color-gray-100);
}

.products-table td {
  padding: var(--spacing-md);
}

.product-name {
  font-weight: 600;
  font-size: var(--font-size-base);
}

.product-category {
  color: var(--color-gray-600);
}

.product-price,
.product-stock {
  text-align: right;
  font-family: "Courier New", monospace;
  font-weight: 600;
}

.low-stock {
  color: #ef4444;
  font-weight: 700;
}

.product-actions {
  text-align: right;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  opacity: 1;
}

@media (min-width: 768px) {
  .action-buttons {
    opacity: 0;
  }

  .product-row:hover .action-buttons {
    opacity: 1;
  }
}

.btn-action {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  text-decoration: underline;
  text-underline-offset: 2px;
  border: none;
  background: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-edit {
  color: var(--color-black);
  text-decoration-color: var(--color-black);
  text-decoration-thickness: 2px;
}

.btn-edit:hover {
  color: var(--color-gray-700);
}

.btn-delete {
  color: #ef4444;
  text-decoration-color: #ef4444;
  text-decoration-thickness: 2px;
}

.btn-delete:hover {
  color: #dc2626;
}

.loading-cell,
.empty-cell {
  padding: var(--spacing-xl);
  text-align: center;
}

.loading-spinner {
  display: inline-block;
  width: 30px;
  height: 30px;
  border: 3px solid var(--color-gray-300);
  border-top-color: var(--color-black);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: var(--spacing-sm);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  padding: var(--spacing-xl);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
}

.empty-text {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-md);
}

.empty-cta {
  display: inline-block;
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--color-black);
  color: var(--color-white);
  text-decoration: none;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.875rem;
  transition: all var(--transition-base);
}

.empty-cta:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .dashboard-content {
    padding: var(--spacing-lg) var(--spacing-md);
  }
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn-add-product {
    width: 100%;
    justify-content: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .table-container {
    font-size: 0.875rem;
  }

  .products-table th,
  .products-table td {
    padding: var(--spacing-sm);
  }
}
</style>
