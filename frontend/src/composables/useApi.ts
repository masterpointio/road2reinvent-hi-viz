import { apiClient } from '../lib/apiClient';

export const useApi = () => {
  const get = <T = any>(path: string, options?: RequestInit) => {
    return apiClient.get<T>(path, options);
  };

  const post = <T = any>(path: string, body?: any, options?: RequestInit) => {
    return apiClient.post<T>(path, body, options);
  };

  const put = <T = any>(path: string, body?: any, options?: RequestInit) => {
    return apiClient.put<T>(path, body, options);
  };

  const patch = <T = any>(path: string, body?: any, options?: RequestInit) => {
    return apiClient.patch<T>(path, body, options);
  };

  const del = <T = any>(path: string, options?: RequestInit) => {
    return apiClient.del<T>(path, options);
  };

  return {
    get,
    post,
    put,
    patch,
    del,
  };
};
