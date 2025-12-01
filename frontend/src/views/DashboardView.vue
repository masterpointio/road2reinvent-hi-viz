<template>
  <div class="dashboard">
    <!-- Achievement Popup -->
    <AchievementPopup
      :show="showAchievementPopup"
      :achievement-title="achievementTitle"
      :achievement-text="achievementText"
      :amount="totalBurned"
      @accept="handleAchievementAccept"
    />

    <div class="dashboard__header">
      <div>
        <h1>AWS Bill Burner</h1>
        <p class="dashboard__subtitle">Watch your money disappear in real-time</p>
      </div>
      <div class="dashboard__controls">
        <div class="amount-adjuster">
          <label class="amount-adjuster__label">Adjust Amount:</label>
          <div class="amount-adjuster__controls">
            <button class="amount-adjuster__btn" @click="adjustAmount(-1000)">-$1k</button>
            <input
              v-model.number="currentAmount"
              type="number"
              class="amount-adjuster__input"
              min="1000"
              step="1000"
            />
            <button class="amount-adjuster__btn" @click="adjustAmount(1000)">+$1k</button>
          </div>
        </div>
        <UiButton variant="primary" @click="startNewBurn">
          🔥 Start New Burn
        </UiButton>
      </div>
    </div>

    <!-- Stat Cards -->
    <div class="dashboard__stats">
      <div class="stat-card stat-card--primary">
        <div class="stat-card__icon">💸</div>
        <div class="stat-card__content">
          <div class="stat-card__value">${{ totalBurned.toLocaleString() }}</div>
          <div class="stat-card__label">Total Burned</div>
        </div>
      </div>

      <div class="stat-card stat-card--success">
        <div class="stat-card__icon">🔥</div>
        <div class="stat-card__content">
          <div class="stat-card__value">{{ activeBurns }}</div>
          <div class="stat-card__label">Active Burns</div>
        </div>
      </div>

      <div class="stat-card stat-card--warning">
        <div class="stat-card__icon">⚡</div>
        <div class="stat-card__content">
          <div class="stat-card__value">{{ totalBurns }}</div>
          <div class="stat-card__label">Total Burns</div>
        </div>
      </div>

      <div class="stat-card stat-card--info">
        <div class="stat-card__icon">⏱️</div>
        <div class="stat-card__content">
          <div class="stat-card__value">{{ avgDuration }}s</div>
          <div class="stat-card__label">Avg Duration</div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="dashboard__content">
      <!-- Current Burn Status -->
      <UiCard class="dashboard__card dashboard__card--featured">
        <template #header>
          <div class="card-header">
            <span>Current Burn Status</span>
            <span class="status-badge status-badge--active">Live</span>
          </div>
        </template>
        <div class="burn-status">
          <div class="burn-status__progress">
            <div class="burn-status__progress-bar" :style="{ width: burnProgress + '%' }"></div>
          </div>
          <div class="burn-status__details">
            <div class="burn-status__detail">
              <span class="burn-status__label">Money Remaining</span>
              <span class="burn-status__value">${{ moneyRemaining.toLocaleString() }}</span>
            </div>
            <div class="burn-status__detail">
              <span class="burn-status__label">Progress</span>
              <span class="burn-status__value">{{ burnProgress }}%</span>
            </div>
            <div class="burn-status__detail">
              <span class="burn-status__label">Time Elapsed</span>
              <span class="burn-status__value">{{ timeElapsed }}s</span>
            </div>
          </div>
        </div>
      </UiCard>

      <!-- Money Burned Chart -->
      <UiCard class="dashboard__card">
        <template #header>Money Burned Over Time</template>
        <v-chart class="dashboard__chart" :option="moneyChartOption" autoresize />
      </UiCard>

      <!-- Top Services -->
      <UiCard class="dashboard__card">
        <template #header>Top Burning Services</template>
        <v-chart class="dashboard__chart" :option="topServicesOption" autoresize />
      </UiCard>

      <!-- Cost Distribution -->
      <UiCard class="dashboard__card">
        <template #header>Cost Distribution</template>
        <v-chart class="dashboard__chart dashboard__chart--pie" :option="pieChartOption" autoresize />
      </UiCard>

      <!-- Recent Burns -->
      <UiCard class="dashboard__card dashboard__card--list">
        <template #header>Recent Burns</template>
        <div class="recent-burns">
          <div v-for="burn in recentBurns" :key="burn.id" class="recent-burn">
            <div class="recent-burn__info">
              <div class="recent-burn__amount">${{ burn.amount.toLocaleString() }}</div>
              <div class="recent-burn__meta">
                <span class="recent-burn__style">{{ burn.style }}</span>
                <span class="recent-burn__time">{{ burn.timeAgo }}</span>
              </div>
            </div>
            <div class="recent-burn__status">
              <span :class="['status-badge', `status-badge--${burn.status}`]">
                {{ burn.status }}
              </span>
            </div>
          </div>
        </div>
      </UiCard>

      <!-- Recent Burn Plans -->
      <UiCard class="dashboard__card dashboard__card--roasts">
        <template #header>Recent Burn Plans 🔥</template>
        <div v-if="burnPlansLoading" class="roasts__loading">
          Loading recent burns...
        </div>
        <div v-else-if="burnPlansError" class="roasts__error">
          {{ burnPlansError }}
        </div>
        <div v-else-if="recentPlans.length === 0" class="roasts__empty">
          No burn plans yet. Start your first burn!
        </div>
        <div v-else class="roasts">
          <div v-for="plan in recentPlans" :key="plan.id" class="roast">
            <div class="roast__icon">💸</div>
            <div class="roast__content">
              <div class="roast__header">
                <span class="roast__amount">{{ plan.burn_plan.total_amount }}</span>
                <span class="roast__time">{{ formatTimeAgo(plan.timestamp) }}</span>
              </div>
              <div class="roast__text">{{ plan.burn_plan.deployment_scenario }}</div>
              <div class="roast__meta">
                <span class="roast__efficiency">{{ plan.burn_plan.efficiency_level }}</span>
                <span class="roast__timeline">{{ plan.burn_plan.timeline_days }} days</span>
              </div>
            </div>
          </div>
        </div>
      </UiCard>

      <!-- Achievement Card -->
      <div v-if="showAchievementCard" class="dashboard__card">
        <AchievementCard
          :show="showAchievementCard"
          :achievement-title="achievementTitle"
          :achievement-text="achievementText"
          :amount="totalBurned"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import VChart from 'vue-echarts';
