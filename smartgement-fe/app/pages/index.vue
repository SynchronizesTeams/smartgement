<template>
  <div class="page-container">
    <div class="container">
      <div class="hero">
        <h1>Smartgement</h1>
        <p class="tagline">Smart Product Management System</p>
        <div class="actions mt-4">
          <NuxtLink to="/login" class="btn btn-primary">Login</NuxtLink>
          <NuxtLink to="/register" class="btn btn-secondary">Register</NuxtLink>
          <NuxtLink to="/transactions" class="btn btn-secondary">Kasir</NuxtLink>
          <NuxtLink to="/chat" class="btn btn-secondary">AI Chat</NuxtLink>
          <NuxtLink to="/profile" class="btn btn-secondary">Profil</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero {
  text-align: center;
  padding: var(--spacing-xl) 0;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.02em;
}

.tagline {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-lg);
}

.actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}
</style>
