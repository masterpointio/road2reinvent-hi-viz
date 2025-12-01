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

    <!-- Overall Progress Meter -->
    <div v-if="burnPlan && animationProgress < 1" class="burn-results__progress">
      <div class="progress-meter">
        <div class="progress-meter__header">
          <span class="progress-meter__label">🔥 Burning Money...</span>
          <span class="progress-meter__percentage">{{ Math.round(animationProgress * 100) }}%</span>
        </div>
        <div class="progress-meter__bar">
          <div class="progress-meter__fill" :style="{ width: `${animationProgress * 100}%` }"></div>
        </div>
      </div>
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
            <div class="stat-card__value">${{ Math.floor(burnPlan.total_calculated_cost * animationProgress).toLocaleString() }}</div>
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
        <!-- Row 1: Three Column Layout -->
        <UiCard class="burn-results__card burn-results__card--third">
          <template #header>🔥 Burn Rate</template>
          <v-chart class="burn-results__chart burn-results__chart--compact" :option="gaugeOption" autoresize />
        </UiCard>

        <UiCard class="burn-results__card burn-results__card--third">
          <template #header>💰 Cost by Service</template>
          <v-chart class="burn-results__chart burn-results__chart--compact" :option="topServicesOption" autoresize />
        </UiCard>

        <UiCard class="burn-results__card burn-results__card--third">
          <template #header>📈 Cost Distribution</template>
          <v-chart class="burn-results__chart burn-results__chart--compact" :option="pieChartOption" autoresize />
        </UiCard>

        <!-- Row 2: Cost Over Time and Service Burn Race -->
        <UiCard class="burn-results__card burn-results__card--half">
          <template #header>📉 Cost Over Time</template>
          <v-chart class="burn-results__chart burn-results__chart--medium" :option="timelineChartOption" autoresize />
        </UiCard>

        <UiCard class="burn-results__card burn-results__card--half">
          <template #header>🏁 Service Burn Race</template>
          <v-chart class="burn-results__chart burn-results__chart--medium" :option="racingBarOption" autoresize />
        </UiCard>

        <!-- Row 3: Money Burn Over Time and Overall Roast -->
        <UiCard class="burn-results__card burn-results__card--half">
          <template #header>💸 Money Burn Over Time</template>
          <v-chart class="burn-results__chart burn-results__chart--medium" :option="stackedAreaOption" autoresize />
        </UiCard>

        <UiCard v-if="burnPlan?.roast" class="burn-results__card burn-results__card--half">
          <template #header>🔥 Overall Roast</template>
          <div class="overall-roast">
            <div class="overall-roast__icon">💬</div>
            <div class="overall-roast__text">{{ displayedRoast }}</div>
          </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToasts } from '../composables/useToasts';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart, PieChart, GaugeChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import type { BurnPlanResponse } from '../types/burnPlan';
import { convertToChartData } from '../types/burnPlan';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';

use([CanvasRenderer, BarChart, LineChart, PieChart, GaugeChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);

const router = useRouter();
const { info } = useToasts();
const burnPlan = ref<BurnPlanResponse | null>(null);
const animationProgress = ref(0);
const currentRoast = ref('');
const displayedRoast = ref('');
const roasts = ref<string[]>([]);
const roastIndex = ref(0);
let animationFrame: number | null = null;
let startTime: number | null = null;
let roastInterval: number | null = null;
let typewriterInterval: number | null = null;

const ANIMATION_DURATION = 10000; // 10 seconds
const ROAST_INTERVAL = 5000; // Show new roast every 5 seconds
const TYPEWRITER_SPEED = 30; // milliseconds per character

onMounted(() => {
  const stored = sessionStorage.getItem('currentBurnPlan');
  if (stored) {
    try {
      burnPlan.value = JSON.parse(stored);
      generateRoasts();
      startAnimation();
      startRoastCycle();
    } catch (error) {
      console.error('Failed to parse burn plan:', error);
    }
  }
});

onUnmounted(() => {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
  }
  if (roastInterval) {
    clearInterval(roastInterval);
  }
  if (typewriterInterval) {
    clearInterval(typewriterInterval);
  }
});

