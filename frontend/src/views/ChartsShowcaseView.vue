<template>
  <div class="charts-showcase">
    <h1>ECharts Showcase</h1>
    <p class="charts-showcase__intro">
      Exploring different chart types with neon aesthetic for the Bill Burner visualization.
    </p>

    <!-- Racing Bar Chart -->
    <section class="charts-showcase__section">
      <h2>Racing Bar Chart - AWS Services Burning Money</h2>
      <p class="charts-showcase__description">
        Perfect for showing which services are consuming the most money over time.
      </p>
      <UiCard>
        <v-chart class="chart" :option="racingBarOption" autoresize />
      </UiCard>
    </section>

    <!-- Line Chart with Area -->
    <section class="charts-showcase__section">
      <h2>Money Remaining Over Time</h2>
      <p class="charts-showcase__description">
        Smooth line chart showing money burning down to zero with neon glow effect.
      </p>
      <UiCard>
        <v-chart class="chart" :option="lineChartOption" autoresize />
      </UiCard>
    </section>

    <!-- Pie Chart -->
    <section class="charts-showcase__section">
      <h2>Cost Distribution by Service Category</h2>
      <p class="charts-showcase__description">
        Pie chart showing how money is distributed across different AWS service categories.
      </p>
      <UiCard>
        <v-chart class="chart" :option="pieChartOption" autoresize />
      </UiCard>
    </section>

    <!-- Stacked Area Chart -->
    <section class="charts-showcase__section">
      <h2>Cumulative Resource Consumption</h2>
      <p class="charts-showcase__description">
        Stacked area chart showing multiple services burning money simultaneously.
      </p>
      <UiCard>
        <v-chart class="chart" :option="stackedAreaOption" autoresize />
      </UiCard>
    </section>

    <!-- Gauge Chart -->
    <section class="charts-showcase__section">
      <h2>Burn Progress Gauge</h2>
      <p class="charts-showcase__description">
        Gauge showing overall burn completion percentage with neon styling.
      </p>
      <UiCard>
        <v-chart class="chart chart--gauge" :option="gaugeOption" autoresize />
      </UiCard>
    </section>

    <!-- Racing Line Chart -->
    <section class="charts-showcase__section">
      <h2>Racing Line Chart - Service Cost Over Time</h2>
      <p class="charts-showcase__description">
        Multiple services racing to burn the most money, with animated lines and end labels.
      </p>
      <UiCard>
        <v-chart class="chart" :option="racingLineOption" autoresize />
      </UiCard>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart, PieChart, GaugeChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components';
import UiCard from '../components/UiCard.vue';

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GaugeChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

const neonColors = {
  hiviz: '#c0ff00',
  hivizBright: '#d4ff4d',
  blue: '#00F0FF',
  pink: '#FF006E',
  green: '#39FF14',
  purple: '#BC13FE',
  orange: '#FF9500',
  yellow: '#FFFF00',
};

// Racing Bar Chart
const racingBarData = ref([
  { name: 'EC2 m5.24xlarge', value: 8500 },
  { name: 'RDS Aurora', value: 6200 },
  { name: 'S3 Storage', value: 4800 },
  { name: 'Lambda Invocations', value: 3500 },
  { name: 'NAT Gateway', value: 2100 },
]);

const racingBarOption = ref({
  backgroundColor: 'transparent',
  grid: {
    left: '20%',
    right: '10%',
    top: '10%',
    bottom: '10%',
  },
  xAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}' },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  yAxis: {
    type: 'category',
    data: racingBarData.value.map((item) => item.name),
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff' },
    inverse: true,
  },
  series: [
    {
      type: 'bar',
      data: racingBarData.value.map((item) => ({
        value: item.value,
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
          shadowBlur: 20,
        },
      })),
      label: {
        show: true,
        position: 'right',
        color: '#fff',
        formatter: '${c}',
      },
      barWidth: '60%',
    },
  ],
});

// Line Chart
const lineChartOption = ref({
  backgroundColor: 'transparent',
  grid: {
    left: '10%',
    right: '10%',
    top: '15%',
    bottom: '15%',
  },
  xAxis: {
    type: 'category',
    data: ['0s', '10s', '20s', '30s', '40s', '50s', '60s'],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff' },
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}' },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  series: [
    {
      type: 'line',
      data: [10000, 8500, 6800, 4200, 2500, 800, 0],
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
      symbol: 'circle',
      symbolSize: 8,
      itemStyle: {
        color: neonColors.hiviz,
        shadowColor: neonColors.hiviz,
        shadowBlur: 10,
      },
    },
  ],
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(10, 10, 15, 0.9)',
    borderColor: neonColors.hiviz,
    borderWidth: 2,
    textStyle: { color: '#fff' },
  },
});