import { mockBurnPlan } from '../data/mockBurnPlan';
import { convertToChartData, scaleBurnPlan } from '../types/burnPlan';
import type { BurnPlanResponse } from '../types/burnPlan';
import { generateRandomAchievement } from '../utils/achievementGenerator';
import { useRecentBurnPlans } from '../composables/useRecentBurnPlans';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';
import AchievementPopup from '../components/AchievementPopup.vue';
import AchievementCard from '../components/AchievementCard.vue';

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const router = useRouter();

// Recent burn plans
const {
  recentPlans,
  loading: burnPlansLoading,
  error: burnPlansError,
  fetchRecentPlans,
  formatTimeAgo,
} = useRecentBurnPlans();

// Load burn plan from session storage or use mock
const loadedBurnPlan = ref<BurnPlanResponse | null>(null);

onMounted(async () => {
  const stored = sessionStorage.getItem('currentBurnPlan');
  if (stored) {
    try {
      loadedBurnPlan.value = JSON.parse(stored);
    } catch (error) {
      console.error('Failed to parse burn plan:', error);
      loadedBurnPlan.value = mockBurnPlan;
    }
  } else {
    loadedBurnPlan.value = mockBurnPlan;
  }

  // Fetch recent burn plans
  await fetchRecentPlans(5);
});

// Use loaded burn plan data
const currentAmount = ref(10000);
const currentBurnPlan = computed(() => {
  const plan = loadedBurnPlan.value || mockBurnPlan;
  return scaleBurnPlan(plan, currentAmount.value);
});
const chartData = computed(() => convertToChartData(currentBurnPlan.value));

// Achievement state
const showAchievementPopup = ref(true);
const showAchievementCard = ref(false);
const randomAchievement = ref(generateRandomAchievement());

