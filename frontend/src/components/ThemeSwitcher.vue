<script setup lang="ts">
import { useTheme, type Theme } from '@/composables/useTheme'

const { theme, setTheme } = useTheme()

const themes: { value: Theme; label: string; emoji: string }[] = [
  { value: 'default', label: 'Default', emoji: '🎨' },
  { value: 'forest', label: 'Forest', emoji: '🌲' },
  { value: 'ocean', label: 'Ocean', emoji: '🌊' },
  { value: 'sunset', label: 'Sunset', emoji: '🌅' },
  { value: 'neon', label: 'Neon', emoji: '⚡' },
]
</script>

<template>
  <div class="theme-switcher">
    <label for="theme-select" class="theme-label">Theme:</label>
    <select
      id="theme-select"
      :value="theme"
      class="theme-select"
      @change="setTheme(($event.target as HTMLSelectElement).value as Theme)"
    >
      <option v-for="t in themes" :key="t.value" :value="t.value">
        {{ t.emoji }} {{ t.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.theme-switcher {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.theme-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-muted);
}

.theme-select {
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-select:hover {
  border-color: var(--color-primary-soft);
}

.theme-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
</style>
