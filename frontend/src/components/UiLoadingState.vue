<template>
  <div class="loading-state">
    <UiSpinner size="lg" />
    <p class="loading-state__message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import UiSpinner from './UiSpinner.vue';

withDefaults(
  defineProps<{
    message?: string;
  }>(),
  {
    message: 'Loading...',
  }
);
</script>

<style scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-lg);
  padding: var(--space-xl);
  min-height: 200px;
}

.loading-state__message {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0;
}
</style>
