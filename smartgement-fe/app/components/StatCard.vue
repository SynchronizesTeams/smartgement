<template>
  <div
    class="relative bg-white border-2 border-black p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl overflow-hidden group"
    :class="{ 'cursor-pointer': clickable }"
  >
    <div
      class="absolute top-0 left-0 right-0 h-1 bg-black scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"
    ></div>

    <div class="flex items-center gap-2 mb-3">
      <div v-if="icon" class="text-2xl">
        <Icon :name="icon" class="w-6 h-6" />
      </div>
      <p class="text-sm font-bold uppercase tracking-wide text-gray-600">
        {{ label }}
      </p>
    </div>

    <p
      class="text-4xl md:text-5xl font-extrabold font-mono leading-none mb-2 tracking-tight"
    >
      <span v-if="prefix" class="text-2xl opacity-80">{{ prefix }}</span>
      <AnimatedNumber
        v-if="animated && typeof value === 'number'"
        :value="value"
        :duration="animationDuration"
      />
      <span v-else>{{ formattedValue }}</span>
      <span v-if="suffix" class="text-2xl opacity-80">{{ suffix }}</span>
    </p>

    <div v-if="trend" class="flex items-center gap-2 text-sm">
      <span
        class="font-bold text-lg"
        :class="{
          'text-green-500': trendDirection === 'up',
          'text-red-500': trendDirection === 'down',
          'text-gray-500': trendDirection === 'neutral',
        }"  
      >
        {{
          trendDirection === "up" ? "↑" : trendDirection === "down" ? "↓" : "→"
        }}
      </span>
      <span class="text-gray-600">{{ trend }}</span>
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
    return props.value.toLocaleString("id-ID");
  }
  return props.value;
});
</script>

<script lang="ts">
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
    let animationFrameId: number | null = null;

    const animateToValue = (targetValue: number) => {
      // Only animate in browser (client-side)
      if (process.server) {
        displayValue.value = targetValue;
        return;
      }

      // Cancel any ongoing animation
      if (animationFrameId !== null) {
        cancelAnimationFrame(animationFrameId);
      }

      const start = displayValue.value;
      const end = targetValue;
      const startTime = Date.now();

      const animate = () => {
        const now = Date.now();
        const progress = Math.min((now - startTime) / props.duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        displayValue.value = Math.round(start + (end - start) * easeOut);

        if (progress < 1) {
          animationFrameId = requestAnimationFrame(animate);
        } else {
          animationFrameId = null;
        }
      };

      animationFrameId = requestAnimationFrame(animate);
    };

    // Watch for value changes
    watch(
      () => props.value,
      (newValue) => {
        animateToValue(newValue);
      },
      { immediate: true }
    );

    return () => h('span', displayValue.value.toLocaleString('id-ID'));
  },
});
</script>
