import { ref } from 'vue';
import { apiClient } from '../lib/apiClient';

export interface RecentBurnPlan {
  id: string;
  timestamp: number;
  burn_plan: {
    total_amount: string;
    timeline_days: number;
    efficiency_level: string;
    deployment_scenario: string;
    total_calculated_cost: number;
  };
}

export function useRecentBurnPlans() {
  const recentPlans = ref<RecentBurnPlan[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchRecentPlans = async (limit: number = 5) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<RecentBurnPlan[]>(`/burn-plan/recent?limit=${limit}`);
      recentPlans.value = response;
    } catch (err: any) {
      console.error('Failed to fetch recent burn plans:', err);
      error.value = err.message || 'Failed to fetch recent burn plans';
      recentPlans.value = [];
    } finally {
      loading.value = false;
    }
  };

  const formatTimeAgo = (timestamp: number): string => {
    const now = Date.now();
    const diff = now - timestamp;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'just now';
  };

  return {
    recentPlans,
    loading,
    error,
    fetchRecentPlans,
    formatTimeAgo,
  };
}
