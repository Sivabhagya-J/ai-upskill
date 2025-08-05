import { apiClient as api } from './api'

export interface DashboardOverview {
  projects: {
    total: number
    active: number
    completed: number
    completion_rate: number
  }
  tasks: {
    total: number
    active: number
    completed: number
    overdue: number
    completion_rate: number
  }
  performance_metrics: {
    efficiency_rate: number
    completion_rate: number
    overdue_rate: number
  }
  recent_activity: Array<{
    type: string
    id: number
    title: string
    status: string
    timestamp: string
  }>
  upcoming_deadlines: Array<{
    task_id: number
    task_title: string
    project_name: string
    due_date: string
    days_until_due: number
  }>
}

export interface ChartData {
  labels: string[]
  data: number[]
}

export interface ProjectAnalytics {
  project_info: {
    id: number
    name: string
    status: string
    progress_percentage: number
  }
  task_statistics: {
    total: number
    completed: number
    active: number
    status_distribution: Record<string, number>
    priority_distribution: Record<string, number>
  }
  assignee_performance: Record<string, any>
  timeline: Array<{
    date: string
    event: string
    description: string
  }>
}

export interface UserPerformance {
  overview: {
    total_tasks: number
    completed_tasks: number
    overdue_tasks: number
    completion_rate: number
    avg_completion_time: number
  }
  productivity_trends: Array<{
    date: string
    tasks_completed: number
  }>
  task_distribution: Record<string, number>
  recent_activity: Array<{
    type: string
    id: number
    title: string
    status: string
    timestamp: string
  }>
}

export interface TeamAnalytics {
  team_overview: {
    total_members: number
    total_tasks: number
    total_completed: number
    avg_completion_rate: number
  }
  member_performance: Array<{
    user_id: number
    user_name: string
    total_tasks: number
    completed_tasks: number
    completion_rate: number
  }>
}

export interface KPIMetrics {
  project_completion_rate: number
  task_completion_rate: number
  overdue_tasks: number
  total_active_projects: number
  efficiency_rate: number
}

export const analyticsService = {
  /**
   * Get dashboard overview data
   */
  async getDashboardOverview(): Promise<DashboardOverview> {
    try {
      const response = await api.get<DashboardOverview>('/analytics/dashboard/overview')
      return response
    } catch (error) {
      console.error('Error fetching dashboard overview:', error)
      throw error
    }
  },

  /**
   * Get project analytics
   */
  async getProjectAnalytics(projectId: number): Promise<ProjectAnalytics> {
    try {
      const response = await api.get<ProjectAnalytics>(`/analytics/projects/${projectId}/analytics`)
      return response
    } catch (error) {
      console.error('Error fetching project analytics:', error)
      throw error
    }
  },

  /**
   * Get user performance analytics
   */
  async getUserPerformance(userId?: number, dateRange?: string): Promise<UserPerformance> {
    try {
      const params = new URLSearchParams()
      if (dateRange) {
        params.append('date_range', dateRange)
      }
      
      const endpoint = userId 
        ? `/analytics/users/${userId}/performance`
        : '/analytics/users/me/performance'
      
      const response = await api.get<UserPerformance>(`${endpoint}?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching user performance:', error)
      throw error
    }
  },

  /**
   * Get team analytics
   */
  async getTeamAnalytics(teamMembers: number[]): Promise<TeamAnalytics> {
    try {
      const response = await api.post<TeamAnalytics>('/analytics/teams/analytics', teamMembers)
      return response
    } catch (error) {
      console.error('Error fetching team analytics:', error)
      throw error
    }
  },

  /**
   * Generate report
   */
  async generateReport(reportType: string, filters?: Record<string, any>): Promise<any> {
    try {
      const params = new URLSearchParams()
      if (filters) {
        params.append('filters', JSON.stringify(filters))
      }
      
      const response = await api.get(`/analytics/reports/${reportType}?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error generating report:', error)
      throw error
    }
  },

  /**
   * Get task status distribution for charts
   */
  async getTaskStatusDistribution(projectId?: number): Promise<ChartData> {
    try {
      const params = new URLSearchParams()
      if (projectId) {
        params.append('project_id', projectId.toString())
      }
      
      const response = await api.get<ChartData>(`/analytics/charts/task-status-distribution?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching task status distribution:', error)
      throw error
    }
  },

  /**
   * Get task priority distribution for charts
   */
  async getTaskPriorityDistribution(projectId?: number): Promise<ChartData> {
    try {
      const params = new URLSearchParams()
      if (projectId) {
        params.append('project_id', projectId.toString())
      }
      
      const response = await api.get<ChartData>(`/analytics/charts/task-priority-distribution?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching task priority distribution:', error)
      throw error
    }
  },

  /**
   * Get productivity trends for charts
   */
  async getProductivityTrends(userId?: number, dateRange: string = '30d'): Promise<any[]> {
    try {
      const params = new URLSearchParams()
      if (userId) {
        params.append('user_id', userId.toString())
      }
      params.append('date_range', dateRange)
      
      const response = await api.get<{labels: string[], data: number[]}>(`/analytics/charts/productivity-trends?${params.toString()}`)
      
      // Convert to chart format
      return response.labels.map((label, index) => ({
        date: label,
        tasks_completed: response.data[index]
      }))
    } catch (error) {
      console.error('Error fetching productivity trends:', error)
      throw error
    }
  },

  /**
   * Get project progress for charts
   */
  async getProjectProgress(projectId: number): Promise<any> {
    try {
      const response = await api.get(`/analytics/charts/project-progress?project_id=${projectId}`)
      return response
    } catch (error) {
      console.error('Error fetching project progress:', error)
      throw error
    }
  },

  /**
   * Get KPI metrics
   */
  async getKPIMetrics(): Promise<KPIMetrics> {
    try {
      const response = await api.get<KPIMetrics>('/analytics/metrics/kpi')
      return response
    } catch (error) {
      console.error('Error fetching KPI metrics:', error)
      throw error
    }
  },

  /**
   * Export report
   */
  async exportReport(reportType: string, format: string = 'json', filters?: Record<string, any>): Promise<any> {
    try {
      const params = new URLSearchParams()
      params.append('format', format)
      if (filters) {
        params.append('filters', JSON.stringify(filters))
      }
      
      const response = await api.get(`/analytics/export/${reportType}?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error exporting report:', error)
      throw error
    }
  }
} 