import React, { useState, useEffect } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { Calendar } from 'lucide-react'
import { Project, Task, User } from '@/types'
import { userService } from '../../services/users'


interface TaskFormProps {
  task?: Task
  projects: Project[]
  onSubmit: (data: any) => void
  onCancel: () => void
}

const TaskForm = ({ task, projects, onSubmit, onCancel }: TaskFormProps) => {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(false)
  
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    setValue,
    watch
  } = useForm({
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      project_id: task?.project_id || '',
      assignee_id: '', // Don't set assignee_id in defaultValues, let useEffect handle it
      status: task?.status || 'todo',
      priority: task?.priority || 'medium',
      due_date: (() => {
        if (!task?.due_date) return ''
        try {
          const date = new Date(task.due_date)
          return date.toISOString().split('T')[0]
        } catch (error) {
          return task.due_date.split('T')[0]
        }
      })()
    }
  })

  // Update form values when task changes (for edit mode)
  useEffect(() => {
    if (task) {
      setValue('title', task.title || '')
      setValue('description', task.description || '')
      setValue('project_id', task.project_id || '')
      setValue('assignee_id', task.assignee_id ? String(task.assignee_id) : '')
      setValue('status', task.status || 'todo')
      setValue('priority', task.priority || 'medium')
      
      // Handle due date formatting
      let formattedDate = ''
      if (task.due_date) {
        try {
          const date = new Date(task.due_date)
          formattedDate = date.toISOString().split('T')[0]
        } catch (error) {
          console.error('Error formatting date:', error)
          formattedDate = task.due_date.split('T')[0]
        }
      }
      setValue('due_date', formattedDate)
    }
  }, [task, setValue, users])

  useEffect(() => {
    // Fetch real users from API
    const fetchUsers = async () => {
      try {
        const fetchedUsers = await userService.getUsers()
        setUsers(fetchedUsers)
      } catch (error) {
        console.error('Error fetching users:', error)
        // Fallback to empty array if API fails
        setUsers([])
      }
    }
    
    fetchUsers()
  }, [])

  // Ensure assignee is set after users are loaded
  useEffect(() => {
    if (task && users.length > 0 && task.assignee_id) {
      setValue('assignee_id', String(task.assignee_id))
    }
  }, [task, users, setValue])

  const handleFormSubmit = async (data: any) => {
    setIsLoading(true)
    try {
      // Convert empty strings to undefined for optional fields
      const formData = {
        ...data,
        assignee_id: data.assignee_id ? Number(data.assignee_id) : undefined,
        due_date: data.due_date || undefined
      }
      await onSubmit(formData)
    } catch (error) {
      console.error('Form submission error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Title *
        </label>
        <input
          type="text"
          {...register('title', { required: 'Title is required' })}
          className="input w-full"
          placeholder="Enter task title"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          {...register('description')}
          rows={3}
          className="input w-full resize-none"
          placeholder="Enter task description"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project *
          </label>
          <select
            {...register('project_id', { required: 'Project is required' })}
            className="input w-full"
          >
            <option value="">Select a project</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
          {errors.project_id && (
            <p className="mt-1 text-sm text-red-600">{errors.project_id.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Assignee
          </label>
          <select
            {...register('assignee_id')}
            className="input w-full"
          >
            <option value="">Unassigned</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.full_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <select
            {...register('status')}
            className="input w-full"
          >
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="review">Review</option>
            <option value="completed">Completed</option>
            <option value="blocked">Blocked</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Priority
          </label>
          <select
            {...register('priority')}
            className="input w-full"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Due Date
          </label>
          <div className="relative">
            <input
              type="date"
              {...register('due_date')}
              className="input w-full cursor-pointer pr-10"
              placeholder="Select due date"
              min={new Date().toISOString().split('T')[0]}
              onFocus={(e) => e.target.showPicker?.()}
            />
            <Calendar className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-secondary"
          disabled={isLoading}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  )
}

export default TaskForm 