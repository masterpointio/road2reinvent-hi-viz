import { ref } from 'vue';
import { useApi } from './useApi';
import type { ApiResponse } from '../lib/apiClient';
import type { BurnPlanResponse } from '../types/burnPlan';

export interface GenerateBurnPlanRequest {
  amount: string;
  timeline: number;
  stupidity: string;
}

export interface RoastRequest {
  total_amount: string;
  timeline_days: number;
  efficiency_level: string;
  services_deployed: Array<{
    service_name: string;
    instance_type: string;
    total_cost: number;
  }>;
}

export const useBurnPlan = () => {
  const api = useApi();
  const isGenerating = ref(false);
  const isRoasting = ref(false);
  const error = ref<string | null>(null);

  const generateBurnPlan = async (request: GenerateBurnPlanRequest): Promise<BurnPlanResponse | null> => {
    isGenerating.value = true;
    error.value = null;

    try {
      const response = await api.post<ApiResponse<BurnPlanResponse>>('/generate-burn-plan', request);
      
      if (response.error) {
        throw new Error(response.error);
      }

      return response.data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to generate burn plan';
      throw err;
    } finally {
      isGenerating.value = false;
    }
  };

  const generateRoast = async (burnPlan: RoastRequest): Promise<string> => {
    isRoasting.value = true;
    error.value = null;

    try {
      const response = await api.post<ApiResponse<{ roast: string }>>('/roast', burnPlan);
      
      if (response.error) {
        throw new Error(response.error);
      }

      return response.data?.roast || '';
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to generate roast';
      throw err;
    } finally {
      isRoasting.value = false;
    }
  };

  return {
    generateBurnPlan,
    generateRoast,
    isGenerating,
    isRoasting,
    error,
  };
};
