<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <!-- Decorative element -->
        <div class="hero-decoration">
          <div class="deco-square"></div>
          <div class="deco-circle"></div>
        </div>

        <h1 class="hero-title">Smart<span class="highlight">gement</span></h1>

        <p class="hero-subtitle">Sistem Manajemen Produk Pintar untuk UMKM</p>

        <p class="hero-description">
          Kelola bisnis Anda dengan lebih cerdas menggunakan AI Chatbot,
          automasi proses, dan analisis risiko yang powerful. Dirancang khusus
          untuk kebutuhan UMKM Indonesia.
        </p>

        <div class="hero-actions">
          <NuxtLink to="/register" class="btn btn-primary btn-large">
            Mulai Sekarang
          </NuxtLink>
          <NuxtLink to="/login" class="btn btn-secondary btn-large">
            Login
          </NuxtLink>
        </div>

        <!-- Feature badges -->
        <div class="hero-features">
          <div class="feature-badge">
            <Icon name="lucide:bot" class="badge-icon" />
            <span class="badge-text">AI Chatbot</span>
          </div>
          <div class="feature-badge">
            <Icon name="lucide:zap" class="badge-icon" />
            <span class="badge-text">Automasi</span>
          </div>
          <div class="feature-badge">
            <Icon name="lucide:trending-up" class="badge-icon" />
            <span class="badge-text">Analisis Risiko</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: var(--spacing-xl) 0;
  overflow: hidden;
}

.hero-content {
  position: relative;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
  animation: fadeInUp 0.8s ease-out;
}

.hero-decoration {
  position: absolute;
  top: -100px;
  right: -50px;
  z-index: -1;
  opacity: 0.05;
}

.deco-square {
  width: 300px;
  height: 300px;
  background-color: var(--color-black);
  transform: rotate(45deg);
  animation: float 6s ease-in-out infinite;
}

.deco-circle {
  width: 200px;
  height: 200px;
  background-color: var(--color-black);
  border-radius: 50%;
  position: absolute;
  top: 150px;
  left: -100px;
  animation: float 8s ease-in-out infinite reverse;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: var(--spacing-md);
  line-height: 1;
  animation: fadeInUp 0.8s ease-out 0.2s backwards;
}

.highlight {
  position: relative;
  display: inline-block;
}

.highlight::after {
  content: "";
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  height: 15px;
  background-color: var(--color-black);
  opacity: 0.1;
  z-index: -1;
}

.hero-subtitle {
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--color-gray-800);
  animation: fadeInUp 0.8s ease-out 0.3s backwards;
}

.hero-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  max-width: 700px;
  margin: 0 auto var(--spacing-xl);
  line-height: 1.8;
  animation: fadeInUp 0.8s ease-out 0.4s backwards;
}

.hero-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: var(--spacing-xl);
  animation: fadeInUp 0.8s ease-out 0.5s backwards;
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

.btn-large::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn-large:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.hero-features {
  display: flex;
  gap: var(--spacing-lg);
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s ease-out 0.6s backwards;
}

.feature-badge {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--color-black);
  background-color: var(--color-white);
  transition: all var(--transition-base);
}

.feature-badge:hover {
  background-color: var(--color-black);
  color: var(--color-white);
  transform: translateY(-4px);
}

.badge-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.badge-text {
  font-weight: 600;
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
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

@keyframes float {
  0%,
  100% {
    transform: translateY(0) rotate(45deg);
  }
  50% {
    transform: translateY(-20px) rotate(45deg);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: var(--spacing-lg) 0;
  }

  .hero-decoration {
    display: none;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .btn-large {
    width: 100%;
  }

  .hero-features {
    flex-direction: column;
    align-items: center;
  }

  .feature-badge {
    width: 100%;
    justify-content: center;
  }
}
</style>
