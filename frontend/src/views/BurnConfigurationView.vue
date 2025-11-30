<template>
  <div class="burn-config">
    <div class="burn-config__container">
      <h1 class="burn-config__title">🔥 Configure Your Burn</h1>
      <p class="burn-config__subtitle">Let's waste some money in style</p>

      <UiCard class="burn-config__card">
        <!-- Step 1: Amount -->
        <div class="burn-config__step">
          <label class="burn-config__label">
            How much money do you want to burn?
            <span class="burn-config__hint">Be honest, we won't judge... much</span>
          </label>
          <div class="burn-config__input-group">
            <span class="burn-config__prefix">$</span>
            <input
              v-model="config.totalAmount"
              type="number"
              class="burn-config__input"
              placeholder="1500"
              min="1"
            />
          </div>
        </div>

        <!-- Step 2: Timeline -->
        <div class="burn-config__step">
          <label class="burn-config__label">
            How long do you have to burn it?
            <span class="burn-config__hint">Patience is a virtue, but so is speed</span>
          </label>
          <div class="burn-config__options">
            <button
              v-for="timeline in timelineOptions"
              :key="timeline.value"
              :class="['burn-config__option', { 'burn-config__option--active': config.timeline === timeline.value }]"
              @click="config.timeline = timeline.value"
            >
              <div class="burn-config__option-icon">{{ timeline.icon }}</div>
              <div class="burn-config__option-label">{{ timeline.label }}</div>
            </button>
          </div>
        </div>

        <!-- Step 3: Architecture Style -->
        <div class="burn-config__step">
          <label class="burn-config__label">
            How do you want to burn it?
            <span class="burn-config__hint">Choose your weapon of financial destruction</span>
          </label>
          <div class="burn-config__options">
            <button
              v-for="arch in architectureOptions"
              :key="arch.value"
              :class="['burn-config__option', { 'burn-config__option--active': config.architecture === arch.value }]"
              @click="config.architecture = arch.value"
            >
              <div class="burn-config__option-icon">{{ arch.icon }}</div>
              <div class="burn-config__option-label">{{ arch.label }}</div>
              <div class="burn-config__option-desc">{{ arch.description }}</div>
            </button>
          </div>
        </div>

        <!-- Step 4: Burning Style -->
        <div class="burn-config__step">
          <label class="burn-config__label">
            Burning style?
            <span class="burn-config__hint">Quality over quantity, or quantity over quality?</span>
          </label>
          <div class="burn-config__options burn-config__options--two">
            <button
              v-for="style in burningStyleOptions"
              :key="style.value"
              :class="['burn-config__option', { 'burn-config__option--active': config.burningStyle === style.value }]"
              @click="config.burningStyle = style.value"
            >
              <div class="burn-config__option-icon">{{ style.icon }}</div>
              <div class="burn-config__option-label">{{ style.label }}</div>
              <div class="burn-config__option-desc">{{ style.description }}</div>
            </button>
          </div>
        </div>

        <!-- Step 5: Efficiency Level -->
        <div class="burn-config__step">
          <label class="burn-config__label">
            How stupid should this be?
            <span class="burn-config__hint">On a scale from "mildly dumb" to "brain damage"</span>
          </label>
          <div class="burn-config__slider">
            <input
              v-model="config.efficiencyLevel"
              type="range"
              min="1"
              max="10"
              class="burn-config__range"
            />
            <div class="burn-config__slider-labels">
              <span>Mildly Dumb</span>
              <span class="burn-config__slider-value">{{ efficiencyLevelLabel }}</span>
              <span>Brain Damage</span>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="burn-config__summary">
          <h3>Your Burn Plan</h3>
          <div class="burn-config__summary-grid">
            <div class="burn-config__summary-item">
              <span class="burn-config__summary-label">Amount</span>
              <span class="burn-config__summary-value">${{ config.totalAmount || 0 }}</span>
            </div>
            <div class="burn-config__summary-item">
              <span class="burn-config__summary-label">Timeline</span>
              <span class="burn-config__summary-value">{{ config.timeline || 'Not set' }}</span>
            </div>
            <div class="burn-config__summary-item">
              <span class="burn-config__summary-label">Architecture</span>
              <span class="burn-config__summary-value">{{ config.architecture || 'Not set' }}</span>
            </div>
            <div class="burn-config__summary-item">
              <span class="burn-config__summary-label">Style</span>
              <span class="burn-config__summary-value">{{ config.burningStyle || 'Not set' }}</span>
            </div>
          </div>
        </div>

        <template #footer>
          <UiButton variant="secondary" @click="resetForm">Reset</UiButton>
          <UiButton variant="primary" :disabled="!isFormValid" @click="startBurn">
            🔥 Start Burning
          </UiButton>
        </template>
      </UiCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useToasts } from '../composables/useToasts';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';

const router = useRouter();
const { success } = useToasts();

interface BurnConfig {
  totalAmount: number | null;
  timeline: string;
  architecture: string;
  burningStyle: string;
  efficiencyLevel: number;
}

