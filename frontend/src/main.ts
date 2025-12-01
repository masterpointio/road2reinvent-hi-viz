import './styles/theme.css'
import './styles/color-contrast.css'
import './styles/globals.css'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Debug helper for auth troubleshooting
import './utils/debugAuth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
