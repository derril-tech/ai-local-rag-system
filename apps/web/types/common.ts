// Common utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Status types
export type Status = 'idle' | 'loading' | 'success' | 'error'

export type ProcessingStatus = 'pending' | 'processing' | 'completed' | 'failed'

export type ConnectorStatus = 'active' | 'inactive' | 'syncing' | 'error'

export type EvaluationStatus = 'pending' | 'running' | 'completed' | 'failed'

// File types
export type SupportedFileType = 
  | '.pdf' 
  | '.txt' 
  | '.docx' 
  | '.doc' 
  | '.pptx' 
  | '.ppt'
  | '.xlsx' 
  | '.xls' 
  | '.csv' 
  | '.json' 
  | '.xml' 
  | '.html'
  | '.md' 
  | '.rtf' 
  | '.odt' 
  | '.ods' 
  | '.odp'

export interface FileUpload {
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'completed' | 'error'
  error?: string
}

// Pagination types
export interface PaginationState {
  page: number
  size: number
  total: number
  totalPages: number
}

export interface SortState {
  field: string
  direction: 'asc' | 'desc'
}

// Filter types
export interface FilterOption {
  label: string
  value: string
  count?: number
}

export interface FilterState {
  [key: string]: string | string[] | boolean | number
}

// Form types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'checkbox' | 'radio' | 'file'
  required?: boolean
  placeholder?: string
  options?: FilterOption[]
  validation?: {
    min?: number
    max?: number
    pattern?: string
    message?: string
  }
}

export interface FormState {
  [key: string]: any
  isValid: boolean
  errors: Record<string, string>
}

// Notification types
export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

// Theme types
export type Theme = 'light' | 'dark' | 'system'

export interface ThemeConfig {
  theme: Theme
  primaryColor: string
  borderRadius: number
}

// API Error types
export interface ApiError {
  message: string
  code?: string
  details?: Record<string, any>
  status?: number
}

// Search types
export interface SearchParams {
  query: string
  filters?: FilterState
  sort?: SortState
  pagination?: PaginationState
}

export interface SearchResult<T> {
  items: T[]
  total: number
  query: string
  filters: FilterState
  sort: SortState
  pagination: PaginationState
}

// WebSocket types
export interface WebSocketMessage<T = any> {
  type: string
  data: T
  timestamp: string
  id?: string
}

export interface WebSocketState {
  isConnected: boolean
  isConnecting: boolean
  error: string | null
}

// Event types
export interface AppEvent {
  type: string
  payload: any
  timestamp: string
  userId?: string
}

// Settings types
export interface UserSettings {
  theme: Theme
  language: string
  notifications: {
    email: boolean
    push: boolean
    desktop: boolean
  }
  preferences: {
    autoSave: boolean
    defaultPageSize: number
    showTutorial: boolean
  }
}

// Audit types
export interface AuditLog {
  id: string
  user_id: string
  action: string
  resource_type: string
  resource_id: string
  details: Record<string, any>
  ip_address: string
  user_agent: string
  created_at: string
}
