<template>
  <div class="auth-layout">
    <div class="auth-layout__container">
      <div class="auth-layout__card">
        <div class="auth-layout__header">
          <h1 class="auth-layout__title">R2R App</h1>
        </div>
        <div class="auth-layout__content">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: var(--space-md);
}

.auth-layout__container {
  width: 100%;
  max-width: 450px;
}

.auth-layout__card {
  background: var(--color-surface);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.auth-layout__header {
  padding: var(--space-lg);
  text-align: center;
  border-bottom: 1px solid var(--color-surface-soft);
}

.auth-layout__title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.auth-layout__content {
  padding: var(--space-lg);
}

@media (min-width: 640px) {
  .auth-layout {
    padding: var(--space-lg);
  }

  .auth-layout__header {
    padding: var(--space-xl);
  }

  .auth-layout__title {
    font-size: 1.75rem;
  }

  .auth-layout__content {
    padding: var(--space-xl);
  }
}
</style>
