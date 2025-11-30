<template>
  <Transition name="achievement-card">
    <div v-if="show" class="achievement-card">
      <div class="achievement-card__header">
        <div class="achievement-card__icon">🏆</div>
        <div class="achievement-card__title">Achievement Unlocked</div>
      </div>
      <div class="achievement-card__content">
        <div class="achievement-card__text">{{ achievementText }}</div>
        <div class="achievement-card__amount">${{ amount.toLocaleString() }} Burned</div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
interface Props {
  show: boolean;
  achievementText: string;
  amount: number;
}

defineProps<Props>();
</script>

<style scoped>
.achievement-card {
  background: var(--color-surface);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  box-shadow: 0 0 30px rgba(192, 255, 0, 0.3);
  animation: card-fade-in 0.5s ease-out;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.achievement-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--color-primary);
}

.achievement-card__icon {
  font-size: 2.5rem;
  flex-shrink: 0;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.6));
  animation: icon-float 3s ease-in-out infinite;
}

.achievement-card__title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.achievement-card__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.achievement-card__text {
  font-size: 0.9375rem;
  color: var(--color-text);
  line-height: 1.6;
  font-style: italic;
  flex: 1;
}

.achievement-card__amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
  text-align: center;
  padding: var(--space-md);
  background: var(--color-bg);
  border-radius: var(--border-radius-md);
  text-shadow: 0 0 10px rgba(192, 255, 0, 0.3);
}

/* Animations */
@keyframes card-fade-in {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes icon-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* Transition */
.achievement-card-enter-active {
  animation: card-fade-in 0.5s ease-out;
}

.achievement-card-leave-active {
  transition: all 0.3s ease;
}

.achievement-card-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
