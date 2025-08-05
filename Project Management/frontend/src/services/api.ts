import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/authStore'
import toast from 'react-hot-toast'

// Extend ImportMeta interface for Vite env variables
declare global {
  interface ImportMeta {
    readonly env: {
      readonly VITE_API_URL?: string
    }
  }
}

// API client configuration
class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors(): void {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = useAuthStore.getState().token
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error: any) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor - handle errors and token refresh
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      async (error: any) => {
        const originalRequest = error.config

        // Handle 401 errors (unauthorized)
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          // Try to refresh token
          try {
            const refreshResult = await this.refreshToken()
            if (refreshResult) {
              // Retry original request with new token
              const token = useAuthStore.getState().token
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${token}`
              }
              return this.client(originalRequest)
            }
          } catch (refreshError) {
            // Refresh failed, logout user
            useAuthStore.getState().logout()
            toast.error('Session expired. Please login again.')
            window.location.href = '/login'
            return Promise.reject(refreshError)
          }
        }

        // Don't show toast for errors here - let the calling code handle them
        // This prevents duplicate error messages
        return Promise.reject(error)
      }
    )
  }

  private async refreshToken(): Promise<boolean> {
    try {
      const response = await this.client.post('/auth/refresh')
      const { access_token, user } = response.data
      useAuthStore.getState().login({ access_token, token_type: 'bearer', expires_in: 1800, user })
      return true
    } catch (error) {
      return false
    }
  }

  // Generic HTTP methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

// Export singleton instance
export const apiClient = new ApiClient() 