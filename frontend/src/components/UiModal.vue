<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="ui-modal-overlay" @click="handleOverlayClick">
        <div
          class="ui-modal"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="titleId"
          @click.stop
        >
          <div class="ui-modal__header">
            <h2 :id="titleId" class="ui-modal__title">{{ title }}</h2>
            <button
              class="ui-modal__close"
              aria-label="Close modal"
              @click="$emit('update:modelValue', false)"
            >
              ×
            </button>
          </div>
          <div class="ui-modal__content">
            <slot />
          </div>
          <div v-if="$slots.actions || primaryAction || secondaryAction" class="ui-modal__actions">
            <slot name="actions">
              <UiButton
                v-if="secondaryAction"
                variant="secondary"
                @click="secondaryAction.onClick"
              >
                {{ secondaryAction.label }}
              </UiButton>
              <UiButton
                v-if="primaryAction"
                variant="primary"
                @click="primaryAction.onClick"
              >
                {{ primaryAction.label }}
              </UiButton>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import UiButton from './UiButton.vue';

const props = defineProps<{
  modelValue: boolean;
  title: string;
  primaryAction?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  closeOnOverlayClick?: boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
}>();

const titleId = computed(() => `modal-title-${Math.random().toString(36).substr(2, 9)}`);

const handleOverlayClick = () => {
  if (props.closeOnOverlayClick !== false) {
    emit('update:modelValue', false);
  }
};
</script>

<style scoped>
.ui-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-lg);
}

.ui-modal {
  background: var(--color-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.ui-modal__header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--color-surface-soft);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ui-modal__title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text);
}

.ui-modal__close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s;
}

.ui-modal__close:hover {
  background: var(--color-surface);
  color: var(--color-text);
}

.ui-modal__content {
  padding: var(--space-lg);
  overflow-y: auto;
  flex: 1;
}

.ui-modal__actions {
  padding: var(--space-lg);
  border-top: 1px solid var(--color-surface-soft);
  display: flex;
  gap: var(--space-sm);
  justify-content: flex-end;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
