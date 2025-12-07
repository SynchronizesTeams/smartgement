<template>
  <footer class="bg-black text-white py-12 md:py-16 border-t-4 border-white">
    <div class="container mx-auto px-4 md:px-6">
      <div class="flex flex-col gap-12">
        <div class="grid grid-cols-1 lg:grid-cols-[1.5fr_2fr] gap-8 md:gap-12">
          <div class="max-w-sm">
            <h3
              class="text-2xl md:text-3xl font-extrabold mb-3 md:mb-4 tracking-tight"
            >
              Smartgement
            </h3>
            <p class="text-gray-400 leading-relaxed">
              Sistem Manajemen Produk Pintar untuk UMKM dengan AI Chatbot,
              Automasi, dan Analisis Risiko
            </p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 md:gap-8">
            <div>
              <h4 class="text-sm font-bold uppercase tracking-widest mb-4">
                Fitur
              </h4>
              <ul class="space-y-2">
                <li>
                  <NuxtLink
                    to="/dashboard"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Manajemen Produk
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink
                    to="/transactions"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Transaksi
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink
                    to="/chat"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    AI Chatbot
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink
                    to="/history"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Riwayat
                  </NuxtLink>
                </li>
              </ul>
            </div>

            <div>
              <h4 class="text-sm font-bold uppercase tracking-widest mb-4">
                Akun
              </h4>
              <ul class="space-y-2">
                <li>
                  <NuxtLink
                    to="/login"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Login
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink
                    to="/register"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Daftar
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink
                    to="/profile"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Profil
                  </NuxtLink>
                </li>
              </ul>
            </div>

            <div>
              <h4 class="text-sm font-bold uppercase tracking-widest mb-4">
                Tentang
              </h4>
              <ul class="space-y-2">
                <li>
                  <a
                    href="#fitur"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Fitur Unggulan
                  </a>
                </li>
                <li>
                  <a
                    href="#keunggulan"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Keunggulan
                  </a>
                </li>
                <li>
                  <a
                    href="#kontak"
                    class="text-gray-400 text-sm hover:text-white hover:translate-x-1 inline-block transition-all duration-200"
                  >
                    Hubungi Kami
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row justify-between items-center gap-4 pt-8 border-t border-white border-opacity-10"
        >
          <p class="text-gray-500 text-sm text-center sm:text-left">
            © {{ currentYear }} Smartgement. Semua hak dilindungi.
          </p>
          <div class="flex gap-4">
            <a
              href="https://github.com/SynchronizesTeams"
              target="_blank"
              rel="noopener noreferrer"
              class="w-10 h-10 border-2 border-white flex items-center justify-center text-white hover:bg-white hover:text-black hover:-translate-y-1 transition-all duration-300"
              aria-label="GitHub"
            >
              <Icon name="lucide:github" class="w-5 h-5" />
            </a>
            <a
              href="https://www.linkedin.com/company/synchronizeteams/"
              target="_blank"
              rel="noopener noreferrer"
              class="w-10 h-10 border-2 border-white flex items-center justify-center text-white hover:bg-white hover:text-black hover:-translate-y-1 transition-all duration-300"
              aria-label="LinkedIn"
            >
              <Icon name="lucide:linkedin" class="w-5 h-5" />
            </a>
            <a
              href="https://www.instagram.com/synchronizeteams?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
              target="_blank"
              rel="noopener noreferrer"
              class="w-10 h-10 border-2 border-white flex items-center justify-center text-white hover:bg-white hover:text-black hover:-translate-y-1 transition-all duration-300"
              aria-label="Instagram"
            >
              <Icon name="lucide:instagram" class="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear();
</script>
