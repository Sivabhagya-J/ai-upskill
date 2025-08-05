import { apiClient } from './api'
import { Task, TaskCreate, TaskUpdate, PaginatedResponse } from '@/types'

class TaskService {
  async getTasks(page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/?skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getMyTasks(page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/my-tasks?skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getProjectTasks(projectId: number, page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/projects/${projectId}/tasks?skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getTask(id: number): Promise<Task> {
    try {
      const response = await apiClient.get<Task>(`/tasks/${id}`)
      return response
    } catch (error) {
      throw error
    }
  }

  async createTask(taskData: TaskCreate): Promise<Task> {
    try {
      const response = await apiClient.post<Task>('/tasks/', taskData)
      return response
    } catch (error) {
      throw error
    }
  }

  async updateTask(id: number, taskData: TaskUpdate): Promise<Task> {
    try {
      const response = await apiClient.put<Task>(`/tasks/${id}`, taskData)
      return response
    } catch (error) {
      throw error
    }
  }

  async deleteTask(id: number): Promise<void> {
    try {
      await apiClient.delete(`/tasks/${id}`)
    } catch (error) {
      throw error
    }
  }

  async getTasksByStatus(status: string, page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/?status=${status}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getTasksByPriority(priority: string, page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/?priority=${priority}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getTasksByProject(projectId: number, page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/?project_id=${projectId}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async searchTasks(searchTerm: string, page = 1, size = 20): Promise<PaginatedResponse<Task>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Task>>(
        `/tasks/?search=${encodeURIComponent(searchTerm)}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }
}

export const taskService = new TaskService() 