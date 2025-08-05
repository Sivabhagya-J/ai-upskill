import { apiClient } from './api'
import { Project, ProjectCreate, ProjectUpdate, PaginatedResponse } from '@/types'

class ProjectService {
  async getProjects(page = 1, size = 20): Promise<PaginatedResponse<Project>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Project>>(
        `/projects/?skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getProject(id: number): Promise<Project> {
    try {
      const response = await apiClient.get<Project>(`/projects/${id}`)
      return response
    } catch (error) {
      throw error
    }
  }

  async createProject(projectData: ProjectCreate): Promise<Project> {
    try {
      const response = await apiClient.post<Project>('/projects/', projectData)
      return response
    } catch (error) {
      throw error
    }
  }

  async updateProject(id: number, projectData: ProjectUpdate): Promise<Project> {
    try {
      const response = await apiClient.put<Project>(`/projects/${id}`, projectData)
      return response
    } catch (error) {
      throw error
    }
  }

  async deleteProject(id: number): Promise<void> {
    try {
      await apiClient.delete(`/projects/${id}`)
    } catch (error) {
      throw error
    }
  }

  async searchProjects(searchTerm: string, page = 1, size = 20): Promise<PaginatedResponse<Project>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Project>>(
        `/projects/?search=${encodeURIComponent(searchTerm)}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }

  async getProjectsByStatus(status: string, page = 1, size = 20): Promise<PaginatedResponse<Project>> {
    try {
      const skip = (page - 1) * size
      const response = await apiClient.get<PaginatedResponse<Project>>(
        `/projects/?status=${status}&skip=${skip}&limit=${size}`
      )
      return response
    } catch (error) {
      throw error
    }
  }
}

export const projectService = new ProjectService() 