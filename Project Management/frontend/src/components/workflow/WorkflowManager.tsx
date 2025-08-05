import React, { useState, useEffect } from 'react'
import { 
  Workflow, 
  Settings, 
  Play, 
  Pause, 
  Edit, 
  Trash2, 
  Plus,
  ArrowRight,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react'
import { workflowService } from '@/services/workflows'

interface WorkflowData {
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

interface WorkflowInstance {
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
  workflow?: WorkflowData
  project?: {
    id: number
    name: string
  }
}

const WorkflowManager: React.FC = () => {
  const [workflows, setWorkflows] = useState<WorkflowData[]>([])
  const [instances, setInstances] = useState<WorkflowInstance[]>([])
  const [selectedWorkflow, setSelectedWorkflow] = useState<WorkflowData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showInstanceModal, setShowInstanceModal] = useState(false)

  useEffect(() => {
    fetchWorkflows()
  }, [])

  const fetchWorkflows = async () => {
    try {
      setLoading(true)
      setError(null)

      const [workflowsData, instancesData] = await Promise.all([
        workflowService.getWorkflows(),
        workflowService.getWorkflowInstances()
      ])

      setWorkflows(workflowsData.items || workflowsData)
      setInstances(instancesData.items || instancesData)

    } catch (err: any) {
      console.error('Error fetching workflows:', err)
      setError(err.message || 'Failed to load workflows')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateWorkflow = async (workflowData: any) => {
    try {
      await workflowService.createWorkflow(workflowData)
      setShowCreateModal(false)
      fetchWorkflows()
    } catch (err: any) {
      console.error('Error creating workflow:', err)
      setError(err.message || 'Failed to create workflow')
    }
  }

  const handleCreateInstance = async (instanceData: any) => {
    try {
      await workflowService.createWorkflowInstance(instanceData)
      setShowInstanceModal(false)
      fetchWorkflows()
    } catch (err: any) {
      console.error('Error creating workflow instance:', err)
      setError(err.message || 'Failed to create workflow instance')
    }
  }

  const handleTransitionStage = async (instanceId: number, newStage: string) => {
    try {
      await workflowService.transitionWorkflowStage(instanceId, {
        from_stage: instances.find(i => i.id === instanceId)?.current_stage || '',
        to_stage: newStage,
        transition_data: {},
        notes: `Transitioned to ${newStage}`
      })
      fetchWorkflows()
    } catch (err: any) {
      console.error('Error transitioning stage:', err)
      setError(err.message || 'Failed to transition stage')
    }
  }

  const getWorkflowTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'sales':
        return 'bg-blue-100 text-blue-800'
      case 'support':
        return 'bg-green-100 text-green-800'
      case 'development':
        return 'bg-purple-100 text-purple-800'
      case 'marketing':
        return 'bg-yellow-100 text-yellow-800'
      case 'operations':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStageColor = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-blue-100 text-blue-800'
      case 'todo':
        return 'bg-gray-100 text-gray-800'
      case 'review':
        return 'bg-yellow-100 text-yellow-800'
      case 'blocked':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Workflows</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchWorkflows}
            className="btn btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Workflow Management</h1>
          <p className="text-gray-600 mt-2">Manage business processes and automation</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowInstanceModal(true)}
            className="btn btn-secondary"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Instance
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Workflow
          </button>
        </div>
      </div>

      {/* Workflows Section */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Workflow Templates</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {workflows.map((workflow) => (
            <div
              key={workflow.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900">{workflow.name}</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setSelectedWorkflow(workflow)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <Settings className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setShowInstanceModal(true)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    <Play className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-3">{workflow.description}</p>
              
              <div className="flex items-center justify-between">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getWorkflowTypeColor(workflow.type)}`}>
                  {workflow.type}
                </span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  workflow.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {workflow.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Workflow Instances Section */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Active Workflow Instances</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Workflow
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Project
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Stage
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Progress
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {instances.map((instance) => (
                <tr key={instance.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {instance.workflow?.name || 'Unknown Workflow'}
                    </div>
                    <div className="text-sm text-gray-500">
                      ID: {instance.workflow_id}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {instance.project?.name || 'Unknown Project'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStageColor(instance.current_stage)}`}>
                      {instance.current_stage}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ 
                            width: `${(instance.history?.length || 0) / (Object.keys(instance.workflow?.stages || {}).length) * 100}%` 
                          }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-500">
                        {instance.history?.length || 0} / {Object.keys(instance.workflow?.stages || {}).length}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {instance.is_completed ? (
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      ) : (
                        <Clock className="h-4 w-4 text-yellow-500 mr-2" />
                      )}
                      <span className="text-sm text-gray-900">
                        {instance.is_completed ? 'Completed' : 'In Progress'}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => {
                          // Show stage transition modal
                          const nextStages = Object.keys(instance.workflow?.stages || {})
                            .filter(stage => stage !== instance.current_stage)
                          
                          if (nextStages.length > 0) {
                            const nextStage = nextStages[0]
                            handleTransitionStage(instance.id, nextStage)
                          }
                        }}
                        className="text-blue-600 hover:text-blue-900"
                        disabled={instance.is_completed}
                      >
                        <ArrowRight className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => {
                          // Show instance details modal
                        }}
                        className="text-gray-600 hover:text-gray-900"
                      >
                        <Settings className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Statistics Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <Workflow className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Total Workflows</h3>
              <p className="text-3xl font-bold text-blue-600">{workflows.length}</p>
              <p className="text-sm text-gray-500">
                {workflows.filter(w => w.is_active).length} active
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <Play className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Active Instances</h3>
              <p className="text-3xl font-bold text-green-600">
                {instances.filter(i => !i.is_completed).length}
              </p>
              <p className="text-sm text-gray-500">
                {instances.filter(i => i.is_completed).length} completed
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Completion Rate</h3>
              <p className="text-3xl font-bold text-purple-600">
                {instances.length > 0 
                  ? Math.round((instances.filter(i => i.is_completed).length / instances.length) * 100)
                  : 0}%
              </p>
              <p className="text-sm text-gray-500">
                Average completion rate
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Modals would go here */}
      {showCreateModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2 className="modal-title">Create New Workflow</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              {/* Workflow creation form would go here */}
              <p className="text-gray-600">Workflow creation form coming soon...</p>
            </div>
          </div>
        </div>
      )}

      {showInstanceModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2 className="modal-title">Create Workflow Instance</h2>
              <button
                onClick={() => setShowInstanceModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              {/* Instance creation form would go here */}
              <p className="text-gray-600">Instance creation form coming soon...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default WorkflowManager 