const startAnimation = () => {
  startTime = Date.now();
  
  const animate = () => {
    if (!startTime) return;
    
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / ANIMATION_DURATION, 1);
    
    animationProgress.value = progress;
    
    if (progress < 1) {
      animationFrame = requestAnimationFrame(animate);
    }
  };
  
  animate();
};

const generateRoasts = () => {
  if (!burnPlan.value) return;
  
  // Use service roasts from each deployed service
  roasts.value = burnPlan.value.services_deployed
    .filter((service) => service.roast)
    .map((service) => `${service.service_name}: ${service.roast}`);
  
  // If no service roasts, generate fallback
  if (roasts.value.length === 0 && burnPlan.value.services_deployed.length > 0) {
    const topService = burnPlan.value.services_deployed[0];
    
    if (topService) {
      roasts.value = [
        `${topService.service_name}: Using ${topService.instance_type} for this? That's like using a rocket to deliver pizza.`,
        `Your ${topService.service_name} instances are burning $${Math.round(topService.total_cost).toLocaleString()}. They're lonelier than a 404 page.`,
      ];
    }
  }
  
  if (roasts.value.length > 0 && roasts.value[0]) {
    currentRoast.value = roasts.value[0];
    startTypewriter(burnPlan.value.roast || '');
  }
};

const startTypewriter = (text: string) => {
  if (typewriterInterval) {
    clearInterval(typewriterInterval);
  }
  
  displayedRoast.value = '';
  let charIndex = 0;
  
  typewriterInterval = window.setInterval(() => {
    if (charIndex < text.length) {
      displayedRoast.value += text[charIndex];
      charIndex++;
    } else {
      if (typewriterInterval) {
        clearInterval(typewriterInterval);
        typewriterInterval = null;
      }
    }
  }, TYPEWRITER_SPEED);
};

const startRoastCycle = () => {
  // Show first roast immediately
  const firstRoast = roasts.value[0];
  if (firstRoast) {
    info(firstRoast, 4500);
  }
  
  // Then cycle through remaining roasts
  roastInterval = window.setInterval(() => {
    roastIndex.value = (roastIndex.value + 1) % roasts.value.length;
    const nextRoast = roasts.value[roastIndex.value];
    if (nextRoast) {
      currentRoast.value = nextRoast;
      // Show as toast
      info(nextRoast, 4500);
    }
  }, ROAST_INTERVAL);
};

const chartData = computed(() => {
  if (!burnPlan.value) return null;
  return convertToChartData(burnPlan.value);
});

const goBack = () => {
  router.push('/app/burn-config');
};

// Get the maximum cost for fixed Y-axis scaling
const maxCost = computed(() => {
  if (!burnPlan.value) return 10000;
  return burnPlan.value.total_calculated_cost;
});

// Get the maximum daily cost for the stacked bar chart
const maxDailyCost = computed(() => {
  if (!burnPlan.value) return 1000;
  const days = burnPlan.value.timeline_days;
  // Estimate max daily cost (total / days with some buffer for stacking)
  return Math.ceil((burnPlan.value.total_calculated_cost / days) * 1.5);
});

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
  animationDuration: ANIMATION_DURATION,
  animationEasing: 'cubicOut' as const,
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
  animationDuration: ANIMATION_DURATION,
  animationEasing: 'cubicOut' as const,
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

