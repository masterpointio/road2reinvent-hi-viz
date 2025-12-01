<template>
  <div class="login-callback">
    <UiSpinner v-if="isProcessing" size="lg" />
    <div v-if="!isProcessing && error" class="login-callback__error">
      <UiAlert variant="error">
        {{ error }}
      </UiAlert>
      <UiButton variant="primary" @click="retryLogin">
        Retry Login
      </UiButton>
    </div>
    <p class="login-callback__message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import UiSpinner from '../components/UiSpinner.vue';
import UiAlert from '../components/UiAlert.vue';
import UiButton from '../components/UiButton.vue';

const router = useRouter();
const { handleCallback, login } = useAuth();
const message = ref('Processing login...');
const isProcessing = ref(true);
const error = ref('');

const retryLogin = () => {
  router.push('/login');
};

onMounted(async () => {
  try {
    await handleCallback();
    message.value = 'Login successful! Redirecting...';
    setTimeout(() => {
      router.push('/app');
    }, 500);
  } catch (err) {
    isProcessing.value = false;
    const errorMessage = err instanceof Error ? err.message : 'Authentication failed';
    error.value = errorMessage;
    message.value = 'Please try logging in again.';
    console.error('Login callback error:', err);
  }
});
</script>

<style scoped>
.login-callback {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-xl);
}

.login-callback__message {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  text-align: center;
}

.login-callback__error {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  width: 100%;
  max-width: 400px;
}
</style>
