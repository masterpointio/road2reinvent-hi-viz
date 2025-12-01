<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleStartBurnin = () => {
  router.push('/app/burn-config')
}
</script>

<template>
  <div class="landing">
    <div class="hero-container">
      <img 
        src="/bill-burner-frontpage.png" 
        alt="Bill Burner by Team Hi-Viz" 
        class="hero-image"
      />
      <button class="neon-button" @click="handleStartBurnin">
        Start Burnin
      </button>
    </div>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  padding: 2rem;
}

.hero-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3rem;
  max-width: 800px;
  width: 100%;
}

.hero-image {
  width: 100%;
  height: auto;
  max-width: 600px;
}

.neon-button {
  position: relative;
  padding: 1rem 3rem;
  font-size: 1.5rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  background: transparent;
  border: 3px solid #00f0ff;
  color: #00f0ff;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 
    0 0 10px #00f0ff,
    0 0 20px #00f0ff,
    inset 0 0 10px rgba(0, 240, 255, 0.2);
}

.neon-button:hover {
  background: rgba(0, 240, 255, 0.1);
  box-shadow: 
    0 0 20px #00f0ff,
    0 0 40px #00f0ff,
    0 0 60px #00f0ff,
    inset 0 0 20px rgba(0, 240, 255, 0.3);
  transform: scale(1.05);
}

.neon-button:active {
  transform: scale(0.98);
}

@media (max-width: 768px) {
  .hero-container {
    gap: 2rem;
  }
  
  .neon-button {
    padding: 0.8rem 2rem;
    font-size: 1.2rem;
  }
}
</style>
