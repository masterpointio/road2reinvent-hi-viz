<template>
  <div class="burn-results">
    <div class="burn-results__header">
      <div>
        <h1>🔥 Your Burn Results</h1>
        <p class="burn-results__subtitle">{{ burnPlan?.deployment_scenario }}</p>
      </div>
      <UiButton variant="secondary" @click="goBack">
        ← Configure New Burn
      </UiButton>
    </div>

    <div v-if="!burnPlan" class="burn-results__empty">
      <p>No burn plan found. Please configure a burn first.</p>
      <UiButton variant="primary" @click="goBack">
        Configure Burn
      </UiButton>
    </div>

    <template v-else>
      <!-- Stats -->
      <div class="burn-results__stats">
        <div class="stat-card stat-card--primary">
          <div class="stat-card__icon">💸</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ burnPlan.total_amount }}</div>
            <div class="stat-card__label">Total Burned</div>
          </div>
        </div>

        <div class="stat-card stat-card--warning">
          <div class="stat-card__icon">📅</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ burnPlan.timeline_days }} days</div>
            <div class="stat-card__label">Timeline</div>
          </div>
        </div>

        <div class="stat-card stat-card--danger">
          <div class="stat-card__icon">🤦</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ burnPlan.efficiency_level }}</div>
            <div class="stat-card__label">Stupidity Level</div>
          </div>
        </div>

        <div class="stat-card stat-card--info">
          <div class="stat-card__icon">🔧</div>
          <div class="stat-card__content">
            <div class="stat-card__value">{{ burnPlan.services_deployed.length }}</div>
            <div class="stat-card__label">Services</div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="burn-results__content">
        <UiCard class="burn-results__card">
          <template #header>Cost by Service</template>
          <v-chart class="burn-results__chart" :option="topServicesOption" autoresize />
        </UiCard>

        <UiCard class="burn-results__card">
          <template #header>Cost Distribution</template>
          <v-chart class="burn-results__chart burn-results__chart--pie" :option="pieChartOption" autoresize />
        </UiCard>

        <UiCard class="burn-results__card burn-results__card--full">
          <template #header>Cost Over Time</template>
          <v-chart class="burn-results__chart" :option="timelineChartOption" autoresize />
        </UiCard>

        <!-- Services List -->
        <UiCard class="burn-results__card burn-results__card--full">
          <template #header>Services Deployed</template>
          <div class="services-list">
            <div v-for="(service, idx) in burnPlan.services_deployed" :key="idx" class="service-item">
              <div class="service-item__header">
                <div class="service-item__name">
                  {{ service.service_name }} <span class="service-item__type">{{ service.instance_type }}</span>
                </div>
                <div class="service-item__cost">${{ service.total_cost.toLocaleString() }}</div>
              </div>
              <div class="service-item__details">
                <span>Quantity: {{ service.quantity }}</span>
                <span>Days: {{ service.start_day }}-{{ service.end_day }}</span>
                <span>Pattern: {{ service.usage_pattern }}</span>
              </div>
              <div class="service-item__waste">💀 {{ service.waste_factor }}</div>
            </div>
          </div>
        </UiCard>

        <!-- Mistakes -->
        <UiCard class="burn-results__card">
          <template #header>Key Mistakes</template>
          <ul class="mistakes-list">
            <li v-for="(mistake, idx) in burnPlan.key_mistakes" :key="idx">{{ mistake }}</li>
          </ul>
        </UiCard>

        <!-- Recommendations -->
        <UiCard class="burn-results__card">
          <template #header>Recommendations</template>
          <ul class="recommendations-list">
            <li v-for="(rec, idx) in burnPlan.recommendations" :key="idx">{{ rec }}</li>
          </ul>
        </UiCard>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import type { BurnPlanResponse } from '../types/burnPlan';
import { convertToChartData } from '../types/burnPlan';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';

