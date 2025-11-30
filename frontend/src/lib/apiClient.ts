import { useAuth } from '../composables/useAuth';
import { config } from '../config';

export interface ApiResponse<T = any> {
  data: T | null;
  error: string | null;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = config.apiBaseUrl;
    console.log('ApiClient initialized with baseUrl:', this.baseUrl);
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const { accessToken } = useAuth();
    if (accessToken.value) {
      headers['Authorization'] = `Bearer ${accessToken.value}`;
    }

    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      let errorDetails;

      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorData.error || errorMessage;
        errorDetails = errorData;
      } catch {
        // Response body is not JSON
      }

      const error: ApiError = {
        message: errorMessage,
        status: response.status,
        details: errorDetails,
      };

      throw error;
    }

    if (response.status === 204) {
      return null as T;
    }

    try {
      return await response.json();
    } catch {
      return null as T;
    }
  }

  async request<T = any>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers = this.getHeaders();

    console.log('API Request:', {
      url,
      method: options.method || 'GET',
      headers,
      body: options.body,
    });

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...headers,
          ...options.headers,
        },
      });

      console.log('API Response:', {
        status: response.status,
        statusText: response.statusText,
      });

      return await this.handleResponse<T>(response);
    } catch (error) {
      console.error('API Request failed:', error);
      if (error instanceof Error && 'status' in error) {
        throw error;
      }
      throw {
        message: error instanceof Error ? error.message : 'Network error',
        status: 0,
      } as ApiError;
    }
  }

  async get<T = any>(path: string, options?: RequestInit): Promise<T> {
    return this.request<T>(path, { ...options, method: 'GET' });
  }

  async post<T = any>(path: string, body?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T = any>(path: string, body?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async patch<T = any>(path: string, body?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(path, {
      ...options,
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async del<T = any>(path: string, options?: RequestInit): Promise<T> {
    return this.request<T>(path, { ...options, method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
