<template>
  <div :class="['ui-input-wrapper', { 'ui-input-wrapper--full-width': fullWidth }]">
    <label v-if="label" :for="inputId" class="ui-input-label">
      {{ label }}
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="['ui-input', { 'ui-input--error': error }]"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="hint && !error" class="ui-input-hint">{{ hint }}</p>
    <p v-if="error" class="ui-input-error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  modelValue: string;
  label?: string;
  placeholder?: string;
  hint?: string;
  error?: string;
  type?: string;
  disabled?: boolean;
  fullWidth?: boolean;
}>();

defineEmits<{
  'update:modelValue': [value: string];
}>();

const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`);
</script>

<style scoped>
.ui-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.ui-input-wrapper--full-width {
  width: 100%;
}

.ui-input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
}

.ui-input {
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  font-size: 0.875rem;
  color: var(--color-text);
  background: var(--color-bg);
  transition: all 0.2s;
}

.ui-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.ui-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ui-input--error {
  border-color: #ef4444;
}

.ui-input--error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.ui-input-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin: 0;
}

.ui-input-error {
  font-size: 0.75rem;
  color: #ef4444;
  margin: 0;
}
</style>
