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
              <span class="burn-config__summary-value">{{ config.timeline ? `${config.timeline} days` : 'Not set' }}</span>
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
          <UiButton variant="secondary" @click="resetForm" :disabled="isBurnPlanLoading">Reset</UiButton>
          <UiButton variant="primary" :disabled="!isFormValid || isBurnPlanLoading" @click="startBurn">
            {{ isBurnPlanLoading ? '🔥 Generating...' : '🔥 Start Burning' }}
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
import { useApi } from '../composables/useApi';
import type { BurnPlanResponse, ServiceDeployment } from '../types/burnPlan';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';

const router = useRouter();
const { success, error: showError } = useToasts();
const isBurnPlanLoading = ref(false);

interface BurnConfig {
  totalAmount: number | null;
  timeline: number | null;
  architecture: string;
  burningStyle: string;
  efficiencyLevel: number;
}

const config = ref<BurnConfig>({
  totalAmount: null,
  timeline: null,
  architecture: '',
  burningStyle: '',
  efficiencyLevel: 5,
});

const timelineOptions = [
  { value: 7, label: '7 Days', icon: '⚡' },
  { value: 14, label: '14 Days', icon: '📅' },
  { value: 30, label: '30 Days', icon: '📆' },
  { value: 45, label: '45 Days', icon: '🗓️' },
  { value: 60, label: '60 Days', icon: '📊' },
  { value: 90, label: '90 Days', icon: '📈' },
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
  if (level <= 2) return 'Mildly dumb';
  if (level <= 4) return 'Moderately stupid';
  if (level <= 6) return 'Very stupid';
  if (level <= 8) return 'Extremely stupid';
  return 'Brain damage';
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
    timeline: null,
    architecture: '',
    burningStyle: '',
    efficiencyLevel: 5,
  };
};

const startBurn = async () => {
  if (!isFormValid.value || !config.value.totalAmount || !config.value.timeline) {
    return;
  }

  isBurnPlanLoading.value = true;
  success('Generating your burn plan...');

  // Make API call directly to store raw response
  try {
    const stupidityMap: Record<number, string> = {
      1: 'Mildly dumb',
      2: 'Mildly dumb',
      3: 'Moderately stupid',
      4: 'Moderately stupid',
      5: 'Moderately stupid',
      6: 'Very stupid',
      7: 'Very stupid',
      8: 'Very stupid',
      9: 'Brain damage',
      10: 'Brain damage',
    };

    const { post } = useApi();
    const response = await post<any>('/api/burn-plan', {
      config: {
        amount: `$${config.value.totalAmount}`,
        timeline: config.value.timeline,
        architecture: config.value.architecture,
        burning_style: config.value.burningStyle,
        stupidity: stupidityMap[config.value.efficiencyLevel] || 'Moderately stupid',
      },
    });

    // Store the raw backend response (BurnResultsView expects this format)
    sessionStorage.setItem('currentBurnPlan', JSON.stringify(response.burn_plan));

    success('Burn plan generated! Redirecting...');

    setTimeout(() => {
      router.push('/app/burn-results');
    }, 500);
  } catch (err) {
    showError('Failed to generate burn plan. Please try again.');
    console.error('Error in startBurn:', err);
  } finally {
    isBurnPlanLoading.value = false;
  }
};

