import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  FolderOpen, 
  CheckSquare, 
  Plus, 
  TrendingUp,
  AlertCircle
} from 'lucide-react'
import { projectService } from '@/services/projects'
import { taskService } from '@/services/tasks'

import { Project, Task } from '@/types'
import ProjectForm from '@/components/forms/ProjectForm'
import { useAuthStore } from '@/stores/authStore'
import { showErrorToast, showSuccessToast } from '@/utils/errorHandler'

const Dashboard = () => {
  const { isAuthenticated, token, user } = useAuthStore()
  const [stats, setStats] = useState({
    totalProjects: 0,
    activeProjects: 0,
    completedProjects: 0,
    totalTasks: 0,
    activeTasks: 0,
    completedTasks: 0,
    overdueTasks: 0,
    
  })
  const [recentProjects, setRecentProjects] = useState<Project[]>([])
  const [recentTasks, setRecentTasks] = useState<Task[]>([])

  const [isLoading, setIsLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)

  useEffect(() => {
    const fetchDashboardData = async () => {
      // Add a small delay to avoid conflicts with auth toasts
      await new Promise(resolve => setTimeout(resolve, 100))
      
      try {
        setIsLoading(true)
        
        // Fetch projects with pagination to get total count
        const projectsResponse = await projectService.getProjects(1, 100)
        const allProjects = projectsResponse.items
        setRecentProjects(allProjects.slice(0, 5)) // Show only 5 most recent
        
        // Fetch tasks with pagination to get total count
        const tasksResponse = await taskService.getTasks(1, 100)
        const allTasks = tasksResponse.items
        setRecentTasks(allTasks.slice(0, 5)) // Show only 5 most recent
        
        // Calculate project statistics
        const activeProjects = allProjects.filter(project => 
          project.status === 'in_progress' || project.status === 'planning'
        ).length
        const completedProjects = allProjects.filter(project => 
          project.status === 'completed'
        ).length
        
        // Calculate task statistics
        const activeTasks = allTasks.filter(task => 
          task.status === 'in_progress' || task.status === 'todo' || task.status === 'review'
        ).length
        const completedTasks = allTasks.filter(task => 
          task.status === 'completed'
        ).length
        const overdueTasks = allTasks.filter(task => {
          if (!task.due_date || task.status === 'completed') return false
          const dueDate = new Date(task.due_date)
          const today = new Date()
          return dueDate < today
        })
        
        
        
        
        
        // Update stats
        setStats({
          totalProjects: projectsResponse.total,
          activeProjects,
          completedProjects,
          totalTasks: tasksResponse.total,
          activeTasks,
          completedTasks,
          overdueTasks: overdueTasks.length
        })
      } catch (error: any) {
        console.error('Error fetching dashboard data:', error)
        showErrorToast(error, 'Failed to load dashboard data')
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboardData()
  }, [])



  const calculateProjectProgress = (project: Project) => {
    if (!project.task_count || project.task_count === 0) {
      return 0
    }
    
    const completedTasks = project.completed_task_count || 0
    const totalTasks = project.task_count
    return Math.round((completedTasks / totalTasks) * 100)
  }

  const getProjectStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-blue-100 text-blue-800'
      case 'planning':
        return 'bg-yellow-100 text-yellow-800'
      case 'on_hold':
        return 'bg-orange-100 text-orange-800'
      case 'cancelled':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTaskStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
        return 'bg-blue-100 text-blue-800'
      case 'review':
        return 'bg-purple-100 text-purple-800'
      case 'todo':
        return 'bg-gray-100 text-gray-800'
      case 'blocked':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const handleCreateProject = async (projectData: any) => {
    try {
      const newProject = await projectService.createProject(projectData)
      setShowCreateModal(false)
      
      // Refresh dashboard data
      const projectsResponse = await projectService.getProjects(1, 100)
      setRecentProjects(projectsResponse.items.slice(0, 5))
      setStats(prev => ({
        ...prev,
        totalProjects: projectsResponse.total,
        activeProjects: projectsResponse.items.filter(p => 
          p.status === 'in_progress' || p.status === 'planning'
        ).length
      }))
      
      // Show success message
      showSuccessToast('Project created successfully!')
    } catch (error: any) {
      console.error('Error creating project:', error)
      showErrorToast(error, 'Failed to create project')
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Welcome back, {user?.full_name || 'User'}!</p>
        </div>
        <button 
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>New Project</span>
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-primary-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <FolderOpen className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Total Projects</h3>
              <p className="text-3xl font-bold text-primary-600">{stats.totalProjects}</p>
              <p className="text-sm text-gray-500">
                {stats.activeProjects} active, {stats.completedProjects} completed
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckSquare className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Total Tasks</h3>
              <p className="text-3xl font-bold text-blue-600">{stats.totalTasks}</p>
              <p className="text-sm text-gray-500">
                {stats.activeTasks} active, {stats.completedTasks} completed
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Completion Rate</h3>
              <p className="text-3xl font-bold text-green-600">
                {stats.totalTasks > 0 ? Math.round((stats.completedTasks / stats.totalTasks) * 100) : 0}%
              </p>
              <p className="text-sm text-gray-500">
                {stats.completedTasks} of {stats.totalTasks} tasks
              </p>
            </div>
          </div>
        </div>


      </div>



      {/* Alerts */}
      {stats.overdueTasks > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-400 mr-3" />
            <div>
              <h3 className="text-sm font-medium text-red-800">
                {stats.overdueTasks} overdue task{stats.overdueTasks > 1 ? 's' : ''}
              </h3>
              <p className="text-sm text-red-700 mt-1">
                You have {stats.overdueTasks} task{stats.overdueTasks > 1 ? 's' : ''} that {stats.overdueTasks > 1 ? 'are' : 'is'} past due date.
              </p>
            </div>
            <div className="ml-auto">
              <Link
                to="/tasks"
                className="text-sm font-medium text-red-800 hover:text-red-900"
              >
                View tasks →
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Projects */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Recent Projects</h2>
            <Link
              to="/projects"
              className="text-sm text-primary-600 hover:text-primary-500"
            >
              View all
            </Link>
          </div>
          {recentProjects.length > 0 ? (
            <div className="space-y-4">
              {recentProjects.map((project) => (
                <div
                  key={project.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  <div className="flex items-center space-x-3">
                    <FolderOpen className="h-5 w-5 text-primary-600" />
                    <div>
                      <h3 className="font-medium text-gray-900">{project.name}</h3>
                      <p className="text-sm text-gray-500">
                        {project.task_count || 0} tasks • {calculateProjectProgress(project)}% complete
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getProjectStatusColor(project.status)}`}>
                      {project.status.replace('_', ' ')}
                    </span>
                    <Link
                      to={`/projects/${project.id}`}
                      className="text-primary-600 hover:text-primary-500"
                    >
                      →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">No projects yet</p>
          )}
        </div>

        {/* Recent Tasks */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Recent Tasks</h2>
            <Link
              to="/tasks"
              className="text-sm text-primary-600 hover:text-primary-500"
            >
              View all
            </Link>
          </div>
          {recentTasks.length > 0 ? (
            <div className="space-y-4">
              {recentTasks.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  <div className="flex items-center space-x-3">
                    <CheckSquare className="h-5 w-5 text-blue-600" />
                    <div>
                      <h3 className="font-medium text-gray-900">{task.title}</h3>
                      <p className="text-sm text-gray-500">
                        {task.project_name} • {task.due_date ? formatDate(task.due_date) : 'No due date'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTaskStatusColor(task.status)}`}>
                      {task.status.replace('_', ' ')}
                    </span>
                    <Link
                      to={`/tasks/${task.id}`}
                      className="text-blue-600 hover:text-blue-500"
                    >
                      →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600 text-center py-8">No tasks yet</p>
          )}
        </div>

        
      </div>

      {/* Create Project Modal */}
      {showCreateModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2 className="modal-title">Create New Project</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <ProjectForm
                onSubmit={handleCreateProject}
                onCancel={() => setShowCreateModal(false)}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard 