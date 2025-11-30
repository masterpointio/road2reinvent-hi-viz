import { ref } from 'vue';
import { apiClient } from '../lib/apiClient';

export interface BurnConfig {
  totalAmount: number;
  timeline: number;
  architecture: 'serverless' | 'kubernetes' | 'traditional' | 'mixed';
  burningStyle: 'horizontal' | 'vertical';
  efficiencyLevel: number;
}

export interface Resource {
  service: string;
  category: string;
  cost: number;
  startTime: number;
  endTime: number;
  description: string;
  costPerSecond?: number;
}

export interface BurnPlan {
  sessionId: string;
  totalAmount: number;
  duration: number;
  timeline: string;
  architecture: string;
  burningStyle: string;
  efficiencyLevel: number;
  resources: Resource[];
}

export interface BurnPlanResponse {
  session_id: string;
  burn_plan: {
    total_amount: string;
    timeline_days: number;
    efficiency_level: string;
    services_deployed: Array<{
      service_name: string;
      instance_type?: string;
      quantity: number;
      start_day: number;
      end_day: number;
      duration_used: string;
      unit_cost: number;
      total_cost: number;
      usage_pattern?: string;
      waste_factor?: string;
    }>;
    total_calculated_cost: number;
    deployment_scenario: string;
    key_mistakes: string[];
    recommendations: string[];
  };
}

export const useBurnPlan = () => {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const createBurnPlan = async (config: BurnConfig): Promise<BurnPlan | null> => {
    isLoading.value = true;
    error.value = null;

    try {
      // Map efficiency level to stupidity label
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

      console.log('Creating burn plan with config:', config);
      
      const requestPayload = {
        config: {
          amount: `$${config.totalAmount}`,
          timeline: config.timeline,
          architecture: config.architecture,
          burning_style: config.burningStyle,
          stupidity: stupidityMap[config.efficiencyLevel] || 'Moderately stupid',
        },
      };
      
      console.log('Request payload:', requestPayload);
      
      const response = await apiClient.post<BurnPlanResponse>('/api/burn-plan', requestPayload);
      
      console.log('Response received:', response);

      // Transform backend response to frontend format
      const burnPlan: BurnPlan = {
        sessionId: response.session_id,
        totalAmount: parseFloat(response.burn_plan.total_amount.replace(/[$,]/g, '')),
        duration: 60, // Default 60 seconds for visualization
        timeline: `${config.timeline}d`,
        architecture: config.architecture,
        burningStyle: config.burningStyle,
        efficiencyLevel: config.efficiencyLevel,
        resources: response.burn_plan.services_deployed.map((service, index) => ({
          service: service.instance_type
            ? `${service.service_name} ${service.instance_type}`
            : service.service_name,
          category: getCategoryFromService(service.service_name),
          cost: service.total_cost,
          startTime: (index * 5) % 60, // Stagger start times
          endTime: 60,
          description: service.usage_pattern || service.waste_factor || '',
          costPerSecond: service.total_cost / 60,
        })),
      };

      return burnPlan;
    } catch (err: unknown) {
      // Provide more helpful error messages
      if (err.status === 401 || err.status === 403) {
        error.value = 'Authentication failed. Please log in again.';
      } else if (err.status === 504) {
        error.value = 'Request timed out. The agent is taking too long to respond.';
      } else if (err.status === 429) {
        error.value = 'Rate limit exceeded. Please try again later.';
      } else if (err.status === 502 || err.status === 503) {
        error.value = 'Service temporarily unavailable. Please try again.';
      } else {
        error.value = err.message || 'Failed to create burn plan';
      }
      console.error('Burn plan creation error:', err);
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    isLoading,
    error,
    createBurnPlan,
  };
};

function getCategoryFromService(serviceName: string): string {
  const service = serviceName.toLowerCase();
  if (service.includes('ec2') || service.includes('eks') || service.includes('lambda')) {
    return 'Compute';
  }
  if (service.includes('rds') || service.includes('dynamodb') || service.includes('documentdb')) {
    return 'Database';
  }
  if (service.includes('s3') || service.includes('ebs') || service.includes('efs')) {
    return 'Storage';
  }
  if (service.includes('cloudfront') || service.includes('nat') || service.includes('vpn')) {
    return 'Networking';
  }
  if (service.includes('sagemaker') || service.includes('braket')) {
    return 'ML';
  }
  return 'Other';
}
