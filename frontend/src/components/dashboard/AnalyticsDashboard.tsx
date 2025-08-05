import React, { useState, useEffect } from 'react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area
} from 'recharts'
import { 
  TrendingUp, 
  Users, 
  Calendar, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Target,
  Activity
} from 'lucide-react'
import { analyticsService } from '@/services/analytics'

interface DashboardData {
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

interface ChartData {
  labels: string[]
  data: number[]
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

const AnalyticsDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [taskStatusData, setTaskStatusData] = useState<ChartData | null>(null)
  const [taskPriorityData, setTaskPriorityData] = useState<ChartData | null>(null)
  const [productivityData, setProductivityData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch dashboard overview
      const overview = await analyticsService.getDashboardOverview()
      setDashboardData(overview)

      // Fetch chart data
      const [statusData, priorityData, productivityData] = await Promise.all([
        analyticsService.getTaskStatusDistribution(),
        analyticsService.getTaskPriorityDistribution(),
        analyticsService.getProductivityTrends()
      ])

      setTaskStatusData(statusData)
      setTaskPriorityData(priorityData)
      setProductivityData(productivityData)

    } catch (err: any) {
      console.error('Error fetching dashboard data:', err)
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const formatChartData = (labels: string[], data: number[]) => {
    return labels.map((label, index) => ({
      name: label,
      value: data[index]
    }))
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'text-green-600'
      case 'in_progress':
        return 'text-blue-600'
      case 'todo':
        return 'text-gray-600'
      case 'overdue':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'text-red-600'
      case 'medium':
        return 'text-yellow-600'
      case 'low':
        return 'text-green-600'
      default:
        return 'text-gray-600'
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
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Dashboard</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="btn btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No dashboard data available</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600 mt-2">Comprehensive project and task analytics</p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="btn btn-secondary"
        >
          Refresh Data
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Target className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Project Completion</h3>
              <p className="text-3xl font-bold text-blue-600">
                {dashboardData.projects.completion_rate}%
              </p>
              <p className="text-sm text-gray-500">
                {dashboardData.projects.completed} of {dashboardData.projects.total} projects
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Task Completion</h3>
              <p className="text-3xl font-bold text-green-600">
                {dashboardData.tasks.completion_rate}%
              </p>
              <p className="text-sm text-gray-500">
                {dashboardData.tasks.completed} of {dashboardData.tasks.total} tasks
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-yellow-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-yellow-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Efficiency Rate</h3>
              <p className="text-3xl font-bold text-yellow-600">
                {dashboardData.performance_metrics.efficiency_rate}%
              </p>
              <p className="text-sm text-gray-500">
                Tasks completed on time
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-red-500">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Overdue Tasks</h3>
              <p className="text-3xl font-bold text-red-600">
                {dashboardData.tasks.overdue}
              </p>
              <p className="text-sm text-gray-500">
                {dashboardData.performance_metrics.overdue_rate}% of total tasks
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Task Status Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Task Status Distribution</h3>
          {taskStatusData && (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={formatChartData(taskStatusData.labels, taskStatusData.data)}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {formatChartData(taskStatusData.labels, taskStatusData.data).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Task Priority Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Task Priority Distribution</h3>
          {taskPriorityData && (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={formatChartData(taskPriorityData.labels, taskPriorityData.data)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Productivity Trends */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Productivity Trends</h3>
        {productivityData.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={productivityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="tasks_completed" 
                stroke="#8884d8" 
                strokeWidth={2}
                name="Tasks Completed"
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Recent Activity and Upcoming Deadlines */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {dashboardData.recent_activity.slice(0, 5).map((activity, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg">
                <div className={`w-2 h-2 rounded-full ${
                  activity.type === 'task' ? 'bg-blue-500' : 'bg-green-500'
                }`} />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                  <p className="text-xs text-gray-500">
                    {activity.type} • {activity.status}
                  </p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(activity.status)}`}>
                  {activity.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Deadlines</h3>
          <div className="space-y-3">
            {dashboardData.upcoming_deadlines.slice(0, 5).map((deadline, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg">
                <Calendar className="h-4 w-4 text-gray-400" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{deadline.task_title}</p>
                  <p className="text-xs text-gray-500">{deadline.project_name}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  deadline.days_until_due <= 1 ? 'bg-red-100 text-red-800' :
                  deadline.days_until_due <= 3 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {deadline.days_until_due === 0 ? 'Due today' :
                   deadline.days_until_due === 1 ? 'Due tomorrow' :
                   `Due in ${deadline.days_until_due} days`}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyticsDashboard 