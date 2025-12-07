<template>
  <div class="stat-card" :class="{ clickable: clickable }">
    <div class="stat-header">
      <div class="stat-icon" v-if="icon">
        <Icon :name="icon" class="icon-svg" />
      </div>
      <p class="stat-label">{{ label }}</p>
    </div>
    <p class="stat-value">
      <span v-if="prefix" class="stat-prefix">{{ prefix }}</span>
      <AnimatedNumber
        v-if="animated"
        :value="value"
        :duration="animationDuration"
      />
      <span v-else>{{ formattedValue }}</span>
      <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
    </p>
    <div class="stat-trend" v-if="trend">
      <span :class="['trend-indicator', trendDirection]">
        {{
          trendDirection === "up" ? "↑" : trendDirection === "down" ? "↓" : "→"
        }}
      </span>
      <span class="trend-text">{{ trend }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  label: string;
  value: number | string;
  icon?: string;
  prefix?: string;
  suffix?: string;
  trend?: string;
  trendDirection?: "up" | "down" | "neutral";
  animated?: boolean;
  animationDuration?: number;
  clickable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  animated: true,
  animationDuration: 1000,
  trendDirection: "neutral",
  clickable: false,
});

const formattedValue = computed(() => {
  if (typeof props.value === "number") {
    return props.value.toLocaleString();
  }
  return props.value;
});
</script>

<script lang="ts">
// Animated Number Component
export const AnimatedNumber = defineComponent({
  props: {
    value: {
      type: Number,
      required: true,
    },
    duration: {
      type: Number,
      default: 1000,
    },
  },
  setup(props) {
    const displayValue = ref(0);

    watch(
      () => props.value,
      (newValue, oldValue) => {
        const start = oldValue || 0;
        const end = newValue;
        const startTime = Date.now();

        const animate = () => {
          const now = Date.now();
          const progress = Math.min((now - startTime) / props.duration, 1);

          // Easing function (ease-out)
          const easeOut = 1 - Math.pow(1 - progress, 3);

          displayValue.value = Math.round(start + (end - start) * easeOut);

          if (progress < 1) {
            // Check if we're in browser before using requestAnimationFrame
            if (typeof window !== "undefined" && window.requestAnimationFrame) {
              requestAnimationFrame(animate);
            }
          }
        };

        // Only start animation in browser
        if (typeof window !== "undefined" && window.requestAnimationFrame) {
          animate();
        } else {
          // If SSR, just set the value directly
          displayValue.value = end;
        }
      },
      { immediate: true }
    );

    return {
      displayValue,
    };
  },
  template: `<span>{{ displayValue.toLocaleString() }}</span>`,
});
</script>

<style scoped>
.stat-card {
  background-color: var(--color-white);
  border: 2px solid var(--color-black);
  padding: var(--spacing-lg);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: var(--color-black);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-base);
}

.stat-card:hover::before {
  transform: scaleX(1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-card.clickable {
  cursor: pointer;
}

.stat-card.clickable:active {
  transform: translateY(-2px);
}

.stat-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
}

.stat-icon {
  font-size: 1.5rem;
}

.icon-svg {
  width: 1.5rem;
  height: 1.5rem;
}

.stat-label {
  font-size: var(--font-size-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-gray-600);
  margin: 0;
}

.stat-value {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  font-family: "Courier New", monospace;
  line-height: 1;
  margin-bottom: var(--spacing-xs);
  letter-spacing: -0.02em;
}

.stat-prefix,
.stat-suffix {
  font-size: 0.6em;
  opacity: 0.8;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
}

.trend-indicator {
  font-weight: 700;
  font-size: 1.2em;
}

.trend-indicator.up {
  color: #22c55e;
}

.trend-indicator.down {
  color: #ef4444;
}

.trend-indicator.neutral {
  color: var(--color-gray-500);
}

.trend-text {
  color: var(--color-gray-600);
}

@media (max-width: 640px) {
  .stat-card {
    padding: var(--spacing-md);
  }

  .stat-value {
    font-size: 2rem;
  }
}
</style>