const achievementTitle = computed(() => {
  return currentBurnPlan.value.achievement?.title || randomAchievement.value.title;
});

const achievementText = computed(() => {
  return currentBurnPlan.value.achievement?.text || randomAchievement.value.description;
});

const handleAchievementAccept = () => {
  showAchievementPopup.value = false;
  showAchievementCard.value = true;
};

// Generate a new random achievement on mount
onMounted(() => {
  randomAchievement.value = generateRandomAchievement();
});

// Dummy data for stats
const totalBurned = computed(() => currentBurnPlan.value.total_calculated_cost);
const activeBurns = ref(1);
const totalBurns = ref(23);
const avgDuration = computed(() => currentBurnPlan.value.timeline_days);
const burnProgress = ref(73);
const moneyRemaining = ref(2700);
const timeElapsed = ref(44);

const recentBurns = ref([
  { id: 1, amount: 10000, style: 'Horizontal', timeAgo: '2 min ago', status: 'completed' },
  { id: 2, amount: 5000, style: 'Vertical', timeAgo: '15 min ago', status: 'completed' },
  { id: 3, amount: 15000, style: 'Horizontal', timeAgo: '1 hour ago', status: 'completed' },
  { id: 4, amount: 8500, style: 'Vertical', timeAgo: '2 hours ago', status: 'completed' },
]);



const neonColors = {
  hiviz: '#c0ff00',
  hivizBright: '#d4ff4d',
  blue: '#00F0FF',
  pink: '#FF006E',
  green: '#39FF14',
  purple: '#BC13FE',
  orange: '#FF9500',
};

// Money Chart
const moneyChartOption = ref({
  backgroundColor: 'transparent',
  animationDuration: 2000,
  animationEasing: 'cubicOut' as const,
  grid: { left: '10%', right: '10%', top: '10%', bottom: '15%' },
  xAxis: {
    type: 'category',
    data: ['0s', '10s', '20s', '30s', '40s', '50s'],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', fontSize: 11 },
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  series: [
    {
      type: 'line',
      data: [10000, 8200, 6100, 4300, 2700, 800],
      smooth: true,
      lineStyle: {
        color: neonColors.hiviz,
        width: 3,
        shadowColor: neonColors.hiviz,
        shadowBlur: 15,
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(192, 255, 0, 0.5)' },
            { offset: 1, color: 'rgba(192, 255, 0, 0)' },
          ],
        },
      },
      symbol: 'none',
    },
  ],
});

// Top Services Chart
const topServicesOption = ref({
  backgroundColor: 'transparent',
  animationDuration: 2500,
  animationEasing: 'cubicOut' as const,
  animationDelay: (idx: number) => idx * 100,
  grid: { left: '30%', right: '10%', top: '5%', bottom: '5%' },
  xAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  yAxis: {
    type: 'category',
    data: ['NAT Gateway', 'Lambda', 'S3', 'RDS', 'EC2'],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', fontSize: 11 },
    inverse: true,
  },
  series: [
    {
      type: 'bar',
      data: [
        {
          value: 2100,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: neonColors.orange },
                { offset: 1, color: neonColors.pink },
              ],
            },
            shadowColor: neonColors.orange,
            shadowBlur: 15,
          },
        },
        {
          value: 3500,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: neonColors.purple },
                { offset: 1, color: neonColors.pink },
              ],
            },
            shadowColor: neonColors.purple,
            shadowBlur: 15,
          },
        },
        {
          value: 4800,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: neonColors.blue },
                { offset: 1, color: neonColors.hiviz },
              ],
            },
            shadowColor: neonColors.blue,
            shadowBlur: 15,
          },
        },
        {
          value: 6200,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: neonColors.pink },
                { offset: 1, color: neonColors.hiviz },
              ],
            },
            shadowColor: neonColors.pink,
            shadowBlur: 15,
          },
        },
        {
          value: 8500,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: neonColors.hiviz },
                { offset: 1, color: neonColors.hivizBright },
              ],
            },
            shadowColor: neonColors.hiviz,
            shadowBlur: 15,
          },
        },
      ],
      label: {
        show: true,
        position: 'right',
        color: '#fff',
        formatter: '${c}',
        fontSize: 11,
      },
      barWidth: '60%',
    },
  ],
});