const config = ref<BurnConfig>({
  totalAmount: null,
  timeline: '',
  architecture: '',
  burningStyle: '',
  efficiencyLevel: 5,
});

const timelineOptions = [
  { value: '1 hour', label: '1 Hour', icon: '⚡' },
  { value: '1 day', label: '1 Day', icon: '☀️' },
  { value: '1 week', label: '1 Week', icon: '📅' },
  { value: '2 weeks', label: '2 Weeks', icon: '📆' },
  { value: '1 month', label: '1 Month', icon: '🗓️' },
];

const architectureOptions = [
  {
    value: 'serverless',
    label: 'Serverless',
    icon: '⚡',
    description: 'Lambda, API Gateway, DynamoDB',
  },
  {
    value: 'kubernetes',
    label: 'Kubernetes',
    icon: '☸️',
    description: 'EKS, EC2, Load Balancers',
  },
  {
    value: 'traditional',
    label: 'Traditional',
    icon: '🖥️',
    description: 'EC2, RDS, Classic infra',
  },
  {
    value: 'mixed',
    label: 'Mixed Bag',
    icon: '🎲',
    description: 'A little bit of everything',
  },
];

const burningStyleOptions = [
  {
    value: 'horizontal',
    label: 'Horizontal',
    icon: '↔️',
    description: 'Many small services',
  },
  {
    value: 'vertical',
    label: 'Vertical',
    icon: '↕️',
    description: 'Few expensive services',
  },
];

const efficiencyLevelLabel = computed(() => {
  const level = config.value.efficiencyLevel;
  if (level <= 2) return 'Mildly Dumb';
  if (level <= 4) return 'Pretty Dumb';
  if (level <= 6) return 'Very Stupid';
  if (level <= 8) return 'Extremely Stupid';
  return 'Brain Damage';
});

const isFormValid = computed(() => {
  return (
    config.value.totalAmount &&
    config.value.totalAmount > 0 &&
    config.value.timeline &&
    config.value.architecture &&
    config.value.burningStyle
  );
});

const resetForm = () => {
  config.value = {
    totalAmount: null,
    timeline: '',
    architecture: '',
    burningStyle: '',
    efficiencyLevel: 5,
  };
};

const startBurn = async () => {
  if (!isFormValid.value) return;

  // Mock API call
  success('Generating your burn plan...');

  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Mock burn plan data
  const mockBurnPlan = generateMockBurnPlan(config.value);

  // Store in session storage for the visualization page
  sessionStorage.setItem('currentBurnPlan', JSON.stringify(mockBurnPlan));

  success('Burn plan generated! Starting visualization...');

  // Navigate to visualization (we'll create this next)
  setTimeout(() => {
    router.push('/app/burn-visualization');
  }, 500);
};

function generateMockBurnPlan(cfg: BurnConfig) {
  const resources = [];
  const amount = cfg.totalAmount || 0;

  // Generate resources based on architecture
  if (cfg.architecture === 'serverless') {
    resources.push(
      {
        service: 'Lambda Invocations',
        category: 'Compute',
        cost: amount * 0.3,
        startTime: 0,
        endTime: 60,
        description: 'Millions of function calls for a hello world API',
      },
      {
        service: 'API Gateway',
        category: 'Networking',
        cost: amount * 0.25,
        startTime: 5,
        endTime: 60,
        description: 'REST API that nobody calls',
      },
      {
        service: 'DynamoDB',
        category: 'Database',
        cost: amount * 0.25,
        startTime: 0,
        endTime: 60,
        description: 'NoSQL database for 3 records',
      },
      {
        service: 'S3 Storage',
        category: 'Storage',
        cost: amount * 0.2,
        startTime: 10,
        endTime: 60,
        description: 'Storing deployment artifacts forever',
      }
    );
  } else if (cfg.architecture === 'kubernetes') {
    resources.push(
      {
        service: 'EKS Cluster',
        category: 'Compute',
        cost: amount * 0.35,
        startTime: 0,
        endTime: 60,
        description: 'Kubernetes cluster for a single pod',
      },
      {
        service: 'EC2 Worker Nodes',
        category: 'Compute',
        cost: amount * 0.3,
        startTime: 5,
        endTime: 60,
        description: 'm5.2xlarge nodes running at 5% CPU',
      },
      {
        service: 'Load Balancer',
        category: 'Networking',
        cost: amount * 0.2,
        startTime: 0,
        endTime: 60,
        description: 'Load balancing zero traffic',
      },
      {
        service: 'EBS Volumes',
        category: 'Storage',
        cost: amount * 0.15,
        startTime: 10,
        endTime: 60,
        description: 'Provisioned IOPS for logs',
      }
    );
  } else if (cfg.architecture === 'traditional') {
    resources.push(
      {
        service: 'EC2 m5.24xlarge',
        category: 'Compute',
        cost: amount * 0.4,
        startTime: 0,
        endTime: 60,
        description: '96 vCPUs for your WordPress blog',
      },
      {
        service: 'RDS Aurora',
        category: 'Database',
        cost: amount * 0.3,
        startTime: 5,
        endTime: 60,
        description: 'Multi-AZ database for a todo list',
      },
      {
        service: 'NAT Gateway',
        category: 'Networking',
        cost: amount * 0.2,
        startTime: 0,
        endTime: 60,
        description: 'Routing packets to nowhere',
      },
      {
        service: 'EBS gp3',
        category: 'Storage',
        cost: amount * 0.1,
        startTime: 10,
        endTime: 60,
        description: 'Fast storage for slow queries',
      }
    );
  } else {
    // Mixed
    resources.push(
      {
        service: 'EC2 Instances',
        category: 'Compute',
        cost: amount * 0.25,
        startTime: 0,
        endTime: 60,
        description: 'A fleet of underutilized servers',
      },
      {
        service: 'Lambda Functions',
        category: 'Compute',
        cost: amount * 0.2,
        startTime: 5,
        endTime: 60,
        description: 'Serverless chaos',
      },
      {
        service: 'RDS + DynamoDB',
        category: 'Database',
        cost: amount * 0.25,
        startTime: 0,
        endTime: 60,
        description: 'Two databases because why not',
      },
      {
        service: 'S3 + EBS',
        category: 'Storage',
        cost: amount * 0.15,
        startTime: 10,
        endTime: 60,
        description: 'Redundant storage redundancy',
      },
      {
        service: 'NAT + ALB',
        category: 'Networking',
        cost: amount * 0.15,
        startTime: 0,
        endTime: 60,
        description: 'Network complexity for fun',
      }
    );
  }

  // Adjust based on burning style
  if (cfg.burningStyle === 'horizontal') {
    // Split resources into more smaller ones
    const newResources: typeof resources = [];
    resources.forEach((r) => {
      const count = Math.floor(Math.random() * 3) + 2;
      for (let i = 0; i < count; i++) {
        newResources.push({
          ...r,
          service: `${r.service} #${i + 1}`,
          cost: r.cost / count,
        });
      }
    });
    resources.length = 0;
    resources.push(...newResources);
  }

  return {
    sessionId: `burn-${Date.now()}`,
    totalAmount: amount,
    duration: 60,
    timeline: cfg.timeline,
    architecture: cfg.architecture,
    burningStyle: cfg.burningStyle,
    efficiencyLevel: cfg.efficiencyLevel,
    resources,
  };
}
</script>

