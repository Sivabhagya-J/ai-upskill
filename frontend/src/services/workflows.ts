import { apiClient as api } from './api'

export interface Workflow {
  id: number
  name: string
  description: string
  type: string
  stages: Record<string, any>
  rules: Record<string, any>
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface WorkflowInstance {
  id: number
  workflow_id: number
  project_id: number
  current_stage: string
  stage_data: Record<string, any>
  history: Array<{
    from_stage: string
    to_stage: string
    timestamp: string
    triggered_by: number
    data: Record<string, any>
  }>
  is_completed: boolean
  created_at: string
  updated_at: string
  workflow?: Workflow
  project?: {
    id: number
    name: string
  }
}

export interface BusinessRule {
  id: number
  name: string
  description: string
  rule_type: string
  conditions: Record<string, any>
  actions: Record<string, any>
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface WorkflowCreate {
  name: string
  description?: string
  type: string
  stages: Record<string, any>
  rules?: Record<string, any>
  is_active?: boolean
}

export interface WorkflowInstanceCreate {
  workflow_id: number
  project_id: number
  current_stage: string
  stage_data?: Record<string, any>
  history?: Array<any>
  is_completed?: boolean
}

export interface WorkflowStageTransition {
  from_stage: string
  to_stage: string
  transition_data?: Record<string, any>
  notes?: string
  triggered_by?: number
}

export interface WorkflowStatistics {
  total_workflows: number
  active_workflows: number
  completed_workflows: number
  workflows_by_type: Record<string, number>
  workflows_by_stage: Record<string, number>
  recent_workflows: Workflow[]
}

export const workflowService = {
  /**
   * Get all workflows
   */
  async getWorkflows(workflowType?: string): Promise<{ items: Workflow[] } | Workflow[]> {
    try {
      const params = new URLSearchParams()
      if (workflowType) {
        params.append('workflow_type', workflowType)
      }
      
      const response = await api.get<{ items: Workflow[] } | Workflow[]>(`/workflows/?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching workflows:', error)
      throw error
    }
  },

  /**
   * Get workflow by ID
   */
  async getWorkflow(id: number): Promise<Workflow> {
    try {
      const response = await api.get<Workflow>(`/workflows/${id}`)
      return response
    } catch (error) {
      console.error('Error fetching workflow:', error)
      throw error
    }
  },

  /**
   * Create new workflow
   */
  async createWorkflow(workflowData: WorkflowCreate): Promise<Workflow> {
    try {
      const response = await api.post<Workflow>('/workflows/', workflowData)
      return response
    } catch (error) {
      console.error('Error creating workflow:', error)
      throw error
    }
  },

  /**
   * Update workflow
   */
  async updateWorkflow(id: number, workflowData: Partial<WorkflowCreate>): Promise<Workflow> {
    try {
      const response = await api.put<Workflow>(`/workflows/${id}`, workflowData)
      return response
    } catch (error) {
      console.error('Error updating workflow:', error)
      throw error
    }
  },

  /**
   * Delete workflow
   */
  async deleteWorkflow(id: number): Promise<void> {
    try {
      await api.delete(`/workflows/${id}`)
    } catch (error) {
      console.error('Error deleting workflow:', error)
      throw error
    }
  },

  /**
   * Get workflow statistics
   */
  async getWorkflowStatistics(): Promise<WorkflowStatistics> {
    try {
      const response = await api.get<WorkflowStatistics>('/workflows/statistics/overview')
      return response
    } catch (error) {
      console.error('Error fetching workflow statistics:', error)
      throw error
    }
  },

  /**
   * Get workflow instances
   */
  async getWorkflowInstances(
    projectId?: number,
    workflowId?: number,
    stage?: string
  ): Promise<{ items: WorkflowInstance[] } | WorkflowInstance[]> {
    try {
      const params = new URLSearchParams()
      if (projectId) {
        params.append('project_id', projectId.toString())
      }
      if (workflowId) {
        params.append('workflow_id', workflowId.toString())
      }
      if (stage) {
        params.append('stage', stage)
      }
      
      const response = await api.get<{ items: WorkflowInstance[] } | WorkflowInstance[]>(`/workflows/instances/?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching workflow instances:', error)
      throw error
    }
  },

  /**
   * Get workflow instance by ID
   */
  async getWorkflowInstance(id: number): Promise<WorkflowInstance> {
    try {
      const response = await api.get<WorkflowInstance>(`/workflows/instances/${id}`)
      return response
    } catch (error) {
      console.error('Error fetching workflow instance:', error)
      throw error
    }
  },

  /**
   * Create new workflow instance
   */
  async createWorkflowInstance(instanceData: WorkflowInstanceCreate): Promise<WorkflowInstance> {
    try {
      const response = await api.post<WorkflowInstance>('/workflows/instances/', instanceData)
      return response
    } catch (error) {
      console.error('Error creating workflow instance:', error)
      throw error
    }
  },

  /**
   * Update workflow instance
   */
  async updateWorkflowInstance(id: number, instanceData: Partial<WorkflowInstanceCreate>): Promise<WorkflowInstance> {
    try {
      const response = await api.put<WorkflowInstance>(`/workflows/instances/${id}`, instanceData)
      return response
    } catch (error) {
      console.error('Error updating workflow instance:', error)
      throw error
    }
  },

  /**
   * Transition workflow stage
   */
  async transitionWorkflowStage(instanceId: number, transitionData: WorkflowStageTransition): Promise<WorkflowInstance> {
    try {
      const response = await api.post<WorkflowInstance>(`/workflows/instances/${instanceId}/transition`, transitionData)
      return response
    } catch (error) {
      console.error('Error transitioning workflow stage:', error)
      throw error
    }
  },

  /**
   * Get business rules
   */
  async getBusinessRules(ruleType?: string): Promise<{ items: BusinessRule[] } | BusinessRule[]> {
    try {
      const params = new URLSearchParams()
      if (ruleType) {
        params.append('rule_type', ruleType)
      }
      
      const response = await api.get<{ items: BusinessRule[] } | BusinessRule[]>(`/workflows/rules/?${params.toString()}`)
      return response
    } catch (error) {
      console.error('Error fetching business rules:', error)
      throw error
    }
  },

  /**
   * Get business rule by ID
   */
  async getBusinessRule(id: number): Promise<BusinessRule> {
    try {
      const response = await api.get<BusinessRule>(`/workflows/rules/${id}`)
      return response
    } catch (error) {
      console.error('Error fetching business rule:', error)
      throw error
    }
  },

  /**
   * Create new business rule
   */
  async createBusinessRule(ruleData: {
    name: string
    description?: string
    rule_type: string
    conditions: Record<string, any>
    actions: Record<string, any>
    is_active?: boolean
  }): Promise<BusinessRule> {
    try {
      const response = await api.post<BusinessRule>('/workflows/rules/', ruleData)
      return response
    } catch (error) {
      console.error('Error creating business rule:', error)
      throw error
    }
  },

  /**
   * Update business rule
   */
  async updateBusinessRule(id: number, ruleData: Partial<BusinessRule>): Promise<BusinessRule> {
    try {
      const response = await api.put<BusinessRule>(`/workflows/rules/${id}`, ruleData)
      return response
    } catch (error) {
      console.error('Error updating business rule:', error)
      throw error
    }
  },

  /**
   * Delete business rule
   */
  async deleteBusinessRule(id: number): Promise<void> {
    try {
      await api.delete(`/workflows/rules/${id}`)
    } catch (error) {
      console.error('Error deleting business rule:', error)
      throw error
    }
  },

  /**
   * Evaluate business rules
   */
  async evaluateBusinessRules(context: Record<string, any>): Promise<{
    triggered_rules: Array<{
      rule_id: number
      rule_name: string
      rule_type: string
      actions: Record<string, any>
    }>
    total_triggered: number
  }> {
    try {
      const response = await api.post<any>('/workflows/rules/evaluate', context)
      return response
    } catch (error) {
      console.error('Error evaluating business rules:', error)
      throw error
    }
  }
} 