// Pie Chart
const pieChartOption = ref({
  backgroundColor: 'transparent',
  animationDuration: 2000,
  animationEasing: 'elasticOut' as const,
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(10, 10, 15, 0.9)',
    borderColor: neonColors.hiviz,
    borderWidth: 2,
    textStyle: { color: '#fff' },
    formatter: '{b}: ${c} ({d}%)',
  },
  legend: {
    orient: 'vertical',
    right: '5%',
    top: 'center',
    textStyle: { color: '#fff', fontSize: 11 },
  },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      data: [
        {
          value: 3500,
          name: 'Compute',
          itemStyle: { color: neonColors.hiviz, shadowColor: neonColors.hiviz, shadowBlur: 20 },
        },
        {
          value: 2800,
          name: 'Storage',
          itemStyle: { color: neonColors.pink, shadowColor: neonColors.pink, shadowBlur: 20 },
        },
        {
          value: 2100,
          name: 'Database',
          itemStyle: { color: neonColors.blue, shadowColor: neonColors.blue, shadowBlur: 20 },
        },
        {
          value: 1200,
          name: 'Network',
          itemStyle: { color: neonColors.purple, shadowColor: neonColors.purple, shadowBlur: 20 },
        },
      ],
      label: { color: '#fff', formatter: '{b}\n${c}', fontSize: 11 },
      emphasis: {
        itemStyle: { shadowBlur: 30, shadowOffsetX: 0, shadowColor: 'rgba(255, 255, 255, 0.5)' },
      },
    },
  ],
});

const adjustAmount = (delta: number) => {
  currentAmount.value = Math.max(1000, currentAmount.value + delta);
};

const startNewBurn = () => {
  router.push('/app/burn-config');
};

// Watch for amount changes and update charts
watch(chartData, (newData) => {
  // Update racing bar chart
  if (topServicesOption.value.series[0]) {
    topServicesOption.value.series[0].data = newData.racingBarData.map((item, idx) => ({
    value: item.value,
    itemStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 1,
        y2: 0,
        colorStops: [
          { offset: 0, color: idx === 0 ? neonColors.hiviz : neonColors.pink },
          { offset: 1, color: idx === 0 ? neonColors.hivizBright : neonColors.purple },
        ],
      },
      shadowColor: idx === 0 ? neonColors.hiviz : neonColors.pink,
      shadowBlur: 15,
    },
  }));
  }
  topServicesOption.value.yAxis.data = newData.racingBarData.map((item) => item.name);

  // Update pie chart
  if (pieChartOption.value.series[0]) {
    pieChartOption.value.series[0].data = newData.pieChartData.map((item, idx) => {
      const colors = [neonColors.hiviz, neonColors.pink, neonColors.blue, neonColors.purple];
      const color = colors[idx % colors.length] || neonColors.hiviz;
      return {
        ...item,
        itemStyle: {
          color,
          shadowColor: color,
          shadowBlur: 20,
        },
      };
    });
  }

  // Update money chart
  moneyChartOption.value.xAxis.data = newData.timelineData.timestamps;
  if (moneyChartOption.value.series[0]) {
    moneyChartOption.value.series[0].data = newData.timelineData.values;
  }
});
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.dashboard__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.dashboard__controls {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  align-items: flex-end;
}