// Pie Chart
const pieChartOption = ref({
  backgroundColor: 'transparent',
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
    right: '10%',
    top: 'center',
    textStyle: { color: '#fff' },
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
          itemStyle: {
            color: neonColors.hiviz,
            shadowColor: neonColors.hiviz,
            shadowBlur: 20,
          },
        },
        {
          value: 2800,
          name: 'Storage',
          itemStyle: {
            color: neonColors.pink,
            shadowColor: neonColors.pink,
            shadowBlur: 20,
          },
        },
        {
          value: 2100,
          name: 'Database',
          itemStyle: {
            color: neonColors.green,
            shadowColor: neonColors.green,
            shadowBlur: 20,
          },
        },
        {
          value: 1200,
          name: 'Networking',
          itemStyle: {
            color: neonColors.purple,
            shadowColor: neonColors.purple,
            shadowBlur: 20,
          },
        },
        {
          value: 400,
          name: 'Other',
          itemStyle: {
            color: neonColors.orange,
            shadowColor: neonColors.orange,
            shadowBlur: 20,
          },
        },
      ],
      label: {
        color: '#fff',
        formatter: '{b}\n${c}',
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 30,
          shadowOffsetX: 0,
          shadowColor: 'rgba(255, 255, 255, 0.5)',
        },
      },
    },
  ],
});

// Stacked Area Chart
const stackedAreaOption = ref({
  backgroundColor: 'transparent',
  grid: {
    left: '10%',
    right: '10%',
    top: '15%',
    bottom: '15%',
  },
  xAxis: {
    type: 'category',
    data: ['0s', '15s', '30s', '45s', '60s'],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff' },
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}' },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(10, 10, 15, 0.9)',
    borderColor: neonColors.hiviz,
    borderWidth: 2,
    textStyle: { color: '#fff' },
  },
  legend: {
    data: ['EC2', 'RDS', 'S3', 'Lambda'],
    textStyle: { color: '#fff' },
    top: '5%',
  },
  series: [
    {
      name: 'EC2',
      type: 'line',
      stack: 'Total',
      data: [0, 2000, 3500, 4200, 4500],
      areaStyle: { color: 'rgba(192, 255, 0, 0.3)' },
      lineStyle: { color: neonColors.hiviz, width: 2 },
      smooth: true,
    },
    {
      name: 'RDS',
      type: 'line',
      stack: 'Total',
      data: [0, 1500, 2200, 2800, 3000],
      areaStyle: { color: 'rgba(255, 0, 110, 0.3)' },
      lineStyle: { color: neonColors.pink, width: 2 },
      smooth: true,
    },
    {
      name: 'S3',
      type: 'line',
      stack: 'Total',
      data: [0, 800, 1200, 1500, 1600],
      areaStyle: { color: 'rgba(57, 255, 20, 0.3)' },
      lineStyle: { color: neonColors.green, width: 2 },
      smooth: true,
    },
    {
      name: 'Lambda',
      type: 'line',
      stack: 'Total',
      data: [0, 500, 800, 1000, 1100],
      areaStyle: { color: 'rgba(188, 19, 254, 0.3)' },
      lineStyle: { color: neonColors.purple, width: 2 },
      smooth: true,
    },
  ],
});

// Gauge Chart
const gaugeOption = ref({
  backgroundColor: 'transparent',
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
          width: 20,
          color: [
            [0.25, neonColors.green],
            [0.5, neonColors.hiviz],
            [0.75, neonColors.orange],
            [1, neonColors.pink],
          ],
        },
      },
      pointer: {
        itemStyle: {
          color: '#fff',
          shadowColor: neonColors.hiviz,
          shadowBlur: 10,
        },
      },
      axisTick: {
        distance: -20,
        length: 8,
        lineStyle: {
          color: '#fff',
          width: 2,
        },
      },
      splitLine: {
        distance: -25,
        length: 15,
        lineStyle: {
          color: '#fff',
          width: 3,
        },
      },
      axisLabel: {
        color: '#fff',
        distance: 20,
        fontSize: 14,
      },
      detail: {
        valueAnimation: true,
        formatter: '{value}%',
        color: '#fff',
        fontSize: 32,
        offsetCenter: [0, '70%'],
      },
      data: [{ value: 73, name: 'Burn Progress' }],
      title: {
        color: '#fff',
        fontSize: 16,
        offsetCenter: [0, '90%'],
      },
    },
  ],
});

