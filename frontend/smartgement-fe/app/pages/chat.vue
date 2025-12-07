<template>
<AppNavbar>
      <template #page-title>
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">Dashboard</span>
      </template>
    </AppNavbar>
  <div class="chat-container">
    <div class="chat-header">
      <h1>AI Assistant</h1>
      <p class="subtitle">Smart Product Management Chatbot</p>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <p>👋 Hello! I'm your AI assistant for product management.</p>
        <p>Ask me about products, trends, risks, or use automation commands.</p>
        <div class="suggested-prompts">
          <button 
            @click="syncAI"
            class="prompt-btn sync-btn"
          >
            🔄 Sync AI Data
          </button>
          <button 
            v-for="prompt in suggestedPrompts" 
            :key="prompt"
            @click="sendMessage(prompt)"
            class="prompt-btn"
          >
            {{ prompt }}
          </button>
        </div>
      </div>

      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        :class="['message', msg.role]"
      >
        <div class="message-content">
          <div v-if="msg.role === 'user'" class="message-text">{{ msg.content }}</div>
          <div v-else class="message-text markdown-body" v-html="renderMarkdown(msg.content)"></div>
          
          <div v-if="msg.intent" class="message-meta">
            <span class="intent-badge">{{ msg.intent }}</span>
            <span v-if="msg.confidence" class="confidence">
              {{ Math.round(msg.confidence * 100) }}% confident
            </span>
          </div>

          <div v-if="msg.suggestedActions?.length" class="suggested-actions">
            <button 
              v-for="action in msg.suggestedActions" 
              :key="action"
              @click="handleSuggestedAction(action, msg)"
              class="action-btn"
            >
              {{ action }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant">
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="chat-input-form">
      <div class="input-wrapper">
        <textarea
          ref="textareaRef"
          v-model="inputMessage"
          class="chat-input"
          placeholder="Ketik pesan... (Enter untuk kirim, Shift+Enter untuk baris baru)"
          :disabled="isLoading"
          @keydown="handleKeyDown"
          rows="1"
        ></textarea>
        <button 
          type="submit" 
          class="send-btn" 
          :disabled="isLoading || !inputMessage.trim()"
          title="Kirim pesan (Enter)"
        >
          <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span v-else class="loading-spinner"></span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'

definePageMeta({
  middleware: 'auth'
})

interface Message {
  role: 'user' | 'assistant'
  content: string
  intent?: string
  confidence?: number
  suggestedActions?: string[]
}

const inputMessage = ref('')
const messages = ref<Message[]>([])
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const currentContext = ref<Record<string, any>>({})
const lastAutomationCommand = ref<string>('')  // Track last automation command

const api = useApi()

// Configure marked for safe rendering
marked.setOptions({
  breaks: true,
  gfm: true
})

const suggestedPrompts = [
  'Tampilkan semua produk saya',
  'Tambahkan produk Roti Tawar harga 15000 stok 50',
  'Produk apa yang berisiko tinggi?',
  'Kosongkan semua produk expired'
]

// Auto-resize textarea
const resizeTextarea = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
  }
}

// Watch for input changes to resize
watch(inputMessage, () => {
  nextTick(resizeTextarea)
})

// Handle keyboard shortcuts
const handleKeyDown = (event: KeyboardEvent) => {
  // Enter without Shift = send message
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSubmit()
  }
  // Shift+Enter = new line (default behavior, do nothing)
}