const timelineChartOption = computed(() => {
  if (!chartData.value) return {};
  
  return {
    backgroundColor: 'transparent',
    animationDuration: ANIMATION_DURATION,
    animationEasing: 'linear' as const,
    grid: { left: '10%', right: '10%', top: '10%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: chartData.value.timelineData.timestamps,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      max: maxCost.value,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
      splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
    },
    series: [
      {
        type: 'line',
        data: chartData.value.timelineData.values,
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
  };
});

// Stacked Area Chart - Shows service contributions over time
const stackedAreaOption = computed(() => {
  if (!burnPlan.value || !chartData.value) return {};
  
  const services = burnPlan.value.services_deployed.slice(0, 5); // Top 5 services
  const colors = [neonColors.hiviz, neonColors.pink, neonColors.blue, neonColors.purple, neonColors.orange];
  
  return {
    backgroundColor: 'transparent',
    animationDuration: ANIMATION_DURATION,
    animationEasing: 'linear' as const,
    grid: { left: '10%', right: '10%', top: '15%', bottom: '15%' },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 10, 15, 0.9)',
      borderColor: neonColors.hiviz,
      borderWidth: 2,
      textStyle: { color: '#fff' },
      formatter: (params: any) => {
        let result = `${params[0].axisValue}<br/>`;
        params.forEach((item: any) => {
          result += `${item.marker} ${item.seriesName}: $${item.value}<br/>`;
        });
        return result;
      },
    },
    legend: {
      data: services.map((s) => s.service_name),
      textStyle: { color: '#fff', fontSize: 11 },
      top: '5%',
    },
    xAxis: {
      type: 'category',
      data: chartData.value.timelineData.timestamps,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      max: maxCost.value,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
      splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
    },
    series: services.map((service, idx) => ({
      name: service.service_name,
      type: 'line',
      stack: 'total',
      areaStyle: {
        color: colors[idx],
        opacity: 0.6,
      },
      lineStyle: {
        color: colors[idx],
        width: 2,
      },
      emphasis: {
        focus: 'series',
      },
      data: chartData.value?.timelineData.values.map((v: number) => 
        Math.round((service.total_cost / burnPlan.value!.total_calculated_cost) * v)
      ) || [],
    })),
  };
});

// Gauge Chart - Shows burn rate as a speedometer
const gaugeOption = computed(() => {
  const progress = Math.round(animationProgress.value * 100);
  
  return {
    backgroundColor: 'transparent',
    animationDuration: ANIMATION_DURATION,
    animationEasing: 'cubicOut' as const,
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 30,
            color: [
              [0.3, neonColors.green],
              [0.6, neonColors.orange],
              [1, neonColors.pink],
            ],
          },
        },
        pointer: {
          itemStyle: {
            color: neonColors.hiviz,
            shadowColor: neonColors.hiviz,
            shadowBlur: 10,
          },
        },
        axisTick: {
          distance: -30,
          length: 8,
          lineStyle: {
            color: '#fff',
            width: 2,
          },
        },
        splitLine: {
          distance: -30,
          length: 30,
          lineStyle: {
            color: '#fff',
            width: 4,
          },
        },
        axisLabel: {
          color: '#fff',
          distance: 40,
          fontSize: 12,
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: neonColors.hiviz,
          fontSize: 32,
          fontWeight: 'bold',
          offsetCenter: [0, '70%'],
        },
        data: [{ value: 100, name: 'Burn Progress' }],
      },
    ],
  };
});

// Racing Bar Chart - Animated horizontal bars
const racingBarOption = computed(() => {
  if (!chartData.value) return {};
  
  const topServices = chartData.value.racingBarData.slice(0, 8);
  
  return {
    backgroundColor: 'transparent',
    animationDuration: ANIMATION_DURATION,
    animationEasing: 'cubicOut' as const,
    grid: { left: '25%', right: '15%', top: '5%', bottom: '5%' },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', formatter: '${value}', fontSize: 10 },
      splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
    },
    yAxis: {
      type: 'category',
      data: topServices.map((item) => item.name),
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', fontSize: 10 },
      inverse: true,
    },
    series: [
      {
        type: 'bar',
        data: topServices.map((item, idx) => ({
          value: item.value,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: [neonColors.hiviz, neonColors.pink, neonColors.blue, neonColors.purple][idx % 4] },
                { offset: 1, color: [neonColors.hivizBright, neonColors.orange, neonColors.green, neonColors.pink][idx % 4] },
              ],
            },
            shadowBlur: 10,
          },
        })),
        label: {
          show: true,
          position: 'right',
          color: '#fff',
          formatter: '${c}',
          fontSize: 10,
        },
        barWidth: '70%',
      },
    ],
  };
});

