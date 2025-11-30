import { ref, watch, onMounted } from 'vue';
import type { Ref } from 'vue';

export interface UseQueryOptions {
  immediate?: boolean;
  dependencies?: Ref<any>[];
}

export const useQuery = <T = any>(
  queryFn: () => Promise<T>,
  options: UseQueryOptions = {}
) => {
  const { immediate = true, dependencies = [] } = options;

  const data = ref<T | null>(null) as Ref<T | null>;
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const execute = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const result = await queryFn();
      data.value = result;
    } catch (err: any) {
      error.value = err.message || 'An error occurred';
      console.error('Query error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const refetch = () => {
    return execute();
  };

  if (dependencies.length > 0) {
    watch(dependencies, () => {
      execute();
    });
  }

  if (immediate) {
    onMounted(() => {
      execute();
    });
  }

  return {
    data,
    isLoading,
    error,
    refetch,
  };
};
