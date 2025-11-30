<template>
  <div :class="['ui-spinner', `ui-spinner--${size}`]" role="status" aria-label="Loading">
    <div class="ui-spinner__circle"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  size?: 'sm' | 'md' | 'lg';
}>();
</script>

<style scoped>
.ui-spinner {
  display: inline-block;
}

.ui-spinner--sm {
  width: 1rem;
  height: 1rem;
}

.ui-spinner--md {
  width: 1.5rem;
  height: 1.5rem;
}

.ui-spinner--lg {
  width: 2rem;
  height: 2rem;
}

.ui-spinner__circle {
  width: 100%;
  height: 100%;
  border: 2px solid var(--color-surface-soft);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
