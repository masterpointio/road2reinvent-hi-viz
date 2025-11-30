<template>
  <div :class="['ui-alert', `ui-alert--${variant}`]" role="alert">
    <div class="ui-alert__icon">{{ icon }}</div>
    <div class="ui-alert__content">
      <slot />
    </div>
    <button
      v-if="dismissible"
      class="ui-alert__close"
      aria-label="Dismiss alert"
      @click="$emit('dismiss')"
    >
      ×
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  variant?: 'info' | 'success' | 'warning' | 'error';
  dismissible?: boolean;
}>();

defineEmits<{
  dismiss: [];
}>();

const icon = computed(() => {
  switch (props.variant) {
    case 'success':
      return '✓';
    case 'warning':
      return '⚠';
    case 'error':
      return '✕';
    default:
      return 'ℹ';
  }
});
</script>

<style scoped>
.ui-alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--border-radius-md);
  border: 1px solid;
}

.ui-alert__icon {
  font-size: 1.25rem;
  font-weight: bold;
  flex-shrink: 0;
}

.ui-alert__content {
  flex: 1;
  font-size: 0.875rem;
}

.ui-alert__close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s;
  flex-shrink: 0;
}

.ui-alert--info {
  background: var(--info-bg);
  border-color: var(--info-border);
  color: var(--text-on-info);
}

.ui-alert--info .ui-alert__close:hover {
  background: var(--info-muted);
}

.ui-alert--success {
  background: var(--success-bg);
  border-color: var(--success-border);
  color: var(--text-on-success);
}

.ui-alert--success .ui-alert__close:hover {
  background: var(--success-muted);
}

.ui-alert--warning {
  background: var(--warning-bg);
  border-color: var(--warning-border);
  color: var(--text-on-warning);
}

.ui-alert--warning .ui-alert__close:hover {
  background: var(--warning-muted);
}

.ui-alert--error {
  background: var(--danger-bg);
  border-color: var(--danger-border);
  color: var(--text-on-danger);
}

.ui-alert--error .ui-alert__close:hover {
  background: var(--danger-muted);
}
</style>
