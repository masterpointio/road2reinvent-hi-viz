<script setup lang="ts">
import { ref } from 'vue'

const currentCost = ref(0.00)

// Simulate cost increasing
setInterval(() => {
  currentCost.value += 0.01
}, 1000)
</script>

<template>
  <div class="dashboard">
    <div class="header">
      <h1>💸 The Self-Aware Dashboard</h1>
      <p class="subtitle">A dashboard that only tracks how much it costs to run itself</p>
    </div>

    <div class="cost-display">
      <div class="main-cost">
        <span class="currency">$</span>
        <span class="amount">{{ currentCost.toFixed(2) }}</span>
      </div>
      <p class="cost-label">Total Cost of This Dashboard</p>
    </div>

    <div class="info-cards">
      <div class="card">
        <h3>Cost Per Second</h3>
        <p class="value">$0.01</p>
      </div>
      <div class="card">
        <h3>Cost Per View</h3>
        <p class="value">$0.08</p>
      </div>
      <div class="card">
        <h3>Monthly Projection</h3>
        <p class="value">$2,592.00</p>
      </div>
    </div>

    <div class="fun-fact">
      <p>💡 You could have bought {{ Math.floor(currentCost / 5) }} coffees instead</p>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.cost-display {
  text-align: center;
  padding: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  margin-bottom: 2rem;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

.main-cost {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0.5rem;
}

.currency {
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 0.5rem;
}

.amount {
  font-size: 6rem;
  font-weight: bold;
  color: white;
  line-height: 1;
}

.cost-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin-top: 1rem;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card h3 {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card .value {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

.fun-fact {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
  font-size: 1.1rem;
  color: #555;
}
</style>
