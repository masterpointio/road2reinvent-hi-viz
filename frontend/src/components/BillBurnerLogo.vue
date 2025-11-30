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
}
</style>
