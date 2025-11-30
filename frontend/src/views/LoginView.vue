<template>
  <div class="login-container">
    <h1>Redirecting to login...</h1>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

const cognitoDomain = import.meta.env.VITE_COGNITO_DOMAIN
const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
const redirectUri = `${window.location.origin}/callback`

onMounted(() => {
  const loginUrl = `https://${cognitoDomain}/login?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}`
  window.location.href = loginUrl
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
