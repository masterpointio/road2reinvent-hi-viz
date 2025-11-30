<template>
  <Teleport to="body">
    <Transition name="achievement-popup">
      <div v-if="show" class="achievement-popup-overlay" @click="handleAccept">
        <div class="achievement-popup" @click.stop>
          <div class="achievement-popup__glow"></div>
          <div class="achievement-popup__icon">🏆</div>
          <h2 class="achievement-popup__title">Achievement Unlocked!</h2>
          <h3 class="achievement-popup__achievement-title">{{ achievementTitle }}</h3>
          <p class="achievement-popup__text">{{ achievementText }}</p>
          <div class="achievement-popup__amount">${{ amount.toLocaleString() }} Burned</div>
          <button class="achievement-popup__button" @click="handleAccept">
            Accept Your Shame
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface Props {
  show: boolean;
  achievementTitle: string;
  achievementText: string;
  amount: number;
}

interface Emits {
  (e: 'accept'): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

const handleAccept = () => {
  emit('accept');
};
</script>

<style scoped>
.achievement-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.achievement-popup {
  position: relative;
  background: var(--color-surface);
  border: 3px solid var(--color-primary);
  border-radius: var(--border-radius-lg);
  padding: 3rem;
  max-width: 600px;
  width: 90%;
  text-align: center;
  box-shadow: 0 0 60px rgba(192, 255, 0, 0.6), 0 20px 40px rgba(0, 0, 0, 0.5);
  animation: popup-bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@media (min-width: 640px) {
  .achievement-popup {
    padding: 4rem;
  }
}

.achievement-popup__glow {
  position: absolute;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: radial-gradient(circle, rgba(192, 255, 0, 0.3) 0%, transparent 70%);
  animation: pulse-glow 2s ease-in-out infinite;
  pointer-events: none;
}

.achievement-popup__icon {
  font-size: 5rem;
  margin-bottom: var(--space-md);
  animation: icon-spin 1s ease-in-out;
  filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.8));
}

.achievement-popup__title {
  color: var(--color-primary);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: var(--space-sm);
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(192, 255, 0, 0.5);
}

.achievement-popup__achievement-title {
  color: var(--color-text);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

.achievement-popup__text {
  color: var(--color-text);
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: var(--space-lg);
  font-style: italic;
}

.achievement-popup__amount {
  color: var(--color-primary);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
  text-shadow: 0 0 15px rgba(192, 255, 0, 0.5);
}

.achievement-popup__button {
  padding: var(--space-md) var(--space-xl);
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  border: none;
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.achievement-popup__button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(192, 255, 0, 0.8);
}

/* Animations */
@keyframes popup-bounce {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.1) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

@keyframes icon-spin {
  0% {
    transform: rotate(0deg) scale(0);
  }
  50% {
    transform: rotate(180deg) scale(1.2);
  }
  100% {
    transform: rotate(360deg) scale(1);
  }
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

/* Transition */
.achievement-popup-enter-active,
.achievement-popup-leave-active {
  transition: opacity 0.3s ease;
}

.achievement-popup-enter-from,
.achievement-popup-leave-to {
  opacity: 0;
}

.achievement-popup-enter-active .achievement-popup {
  animation: popup-bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.achievement-popup-leave-active .achievement-popup {
  animation: popup-bounce 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) reverse;
}
</style>