// Racing Line Chart
const racingLineOption = ref({
  backgroundColor: 'transparent',
  animationDuration: 10000,
  grid: {
    left: '10%',
    right: '15%',
    top: '15%',
    bottom: '15%',
  },
  xAxis: {
    type: 'category',
    data: ['0s', '10s', '20s', '30s', '40s', '50s', '60s'],
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff' },
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: neonColors.hiviz, width: 2 } },
    axisLabel: { color: '#fff', formatter: '${value}' },
    splitLine: { lineStyle: { color: 'rgba(192, 255, 0, 0.1)' } },
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(10, 10, 15, 0.9)',
    borderColor: neonColors.hiviz,
    borderWidth: 2,
    textStyle: { color: '#fff' },
  },
  series: [
    {
      name: 'EC2 m5.24xlarge',
      type: 'line',
      data: [0, 1200, 2800, 4500, 6200, 7800, 8500],
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: neonColors.hiviz,
        width: 3,
        shadowColor: neonColors.hiviz,
        shadowBlur: 10,
      },
      endLabel: {
        show: true,
        formatter: '{a}: ${c}',
        color: neonColors.hiviz,
        fontSize: 12,
      },
      emphasis: { focus: 'series' },
    },
    {
      name: 'RDS Aurora',
      type: 'line',
      data: [0, 800, 2000, 3500, 4800, 5800, 6200],
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: neonColors.pink,
        width: 3,
        shadowColor: neonColors.pink,
        shadowBlur: 10,
      },
      endLabel: {
        show: true,
        formatter: '{a}: ${c}',
        color: neonColors.pink,
        fontSize: 12,
      },
      emphasis: { focus: 'series' },
    },
    {
      name: 'S3 Storage',
      type: 'line',
      data: [0, 600, 1500, 2600, 3600, 4400, 4800],
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: neonColors.blue,
        width: 3,
        shadowColor: neonColors.blue,
        shadowBlur: 10,
      },
      endLabel: {
        show: true,
        formatter: '{a}: ${c}',
        color: neonColors.blue,
        fontSize: 12,
      },
      emphasis: { focus: 'series' },
    },
    {
      name: 'Lambda',
      type: 'line',
      data: [0, 400, 1000, 1800, 2600, 3200, 3500],
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: neonColors.purple,
        width: 3,
        shadowColor: neonColors.purple,
        shadowBlur: 10,
      },
      endLabel: {
        show: true,
        formatter: '{a}: ${c}',
        color: neonColors.purple,
        fontSize: 12,
      },
      emphasis: { focus: 'series' },
    },
    {
      name: 'NAT Gateway',
      type: 'line',
      data: [0, 300, 700, 1200, 1600, 1900, 2100],
      smooth: true,
      showSymbol: false,
      lineStyle: {
        color: neonColors.orange,
        width: 3,
        shadowColor: neonColors.orange,
        shadowBlur: 10,
      },
      endLabel: {
        show: true,
        formatter: '{a}: ${c}',
        color: neonColors.orange,
        fontSize: 12,
      },
      emphasis: { focus: 'series' },
    },
  ],
});

// Simulate racing bar animation
let racingInterval: number | null = null;

onMounted(() => {
  racingInterval = window.setInterval(() => {
    racingBarData.value = racingBarData.value.map((item) => ({
      ...item,
      value: Math.max(0, item.value + (Math.random() - 0.5) * 1000),
    }));
    racingBarData.value.sort((a, b) => b.value - a.value);
    racingBarOption.value.yAxis.data = racingBarData.value.map((item) => item.name);
    racingBarOption.value.series[0].data = racingBarData.value.map((item) => ({
      value: item.value,
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
        shadowBlur: 20,
      },
    }));
  }, 2000);
});

onUnmounted(() => {
  if (racingInterval) {
    clearInterval(racingInterval);
  }
});
</script>

<style scoped>
.charts-showcase {
  max-width: 1400px;
  margin: 0 auto;
}

.charts-showcase h1 {
  color: var(--color-text);
  margin-bottom: var(--space-sm);
  font-size: 1.75rem;
}

.charts-showcase__intro {
  color: var(--color-text-muted);
  margin-bottom: var(--space-xl);
  font-size: 0.875rem;
}

.charts-showcase__section {
  margin-bottom: var(--space-xl);
}

.charts-showcase__section h2 {
  color: var(--color-text);
  margin-bottom: var(--space-sm);
  font-size: 1.25rem;
}

.charts-showcase__description {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-bottom: var(--space-md);
}

.chart {
  height: 400px;
  width: 100%;
}

.chart--gauge {
  height: 350px;
}

@media (min-width: 640px) {
  .charts-showcase h1 {
    font-size: 2rem;
  }

  .charts-showcase__section h2 {
    font-size: 1.5rem;
  }

  .charts-showcase__intro,
  .charts-showcase__description {
    font-size: 1rem;
  }
}
</style>
