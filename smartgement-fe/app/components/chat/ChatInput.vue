<template>
  <form @submit.prevent="$emit('submit')" class="flex gap-2 p-4 border-t border-gray-300 bg-white">
    <div class="flex-1 flex gap-2 items-end sticky">
      <textarea
        ref="textareaRef"
        :value="modelValue"
        @input="handleInput"
        class="flex-1 p-2 px-4 text-base font-sans leading-relaxed border border-gray-400 rounded outline-none transition-colors resize-none min-h-[44px] max-h-[200px] overflow-y-auto focus:border-black"
        placeholder="Ketik pesan... (Enter untuk kirim, Shift+Enter untuk baris baru)"
        :disabled="isLoading"
        @keydown="handleKeyDown"
        rows="1"
      ></textarea>
      <button 
        type="submit" 
        class="p-2 px-4 min-w-[44px] h-11 bg-black text-white border-none rounded cursor-pointer font-medium transition-colors flex items-center justify-center hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="isLoading || !modelValue.trim()"
        title="Kirim pesan (Enter)"
      >
        <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span v-else class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string
  isLoading: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  submit: []
}>()

const textareaRef = ref<HTMLTextAreaElement | null>(null)

const handleInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement
  emit('update:modelValue', target.value)
  resizeTextarea()
}

const resizeTextarea = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  // Enter without Shift = send message
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    emit('submit')
  }
}

watch(() => props.modelValue, () => {
  nextTick(resizeTextarea)
})
</script>
