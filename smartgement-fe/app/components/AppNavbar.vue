<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="navbar-container">
      <div class="navbar-brand">
        <NuxtLink to="/dashboard" class="logo-link">
          Smart<span class="logo-highlight">gement</span>
        </NuxtLink>
        <slot name="page-title">
          <span class="page-badge">Dashboard</span>
        </slot>
      </div>

      <div class="navbar-nav desktop-nav">
        <NuxtLink to="/dashboard" class="nav-link" active-class="active">
          Products
        </NuxtLink>
        <NuxtLink to="/transactions" class="nav-link" active-class="active">
          Transactions
        </NuxtLink>
        <NuxtLink to="/chat" class="nav-link" active-class="active">
          AI Chat
        </NuxtLink>

        <NuxtLink v-if="user" to="/profile" class="user-profile">
          <div class="user-avatar">
            {{ userInitial }}
          </div>
          <span class="user-name">{{ user.username || "User" }}</span>
        </NuxtLink>

        <button @click="handleLogout" class="btn-logout">Logout</button>
      </div>

      <button
        @click="toggleMobileMenu"
        class="mobile-menu-btn"
        aria-label="Toggle menu"
      >
        <span :class="{ open: isMobileMenuOpen }"></span>
        <span :class="{ open: isMobileMenuOpen }"></span>
        <span :class="{ open: isMobileMenuOpen }"></span>
      </button>
    </div>

    <div class="mobile-nav" :class="{ open: isMobileMenuOpen }">
      <NuxtLink
        to="/dashboard"
        class="mobile-nav-link"
        @click="closeMobileMenu"
      >
        Products
      </NuxtLink>
      <NuxtLink
        to="/transactions"
        class="mobile-nav-link"
        @click="closeMobileMenu"
      >
        Transactions
      </NuxtLink>
      <NuxtLink to="/chat" class="mobile-nav-link" @click="closeMobileMenu">
        AI Chat
      </NuxtLink>
      <NuxtLink
        v-if="user"
        to="/profile"
        class="mobile-nav-link"
        @click="closeMobileMenu"
      >
        Profile
      </NuxtLink>
      <button @click="handleLogout" class="mobile-nav-link logout-btn">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
const { user, logout } = useAuth();
const router = useRouter();

const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);

const userInitial = computed(() => {
  if (!user.value?.username) return "?";
  return user.value.username.charAt(0).toUpperCase();
});

const handleLogout = () => {
  logout();
  isMobileMenuOpen.value = false;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

// Handle scroll effect
onMounted(() => {
  const handleScroll = () => {
    isScrolled.value = window.scrollY > 10;
  };
  window.addEventListener("scroll", handleScroll);

  onUnmounted(() => {
    window.removeEventListener("scroll", handleScroll);
  });
});
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--color-white);
  border-bottom: 2px solid var(--color-black);
  transition: all var(--transition-base);
}

.navbar.scrolled {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.logo-link {
  font-size: 1.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.03em;
  text-decoration: none;
  color: var(--color-black);
  transition: opacity var(--transition-fast);
}

.logo-link:hover {
  opacity: 0.7;
}

.logo-highlight {
  position: relative;
}

.page-badge {
  padding: 0.25rem 0.75rem;
  background-color: var(--color-black);
  color: var(--color-white);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-link {
  position: relative;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  color: var(--color-black);
  padding: 0.5rem 0;
  transition: color var(--transition-fast);
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-black);
  transition: width var(--transition-base);
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.nav-link:hover {
  color: var(--color-gray-700);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  text-decoration: none;
  color: var(--color-black);
  border-radius: var(--border-radius);
  transition: background-color var(--transition-fast);
}

.user-profile:hover {
  background-color: var(--color-gray-100);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: var(--color-black);
  color: var(--color-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
}

.user-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-logout {
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: transparent;
  color: var(--color-black);
  border: 2px solid var(--color-black);
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-logout:hover {
  background-color: var(--color-black);
  color: var(--color-white);
  transform: translateY(-2px);
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs);
}

.mobile-menu-btn span {
  width: 25px;
  height: 3px;
  background-color: var(--color-black);
  transition: all var(--transition-base);
}

.mobile-menu-btn span.open:nth-child(1) {
  transform: rotate(45deg) translateY(8px);
}

.mobile-menu-btn span.open:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn span.open:nth-child(3) {
  transform: rotate(-45deg) translateY(-8px);
}

/* Mobile Navigation */
.mobile-nav {
  display: none;
  flex-direction: column;
  max-height: 0;
  overflow: hidden;
  transition: max-height var(--transition-base);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-gray-300);
}

.mobile-nav.open {
  max-height: 400px;
  padding: var(--spacing-md) 0;
}

.mobile-nav-link {
  padding: var(--spacing-md) var(--spacing-lg);
  text-decoration: none;
  color: var(--color-black);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  transition: all var(--transition-fast);
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  width: 100%;
}

.mobile-nav-link:hover {
  background-color: var(--color-gray-100);
  padding-left: calc(var(--spacing-lg) + 0.5rem);
}

.mobile-nav-link.logout-btn {
  color: var(--color-black);
  font-weight: 700;
  margin-top: var(--spacing-sm);
  border-top: 1px solid var(--color-gray-300);
  padding-top: var(--spacing-md);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-nav {
    display: flex;
  }
}

@media (max-width: 640px) {
  .navbar-container {
    padding: var(--spacing-sm) var(--spacing-md);
  }

  .logo-link {
    font-size: 1.5rem;
  }

  .page-badge {
    font-size: 0.625rem;
    padding: 0.2rem 0.5rem;
  }
}
</style>
