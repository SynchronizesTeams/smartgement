<template>
  <section class="benefits-section">
    <div class="container">
      <div class="benefits-content">
        <div class="benefits-text">
          <h2 class="section-title">Kenapa Memilih Smartgement?</h2>
          <p class="section-intro">
            Dirancang khusus untuk kebutuhan UMKM Indonesia yang ingin
            berkembang dengan teknologi modern
          </p>

          <div class="benefits-list">
            <div
              v-for="(benefit, index) in benefits"
              :key="index"
              class="benefit-item"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="benefit-check">
                <Icon name="lucide:check" class="check-icon" />
              </div>
              <div class="benefit-content">
                <h3 class="benefit-title">{{ benefit.title }}</h3>
                <p class="benefit-description">{{ benefit.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="benefits-stats">
          <div
            v-for="(stat, index) in stats"
            :key="index"
            class="stat-card"
            :style="{ animationDelay: `${(index + 3) * 0.1}s` }"
          >
            <div class="stat-number">{{ stat.number }}</div>
            <div class="stat-label">{{ stat.label }}</div>
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
    description: "Tim support berbahasa Indonesia SynchronizeTeams siap membantu 24/7.",
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
.benefits-section {
  padding: var(--spacing-xl) 0;
  background-color: var(--color-black);
  color: var(--color-white);
}

.benefits-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.section-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  letter-spacing: -0.02em;
}

.section-intro {
  font-size: var(--font-size-lg);
  color: var(--color-gray-300);
  margin-bottom: var(--spacing-xl);
  line-height: 1.7;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.benefit-item {
  display: flex;
  gap: var(--spacing-md);
  animation: fadeInLeft 0.6s ease-out backwards;
}

.benefit-check {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background-color: var(--color-white);
  color: var(--color-black);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  transition: all var(--transition-base);
}

.benefit-item:hover .benefit-check {
  transform: scale(1.1) rotate(10deg);
}

.benefit-content {
  flex: 1;
}

.benefit-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.benefit-description {
  color: var(--color-gray-400);
  line-height: 1.6;
  font-size: var(--font-size-sm);
}

.benefits-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.stat-card {
  background-color: rgba(255, 255, 255, 0.05);
  border: 2px solid var(--color-white);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all var(--transition-base);
  animation: fadeInRight 0.6s ease-out backwards;
}

.stat-card:hover {
  background-color: var(--color-white);
  color: var(--color-black);
  transform: translateY(-8px);
}

.stat-number {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: var(--font-size-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.8;
}

.stat-card:hover .stat-label {
  opacity: 1;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 1024px) {
  .benefits-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
  }

  .benefits-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .benefits-stats {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: var(--spacing-lg);
  }
}
</style>
