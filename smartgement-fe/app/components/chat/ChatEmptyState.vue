<template>
  <div class="text-center p-8 text-gray-600">
    <p class="mb-2">👋 Hello! I'm your AI assistant for product management.</p>
    <p class="mb-6">Ask me about products, trends, risks, or use automation commands.</p>
    <div class="flex flex-wrap gap-2 justify-center">
      <button 
        @click="$emit('sync')"
        class="px-4 py-2 bg-gray-100 border border-gray-300 rounded cursor-pointer text-sm transition-all hover:bg-gray-200 hover:border-gray-400"
      >
        🔄 Sync AI Data
      </button>
      <button 
        v-for="prompt in prompts" 
        :key="prompt"
        @click="$emit('promptClick', prompt)"
        class="px-4 py-2 bg-gray-100 border border-gray-300 rounded cursor-pointer text-sm transition-all hover:bg-gray-200 hover:border-gray-400"
      >
        {{ prompt }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  prompts: string[]
}>()

defineEmits<{
  promptClick: [prompt: string]
  sync: []
}>()
</script>
