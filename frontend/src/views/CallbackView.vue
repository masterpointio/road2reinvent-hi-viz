<template>
  <div class="callback-container">
    <div v-if="error" class="error">
      <h2>Authentication Error</h2>
      <p>{{ error }}</p>
    </div>
    <div v-else class="loading">
      <h2>Processing authentication...</h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref<string | null>(null)

const exchangeCodeForTokens = async (code: string) => {
  const cognitoDomain = import.meta.env.VITE_COGNITO_DOMAIN
  const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
  const redirectUri = `${window.location.origin}/callback`

  try {
    const response = await fetch(`https://${cognitoDomain}/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: clientId,
        code: code,
        redirect_uri: redirectUri,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to exchange code for tokens')
    }

    const tokens = await response.json()
    
    // Store tokens in localStorage
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('id_token', tokens.id_token)
    if (tokens.refresh_token) {
      localStorage.setItem('refresh_token', tokens.refresh_token)
    }

    // Redirect to home
    router.push('/')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error occurred'
  }
}

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')
  const errorParam = urlParams.get('error')

  if (errorParam) {
    error.value = urlParams.get('error_description') || errorParam
  } else if (code) {
    exchangeCodeForTokens(code)
  } else {
    error.value = 'No authorization code received'
  }
})
</script>

<style scoped>
.callback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.error {
  text-align: center;
  color: #d32f2f;
}

.loading {
  text-align: center;
}
</style>
