import { ref } from 'vue';
import { apiClient } from '../lib/apiClient';

export interface BurnConfig {
  totalAmount: number;
  timeline: string;
  architecture: string;
  burningStyle: string;
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
    total_amount: number;
    timeline_days: number;
    efficiency_level: string;
    services_deployed: Array<{
      service_name: string;
      instance_type?: string;
      quantity: number;
      start_day: number;
      end_day: number;
      duration_used: number;
      unit_cost: number;
      total_cost: number;
      usage_pattern: string;
      waste_factor: number;
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
      const response = await apiClient.post<BurnPlanResponse>('/burn-plan', {
        config: {
          total_amount: config.totalAmount,
          timeline: config.timeline,
          architecture: config.architecture,
          burning_style: config.burningStyle,
          efficiency_level: config.efficiencyLevel,
        },
      });

      // Transform backend response to frontend format
      const burnPlan: BurnPlan = {
        sessionId: response.session_id,
        totalAmount: response.burn_plan.total_amount,
        duration: 60, // Default 60 seconds for visualization
        timeline: config.timeline,
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
          description: service.usage_pattern,
          costPerSecond: service.total_cost / 60,
        })),
      };

      return burnPlan;
    } catch (err: any) {
      error.value = err.message || 'Failed to create burn plan';
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
