<template>
  <section class="py-12 md:py-24 bg-black text-white">
    <div class="container mx-auto px-4 md:px-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 items-start">
        <div>
          <h2
            class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 md:mb-6 tracking-tight"
          >
            Kenapa Memilih Smartgement?
          </h2>
          <p
            class="text-lg md:text-xl text-gray-300 mb-8 md:mb-12 leading-relaxed"
          >
            Dirancang khusus untuk kebutuhan UMKM Indonesia yang ingin
            berkembang dengan teknologi modern
          </p>

          <div class="space-y-6 md:space-y-8">
            <div
              v-for="(benefit, index) in benefits"
              :key="index"
              class="flex gap-4 animate-fade-in-left"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div
                class="flex-shrink-0 w-10 h-10 bg-white text-black flex items-center justify-center font-bold text-xl transition-transform duration-300 hover:scale-110 hover:rotate-12"
              >
                <Icon name="lucide:check" class="w-6 h-6" />
              </div>
              <div class="flex-1">
                <h3 class="text-lg md:text-xl font-semibold mb-1">
                  {{ benefit.title }}
                </h3>
                <p class="text-sm md:text-base text-gray-400 leading-relaxed">
                  {{ benefit.description }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 md:gap-6">
          <div
            v-for="(stat, index) in stats"
            :key="index"
            class="bg-white bg-opacity-5 border-2 border-white p-6 md:p-8 text-center transition-all duration-300 hover:bg-white hover:text-black hover:-translate-y-2 animate-fade-in-right"
            :style="{ animationDelay: `${(index + 3) * 0.1}s` }"
          >
            <div
              class="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-2 md:mb-4 tracking-tight font-mono"
            >
              {{ stat.number }}
            </div>
            <div
              class="text-xs md:text-sm font-bold uppercase tracking-widest opacity-80 group-hover:opacity-100"
            >
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const benefits = [
  {
    title: "Mudah Digunakan",
    description:
      "Interface intuitif yang tidak memerlukan keahlian teknis khusus",
  },
  {
    title: "Hemat Waktu & Biaya",
    description: "Automasi proses mengurangi pekerjaan manual hingga 70%",
  },
  {
    title: "Keputusan Lebih Cerdas",
    description: "AI membantu analisis data untuk keputusan bisnis yang tepat",
  },
  {
    title: "Skalabilitas Tinggi",
    description: "Berkembang bersama bisnis Anda tanpa batasan",
  },
  {
    title: "Support Lokal",
    description: "Tim support berbahasa Indonesia SynchronizeTeams siap membantu 24/7",
  },
];

const stats = [
  { number: "10K+", label: "(aminn) UMKM Pengguna" },
  { number: "99.9%", label: "Uptime" },
  { number: "24/7", label: "Support" },
  { number: "70%", label: "Hemat Waktu" },
];
</script>

<style scoped>
@keyframes fade-in-left {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fade-in-right {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-fade-in-left {
  animation: fade-in-left 0.6s ease-out backwards;
}

.animate-fade-in-right {
  animation: fade-in-right 0.6s ease-out backwards;
}
</style>
