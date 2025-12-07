<template>
  <nav class="border-b-2 border-black p-4 flex justify-between items-center sticky top-0 bg-white z-10">
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard" class="text-2xl font-bold uppercase tracking-tighter hover:opacity-80 transition-opacity">
        Smartgement
      </NuxtLink>
      <slot name="page-title">
        <span class="px-2 py-0.5 bg-black text-white text-xs font-bold uppercase">Dashboard</span>
      </slot>
    </div>
    
    <div class="flex items-center gap-6 text-sm font-medium uppercase tracking-wide">
      <NuxtLink to="/dashboard" class="hover:underline decoration-2 underline-offset-4">
        Products
      </NuxtLink>
      <NuxtLink to="/chat" class="hover:underline decoration-2 underline-offset-4">
        AI Chat
      </NuxtLink>
      
      <!-- User Profile Link -->
      <NuxtLink 
        v-if="user" 
        to="/profile" 
        class="flex items-center gap-2 hover:bg-gray-100 px-3 py-2 rounded transition-colors"
      >
        <div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">
          {{ userInitial }}
        </div>
        <span class="font-semibold">{{ user.username || 'User' }}</span>
      </NuxtLink>
      
      <button 
        @click="handleLogout" 
        class="hover:bg-black hover:text-white px-3 py-1 transition-colors border border-black"
      >
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
const { user, logout } = useAuth()
const router = useRouter()

const userInitial = computed(() => {
  if (!user.value?.username) return '?'
  return user.value.username.charAt(0).toUpperCase()
})

const handleLogout = () => {
  logout()
}
</script>
