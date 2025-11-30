<template>
  <button
    :class="['ui-button', `ui-button--${variant}`, { 'ui-button--full-width': fullWidth }]"
    :type="type"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  fullWidth?: boolean;
}>();
</script>

<style scoped>
.ui-button {
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--border-radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
}

.ui-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ui-button--primary {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  border-color: var(--color-primary);
}

.ui-button--primary:hover:not(:disabled) {
  background: var(--color-primary-soft);
  border-color: var(--color-primary-soft);
}

.ui-button--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-surface-soft);
}

.ui-button--secondary:hover:not(:disabled) {
  background: var(--color-surface-soft);
}

.ui-button--ghost {
  background: transparent;
  color: var(--color-primary);
  border-color: transparent;
}

.ui-button--ghost:hover:not(:disabled) {
  background: var(--color-surface);
}

.ui-button--destructive {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.ui-button--destructive:hover:not(:disabled) {
  background: #dc2626;
  border-color: #dc2626;
}

.ui-button--full-width {
  width: 100%;
}
</style>
