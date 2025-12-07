<template>
  <section class="cta-section">
    <div class="container">
      <div class="cta-content">
        <h2 class="cta-title">Siap Mengembangkan Bisnis Anda?</h2>
        <p class="cta-description">
          Bergabunglah dengan ribuan UMKM yang telah merasakan transformasi
          digital bersama Smartgement. Mulai gratis hari ini!
        </p>
        <div class="cta-actions">
          <NuxtLink to="/register" class="btn btn-primary btn-large">
            Daftar Gratis Sekarang
          </NuxtLink>
          <NuxtLink to="/chat" class="btn btn-secondary btn-large">
            Coba AI Chatbot
          </NuxtLink>
        </div>
        <p class="cta-note">
          ✓ Tidak perlu kartu kredit &nbsp;&nbsp; ✓ Setup dalam 5 menit
          &nbsp;&nbsp; ✓ Cancel kapan saja
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-section {
  padding: calc(var(--spacing-xl) * 2) 0;
  background-color: var(--color-gray-100);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: "";
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background-color: var(--color-black);
  opacity: 0.02;
  border-radius: 50%;
}

.cta-section::after {
  content: "";
  position: absolute;
  bottom: -50%;
  left: -10%;
  width: 600px;
  height: 600px;
  background-color: var(--color-black);
  opacity: 0.02;
  border-radius: 50%;
}

.cta-content {
  position: relative;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  z-index: 1;
}

.cta-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  margin-bottom: var(--spacing-md);
  letter-spacing: -0.03em;
  animation: fadeInUp 0.6s ease-out;
}

.cta-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-xl);
  line-height: 1.8;
  animation: fadeInUp 0.6s ease-out 0.1s backwards;
}

.cta-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: var(--spacing-lg);
  animation: fadeInUp 0.6s ease-out 0.2s backwards;
}

.btn-large {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-lg);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.btn-primary {
  animation: pulse 2s ease-in-out infinite;
}

.btn-large:hover {
  transform: translateY(-3px) scale(1.02);
}

.btn-primary:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.btn-secondary:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cta-note {
  font-size: var(--font-size-sm);
  color: var(--color-gray-500);
  animation: fadeInUp 0.6s ease-out 0.3s backwards;
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

@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
  }
}

@media (max-width: 768px) {
  .cta-section {
    padding: var(--spacing-xl) 0;
  }

  .cta-actions {
    flex-direction: column;
  }

  .btn-large {
    width: 100%;
  }

  .cta-note {
    font-size: 0.75rem;
  }
}
</style>
