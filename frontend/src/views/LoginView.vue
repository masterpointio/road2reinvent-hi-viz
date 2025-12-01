<template>
  <div class="login-view">
    <div class="login-card">
      <div class="login-card__header">
        <BillBurnerLogo class="login-card__logo" />
        <h1>Welcome to Bill Burner</h1>
        <p class="login-card__subtitle">Sign in to start burning money</p>
      </div>

      <div class="login-card__content">
        <div v-if="!hasCognitoConfig" class="demo-notice">
          <p>⚠️ Cognito not configured</p>
          <p class="demo-notice__text">Set VITE_COGNITO_DOMAIN and VITE_COGNITO_CLIENT_ID</p>
        </div>

        <UiButton variant="primary" size="large" @click="handleLogin" class="login-button">
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </UiButton>

        <div class="login-card__footer">
          <p>Don't have an account? <a href="#" @click.prevent="handleSignUp">Sign up</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { config } from '../config';
import BillBurnerLogo from '../components/BillBurnerLogo.vue';
import UiButton from '../components/UiButton.vue';

const isLoading = ref(false);
const hasCognitoConfig = ref(false);

onMounted(() => {
  hasCognitoConfig.value = !!(config.cognitoLoginUrl || config.cognitoDomain);
});

const handleLogin = () => {
  isLoading.value = true;
  
  if (config.cognitoLoginUrl) {
    // Redirect to Cognito hosted UI
    window.location.href = config.cognitoLoginUrl;
  } else {
    console.error('Cognito login URL not configured');
    isLoading.value = false;
  }
};

const handleSignUp = () => {
  // Redirect to Cognito sign up page
  if (config.cognitoDomain && config.cognitoClientId) {
    const redirectUri = `${window.location.origin}/login-callback`;
    const signUpUrl = `https://${config.cognitoDomain}/signup?client_id=${config.cognitoClientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}`;
    window.location.href = signUpUrl;
  }
};
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-background) 0%, #0a0a0f 100%);
  padding: var(--space-lg);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border-radius: var(--border-radius-xl);
  border: 2px solid var(--color-border);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.login-card__header {
  text-align: center;
  padding: var(--space-xxl) var(--space-xl) var(--space-xl);
  background: linear-gradient(135deg, rgba(192, 255, 0, 0.1), rgba(255, 0, 110, 0.1));
  border-bottom: 2px solid var(--color-border);
}

.login-card__logo {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-lg);
}

.login-card__header h1 {
  color: var(--color-text);
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 var(--space-sm) 0;
}

.login-card__subtitle {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0;
}

.login-card__content {
  padding: var(--space-xxl) var(--space-xl);
}

.demo-notice {
  text-align: center;
  padding: var(--space-lg);
  background: rgba(192, 255, 0, 0.1);
  border: 1px solid var(--color-primary);
  border-radius: var(--border-radius-md);
  margin-bottom: var(--space-xl);
}

.demo-notice p {
  margin: 0;
  color: var(--color-text);
  font-size: 0.875rem;
}

.demo-notice__text {
  margin-top: var(--space-xs);
  color: var(--color-text-muted);
  font-size: 0.75rem;
}

.login-button {
  width: 100%;
  margin-bottom: var(--space-lg);
}

.login-card__footer {
  text-align: center;
  padding-top: var(--space-lg);
  border-top: 1px solid var(--color-border);
}

.login-card__footer p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.login-card__footer a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.login-card__footer a:hover {
  text-decoration: underline;
}
</style>
