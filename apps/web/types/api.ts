// API Response Types
export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user' | 'viewer'
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Collection {
  id: string
  name: string
  description?: string
  owner_id: string
  is_public: boolean
  document_count: number
  created_at: string
  updated_at: string
}

export interface Document {
  id: string
  filename: string
  collection_id: string
  file_size: number
  mime_type: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  processing_progress?: number
  error_message?: string
  created_at: string
  updated_at: string
}

export interface ChatSession {
  id: string
  title: string
  user_id: string
  collection_ids: string[]
  settings: Record<string, any>
  is_archived: boolean
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: string
  session_id: string
  content: string
  role: 'user' | 'assistant' | 'system'
  metadata?: Record<string, any>
  created_at: string
}

export interface Connector {
  id: string
  name: string
  connector_type: string
  status: 'active' | 'inactive' | 'syncing' | 'error'
  config: Record<string, any>
  last_sync?: string
  created_at: string
  updated_at: string
}

export interface Evaluation {
  id: string
  name: string
  description?: string
  collection_ids: string[]
  status: 'pending' | 'running' | 'completed' | 'failed'
  results?: Record<string, any>
  created_at: string
  updated_at: string
}

// API Request Types
export interface CreateCollectionRequest {
  name: string
  description?: string
  is_public?: boolean
}

export interface UpdateCollectionRequest {
  name?: string
  description?: string
  is_public?: boolean
}

export interface CreateDocumentRequest {
  filename: string
  collection_id: string
  metadata?: string
}

export interface CreateChatSessionRequest {
  title?: string
  collection_ids?: string[]
  settings?: Record<string, any>
}

export interface CreateChatMessageRequest {
  session_id: string
  content: string
  role?: 'user' | 'assistant' | 'system'
  metadata?: Record<string, any>
}

export interface QueryRequest {
  query: string
  session_id?: string
  collection_ids?: string[]
  settings?: Record<string, any>
  filters?: Record<string, any>
}

export interface CreateConnectorRequest {
  name: string
  connector_type: string
  config: Record<string, any>
  sync_settings?: Record<string, any>
  filters?: Record<string, any>
}

export interface UpdateConnectorRequest {
  name?: string
  config?: Record<string, any>
  status?: string
  sync_settings?: Record<string, any>
  filters?: Record<string, any>
}

export interface CreateEvaluationRequest {
  name: string
  description?: string
  collection_ids: string[]
  test_queries: Array<{
    query: string
    expected_answer?: string
  }>
  metrics: string[]
}

// Common API Types
export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
}

export interface PaginationParams {
  page: number
  size: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

// RAG Response Types
export interface QueryResponse {
  query: string
  answer: string
  citations: Array<{
    document_id: string
    filename: string
    content: string
    page?: number
  }>
  confidence: number
  sources: string[]
  processing_time_ms: number
}

// System Types
export interface SystemStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  timestamp: string
  metrics: {
    total_users: number
    total_documents: number
    active_sessions: number
  }
  services: Array<{
    name: string
    status: 'healthy' | 'degraded' | 'unhealthy'
    response_time_ms: number
  }>
}

export interface SystemMetrics {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  active_connections: number
  requests_per_minute: number
  error_rate: number
}
