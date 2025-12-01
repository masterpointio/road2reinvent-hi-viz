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

export interface ApiServiceDeployment {
  service_name: string;
  instance_type?: string;
  quantity: number;
  start_day: number;
  end_day: number;
  duration_used: string;
  unit_cost: number;
  total_cost: number;
  usage_pattern: string;
  waste_factor: string;
  roast: string;
}

export interface PdfInvoice {
  url: string;
  s3_key: string;
  bucket: string;
  expiration_seconds: number;
  upload_status: string;
}

export interface BurnPlanAnalysis {
  total_amount: string;
  timeline_days: number;
  efficiency_level: string;
  architecture_type?: string;
  burning_style?: string;
  services_deployed: ApiServiceDeployment[];
  total_calculated_cost: number;
  deployment_scenario: string;
  key_mistakes: string[];
  recommendations: string[];
  roast: string;
  pdf_invoice?: PdfInvoice;
}

export interface BurnPlanApiResponse {
  analysis: BurnPlanAnalysis;
  status: string;
}

export const useBurnPlan = () => {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const createBurnPlan = async (config: BurnConfig): Promise<BurnPlanAnalysis | null> => {
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
      
      const response = await apiClient.post<BurnPlanApiResponse>('/api/burn-plan', requestPayload);
      
      console.log('Response received:', response);

      // Return the analysis object which contains all burn plan data including pdf_invoice
      return response.analysis;
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
