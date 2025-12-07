<template>
  <section class="py-12 md:py-24 bg-gray-100">
    <div class="container mx-auto px-4 md:px-6">
      <div class="text-center mb-12 md:mb-16">
        <h2
          class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 md:mb-6 tracking-tight"
        >
          Fitur Unggulan
        </h2>
        <p class="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
          Solusi lengkap untuk mengelola bisnis UMKM Anda dengan lebih efisien
        </p>
      </div>

      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 mt-12"
      >
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="group bg-white border-2 border-black p-6 md:p-8 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl relative animate-fade-in-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div
            class="absolute top-0 left-0 right-0 h-1 bg-black scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"
          ></div>

          <div
            class="w-20 h-20 bg-black flex items-center justify-center mb-4 md:mb-6 transition-all duration-300 group-hover:scale-110 group-hover:rotate-6"
          >
            <Icon :name="feature.icon" class="w-10 h-10 text-white" />
          </div>

          <h3 class="text-xl md:text-2xl font-bold mb-3 md:mb-4 tracking-tight">
            {{ feature.title }}
          </h3>
          <p class="text-gray-600 mb-4 md:mb-6 leading-relaxed">
            {{ feature.description }}
          </p>

          <ul class="space-y-2">
            <li
              v-for="(item, idx) in feature.items"
              :key="idx"
              class="flex items-start gap-2 text-gray-700 text-sm"
            >
              <span class="text-black font-bold mt-0.5">✓</span>
              <span>{{ item }}</span>
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
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out backwards;
}
</style>