const renderMarkdown = (content: string): string => {
  return marked.parse(content) as string
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Handle suggested action clicks
const handleSuggestedAction = async (action: string, relatedMessage: any) => {
  const actionLower = action.toLowerCase()
  
  // Check if this is an automation execution action
  if (actionLower.includes('eksekusi') || actionLower.includes('execute')) {
    // This is an automation execution request
    await executeAutomation()
  } else if (actionLower.includes('batal') || actionLower.includes('cancel')) {
    // Clear automation context
    lastAutomationCommand.value = ''
    messages.value.push({
      role: 'assistant',
      content: 'Operasi dibatalkan.',
      intent: 'system'
    })
    scrollToBottom()
  } else {
    // Regular action - send as message
    sendMessage(action)
  }
}

// Execute automation
const executeAutomation = async () => {
  if (!lastAutomationCommand.value) {
    messages.value.push({
      role: 'assistant',
      content: '❌ Tidak ada operasi automasi yang bisa dieksekusi.',
      intent: 'error'
    })
    scrollToBottom()
    return
  }

  try {
    const { user } = useAuth()
    
    if (!user.value?.id) {
      throw new Error('User not authenticated')
    }
    
    const merchantId = user.value.id
    const config = useRuntimeConfig()
    const aiBase = config.public.aiBase
    
    isLoading.value = true
    
    const response = await $fetch<any>(`${aiBase}/chatbot/automation/execute`, {
      method: 'POST',
      body: {
        merchant_id: String(merchantId),
        command: lastAutomationCommand.value,
        confirmed: true
      }
    })
    
    messages.value.push({
      role: 'assistant',
      content: `✅ ${response.message}\n\nOperasi berhasil dieksekusi pada ${response.affected_count} produk.`,
      intent: 'system',
      suggestedActions: response.can_undo ? ['Undo operasi ini', 'Lihat produk'] : ['Lihat produk']
    })
    
    // Clear automation command after execution
    lastAutomationCommand.value = ''
  } catch (error) {
    console.error('Execute automation error:', error)
    messages.value.push({
      role: 'assistant',
      content: '❌ Gagal mengeksekusi automasi. Silakan coba lagi.',
      intent: 'error'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const sendMessage = async (content: string) => {
  if (!content.trim()) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: content.trim()
  })
  
  inputMessage.value = ''
  isLoading.value = true

  try {
    const { user } = useAuth()
    
    // Use authenticated user's ID
    if (!user.value?.id) {
      throw new Error('User not authenticated')
    }
    
    const merchantId = user.value.id
    
    // Get last 7 messages for conversation context (excluding the current one)
    const conversationHistory = messages.value
      .slice(-8, -1) // Get last 7 messages (excluding the one just added)
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }))
    
    // Direct fetch to AI service
    const config = useRuntimeConfig()
    const aiBase = config.public.aiBase
    
    const response = await $fetch<any>(`${aiBase}/chatbot/message`, {
        method: 'POST',
        body: {
            merchant_id: String(merchantId),
            message: content.trim(),
            conversation_history: conversationHistory, // Send last 7 messages
            context: currentContext.value
        }
    })
    
    // Update context for next turn
    if (response.context) {
        currentContext.value = response.context
    }
    
    // Check if context was cleared (e.g. after execution)
    if (response.context === null) {
        currentContext.value = {}
    }

    messages.value.push({
      role: 'assistant',
      content: response.response || 'No response received',
      intent: response.intent,
      confidence: response.confidence,
      suggestedActions: response.suggested_actions
    })
    
    // Save automation command if this was an automation intent
    if (response.intent === 'automation') {
      lastAutomationCommand.value = content.trim()
    }
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({
      role: 'assistant',
      content: '❌ Maaf, terjadi kesalahan. Silakan login ulang atau coba lagi.',
      intent: 'error'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const handleSubmit = () => {
  if (inputMessage.value.trim()) {
    sendMessage(inputMessage.value)
    // Reset textarea height
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.style.height = 'auto'
      }
    })
  }
}

const syncAI = async () => {
    try {
        const { user } = useAuth()
        
        if (!user.value?.id) {
            throw new Error('User not authenticated')
        }
        
        const merchantId = user.value.id
        const config = useRuntimeConfig()
        const aiBase = config.public.aiBase
        
        isLoading.value = true
        const response = await $fetch<any>(`${aiBase}/chatbot/automation/sync?merchant_id=${merchantId}`, {
            method: 'POST'
        })
        
        messages.value.push({
            role: 'assistant',
            content: `✅ ${response.message}`,
            intent: 'system'
        })
    } catch (error) {
        console.error('Sync error:', error)
         messages.value.push({
            role: 'assistant',
            content: `❌ Sync gagal. Silakan coba lagi.`,
            intent: 'error'
        })
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  background-color: var(--color-white);
}

.chat-header {
  padding: var(--spacing-lg);
  border-bottom: var(--border-width) solid var(--color-gray-300);
  text-align: center;
}

.chat-header h1 {
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  color: var(--color-gray-600);
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--color-gray-600);
}

.empty-state p {
  margin-bottom: var(--spacing-sm);
}

.suggested-prompts {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.prompt-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--color-gray-100);
  border: var(--border-width) solid var(--color-gray-300);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
}

