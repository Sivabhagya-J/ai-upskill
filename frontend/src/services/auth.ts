import { apiClient } from './api'
import { useAuthStore } from '@/stores/authStore'
import { UserLogin, UserCreate, UserToken, User } from '@/types'
import { showErrorToast, showSuccessToast } from '@/utils/errorHandler'

class AuthService {
  async login(credentials: UserLogin): Promise<UserToken> {
    try {
      const response = await apiClient.post<UserToken>('/auth/login', credentials)
      useAuthStore.getState().login(response)
      return response
    } catch (error: any) {
      showErrorToast(error, 'Login failed. Please check your credentials.')
      throw error
    }
  }

  async signup(userData: UserCreate): Promise<UserToken> {
    try {
      const response = await apiClient.post<UserToken>('/auth/signup', userData)
      useAuthStore.getState().login(response)
      return response
    } catch (error: any) {
      showErrorToast(error, 'Signup failed. Please try again.')
      throw error
    }
  }

  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout')
    } catch (error) {
      // Ignore logout errors
    } finally {
      useAuthStore.getState().logout()
      showSuccessToast('Logged out successfully')
    }
  }

  async refreshToken(): Promise<UserToken> {
    try {
      const response = await apiClient.post<UserToken>('/auth/refresh')
      useAuthStore.getState().login(response)
      return response
    } catch (error) {
      useAuthStore.getState().logout()
      throw error
    }
  }

  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/auth/me')
      useAuthStore.getState().setUser(response)
      return response
    } catch (error) {
      throw error
    }
  }

  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put<User>('/users/me', userData)
      useAuthStore.getState().setUser(response)
      showSuccessToast('Profile updated successfully!')
      return response
    } catch (error: any) {
      showErrorToast(error, 'Failed to update profile')
      throw error
    }
  }

  isAuthenticated(): boolean {
    return useAuthStore.getState().isAuthenticated
  }

  getToken(): string | null {
    return useAuthStore.getState().token
  }

  getUser(): User | null {
    return useAuthStore.getState().user
  }
}

export const authService = new AuthService() 