use([CanvasRenderer, BarChart, LineChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);

const router = useRouter();
const burnPlan = ref<BurnPlanResponse | null>(null);

onMounted(() => {
  const stored = sessionStorage.getItem('currentBurnPlan');
  if (stored) {
    try {
      burnPlan.value = JSON.parse(stored);
    } catch (error) {
      console.error('Failed to parse burn plan:', error);
    }
  }
});

const chartData = computed(() => {
  if (!burnPlan.value) return null;
  return convertToChartData(burnPlan.value);
});

const goBack = () => {
  router.push('/app/burn-config');
};

const neonColors = {
  hiviz: '#c0ff00',
  hivizBright: '#d4ff4d',
  blue: '#00F0FF',
  pink: '#FF006E',
  green: '#39FF14',
  purple: '#BC13FE',
  orange: '#FF9500',
};

const topServicesOption = computed(() => ({
  backgroundColor: 'transparent',
  animationDuration: 2500,
  grid: { left: '30%', right: '10%', top: '5%', bottom: '5%' },
  xAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  yAxis: {
    type: 'category',
    data: chartData.value?.racingBarData.map((item) => item.name) || [],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', fontSize: 11 },
    inverse: true,
  },
  series: [
    {
      type: 'bar',
      data: chartData.value?.racingBarData.map((item, idx) => ({
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
      })) || [],
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
}));

const pieChartOption = computed(() => ({
  backgroundColor: 'transparent',
  animationDuration: 2000,
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
      data: chartData.value?.pieChartData.map((item, idx) => {
        const colors = [neonColors.hiviz, neonColors.pink, neonColors.blue, neonColors.purple];
        const color = colors[idx % colors.length] || neonColors.hiviz;
        return {
          ...item,
          itemStyle: { color, shadowColor: color, shadowBlur: 20 },
        };
      }) || [],
      label: { color: '#fff', formatter: '{b}\n${c}', fontSize: 11 },
      emphasis: {
        itemStyle: { shadowBlur: 30, shadowOffsetX: 0, shadowColor: 'rgba(255, 255, 255, 0.5)' },
      },
    },
  ],
}));

const timelineChartOption = computed(() => ({
  backgroundColor: 'transparent',
  animationDuration: 2000,
  grid: { left: '10%', right: '10%', top: '10%', bottom: '15%' },
  xAxis: {
    type: 'category',
    data: chartData.value?.timelineData.timestamps || [],
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
      data: chartData.value?.timelineData.values || [],
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
}));
</script>

<style scoped>
.burn-results {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.burn-results__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.burn-results__header h1 {
  color: var(--color-text);
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
}

.burn-results__subtitle {
  color: var(--color-text-muted);
  margin: var(--space-xs) 0 0 0;
  font-size: 0.875rem;
}

.burn-results__empty {
  text-align: center;
  padding: var(--space-xxl);
  color: var(--color-text-muted);
}

.burn-results__stats {
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
}

.stat-card--primary {
  border-color: var(--color-primary);
  box-shadow: 0 0 20px rgba(192, 255, 0, 0.2);
}

.stat-card--warning {
  border-color: var(--warning-border);
  box-shadow: 0 0 20px rgba(168, 122, 42, 0.2);
}

.stat-card--danger {
  border-color: var(--error-border);
  box-shadow: 0 0 20px rgba(168, 42, 42, 0.2);
}

.stat-card--info {
  border-color: var(--info-border);
  box-shadow: 0 0 20px rgba(33, 73, 138, 0.2);
}

.stat-card__icon {
  font-size: 2rem;
}

.stat-card__value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-xs);
}

.stat-card__label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.burn-results__content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

.burn-results__card--full {
  grid-column: 1 / -1;
}

.burn-results__chart {
  height: 300px;
  width: 100%;
}

.burn-results__chart--pie {
  height: 350px;
}

.services-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.service-item {
  padding: var(--space-md);
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  border-left: 3px solid var(--color-primary);
}

.service-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.service-item__name {
  font-weight: 600;
  color: var(--color-text);
}

.service-item__type {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  font-weight: 400;
}

.service-item__cost {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-primary);
}

.service-item__details {
  display: flex;
  gap: var(--space-md);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-bottom: var(--space-sm);
}

.service-item__waste {
  font-size: 0.875rem;
  color: var(--color-text);
  font-style: italic;
}

.mistakes-list,
.recommendations-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.mistakes-list li,
.recommendations-list li {
  padding: var(--space-sm);
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-sm);
  color: var(--color-text);
}

.mistakes-list li::before {
  content: '❌ ';
  margin-right: var(--space-xs);
}

.recommendations-list li::before {
  content: '✅ ';
  margin-right: var(--space-xs);
}

@media (max-width: 1024px) {
  .burn-results__content {
    grid-template-columns: 1fr;
  }
}
</style>
