import { ref } from 'vue';

export interface Toast {
  id: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timeout: number;
}

const toasts = ref<Toast[]>([]);
let toastIdCounter = 0;

export const useToasts = () => {
  const showToast = (
    message: string,
    type: Toast['type'] = 'info',
    timeout: number = 5000
  ) => {
    const id = `toast-${++toastIdCounter}`;
    const toast: Toast = { id, message, type, timeout };

    toasts.value.push(toast);

    if (timeout > 0) {
      setTimeout(() => {
        clearToast(id);
      }, timeout);
    }

    return id;
  };

  const success = (message: string, timeout?: number) => {
    return showToast(message, 'success', timeout);
  };

  const error = (message: string, timeout?: number) => {
    return showToast(message, 'error', timeout);
  };

  const warning = (message: string, timeout?: number) => {
    return showToast(message, 'warning', timeout);
  };

  const info = (message: string, timeout?: number) => {
    return showToast(message, 'info', timeout);
  };

  const clearToast = (id: string) => {
    const index = toasts.value.findIndex((t) => t.id === id);
    if (index !== -1) {
      toasts.value.splice(index, 1);
    }
  };

  const clearAll = () => {
    toasts.value = [];
  };

  return {
    toasts,
    showToast,
    success,
    error,
    warning,
    info,
    clearToast,
    clearAll,
  };
};
