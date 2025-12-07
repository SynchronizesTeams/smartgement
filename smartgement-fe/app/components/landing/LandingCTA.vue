<template>
  <section class="relative py-16 md:py-32 bg-gray-100 overflow-hidden">
    <div class="container mx-auto px-4 md:px-6 relative z-10">
      <div class="text-center max-w-3xl mx-auto">
        <h2
          class="text-3xl sm:text-4xl md:text-6xl font-extrabold mb-4 md:mb-6 tracking-tight animate-fade-in-up"
        >
          Siap Mengembangkan Bisnis Anda?
        </h2>
        <p
          class="text-lg md:text-xl text-gray-600 mb-8 md:mb-12 leading-relaxed animate-fade-in-up animation-delay-100"
        >
          Bergabunglah dengan ribuan UMKM yang telah merasakan transformasi
          digital bersama Smartgement. Mulai gratis hari ini!
        </p>
        <div
          class="flex flex-col sm:flex-row gap-4 justify-center mb-6 md:mb-8 animate-fade-in-up animation-delay-200"
        >
          <NuxtLink
            to="/register"
            class="group bg-black text-white font-bold uppercase py-4 px-8 text-base md:text-lg tracking-wide transition-all duration-300 hover:-translate-y-1 hover:scale-105 hover:shadow-2xl animate-pulse-subtle"
          >
            Daftar Gratis Sekarang
          </NuxtLink>
          <NuxtLink
            to="/chat"
            class="bg-white text-black font-bold uppercase py-4 px-8 text-base md:text-lg tracking-wide border-2 border-black transition-all duration-300 hover:-translate-y-1 hover:bg-gray-100 hover:shadow-lg"
          >
            Coba AI Chatbot
          </NuxtLink>
        </div>
        <!-- <p
          class="text-sm md:text-base text-gray-500 animate-fade-in-up animation-delay-300"
        >
          ✓ Tidak perlu kartu kredit &nbsp;&nbsp; ✓ Setup dalam 5 menit
          &nbsp;&nbsp; ✓ Cancel kapan saja
        </p> -->
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

@keyframes pulse-subtle {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out backwards;
}

.animation-delay-100 {
  animation-delay: 0.1s;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}

.animate-pulse-subtle {
  animation: pulse-subtle 2s ease-in-out infinite;
}
</style>
