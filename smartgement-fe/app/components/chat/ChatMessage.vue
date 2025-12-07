<template>
  <div :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start', 'max-w-[80%]', message.role === 'user' ? 'self-end' : 'self-start']">
    <div :class="['p-3 rounded', message.role === 'user' ? 'bg-black text-white' : 'bg-gray-100 border border-gray-300']">
      <div v-if="message.role === 'user'" class="leading-relaxed">{{ message.content }}</div>
      <div v-else class="leading-relaxed markdown-prose" v-html="renderMarkdown(message.content)"></div>
      
      <div v-if="message.intent" class="flex gap-2 mt-1 text-sm">
        <span class="bg-gray-200 px-2 py-0.5 rounded-full capitalize text-xs">{{ message.intent }}</span>
        <span v-if="message.confidence" class="text-gray-500 text-xs">
          {{ Math.round(message.confidence * 100) }}% confident
        </span>
      </div>

      <div v-if="message.suggestedActions?.length" class="flex flex-wrap gap-1 mt-2">
        <button 
          v-for="action in message.suggestedActions" 
          :key="action"
          @click="$emit('actionClick', action,message)"
          class="px-3 py-1 bg-white border border-gray-400 rounded cursor-pointer text-sm transition-all hover:bg-gray-100 hover:border-black"
        >
          {{ action }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'

interface Message {
  role: 'user' | 'assistant'
  content: string
  intent?: string
  confidence?: number
  suggestedActions?: string[]
}

defineProps<{
  message: Message
}>()

defineEmits<{
  actionClick: [action: string, message: Message]
}>()

// Configure marked for safe rendering
marked.setOptions({
  breaks: true,
  gfm: true
})

const renderMarkdown = (content: string): string => {
  return marked.parse(content) as string
}
</script>

<style scoped>
.markdown-prose :deep(h1),
.markdown-prose :deep(h2),
.markdown-prose :deep(h3) {
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
}

.markdown-prose :deep(p) {
  margin-bottom: 0.25rem;
}

.markdown-prose :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-prose :deep(ul),
.markdown-prose :deep(ol) {
  margin: 0.25rem 0;
  padding-left: 1.5rem;
}

.markdown-prose :deep(code) {
  background-color: #e5e7eb;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 0.875rem;
}

.markdown-prose :deep(pre) {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 0.5rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin: 0.25rem 0;
}

.markdown-prose :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.markdown-prose :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.25rem 0;
}

.markdown-prose :deep(th),
.markdown-prose :deep(td) {
  border: 1px solid #d1d5db;
  padding: 0.25rem 0.5rem;
  text-align: left;
}

.markdown-prose :deep(th) {
  background-color: #e5e7eb;
  font-weight: 600;
}
</style>
