import { ref, watch } from 'vue'

export type Theme = 'hi-viz' | 'default' | 'forest' | 'ocean' | 'sunset' | 'neon'

const STORAGE_KEY = 'app-theme'
const currentTheme = ref<Theme>('hi-viz')

const themes: Theme[] = ['hi-viz', 'default', 'forest', 'ocean', 'sunset', 'neon']

const applyTheme = (theme: Theme) => {
  if (typeof document === 'undefined') return
  document.documentElement.dataset.theme = theme
}

export function useTheme() {
  const setTheme = (theme: Theme) => {
    currentTheme.value = theme
    localStorage.setItem(STORAGE_KEY, theme)
    applyTheme(theme)
  }

  const cycleTheme = () => {
    const currentIndex = themes.indexOf(currentTheme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    const nextTheme = themes[nextIndex]
    if (nextTheme) {
      setTheme(nextTheme)
    }
  }

  const initTheme = () => {
    const savedTheme = localStorage.getItem(STORAGE_KEY) as Theme | null
    if (savedTheme && themes.includes(savedTheme)) {
      currentTheme.value = savedTheme
    } else {
      currentTheme.value = 'hi-viz'
    }
    applyTheme(currentTheme.value)
  }

  watch(currentTheme, (newTheme) => {
    applyTheme(newTheme)
  })

  return {
    currentTheme,
    theme: currentTheme,
    setTheme,
    cycleTheme,
    initTheme,
  }
}
