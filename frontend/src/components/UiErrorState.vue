<template>
  <div class="error-state">
    <div class="error-state__icon">⚠️</div>
    <h3 class="error-state__title">{{ title }}</h3>
    <p v-if="message" class="error-state__message">{{ message }}</p>
    <UiButton v-if="retryLabel" variant="primary" @click="$emit('retry')">
      {{ retryLabel }}
    </UiButton>
  </div>
</template>

<script setup lang="ts">
import UiButton from './UiButton.vue';

withDefaults(
  defineProps<{
    title?: string;
    message?: string;
    retryLabel?: string;
  }>(),
  {
    title: 'Something went wrong',
  }
);

defineEmits<{
  retry: [];
}>();
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
  min-height: 200px;
  text-align: center;
}

.error-state__icon {
  font-size: 3rem;
  opacity: 0.8;
}

.error-state__title {
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.error-state__message {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0;
  max-width: 400px;
}
</style>
