<template>
  <div class="ui-card">
    <div v-if="$slots.header" class="ui-card__header">
      <slot name="header" />
    </div>
    <div class="ui-card__body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="ui-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.ui-card {
  background: var(--color-surface);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.ui-card__header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--color-surface-soft);
  font-weight: 600;
  color: var(--color-text);
}

.ui-card__body {
  padding: var(--space-lg);
}

.ui-card__footer {
  padding: var(--space-lg);
  border-top: 1px solid var(--color-surface-soft);
  display: flex;
  gap: var(--space-sm);
  justify-content: flex-end;
}
</style>