<style scoped>
.burn-config {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
}

.burn-config__container {
  width: 100%;
  max-width: 800px;
}

.burn-config__title {
  text-align: center;
  color: var(--color-text);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-xs);
}

.burn-config__subtitle {
  text-align: center;
  color: var(--color-text-muted);
  margin-bottom: var(--space-xl);
}

.burn-config__card {
  background: var(--color-surface);
}

.burn-config__step {
  margin-bottom: var(--space-xl);
}

.burn-config__label {
  display: block;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-md);
}

.burn-config__hint {
  display: block;
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--color-text-muted);
  margin-top: var(--space-xs);
}

.burn-config__input-group {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.burn-config__prefix {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-primary);
}

.burn-config__input {
  flex: 1;
  padding: var(--space-md);
  font-size: 1.5rem;
  font-weight: 600;
  background: var(--color-bg);
  border: 2px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  color: var(--color-text);
  transition: all 0.2s;
}

.burn-config__input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(192, 255, 0, 0.1);
}

.burn-config__options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-md);
}

.burn-config__options--two {
  grid-template-columns: repeat(2, 1fr);
}

.burn-config__option {
  padding: var(--space-lg);
  background: var(--color-bg);
  border: 2px solid var(--color-surface-soft);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.burn-config__option:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.burn-config__option--active {
  border-color: var(--color-primary);
  background: var(--color-surface-soft);
  box-shadow: 0 0 20px rgba(192, 255, 0, 0.2);
}

.burn-config__option-icon {
  font-size: 2rem;
  margin-bottom: var(--space-sm);
}

.burn-config__option-label {
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-xs);
}

.burn-config__option-desc {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.burn-config__slider {
  padding: var(--space-md);
  background: var(--color-bg);
  border-radius: var(--border-radius-md);
}

.burn-config__range {
  width: 100%;
  height: 8px;
  border-radius: var(--border-radius-sm);
  background: var(--color-surface-soft);
  outline: none;
  -webkit-appearance: none;
}

.burn-config__range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  cursor: pointer;
  box-shadow: 0 0 10px var(--color-primary);
}

.burn-config__range::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px var(--color-primary);
}

.burn-config__slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-md);
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.burn-config__slider-value {
  font-weight: 600;
  color: var(--color-primary);
}

.burn-config__summary {
  padding: var(--space-lg);
  background: var(--color-bg);
  border-radius: var(--border-radius-md);
  border: 2px solid var(--color-primary);
}

.burn-config__summary h3 {
  color: var(--color-text);
  margin-bottom: var(--space-md);
}

.burn-config__summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

.burn-config__summary-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.burn-config__summary-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.burn-config__summary-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-primary);
}

@media (min-width: 640px) {
  .burn-config__summary-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
