<template>
  <section
    class="relative min-h-screen flex items-center overflow-hidden py-12 md:py-24"
  >
    <div class="container mx-auto px-4 md:px-6">
      <div class="relative text-center max-w-4xl mx-auto animate-fade-in-up">
        <div
          class="absolute -top-24 -right-12 w-72 h-72 bg-black opacity-5 rotate-45 animate-float -z-10 hidden md:block"
        ></div>
        <div
          class="absolute top-36 -left-24 w-48 h-48 bg-black opacity-5 rounded-full animate-float-reverse -z-10 hidden md:block"
        ></div>

        <h1
          class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-extrabold tracking-tighter mb-4 md:mb-6 leading-none"
        >
          Smart<span class="relative inline-block">
            gement
            <span
              class="absolute bottom-2 left-0 right-0 h-4 bg-black opacity-10 -z-10"
            ></span>
          </span>
        </h1>

        <p
          class="text-xl sm:text-2xl md:text-3xl font-semibold mb-4 md:mb-6 text-gray-800"
        >
          Sistem Manajemen Produk Pintar untuk UMKM
        </p>

        <p
          class="text-base sm:text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-8 md:mb-12 leading-relaxed"
        >
          Kelola bisnis Anda dengan lebih cerdas menggunakan AI Chatbot,
          automasi proses, dan analisis risiko yang powerful. Dirancang khusus
          untuk kebutuhan UMKM Indonesia.
        </p>

        <div
          class="flex flex-col sm:flex-row gap-4 justify-center mb-8 md:mb-12"
        >
          <NuxtLink
            to="/register"
            class="group relative overflow-hidden bg-black text-white font-bold uppercase py-4 px-8 text-base md:text-lg tracking-wide transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
          >
            <span class="relative z-10">Mulai Sekarang</span>
            <span
              class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity duration-600"
            ></span>
          </NuxtLink>
          <NuxtLink
            to="/login"
            class="bg-white text-black font-bold uppercase py-4 px-8 text-base md:text-lg tracking-wide border-2 border-black transition-all duration-300 hover:-translate-y-1 hover:bg-gray-100 hover:shadow-lg"
          >
            Login
          </NuxtLink>
        </div>

        <div
          class="flex flex-col sm:flex-row gap-4 md:gap-6 justify-center items-center"
        >
          <div
            class="group flex items-center gap-2 px-4 py-3 border-2 border-black bg-white transition-all duration-300 hover:bg-black hover:text-white hover:-translate-y-1 w-full sm:w-auto justify-center"
          >
            <Icon name="lucide:bot" class="w-6 h-6" />
            <span class="font-semibold text-sm uppercase tracking-wide"
              >AI Chatbot</span
            >
          </div>
          <div
            class="group flex items-center gap-2 px-4 py-3 border-2 border-black bg-white transition-all duration-300 hover:bg-black hover:text-white hover:-translate-y-1 w-full sm:w-auto justify-center"
          >
            <Icon name="lucide:zap" class="w-6 h-6" />
            <span class="font-semibold text-sm uppercase tracking-wide"
              >Automasi</span
            >
          </div>
          <div
            class="group flex items-center gap-2 px-4 py-3 border-2 border-black bg-white transition-all duration-300 hover:bg-black hover:text-white hover:-translate-y-1 w-full sm:w-auto justify-center"
          >
            <Icon name="lucide:trending-up" class="w-6 h-6" />
            <span class="font-semibold text-sm uppercase tracking-wide"
              >Analisis Risiko</span
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

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

@keyframes float {
  0%,
  100% {
    transform: translateY(0) rotate(45deg);
  }
  50% {
    transform: translateY(-20px) rotate(45deg);
  }
}

@keyframes float-reverse {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-reverse {
  animation: float-reverse 8s ease-in-out infinite;
}
</style>
