import toast from 'react-hot-toast'

export interface ApiError {
  response?: {
    data?: {
      detail?: string
      message?: string
    }
    status?: number
  }
  message?: string
  code?: string
}

export const handleApiError = (error: ApiError, defaultMessage: string = 'An unexpected error occurred'): string => {
  let message = defaultMessage

  if (error.response?.data?.detail) {
    message = error.response.data.detail
  } else if (error.response?.data?.message) {
    message = error.response.data.message
  } else if (error.response?.status === 404) {
    message = 'Resource not found'
  } else if (error.response?.status === 403) {
    message = 'Access denied'
  } else if (error.response?.status === 500) {
    message = 'Server error'
  } else if (error.code === 'ECONNABORTED') {
    message = 'Request timeout'
  } else if (error.code === 'ERR_NETWORK') {
    message = 'Network error - unable to connect to server'
  } else if (error.message) {
    message = error.message
  }

  return message
}

export const showErrorToast = (error: ApiError, defaultMessage: string = 'An unexpected error occurred'): void => {
  const message = handleApiError(error, defaultMessage)
  toast.error(message)
}

export const showSuccessToast = (message: string): void => {
  toast.success(message)
}

export const showInfoToast = (message: string): void => {
  toast(message, {
    icon: 'ℹ️',
  })
} 