function generateMockBurnPlan(cfg: BurnConfig): BurnPlanResponse {
  const amount = cfg.totalAmount || 0;
  const timeline = cfg.timeline || 30;
  const services: ServiceDeployment[] = [];

  const generateServiceRoast = (serviceName: string, instanceType: string, wasteFactor: string): string => {
    const roasts: Record<string, string[]> = {
      Lambda: [
        `${instanceType} Lambda functions? That's like using a sledgehammer to hang a picture.`,
        'Millions of Lambda invocations for hello world? The cloud is crying.',
      ],
      'API Gateway': [
        'An API Gateway that nobody calls? At least it has job security.',
        'REST API for internal use? That\'s like hiring a translator for yourself.',
      ],
      DynamoDB: [
        'DynamoDB for 3 records? That\'s like renting a warehouse for a shoebox.',
        'On-demand pricing for data you never access? Bold strategy.',
      ],
      S3: [
        'S3 Standard for archival data? Glacier is having an existential crisis.',
        'Storing artifacts forever? Marie Kondo would not approve.',
      ],
      EKS: [
        'EKS cluster for a single pod? That\'s like buying a stadium for a chess match.',
        'Kubernetes for this? You could\'ve just used a Raspberry Pi.',
      ],
      EC2: [
        `${instanceType} for this workload? That's like using a rocket to deliver pizza.`,
        'Those vCPUs are lonelier than a 404 page.',
      ],
      ALB: [
        'Load balancing zero traffic? At least it\'s getting paid to do nothing.',
        'An ALB for one server? That\'s adorable.',
      ],
      EBS: [
        'Provisioned IOPS for logs? Those logs must be very important.',
        'That storage costs more than the data it holds.',
      ],
      RDS: [
        `${instanceType} database for a todo list? Your 3 users will appreciate the redundancy.`,
        'Multi-AZ for dev? That\'s like having a backup parachute for your office chair.',
      ],
      'NAT Gateway': [
        'NAT Gateway routing packets to nowhere? Efficient.',
        'That NAT Gateway costs more than your actual compute.',
      ],
      SageMaker: [
        'SageMaker notebooks running 24/7? Those GPUs are bored.',
        `${instanceType} for a simple model? That's like using a supercomputer for a calculator.`,
      ],
    };

    const serviceRoasts = roasts[serviceName] || [`${serviceName} ${instanceType}? Interesting choice.`];
    return serviceRoasts[Math.floor(Math.random() * serviceRoasts.length)] || `${serviceName} roast unavailable`;
  };

  if (cfg.architecture === 'serverless') {
    services.push(
      {
        service_name: 'Lambda',
        instance_type: '1GB Memory',
        quantity: 1000000,
        unit_cost: 0.0000166667,
        total_cost: amount * 0.3,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Millions of invocations for hello world',
        roast: generateServiceRoast('Lambda', '1GB Memory', 'Millions of invocations for hello world'),
      },
      {
        service_name: 'API Gateway',
        instance_type: 'REST API',
        quantity: 1,
        unit_cost: amount * 0.25,
        total_cost: amount * 0.25,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'API that nobody calls',
        roast: generateServiceRoast('API Gateway', 'REST API', 'API that nobody calls'),
      },
      {
        service_name: 'DynamoDB',
        instance_type: 'On-Demand',
        quantity: 1,
        unit_cost: amount * 0.25,
        total_cost: amount * 0.25,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Database for 3 records',
        roast: generateServiceRoast('DynamoDB', 'On-Demand', 'Database for 3 records'),
      },
      {
        service_name: 'S3',
        instance_type: 'Standard',
        quantity: 1000,
        unit_cost: 0.023,
        total_cost: amount * 0.2,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Storing artifacts forever',
        roast: generateServiceRoast('S3', 'Standard', 'Storing artifacts forever'),
      }
    );
  } else if (cfg.architecture === 'kubernetes') {
    services.push(
      {
        service_name: 'EKS',
        instance_type: 'Cluster',
        quantity: 1,
        unit_cost: 0.1,
        total_cost: amount * 0.15,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Cluster for single pod',
        roast: generateServiceRoast('EKS', 'Cluster', 'Cluster for single pod'),
      },
      {
        service_name: 'EC2',
        instance_type: 'm5.2xlarge',
        quantity: 10,
        unit_cost: 0.384,
        total_cost: amount * 0.4,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Nodes at 5% CPU',
        roast: generateServiceRoast('EC2', 'm5.2xlarge', 'Nodes at 5% CPU'),
      },
      {
        service_name: 'ALB',
        instance_type: 'Load Balancer',
        quantity: 2,
        unit_cost: 0.0225,
        total_cost: amount * 0.2,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Load balancing zero traffic',
        roast: generateServiceRoast('ALB', 'Load Balancer', 'Load balancing zero traffic'),
      },
      {
        service_name: 'EBS',
        instance_type: 'io2',
        quantity: 500,
        unit_cost: 0.125,
        total_cost: amount * 0.25,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Provisioned IOPS for logs',
        roast: generateServiceRoast('EBS', 'io2', 'Provisioned IOPS for logs'),
      }
    );
  } else if (cfg.architecture === 'traditional') {
    services.push(
      {
        service_name: 'EC2',
        instance_type: 'm5.24xlarge',
        quantity: 3,
        unit_cost: 4.608,
        total_cost: amount * 0.4,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: '96 vCPUs for WordPress',
        roast: generateServiceRoast('EC2', 'm5.24xlarge', '96 vCPUs for WordPress'),
      },
      {
        service_name: 'RDS',
        instance_type: 'db.r6g.8xlarge',
        quantity: 1,
        unit_cost: 2.88,
        total_cost: amount * 0.3,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Multi-AZ for todo list',
        roast: generateServiceRoast('RDS', 'db.r6g.8xlarge', 'Multi-AZ for todo list'),
      },
      {
        service_name: 'NAT Gateway',
        instance_type: 'NAT Gateway',
        quantity: 3,
        unit_cost: 0.045,
        total_cost: amount * 0.2,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Routing to nowhere',
        roast: generateServiceRoast('NAT Gateway', 'NAT Gateway', 'Routing to nowhere'),
      },
      {
        service_name: 'EBS',
        instance_type: 'gp3',
        quantity: 2000,
        unit_cost: 0.08,
        total_cost: amount * 0.1,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Fast storage for slow queries',
        roast: generateServiceRoast('EBS', 'gp3', 'Fast storage for slow queries'),
      }
    );
  } else {
    services.push(
      {
        service_name: 'EC2',
        instance_type: 'm5.xlarge',
        quantity: 20,
        unit_cost: 0.192,
        total_cost: amount * 0.25,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Underutilized fleet',
        roast: generateServiceRoast('EC2', 'm5.xlarge', 'Underutilized fleet'),
      },
      {
        service_name: 'Lambda',
        instance_type: '512MB',
        quantity: 500000,
        unit_cost: 0.0000083333,
        total_cost: amount * 0.2,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Serverless chaos',
        roast: generateServiceRoast('Lambda', '512MB', 'Serverless chaos'),
      },
      {
        service_name: 'RDS',
        instance_type: 'db.t3.large',
        quantity: 2,
        unit_cost: 0.136,
        total_cost: amount * 0.15,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Two databases',
        roast: generateServiceRoast('RDS', 'db.t3.large', 'Two databases'),
      },
      {
        service_name: 'DynamoDB',
        instance_type: 'On-Demand',
        quantity: 1,
        unit_cost: amount * 0.1,
        total_cost: amount * 0.1,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Redundant with RDS',
        roast: generateServiceRoast('DynamoDB', 'On-Demand', 'Redundant with RDS'),
      },
      {
        service_name: 'S3',
        instance_type: 'Standard',
        quantity: 500,
        unit_cost: 0.023,
        total_cost: amount * 0.15,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Redundant storage',
        roast: generateServiceRoast('S3', 'Standard', 'Redundant storage'),
      },
      {
        service_name: 'NAT Gateway',
        instance_type: 'NAT Gateway',
        quantity: 2,
        unit_cost: 0.045,
        total_cost: amount * 0.15,
        start_day: 0,
        end_day: timeline,
        duration_used: 'entire timeline',
        usage_pattern: 'Running 24/7',
        waste_factor: 'Network complexity',
        roast: generateServiceRoast('NAT Gateway', 'NAT Gateway', 'Network complexity'),
      }
    );
  }

  const totalCost = services.reduce((sum, s) => sum + s.total_cost, 0);
  const topService = services[0];
  const topServiceName = topService?.service_name || 'services';
  const topServiceType = topService?.instance_type || 'instances';

  return {
    total_amount: `$${amount}`,
    timeline_days: timeline,
    efficiency_level: efficiencyLevelLabel.value,
    architecture_type: cfg.architecture,
    burning_style: cfg.burningStyle,
    services_deployed: services,
    total_calculated_cost: totalCost,
    deployment_scenario: `${cfg.architecture} architecture with ${cfg.burningStyle} scaling over ${timeline} days`,
    key_mistakes: services.map((s) => s.waste_factor),
    recommendations: [
      'Right-size instances based on workload',
      'Use auto-scaling to match demand',
      'Consider reserved instances',
      'Implement cost monitoring',
    ],
    roast: `You've spent $${Math.round(totalCost).toLocaleString()} on a ${cfg.architecture} architecture that's more over-engineered than a NASA rover. Using ${topServiceName} ${topServiceType} for this workload? You've built a spaceship to deliver a letter. That's ${Math.round(totalCost / 2)} burritos or ${Math.round(totalCost / 15)} Netflix subscriptions you'll never enjoy. Congratulations on achieving "${efficiencyLevelLabel.value}" level efficiency!`,
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
