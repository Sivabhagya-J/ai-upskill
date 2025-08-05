// User types
export interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface UserCreate {
  email: string
  username: string
  full_name: string
  password: string
}

export interface UserUpdate {
  email?: string
  username?: string
  full_name?: string
  is_active?: boolean
}

export interface UserLogin {
  email: string
  password: string
}

export interface UserSignup {
  email: string
  username: string
  full_name: string
  password: string
  confirm_password: string
}

export interface UserToken {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// Project types
export interface Project {
  id: number
  name: string
  description?: string
  owner_id: number
  owner_name?: string
  status: 'planning' | 'in_progress' | 'on_hold' | 'completed' | 'cancelled'
  start_date?: string
  end_date?: string
  created_at: string
  updated_at: string
  task_count: number
  completed_task_count: number
  progress_percentage: number
  is_active: boolean
}

export interface ProjectCreate {
  name: string
  description?: string
  start_date?: string
  end_date?: string
}

export interface ProjectUpdate {
  name?: string
  description?: string
  status?: string
  start_date?: string
  end_date?: string
}

// Task types
export interface Task {
  id: number
  title: string
  description?: string
  project_id: number
  project_name?: string
  assignee_id?: number
  assignee_name?: string
  status: 'todo' | 'in_progress' | 'review' | 'completed' | 'blocked'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  due_date?: string
  created_at: string
  updated_at: string
  is_overdue: boolean

  is_completed: boolean
  is_active: boolean
}

export interface TaskCreate {
  title: string
  description?: string
  project_id: number
  assignee_id?: number
  status?: string
  priority?: string
  due_date?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  project_id?: number
  assignee_id?: number
  status?: string
  priority?: string
  due_date?: string
}



// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// Form types
export interface LoginForm {
  email: string
  password: string
}

export interface SignupForm {
  email: string
  username: string
  full_name: string
  password: string
  confirm_password: string
}

// Filter types
export interface ProjectFilters {
  status?: string
  search?: string
  page?: number
  size?: number
}

export interface TaskFilters {
  status?: string
  priority?: string
  assignee_id?: number
  project_id?: number
  search?: string
  page?: number
  size?: number
}

 