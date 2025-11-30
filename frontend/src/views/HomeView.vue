<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const apiResponse = ref<Record<string, unknown> | null>(null)
const error = ref<string | null>(null)
const loading = ref(false)
const isLoggedIn = ref(false)

const checkAuth = () => {
  const token = localStorage.getItem('id_token')
  isLoggedIn.value = !!token
  return token
}

const callApi = async () => {
  const token = checkAuth()
  if (!token) {
    error.value = 'Not authenticated. Please log in.'
    return
  }

  loading.value = true
  error.value = null

  try {
    const apiUrl = import.meta.env.VITE_API_URL
    const response = await fetch(`${apiUrl}/hello`, {
      headers: {
        Authorization: token,
      },
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    apiResponse.value = await response.json()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to call API'
  } finally {
    loading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('id_token')
  localStorage.removeItem('refresh_token')
  isLoggedIn.value = false
  apiResponse.value = null
  router.push('/login')
}

onMounted(() => {
  checkAuth()
})
</script>

<template>
  <main>
    <div class="container">
      <h1>R2R Application</h1>

      <div v-if="!isLoggedIn" class="auth-section">
        <p>You are not logged in.</p>
        <button @click="router.push('/login')" class="btn">Login</button>
      </div>

      <div v-else class="auth-section">
        <p>You are logged in!</p>
        <button @click="callApi" :disabled="loading" class="btn">
          {{ loading ? 'Loading...' : 'Call Hello World API' }}
        </button>
        <button @click="logout" class="btn btn-secondary">Logout</button>
      </div>

      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>

      <div v-if="apiResponse" class="response">
        <h2>API Response:</h2>
        <pre>{{ JSON.stringify(apiResponse, null, 2) }}</pre>
      </div>
    </div>
  </main>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
}

.auth-section {
  margin-bottom: 2rem;
}

.btn {
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn:hover:not(:disabled) {
  background-color: #359268;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #666;
}

.btn-secondary:hover {
  background-color: #555;
}

.error {
  padding: 1rem;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
  margin-bottom: 1rem;
}

.response {
  margin-top: 2rem;
}

.response h2 {
  margin-bottom: 1rem;
}

pre {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  border: 1px solid #ddd;
}
</style>
