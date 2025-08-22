// Core domain types for the RAG system
// These types define the data structures used throughout the application

// ============================================================================
// USER & AUTHENTICATION TYPES
// ============================================================================

export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  tenant_id: string
  created_at: string
  updated_at: string
  last_login?: string
  is_active: boolean
  preferences: UserPreferences
}

export type UserRole = 'admin' | 'user' | 'viewer'

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  language: string
  timezone: string
  notifications: NotificationSettings
}

export interface NotificationSettings {
  email: boolean
  push: boolean
  chat_notifications: boolean
  ingestion_complete: boolean
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

// ============================================================================
// COLLECTION TYPES
// ============================================================================

export interface Collection {
  id: string
  name: string
  description: string
  tenant_id: string
  created_by: string
  created_at: string
  updated_at: string
  is_public: boolean
  settings: CollectionSettings
  stats: CollectionStats
  permissions: CollectionPermissions[]
}

export interface CollectionSettings {
  chunk_size: number
  chunk_overlap: number
  embedding_model: string
  retrieval_strategy: 'hybrid' | 'semantic' | 'keyword'
  reranker_enabled: boolean
  pii_redaction: boolean
  retention_policy: RetentionPolicy
}

export interface RetentionPolicy {
  enabled: boolean
  days: number
  action: 'delete' | 'archive'
}

export interface CollectionStats {
  total_documents: number
  total_chunks: number
  total_size_bytes: number
  last_ingestion: string
  last_query: string
}

export interface CollectionPermissions {
  user_id: string
  role: 'owner' | 'editor' | 'viewer'
  granted_at: string
  granted_by: string
}

// ============================================================================
// DOCUMENT TYPES
// ============================================================================

export interface Document {
  id: string
  collection_id: string
  name: string
  file_path: string
  file_size: number
  mime_type: string
  status: DocumentStatus
  created_at: string
  updated_at: string
  metadata: DocumentMetadata
  chunks: DocumentChunk[]
  processing_info: ProcessingInfo
}

export type DocumentStatus = 
  | 'pending' 
  | 'processing' 
  | 'completed' 
  | 'failed' 
  | 'archived'

export interface DocumentMetadata {
  title?: string
  author?: string
  subject?: string
  keywords?: string[]
  language?: string
  page_count?: number
  extracted_text_length?: number
  ocr_applied?: boolean
  tables_extracted?: number
  images_extracted?: number
  custom_fields: Record<string, any>
}

export interface DocumentChunk {
  id: string
  document_id: string
  content: string
  chunk_index: number
  page_number?: number
  section?: string
  metadata: ChunkMetadata
  embeddings?: number[]
  created_at: string
}

export interface ChunkMetadata {
  heading?: string
  table_data?: any
  image_caption?: string
  citation_spans: CitationSpan[]
  confidence_score: number
}

export interface CitationSpan {
  start: number
  end: number
  page?: number
  section?: string
  confidence: number
}

export interface ProcessingInfo {
  started_at: string
  completed_at?: string
  error_message?: string
  steps_completed: ProcessingStep[]
  current_step?: ProcessingStep
}

export interface ProcessingStep {
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  started_at?: string
  completed_at?: string
  error_message?: string
  metadata?: Record<string, any>
}

// ============================================================================
// CHAT & RAG TYPES
// ============================================================================

export interface ChatSession {
  id: string
  user_id: string
  collection_id?: string
  title: string
  created_at: string
  updated_at: string
  messages: ChatMessage[]
  settings: ChatSettings
}

export interface ChatMessage {
  id: string
  session_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  citations: Citation[]
  metadata: MessageMetadata
}

export interface Citation {
  id: string
  document_id: string
  document_name: string
  chunk_id: string
  content: string
  page_number?: number
  confidence_score: number
  span_start: number
  span_end: number
  highlight_spans: HighlightSpan[]
}

export interface HighlightSpan {
  start: number
  end: number
  page?: number
  section?: string
}

export interface MessageMetadata {
  model_used?: string
  tokens_used?: number
  processing_time_ms?: number
  confidence_score?: number
  groundedness_score?: number
  sources_retrieved?: number
  query_type?: 'factual' | 'analytical' | 'creative'
}

export interface ChatSettings {
  model: string
  temperature: number
  max_tokens: number
  retrieval_strategy: 'hybrid' | 'semantic' | 'keyword'
  reranker_enabled: boolean
  citation_threshold: number
  max_sources: number
}

export interface QueryRequest {
  query: string
  session_id?: string
  collection_id?: string
  settings?: Partial<ChatSettings>
  filters?: QueryFilters
}

export interface QueryResponse {
  answer: string
  citations: Citation[]
  confidence_score: number
  groundedness_score: number
  processing_time_ms: number
  tokens_used: number
  sources_retrieved: number
  session_id: string
  message_id: string
}

export interface QueryFilters {
  date_range?: {
    start: string
    end: string
  }
  document_types?: string[]
  authors?: string[]
  tags?: string[]
  confidence_threshold?: number
}

// ============================================================================
// CONNECTOR TYPES
// ============================================================================

export interface Connector {
  id: string
  name: string
  type: ConnectorType
  status: ConnectorStatus
  tenant_id: string
  created_by: string
  created_at: string
  updated_at: string
  config: ConnectorConfig
  last_sync?: string
  stats: ConnectorStats
}

export type ConnectorType = 
  | 'sharepoint' 
  | 'google_drive' 
  | 's3' 
  | 'box' 
  | 'confluence' 
  | 'jira' 
  | 'imap' 
  | 'slack'

export type ConnectorStatus = 
  | 'active' 
  | 'inactive' 
  | 'error' 
  | 'syncing'

export interface ConnectorConfig {
  base_url?: string
  credentials: Record<string, any>
  sync_settings: SyncSettings
  filters?: ConnectorFilters
}

export interface SyncSettings {
  frequency: 'manual' | 'hourly' | 'daily' | 'weekly'
  last_sync?: string
  next_sync?: string
  incremental_sync: boolean
  delete_removed_files: boolean
  max_file_size: number
}

export interface ConnectorFilters {
  include_patterns?: string[]
  exclude_patterns?: string[]
  folder_paths?: string[]
  date_modified_after?: string
}

export interface ConnectorStats {
  total_files_synced: number
  total_size_bytes: number
  last_sync_duration_ms: number
  errors_count: number
  pending_files: number
}

// ============================================================================
// EVALUATION TYPES
// ============================================================================

export interface Evaluation {
  id: string
  name: string
  description: string
  created_by: string
  created_at: string
  status: EvaluationStatus
  results: EvaluationResults
  settings: EvaluationSettings
}

export type EvaluationStatus = 
  | 'pending' 
  | 'running' 
  | 'completed' 
  | 'failed'

export interface EvaluationSettings {
  metrics: EvaluationMetric[]
  test_queries: TestQuery[]
  collection_id: string
  model_config: ModelConfig
}

export interface EvaluationMetric {
  name: string
  weight: number
  threshold: number
}

export interface TestQuery {
  id: string
  query: string
  expected_answer?: string
  expected_sources?: string[]
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
}

export interface ModelConfig {
  model: string
  temperature: number
  max_tokens: number
  retrieval_strategy: string
}

export interface EvaluationResults {
  overall_score: number
  metrics: MetricResult[]
  query_results: QueryResult[]
  summary: EvaluationSummary
}

export interface MetricResult {
  name: string
  score: number
  weight: number
  weighted_score: number
  details: Record<string, any>
}

export interface QueryResult {
  query_id: string
  query: string
  answer: string
  citations: Citation[]
  metrics: Record<string, number>
  success: boolean
  error_message?: string
}

export interface EvaluationSummary {
  total_queries: number
  successful_queries: number
  average_groundedness: number
  average_citation_coverage: number
  average_confidence: number
  common_issues: string[]
  recommendations: string[]
}

// ============================================================================
// SYSTEM & ADMIN TYPES
// ============================================================================

export interface SystemStatus {
  status: 'healthy' | 'degraded' | 'down'
  services: ServiceStatus[]
  metrics: SystemMetrics
  last_updated: string
}

export interface ServiceStatus {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  response_time_ms: number
  error_rate: number
  last_check: string
}

export interface SystemMetrics {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  active_users: number
  total_queries: number
  average_response_time: number
}

export interface AuditLog {
  id: string
  user_id: string
  action: string
  resource_type: string
  resource_id: string
  timestamp: string
  ip_address: string
  user_agent: string
  details: Record<string, any>
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: PaginationInfo
  total: number
}

export interface PaginationInfo {
  page: number
  per_page: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, any>
  timestamp: string
}

// ============================================================================
// WEBSOCKET TYPES
// ============================================================================

export interface WebSocketMessage {
  type: string
  payload: any
  timestamp: string
  session_id?: string
}

export interface StreamingResponse {
  type: 'token' | 'citation' | 'complete' | 'error'
  content?: string
  citations?: Citation[]
  metadata?: Record<string, any>
  error?: string
}

// ============================================================================
// FILE UPLOAD TYPES
// ============================================================================

export interface FileUpload {
  id: string
  name: string
  size: number
  type: string
  status: 'uploading' | 'processing' | 'completed' | 'failed'
  progress: number
  error?: string
  uploaded_at: string
}

export interface UploadConfig {
  max_file_size: number
  allowed_types: string[]
  max_files_per_upload: number
  chunk_size: number
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type LoadingState = 'idle' | 'loading' | 'success' | 'error'

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface FilterOption {
  field: string
  operator: 'eq' | 'ne' | 'gt' | 'lt' | 'gte' | 'lte' | 'contains' | 'in'
  value: any
}

export interface SortOption {
  field: string
  direction: 'asc' | 'desc'
}
