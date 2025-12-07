<template>
  <section class="features-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Fitur Unggulan</h2>
        <p class="section-description">
          Solusi lengkap untuk mengelola bisnis UMKM Anda dengan lebih efisien
        </p>
      </div>

      <div class="features-grid">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="feature-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="feature-icon">
            <Icon :name="feature.icon" class="icon-svg" />
          </div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
          <ul class="feature-list">
            <li v-for="(item, idx) in feature.items" :key="idx">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  {
    icon: "lucide:package",
    title: "Manajemen Produk",
    description: "Kelola inventori dan produk dengan mudah dan efisien",
    items: [
      "Tambah, edit, hapus produk",
      "Pencarian produk real-time",
      "Monitoring stok otomatis",
      "Alert produk low stock",
    ],
  },
  {
    icon: "lucide:shopping-cart",
    title: "Point of Sale",
    description:
      "Sistem kasir modern untuk proses transaksi yang cepat dan akurat",
    items: [
      "Input transaksi cepat",
      "Riwayat transaksi lengkap",
      "Laporan penjualan",
      "Print receipt otomatis",
    ],
  },
  {
    icon: "lucide:bot",
    title: "AI Chatbot",
    description:
      "Asisten virtual yang membantu Anda mengelola bisnis dengan cerdas",
    items: [
      "Konsultasi bisnis 24/7",
      "Analisis data produk",
      "Rekomendasi strategi",
      "Automasi operasional",
    ],
  },
];
</script>

<style scoped>
.features-section {
  padding: var(--spacing-xl) 0;
  background-color: var(--color-gray-100);
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  letter-spacing: -0.02em;
}

.section-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-xl);
}

.feature-card {
  background-color: var(--color-white);
  border: 2px solid var(--color-black);
  padding: var(--spacing-xl);
  transition: all var(--transition-base);
  position: relative;
  animation: fadeInUp 0.6s ease-out backwards;
}

.feature-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background-color: var(--color-black);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-base);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background-color: var(--color-black);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-md);
  transition: all var(--transition-base);
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.icon-svg {
  width: 2.5rem;
  height: 2.5rem;
  color: var(--color-white);
}

.feature-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.01em;
}

.feature-description {
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  padding: var(--spacing-xs) 0;
  padding-left: var(--spacing-md);
  position: relative;
  color: var(--color-gray-700);
  font-size: var(--font-size-sm);
}

.feature-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  font-weight: bold;
  color: var(--color-black);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }

  .feature-card {
    padding: var(--spacing-lg);
  }
}
</style>
