<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'small' | 'compact' | 'default' | 'large'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'default'
})

const sizeClasses = computed(() => {
  return `logo--${props.size}`
})
</script>

<template>
  <div :class="['bill-burner-logo', sizeClasses]">
    <div class="logo-container">
      <div class="burning-dollar">
        <span class="dollar-sign">$</span>
        <div class="flame flame-1"></div>
        <div class="flame flame-2"></div>
        <div class="flame flame-3"></div>
      </div>
      <div class="text-container">
        <div class="bill-burner-text">
          <span class="bill">BILL</span>
          <span class="burner">BURNER</span>
        </div>
        <div class="team-hiviz">
          <span class="by-text">BY</span>
          <span class="team-text">TEAM</span>
          <span class="hiviz-text">HI-VIZ</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bill-burner-logo {
  display: inline-flex;
  align-items: center;
  user-select: none;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Burning Dollar Icon */
.burning-dollar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dollar-sign {
  font-family: 'Orbitron', monospace;
  font-weight: 900;
  color: #00f0ff;
  text-shadow: 
    0 0 10px #00f0ff,
    0 0 20px #00f0ff,
    0 0 30px #00f0ff;
  z-index: 2;
  position: relative;
}

.flame {
  position: absolute;
  bottom: 50%;
  left: 50%;
  transform: translateX(-50%);
  width: 8px;
  height: 12px;
  background: linear-gradient(to top, #ff6b00 0%, #ff0066 50%, #ffaa00 100%);
  border-radius: 50% 50% 0 0;
  animation: flicker 0.3s infinite alternate;
  filter: blur(1px);
}

.flame-1 {
  animation-delay: 0s;
  opacity: 0.9;
}

.flame-2 {
  animation-delay: 0.1s;
  opacity: 0.7;
  transform: translateX(-50%) translateX(-4px);
}

.flame-3 {
  animation-delay: 0.2s;
  opacity: 0.8;
  transform: translateX(-50%) translateX(4px);
}

@keyframes flicker {
  0% {
    transform: translateX(-50%) scaleY(1) scaleX(1);
    opacity: 0.9;
  }
  50% {
    transform: translateX(-50%) scaleY(1.1) scaleX(0.9);
    opacity: 1;
  }
  100% {
    transform: translateX(-50%) scaleY(0.95) scaleX(1.05);
    opacity: 0.85;
  }
}

/* Text Container */
.text-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bill-burner-text {
  display: flex;
  flex-direction: column;
  line-height: 0.85;
  font-family: 'Orbitron', monospace;
  font-weight: 900;
}

.bill,
.burner {
  color: #FF006E;
  text-shadow: 
    0 0 10px #FF006E,
    0 0 20px #FF006E,
    0 0 30px #FF006E;
  animation: textFlicker 3s infinite alternate;
}

@keyframes textFlicker {
  0%, 100% {
    text-shadow: 
      0 0 10px #FF006E,
      0 0 20px #FF006E,
      0 0 30px #FF006E;
  }
  50% {
    text-shadow: 
      0 0 15px #FF006E,
      0 0 25px #FF006E,
      0 0 35px #FF006E;
  }
}

.team-hiviz {
  font-family: 'Rajdhani', sans-serif;
  font-weight: 700;
  display: flex;
  flex-direction: column;
  line-height: 0.9;
}

.by-text,
.team-text,
.hiviz-text {
  background: linear-gradient(90deg, #00ff88 0%, #ffaa00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: hivizGlow 2s infinite alternate;
}

@keyframes hivizGlow {
  0% {
    filter: brightness(1);
  }
  100% {
    filter: brightness(1.3);
  }
}

/* Size Variants */
.logo--small .dollar-sign {
  font-size: 1rem;
}

.logo--small .flame {
  width: 4px;
  height: 6px;
}

.logo--small .bill,
.logo--small .burner {
  font-size: 0.625rem;
}

.logo--small .team-hiviz {
  font-size: 0.375rem;
}

.logo--small .logo-container {
  gap: 0.375rem;
}

.logo--compact .dollar-sign {
  font-size: 2rem;
}

.logo--compact .flame {
  width: 8px;
  height: 12px;
}

.logo--compact .bill,
.logo--compact .burner {
  font-size: 1.25rem;
}

.logo--compact .by-text {
  font-size: 0.65rem;
}

.logo--compact .team-text,
.logo--compact .hiviz-text {
  font-size: 1.3rem;
}

.logo--compact .logo-container {
  gap: 0.625rem;
}

.logo--compact .text-container {
  gap: 0.5rem;
}

.logo--default .dollar-sign {
  font-size: 2.5rem;
}

.logo--default .flame {
  width: 8px;
  height: 12px;
}

.logo--default .bill,
.logo--default .burner {
  font-size: 1.5rem;
}

.logo--default .team-hiviz {
  font-size: 0.75rem;
}

.logo--large .dollar-sign {
  font-size: 4rem;
}

.logo--large .flame {
  width: 12px;
  height: 18px;
}

.logo--large .bill,
.logo--large .burner {
  font-size: 2.5rem;
}

.logo--large .team-hiviz {
  font-size: 1.25rem;
}

.logo--large .logo-container {
  gap: 1rem;
}
</style>
