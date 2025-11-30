<<<<<<< HEAD
<template>
  <div :class="['bill-burner-logo', `bill-burner-logo--${size}`]">
    <svg
      :width="dimensions.width"
      :height="dimensions.height"
      viewBox="0 0 800 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <!-- Flame Icon -->
      <g class="logo-flame">
        <path
          d="M80 120C80 120 60 100 60 80C60 60 70 40 90 40C90 40 85 60 95 70C105 80 110 85 110 100C110 115 100 130 80 130C60 130 50 115 50 100C50 85 60 75 70 80"
          stroke="#FF006E"
          stroke-width="4"
          fill="none"
          class="flame-outer"
        />
        <path
          d="M85 110C85 110 80 100 80 90C80 80 85 70 95 75C95 75 93 85 98 90C103 95 105 100 105 105C105 110 100 115 95 115C90 115 85 110 85 105"
          stroke="#FF006E"
          stroke-width="3"
          fill="none"
          class="flame-inner"
        />
      </g>

      <!-- Dollar Bill Icon -->
      <g class="logo-bill">
        <rect
          x="40"
          y="100"
          width="80"
          height="50"
          rx="5"
          stroke="#00F0FF"
          stroke-width="3"
          fill="none"
          class="bill-outline"
        />
        <text
          x="80"
          y="135"
          font-family="Orbitron, monospace"
          font-size="32"
          font-weight="700"
          fill="#00F0FF"
          text-anchor="middle"
          class="bill-dollar"
        >
          $
        </text>
      </g>

      <!-- BILL text -->
      <text
        x="150"
        y="100"
        font-family="Orbitron, sans-serif"
        font-size="80"
        font-weight="900"
        fill="#00F0FF"
        class="text-bill"
      >
        BILL
      </text>

      <!-- BURNER text -->
      <text
        x="150"
        y="170"
        font-family="Orbitron, sans-serif"
        font-size="80"
        font-weight="900"
        fill="#FF006E"
        class="text-burner"
      >
        BURNER
      </text>

      <!-- BY TEAM HI-VIZ text (only for default and large sizes) -->
      <text
        v-if="size !== 'compact' && size !== 'small'"
        x="150"
        y="195"
        font-family="Rajdhani, sans-serif"
        font-size="24"
        font-weight="700"
        class="text-team"
      >
        <tspan fill="#52b788">BY</tspan>
        <tspan fill="#74c69d" dx="10">TEAM</tspan>
        <tspan fill="#c0ff00" dx="10">HI-VIZ</tspan>
      </text>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    size?: 'compact' | 'small' | 'default' | 'large';
  }>(),
  {
    size: 'default',
  }
);

const dimensions = computed(() => {
  switch (props.size) {
    case 'compact':
      return { width: 200, height: 50 };
    case 'small':
      return { width: 400, height: 100 };
    case 'large':
      return { width: 1000, height: 250 };
    default:
      return { width: 800, height: 200 };
  }
});
</script>

<style scoped>
.bill-burner-logo {
  display: inline-block;
}

/* Neon glow effects */
.text-bill {
  filter: drop-shadow(0 0 10px #00f0ff) drop-shadow(0 0 20px #00f0ff) drop-shadow(0 0 30px #00f0ff);
}

.text-burner {
  filter: drop-shadow(0 0 10px #ff006e) drop-shadow(0 0 20px #ff006e) drop-shadow(0 0 30px #ff006e);
}

.text-team tspan {
  filter: drop-shadow(0 0 5px currentColor) drop-shadow(0 0 10px currentColor);
}

.flame-outer,
.flame-inner {
  filter: drop-shadow(0 0 5px #ff006e) drop-shadow(0 0 10px #ff006e);
  animation: flicker 2s infinite alternate;
}

.bill-outline,
.bill-dollar {
  filter: drop-shadow(0 0 5px #00f0ff) drop-shadow(0 0 10px #00f0ff);
}

/* Flame flicker animation */
@keyframes flicker {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

/* Compact size adjustments */
.bill-burner-logo--compact svg {
  transform: scale(0.25);
  transform-origin: left center;
}

.bill-burner-logo--small svg {
  transform: scale(0.5);
  transform-origin: left center;
}

.bill-burner-logo--large svg {
  transform: scale(1.25);
  transform-origin: left center;
=======
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
>>>>>>> 81328305bc2dd54c5d72e32d4955b603f02824ba
}
</style>