.prompt-btn:hover {
  background-color: var(--color-gray-200);
  border-color: var(--color-gray-400);
}

.message {
  display: flex;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
}

.message.user .message-content {
  background-color: var(--color-black);
  color: var(--color-white);
}

.message.assistant .message-content {
  background-color: var(--color-gray-100);
  border: var(--border-width) solid var(--color-gray-300);
}

.message-text {
  line-height: 1.5;
}

/* Markdown content styling */
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin-top: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}

.markdown-body :deep(p) {
  margin-bottom: var(--spacing-xs);
}

.markdown-body :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: var(--spacing-xs) 0;
  padding-left: var(--spacing-lg);
}

.markdown-body :deep(code) {
  background-color: var(--color-gray-200);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  font-size: var(--font-size-sm);
}

.markdown-body :deep(pre) {
  background-color: var(--color-gray-900);
  color: var(--color-gray-100);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
  overflow-x: auto;
  margin: var(--spacing-xs) 0;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--color-gray-400);
  padding-left: var(--spacing-sm);
  margin: var(--spacing-xs) 0;
  color: var(--color-gray-600);
}

.markdown-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: var(--spacing-xs) 0;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: var(--border-width) solid var(--color-gray-300);
  padding: var(--spacing-xs) var(--spacing-sm);
  text-align: left;
}

.markdown-body :deep(th) {
  background-color: var(--color-gray-200);
  font-weight: 600;
}

.message-meta {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-sm);
}

.intent-badge {
  background-color: var(--color-gray-200);
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: capitalize;
}

.confidence {
  color: var(--color-gray-500);
}

.suggested-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-sm);
}

.action-btn {
  padding: 4px 12px;
  background-color: var(--color-white);
  border: var(--border-width) solid var(--color-gray-400);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-black);
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: var(--spacing-xs) 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: var(--color-gray-400);
  border-radius: 50%;
  animation: typing 1.4s infinite both;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-4px);
  }
}

.chat-input-form {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border-top: var(--border-width) solid var(--color-gray-300);
  background-color: var(--color-white);
}

.input-wrapper {
  flex: 1;
  display: flex;
  gap: var(--spacing-sm);
  align-items: flex-end;
  position:sticky;
}

.chat-input {
  flex: 1;
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-base);
  font-family: var(--font-family);
  line-height: 1.5;
  border: var(--border-width) solid var(--color-gray-400);
  border-radius: var(--border-radius);
  outline: none;
  transition: border-color var(--transition-fast);
  resize: none;
  min-height: 44px;
  max-height: 200px;
  overflow-y: auto;
}

.chat-input:focus {
  border-color: var(--color-black);
}

.chat-input::placeholder {
  color: var(--color-gray-500);
}

.send-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  min-width: 44px;
  height: 44px;
  background-color: var(--color-black);
  color: var(--color-white);
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 500;
  transition: background-color var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover:not(:disabled) {
  background-color: var(--color-gray-800);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-white);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .chat-container {
    max-width: 100%;
  }
  
  .message {
    max-width: 90%;
  }
  
  .chat-header h1 {
    font-size: 1.5rem;
  }
}
</style>
