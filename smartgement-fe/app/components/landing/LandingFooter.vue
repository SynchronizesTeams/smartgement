<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-main">
          <div class="footer-brand">
            <h3 class="brand-name">Smartgement</h3>
            <p class="brand-tagline">
              Sistem Manajemen Produk Pintar untuk UMKM dengan AI Chatbot,
              Automasi, dan Analisis Risiko
            </p>
          </div>

          <div class="footer-links">
            <div class="link-group">
              <h4 class="link-title">Fitur</h4>
              <ul class="link-list">
                <li><NuxtLink to="/dashboard">Manajemen Produk</NuxtLink></li>
                <li><NuxtLink to="/transactions">Transaksi</NuxtLink></li>
                <li><NuxtLink to="/chat">AI Chatbot</NuxtLink></li>
                <li><NuxtLink to="/history">Riwayat</NuxtLink></li>
              </ul>
            </div>

            <div class="link-group">
              <h4 class="link-title">Akun</h4>
              <ul class="link-list">
                <li><NuxtLink to="/login">Login</NuxtLink></li>
                <li><NuxtLink to="/register">Daftar</NuxtLink></li>
                <li><NuxtLink to="/profile">Profil</NuxtLink></li>
              </ul>
            </div>

            <div class="link-group">
              <h4 class="link-title">Tentang</h4>
              <ul class="link-list">
                <li><a href="#fitur">Fitur Unggulan</a></li>
                <li><a href="#keunggulan">Keunggulan</a></li>
                <li><a href="#kontak">Hubungi Kami</a></li>
              </ul>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p class="copyright">
            © {{ currentYear }} Smartgement. Semua hak dilindungi.
          </p>
          <div class="footer-social">
            <a href="https://github.com/SynchronizesTeams" class="social-link" aria-label="Twitter">
              <Icon name="lucide:github" />
            </a>
            <a href="https://www.linkedin.com/company/synchronizeteams/" class="social-link" aria-label="LinkedIn">
              <Icon name="lucide:linkedin" />
            </a>
            <a href="https://www.instagram.com/synchronizeteams?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" class="social-link" aria-label="Instagram">
              <Icon name="lucide:instagram" />
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

<style scoped>
.footer {
  background-color: var(--color-black);
  color: var(--color-white);
  padding: var(--spacing-xl) 0 var(--spacing-lg);
  border-top: 4px solid var(--color-white);
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.footer-main {
  display: grid;
  grid-template-columns: 1.5fr 2fr;
  gap: var(--spacing-xl);
}

.footer-brand {
  max-width: 350px;
}

.brand-name {
  font-size: var(--font-size-2xl);
  font-weight: 800;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.02em;
}

.brand-tagline {
  color: var(--color-gray-400);
  line-height: 1.6;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
}

.link-group {
  display: flex;
  flex-direction: column;
}

.link-title {
  font-size: var(--font-size-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: var(--spacing-md);
  color: var(--color-white);
}

.link-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.link-list a {
  color: var(--color-gray-400);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
  display: inline-block;
}

.link-list a:hover {
  color: var(--color-white);
  transform: translateX(4px);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.copyright {
  color: var(--color-gray-500);
  font-size: var(--font-size-sm);
}

.footer-social {
  display: flex;
  gap: var(--spacing-md);
}

.social-link {
  width: 40px;
  height: 40px;
  border: 2px solid var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white);
  text-decoration: none;
  font-weight: bold;
  transition: all var(--transition-base);
}

.social-link:hover {
  background-color: var(--color-white);
  color: var(--color-black);
  transform: translateY(-4px);
}

@media (max-width: 1024px) {
  .footer-main {
    grid-template-columns: 1fr;
  }

  .footer-links {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .footer-links {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
}
</style>
