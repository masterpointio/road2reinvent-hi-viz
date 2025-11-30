<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast--${toast.type}`]"
          role="alert"
        >
          <div class="toast__icon">{{ getIcon(toast.type) }}</div>
          <div class="toast__message">{{ toast.message }}</div>
          <button
            class="toast__close"
            aria-label="Close notification"
            @click="clearToast(toast.id)"
          >
            ×
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToasts } from '../composables/useToasts';
import type { Toast } from '../composables/useToasts';

const { toasts, clearToast } = useToasts();

const getIcon = (type: Toast['type']): string => {
  switch (type) {
    case 'success':
      return '✓';
    case 'warning':
      return '⚠';
    case 'error':
      return '✕';
    default:
      return 'ℹ';
  }
};
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: var(--space-lg);
  right: var(--space-lg);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  max-width: 400px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  border: 1px solid;
  pointer-events: auto;
  min-width: 300px;
}

.toast__icon {
  font-size: 1.25rem;
  font-weight: bold;
  flex-shrink: 0;
}

.toast__message {
  flex: 1;
  font-size: 0.875rem;
  line-height: 1.5;
}

.toast__close {
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
  opacity: 0.7;
}

.toast__close:hover {
  opacity: 1;
}

.toast--info {
  background: var(--info-bg);
  border-color: var(--info-border);
  color: var(--text-on-info);
}

.toast--info .toast__close:hover {
  background: var(--info-muted);
}

.toast--success {
  background: var(--success-bg);
  border-color: var(--success-border);
  color: var(--text-on-success);
}

.toast--success .toast__close:hover {
  background: var(--success-muted);
}

.toast--warning {
  background: var(--warning-bg);
  border-color: var(--warning-border);
  color: var(--text-on-warning);
}

.toast--warning .toast__close:hover {
  background: var(--warning-muted);
}

.toast--error {
  background: var(--danger-bg);
  border-color: var(--danger-border);
  color: var(--text-on-danger);
}

.toast--error .toast__close:hover {
  background: var(--danger-muted);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
