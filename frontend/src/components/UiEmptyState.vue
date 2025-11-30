<template>
  <div class="empty-state">
    <div class="empty-state__icon">{{ icon }}</div>
    <h3 class="empty-state__title">{{ title }}</h3>
    <p v-if="message" class="empty-state__message">{{ message }}</p>
    <UiButton v-if="actionLabel" variant="primary" @click="$emit('action')">
      {{ actionLabel }}
    </UiButton>
  </div>
</template>

<script setup lang="ts">
import UiButton from './UiButton.vue';

withDefaults(
  defineProps<{
    title: string;
    message?: string;
    actionLabel?: string;
    icon?: string;
  }>(),
  {
    icon: '📭',
  }
);

defineEmits<{
  action: [];
}>();
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  padding: var(--space-xl);
  min-height: 200px;
  text-align: center;
}

.empty-state__icon {
  font-size: 3rem;
  opacity: 0.8;
}

.empty-state__title {
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.empty-state__message {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0;
  max-width: 400px;
}
</style>