.amount-adjuster {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.amount-adjuster__label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.amount-adjuster__controls {
  display: flex;
  gap: var(--space-xs);
  align-items: center;
}

.amount-adjuster__btn {
  padding: var(--space-xs) var(--space-sm);
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  border-radius: var(--border-radius-sm);
  color: var(--color-primary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.amount-adjuster__btn:hover {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  box-shadow: 0 0 10px var(--color-primary);
}

.amount-adjuster__input {
  width: 120px;
  padding: var(--space-xs) var(--space-sm);
  background: var(--color-surface);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-sm);
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 600;
  text-align: center;
}

.amount-adjuster__input:focus {
  outline: none;
  box-shadow: 0 0 10px var(--color-primary);
}

.dashboard__header h1 {
  color: var(--color-text);
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
}

.dashboard__subtitle {
  color: var(--color-text-muted);
  margin: var(--space-xs) 0 0 0;
  font-size: 0.875rem;
}

/* Stat Cards */
.dashboard__stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
}

.stat-card {
  background: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  display: flex;
  align-items: center;
  gap: var(--space-md);
  border: 2px solid transparent;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.stat-card--primary {
  border-color: var(--color-primary);
  box-shadow: 0 0 20px rgba(192, 255, 0, 0.2);
}

.stat-card--success {
  border-color: var(--success-border);
  box-shadow: 0 0 20px rgba(34, 148, 110, 0.2);
}

.stat-card--warning {
  border-color: var(--warning-border);
  box-shadow: 0 0 20px rgba(168, 122, 42, 0.2);
}

.stat-card--info {
  border-color: var(--info-border);
  box-shadow: 0 0 20px rgba(33, 73, 138, 0.2);
}

.stat-card__icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.stat-card__value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1;
  margin-bottom: var(--space-xs);
}

.stat-card__label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Main Content Grid */
.dashboard__content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-lg);
}

.dashboard__card {
  min-height: 200px;
}

.dashboard__card--featured {
  grid-column: 1 / -1;
}

.dashboard__chart {
  height: 300px;
  width: 100%;
}

.dashboard__chart--pie {
  height: 350px;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* Burn Status */
.burn-status__progress {
  width: 100%;
  height: 8px;
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-sm);
  overflow: hidden;
  margin-bottom: var(--space-lg);
}

.burn-status__progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-soft));
  box-shadow: 0 0 10px var(--color-primary);
  transition: width 0.3s ease;
}

.burn-status__details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-lg);
}

.burn-status__detail {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.burn-status__label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.burn-status__value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
}

/* Recent Burns */
.recent-burns {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.recent-burn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md);
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  transition: all 0.2s;
}

.recent-burn:hover {
  background: var(--color-surface);
  transform: translateX(4px);
}

.recent-burn__amount {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-xs);
}

.recent-burn__meta {
  display: flex;
  gap: var(--space-sm);
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.recent-burn__style {
  font-weight: 500;
}

/* Roasts */
.roasts {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.roasts__loading,
.roasts__error,
.roasts__empty {
  padding: var(--space-lg);
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.roasts__error {
  color: var(--color-danger);
}

.roast {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  border-left: 3px solid var(--color-primary);
  transition: all 0.2s;
}

.roast:hover {
  background: var(--color-surface);
  transform: translateX(4px);
}

.roast__icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.roast__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.roast__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xs);
}

.roast__amount {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-primary);
}

.roast__time {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.roast__text {
  font-size: 0.875rem;
  color: var(--color-text);
  line-height: 1.5;
  font-style: italic;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.roast__meta {
  display: flex;
  gap: var(--space-sm);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: var(--space-xs);
}

.roast__efficiency {
  padding: 2px 8px;
  background: var(--color-surface);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--color-primary);
}

.roast__timeline {
  padding: 2px 8px;
  background: var(--color-surface);
  border-radius: var(--border-radius-sm);
}

/* Status Badge */
.status-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--border-radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge--active {
  background: var(--success-bg);
  color: var(--text-on-success);
  border: 1px solid var(--success-border);
}

.status-badge--completed {
  background: var(--info-bg);
  color: var(--text-on-info);
  border: 1px solid var(--info-border);
}

/* Responsive */
@media (min-width: 640px) {
  .dashboard__header h1 {
    font-size: 2.25rem;
  }

  .dashboard__subtitle {
    font-size: 1rem;
  }

  .stat-card__value {
    font-size: 2rem;
  }

  .stat-card__label {
    font-size: 0.875rem;
  }
}

@media (min-width: 1024px) {
  .dashboard__content {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard__card--list,
  .dashboard__card--roasts {
    grid-column: span 1;
  }
}

@media (min-width: 1280px) {
  .dashboard__content {
    grid-template-columns: repeat(3, 1fr);
  }

  .dashboard__card--featured {
    grid-column: 1 / -1;
  }
}
</style>
