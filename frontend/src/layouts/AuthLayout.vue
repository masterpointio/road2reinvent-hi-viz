<template>
  <div class="auth-layout">
    <div class="auth-layout__container">
      <div class="auth-layout__card">
        <router-view />
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



@media (min-width: 640px) {
  .auth-layout {
    padding: var(--space-lg);
  }
}
</style>
