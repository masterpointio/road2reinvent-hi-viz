<template>
  <div :class="['ui-select-wrapper', { 'ui-select-wrapper--full-width': fullWidth }]">
    <label v-if="label" :for="selectId" class="ui-select-label">
      {{ label }}
    </label>
    <select
      :id="selectId"
      :value="modelValue"
      :disabled="disabled"
      :class="['ui-select', { 'ui-select--error': error }]"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <p v-if="hint && !error" class="ui-select-hint">{{ hint }}</p>
    <p v-if="error" class="ui-select-error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

defineProps<{
  modelValue: string;
  options: Array<{ value: string; label: string }>;
  label?: string;
  placeholder?: string;
  hint?: string;
  error?: string;
  disabled?: boolean;
  fullWidth?: boolean;
}>();

defineEmits<{
  'update:modelValue': [value: string];
}>();

const selectId = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`);
</script>

<style scoped>
.ui-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.ui-select-wrapper--full-width {
  width: 100%;
}

.ui-select-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
}

.ui-select {
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  font-size: 0.875rem;
  color: var(--color-text);
  background: var(--color-bg);
  transition: all 0.2s;
  cursor: pointer;
}

.ui-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.ui-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ui-select--error {
  border-color: #ef4444;
}

.ui-select--error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.ui-select-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin: 0;
}

.ui-select-error {
  font-size: 0.75rem;
  color: #ef4444;
  margin: 0;
}
</style>
