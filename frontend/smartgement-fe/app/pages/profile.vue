<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <h1>Profil Saya</h1>
        <p class="subtitle">Kelola informasi akun Anda</p>
      </div>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
      </div>

      <!-- Profile Info Section -->
      <div class="profile-section">
        <h2>Informasi Akun</h2>
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-group">
            <label class="form-label">Nama</label>
            <input
              v-model="profileForm.name"
              type="text"
              class="form-input"
              placeholder="Nama Anda"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="profileForm.email"
              type="email"
              class="form-input"
              placeholder="email@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Nomor Telepon</label>
            <input
              v-model="profileForm.phone"
              type="tel"
              class="form-input"
              placeholder="08123456789"
            />
          </div>

          <button
type="submit"
            class="btn btn-primary"
            :disabled="isUpdatingProfile"
          >
            {{ isUpdatingProfile ? 'Menyimpan...' : 'Simpan Perubahan' }}
          </button>
        </form>
      </div>

      <!-- Password Change Section -->
      <div class="profile-section">
        <h2>Ubah Password</h2>
        <form @submit.prevent="changePassword" class="profile-form">
          <div class="form-group">
            <label class="form-label">Password Lama</label>
            <input
              v-model="passwordForm.currentPassword"
              type="password"
              class="form-input"
              placeholder="Masukkan password lama"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Password Baru</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              class="form-input"
              placeholder="Masukkan password baru"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Konfirmasi Password Baru</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              class="form-input"
              placeholder="Konfirmasi password baru"
              required
            />
          </div>

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="isChangingPassword"
          >
            {{ isChangingPassword ? 'Mengubah...' : 'Ubah Password' }}
          </button>
        </form>
      </div>

      <!-- Logout Button -->
      <div class="profile-section">
        <button @click="handleLogout" class="btn btn-secondary w-full">
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

const { user, logout } = useAuth()
const api = useApi()

const profileForm = ref({
  name: '',
  email: '',
  phone: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const isUpdatingProfile = ref(false)
const isChangingPassword = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Load user data
onMounted(() => {
  if (user.value) {
    profileForm.value = {
      name: user.value.name || '',
      email: user.value.email || '',
      phone: user.value.phone || ''
    }
  }
})

const updateProfile = async () => {
  try {
    isUpdatingProfile.value = true
    errorMessage.value = ''
    successMessage.value = ''

    const response = await api.put(`/users/${user.value.id}`, profileForm.value)
    
    // Update local user state
    user.value = { ...user.value, ...profileForm.value }
    
    successMessage.value = 'Profil berhasil diperbarui!'
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error: any) {
    errorMessage.value = error.data?.message || 'Gagal memperbarui profil'
  } finally {
    isUpdatingProfile.value = false
  }
}

const changePassword = async () => {
  try {
    isChangingPassword.value = true
    errorMessage.value = ''
    successMessage.value = ''

    // Validate password match
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      errorMessage.value = 'Password baru dan konfirmasi tidak cocok'
      return
    }

    // Validate password length
    if (passwordForm.value.newPassword.length < 6) {
      errorMessage.value = 'Password baru minimal 6 karakter'
      return
    }

    await api.put(`/users/${user.value.id}/password`, {
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    })
    
    successMessage.value = 'Password berhasil diubah!'
    
    // Clear password form
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error: any) {
    errorMessage.value = error.data?.message || 'Gagal mengubah password'
  } finally {
    isChangingPassword.value = false
  }
}

const handleLogout = () => {
  logout()
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  padding: var(--spacing-xl) var(--spacing-md);
  background-color: var(--color-gray-100);
}

.profile-card {
  max-width: 600px;
  margin: 0 auto;
  background-color: var(--color-white);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: var(--border-width) solid var(--color-gray-300);
}

.profile-header h1 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  color: var(--color-gray-600);
  font-size: var(--font-size-base);
}

.profile-section {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: var(--border-width) solid var(--color-gray-300);
}

.profile-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.profile-section h2 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-lg);
  color: var(--color-gray-900);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.alert {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-sm);
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: var(--border-width) solid #c3e6cb;
}

.alert-error {
  background-color: #f8d7da;
  color: #721c24;
  border: var(--border-width) solid #f5c6cb;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-container {
    padding: var(--spacing-md);
  }
  
  .profile-card {
    padding: var(--spacing-lg);
  }
  
  .profile-header h1 {
    font-size: var(--font-size-2xl);
  }
}
</style>
