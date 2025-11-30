<script setup lang="ts">
interface Props {
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hover?: boolean
}

withDefaults(defineProps<Props>(), {
  padding: 'md',
  hover: false,
})
</script>

<template>
  <div :class="['card', `card-padding-${padding}`, { 'card-hover': hover }]">
    <slot />
  </div>
</template>

<style scoped>
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
}

.card-padding-none {
  padding: 0;
}

.card-padding-sm {
  padding: var(--spacing-md);
}

.card-padding-md {
  padding: var(--spacing-lg);
}

.card-padding-lg {
  padding: var(--spacing-xl);
}

.card-hover {
  transition: all 0.2s;
  cursor: pointer;
}

.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
</style>
