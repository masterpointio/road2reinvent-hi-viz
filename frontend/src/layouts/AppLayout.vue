<template>
  <div class="app-layout">
    <nav class="app-layout__nav">
      <div class="app-layout__nav-content">
        <BillBurnerLogo size="compact" />
        <nav class="app-layout__nav-links">
          <router-link to="/app/dashboard" class="app-layout__nav-link">
            🔥 Dashboard
          </router-link>
          <router-link to="/app/burn-config" class="app-layout__nav-link">
            ⚙️ Configure Burn
          </router-link>
        </nav>
        <div class="app-layout__nav-actions">
          <div class="app-layout__theme-menu">
            <button class="app-layout__theme-btn" @click="toggleThemeMenu">
              🎨
            </button>
            <div v-if="showThemeMenu" class="app-layout__theme-dropdown">
              <button
                v-for="theme in themes"
                :key="theme.value"
                :class="['app-layout__theme-item', { 'app-layout__theme-item--active': currentTheme === theme.value }]"
                @click="selectTheme(theme.value)"
              >
                {{ theme.label }}
              </button>
            </div>
          </div>
          <div class="app-layout__user-menu">
            <button class="app-layout__user-btn" @click="toggleUserMenu">
              👤
            </button>
            <div v-if="showUserMenu" class="app-layout__user-dropdown">
              <div class="app-layout__user-info">
                <div class="app-layout__user-email">{{ user?.email || 'User' }}</div>
              </div>
              <button class="app-layout__menu-item" @click="handleLogout">
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <main class="app-layout__main">
      <router-view />
    </main>
    <UiToastContainer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useTheme, type Theme } from '../composables/useTheme';
import { useAuth } from '../composables/useAuth';
import UiToastContainer from '../components/UiToastContainer.vue';
import BillBurnerLogo from '../components/BillBurnerLogo.vue';

const router = useRouter();
const { currentTheme, setTheme } = useTheme();
const { user, logout } = useAuth();

const showUserMenu = ref(false);
const showThemeMenu = ref(false);

const themes = [
  { value: 'default', label: 'Hi-Viz' },
  { value: 'neon', label: 'Neon' },
  { value: 'ocean', label: 'Ocean' },
  { value: 'forest', label: 'Forest' },
  { value: 'sunset', label: 'Sunset' },
];

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
  showThemeMenu.value = false;
};

const toggleThemeMenu = () => {
  showThemeMenu.value = !showThemeMenu.value;
  showUserMenu.value = false;
};

const selectTheme = (theme: string) => {
  setTheme(theme as Theme);
  showThemeMenu.value = false;
};

const handleLogout = async () => {
  await logout();
  showUserMenu.value = false;
  router.push('/login');
};

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.app-layout__user-menu')) {
    showUserMenu.value = false;
  }
  if (!target.closest('.app-layout__theme-menu')) {
    showThemeMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.app-layout__nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-surface-soft);
  box-shadow: var(--shadow-sm);
}

.app-layout__nav-content {
  padding: var(--space-sm) var(--space-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-md);
}

.app-layout__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.app-layout__nav-links {
  display: none;
  gap: var(--space-xs);
  flex: 1;
  justify-content: center;
}

.app-layout__nav-link {
  padding: var(--space-xs) var(--space-md);
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: var(--border-radius-md);
  transition: all 0.2s;
  white-space: nowrap;
}

.app-layout__nav-link:hover {
  color: var(--color-text);
  background: var(--color-surface-soft);
}

.app-layout__nav-link.router-link-active {
  color: var(--color-primary);
  background: var(--color-surface-soft);
}

.app-layout__nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;
}

.app-layout__theme-btn,
.app-layout__user-btn {
  background: none;
  border: none;
  font-size: 1.125rem;
  cursor: pointer;
  padding: var(--space-xs);
  border-radius: var(--border-radius-md);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  min-height: 2rem;
}

.app-layout__theme-btn:hover,
.app-layout__user-btn:hover {
  background: var(--color-surface-soft);
}

.app-layout__theme-menu {
  position: relative;
}

.app-layout__theme-dropdown {
  position: absolute;
  top: calc(100% + var(--space-sm));
  right: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  min-width: 150px;
  z-index: 100;
  overflow: hidden;
}

.app-layout__theme-item {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  background: none;
  border: none;
  text-align: left;
  font-size: 0.875rem;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.2s;
  display: block;
}

.app-layout__theme-item:hover {
  background: var(--color-surface-soft);
}

.app-layout__theme-item--active {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  font-weight: 600;
}

.app-layout__theme-item--active:hover {
  background: var(--color-primary-soft);
}

.app-layout__user-menu {
  position: relative;
}

.app-layout__user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-sm));
  right: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  min-width: 200px;
  z-index: 100;
}

.app-layout__user-info {
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-surface-soft);
}

.app-layout__user-email {
  font-size: 0.875rem;
  color: var(--color-text);
  font-weight: 500;
  word-break: break-word;
}

.app-layout__menu-item {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  background: none;
  border: none;
  text-align: left;
  font-size: 0.875rem;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.2s;
}

.app-layout__menu-item:hover {
  background: var(--color-surface-soft);
}

.app-layout__main {
  flex: 1;
  width: 100%;
  padding: var(--space-md);
}

@media (min-width: 640px) {
  .app-layout__nav-content {
    padding: var(--space-md) var(--space-lg);
  }

  .app-layout__title {
    font-size: 1.25rem;
  }

  .app-layout__nav-links {
    display: flex;
  }

  .app-layout__nav-link {
    font-size: 0.875rem;
  }

  .app-layout__theme-btn,
  .app-layout__user-btn {
    font-size: 1.25rem;
    padding: var(--space-sm);
  }

  .app-layout__nav-actions {
    gap: var(--space-sm);
  }

  .app-layout__main {
    padding: var(--space-lg);
  }
}

@media (min-width: 768px) {
  .app-layout__main {
    padding: var(--space-xl);
  }
}

@media (min-width: 1024px) {
  .app-layout__nav-content {
    max-width: 1400px;
    margin: 0 auto;
  }

  .app-layout__nav-actions {
    gap: var(--space-md);
  }

  .app-layout__main {
    max-width: 1400px;
    margin: 0 auto;
  }
}
</style>
