import { apiClient as api } from './api'
import { User } from '../types'

export const userService = {
  /**
   * Get all users
   */
  async getUsers(): Promise<User[]> {
    try {
      const response = await api.get<any>('/users/')
      return response.items || response
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  /**
   * Get user by ID
   */
  async getUser(id: number): Promise<User> {
    try {
      const response = await api.get<User>(`/users/${id}`)
      return response
    } catch (error) {
      console.error('Error fetching user:', error)
      throw error
    }
  },

  /**
   * Search users
   */
  async searchUsers(searchTerm: string): Promise<User[]> {
    try {
      const response = await api.get<any>(`/users/search?search_term=${searchTerm}`)
      return response.items || response
    } catch (error) {
      console.error('Error searching users:', error)
      throw error
    }
  }
} 