// Stacked Bar Timeline - Shows daily breakdown
const stackedBarOption = computed(() => {
  if (!burnPlan.value || !chartData.value) return {};
  
  const services = burnPlan.value.services_deployed.slice(0, 5);
  const colors = [neonColors.hiviz, neonColors.pink, neonColors.blue, neonColors.purple, neonColors.orange];
  const days = Math.min(burnPlan.value.timeline_days, 30);
  const categories = Array.from({ length: days }, (_, i) => `Day ${i + 1}`);
  
  return {
    backgroundColor: 'transparent',
    animationDuration: ANIMATION_DURATION,
    animationEasing: 'cubicOut',
    grid: { left: '10%', right: '10%', top: '15%', bottom: '15%' },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 10, 15, 0.9)',
      borderColor: neonColors.hiviz,
      borderWidth: 2,
      textStyle: { color: '#fff' },
      axisPointer: {
        type: 'shadow',
      },
    },
    legend: {
      data: services.map((s) => s.service_name),
      textStyle: { color: '#fff', fontSize: 10 },
      top: '5%',
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', fontSize: 9, rotate: 45 },
    },
    yAxis: {
      type: 'value',
      max: maxDailyCost.value,
      axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
      axisLabel: { color: '#fff', formatter: '${value}', fontSize: 11 },
      splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
    },
    series: services.map((service, idx) => ({
      name: service.service_name,
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series',
      },
      itemStyle: {
        color: colors[idx],
      },
      data: Array.from({ length: days }, (_, day) => {
        if (day >= service.start_day && day <= service.end_day) {
          return Math.round(service.total_cost / (service.end_day - service.start_day));
        }
        return 0;
      }),
    })),
  };
});

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

.burn-results__header-actions {
  display: flex;
  gap: var(--space-sm);
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

.burn-results__progress {
  margin-bottom: var(--space-lg);
}

.progress-meter {
  background: var(--color-surface);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-lg);
  padding: var(--space-lg);
  box-shadow: 0 0 20px rgba(192, 255, 0, 0.2);
}

.progress-meter__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.progress-meter__label {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}

.progress-meter__percentage {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary);
}

.progress-meter__bar {
  height: 24px;
  background: var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  position: relative;
}

.progress-meter__fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), #d4ff4d);
  border-radius: var(--border-radius-md);
  transition: width 0.1s linear;
  box-shadow: 0 0 15px rgba(192, 255, 0, 0.5);
  position: relative;
}

.progress-meter__fill::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 40px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3));
  animation: shimmer 1s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.overall-roast {
  display: flex;
  gap: var(--space-md);
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: var(--space-xl);
  background: linear-gradient(135deg, rgba(192, 255, 0, 0.1), rgba(255, 0, 110, 0.1));
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--color-primary);
}

.overall-roast__icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.overall-roast__text {
  font-size: 1.125rem;
  color: var(--color-text);
  line-height: 1.7;
  font-style: italic;
  font-weight: 500;
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
  grid-template-columns: repeat(6, 1fr);
  gap: var(--space-lg);
}

.burn-results__card--full {
  grid-column: 1 / -1;
}

.burn-results__card--half {
  grid-column: span 3;
}

.burn-results__card--third {
  grid-column: span 2;
}

.burn-results__chart {
  height: 300px;
  width: 100%;
}

.burn-results__chart--medium {
  height: 280px;
}

.burn-results__chart--compact {
  height: 240px;
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

@media (max-width: 1400px) {
  .burn-results__content {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .burn-results__card--third {
    grid-column: span 2;
  }
}

@media (max-width: 1024px) {
  .burn-results__content {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .burn-results__card--half,
  .burn-results__card--third {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .burn-results__content {
    grid-template-columns: 1fr;
  }
  
  .burn-results__card--full,
  .burn-results__card--half,
  .burn-results__card--third {
    grid-column: 1 / -1;
  }
  
  .burn-results__chart--compact {
    height: 280px;
  }
}
</style>
