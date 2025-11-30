<template>
  <div class="form-section">
    <div class="form-section__fields">
      <slot />
    </div>
    <div v-if="$slots.actions" class="form-section__actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.form-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  max-width: 600px;
}

.form-section__fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.form-section__actions {
  display: flex;
  gap: var(--space-sm);
  justify-content: flex-end;
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-surface-soft);
}
</style>
