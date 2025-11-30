<template>
  <div class="login">
    <div class="login__content">
      <h2 class="login__title">Welcome to R2R App</h2>
      <p class="login__description">Sign in to access your dashboard</p>
      <UiButton variant="primary" full-width @click="handleLogin">
        Sign in with Cognito
      </UiButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../composables/useAuth';
import UiButton from '../components/UiButton.vue';

const { login } = useAuth();

const handleLogin = () => {
  login();
};
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xl);
}

.login__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  width: 100%;
}

.login__title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
  text-align: center;
}

.login__description {
  margin: 0;
  color: var(--color-text-muted);
  text-align: center;
  font-size: 0.875rem;
}
</style>
