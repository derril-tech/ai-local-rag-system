# API Specification - AI Local RAG System

This document provides comprehensive API specifications for the AI Local RAG System backend.

## 🔗 Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.rag-system.com`

## 📋 API Versioning

All endpoints are versioned under `/api/v1/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Authentication Headers

```http
Authorization: Bearer <access_token>
```

### Token Endpoints

#### POST `/api/v1/auth/login`

Authenticate user and receive access/refresh tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST `/api/v1/auth/refresh`

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 📚 Collections API

### GET `/api/v1/collections`

List all collections accessible to the user.

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 20)
- `search` (string, optional): Search term for collection names

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Legal Documents",
      "description": "Collection of legal documents",
      "document_count": 150,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "permissions": {
        "read": true,
        "write": true,
        "admin": false
      }
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

### POST `/api/v1/collections`

Create a new collection.

**Request Body:**
```json
{
  "name": "New Collection",
  "description": "Description of the collection",
  "settings": {
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "embedding_model": "text-embedding-3-large"
  }
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "New Collection",
  "description": "Description of the collection",
  "document_count": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "settings": {
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "embedding_model": "text-embedding-3-large"
  }
}
```

### GET `/api/v1/collections/{collection_id}`

Get collection details.

**Response:**
```json
{
  "id": "uuid",
  "name": "Legal Documents",
  "description": "Collection of legal documents",
  "document_count": 150,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "settings": {
    "chunk_size": 1000,
    "chunk_overlap": 150,
    "embedding_model": "text-embedding-3-large"
  },
  "permissions": {
    "read": true,
    "write": true,
    "admin": false
  }
}
```

## 📄 Documents API

### POST `/api/v1/collections/{collection_id}/documents`

Upload documents to a collection.

**Request Body:** (multipart/form-data)
- `files`: Array of files to upload
- `metadata` (optional): JSON string with document metadata

**Response:**
```json
{
  "upload_id": "uuid",
  "files": [
    {
      "id": "uuid",
      "filename": "document.pdf",
      "size": 1024000,
      "status": "processing",
      "uploaded_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_files": 1,
  "processing_status": "queued"
}
```

### GET `/api/v1/collections/{collection_id}/documents`

List documents in a collection.

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 20)
- `search` (string, optional): Search term for document names
- `status` (string, optional): Filter by processing status

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "filename": "document.pdf",
      "file_size": 1024000,
      "file_type": "application/pdf",
      "status": "processed",
      "chunk_count": 45,
      "uploaded_at": "2024-01-15T10:30:00Z",
      "processed_at": "2024-01-15T10:35:00Z",
      "metadata": {
        "title": "Legal Document",
        "author": "John Doe",
        "date": "2024-01-01"
      }
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

### GET `/api/v1/documents/{document_id}`

Get document details and content.

**Response:**
```json
{
  "id": "uuid",
  "filename": "document.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "status": "processed",
  "chunk_count": 45,
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:35:00Z",
  "metadata": {
    "title": "Legal Document",
    "author": "John Doe",
    "date": "2024-01-01"
  },
  "chunks": [
    {
      "id": "uuid",
      "content": "Document content...",
      "page_number": 1,
      "start_offset": 0,
      "end_offset": 1000,
      "embedding_id": "uuid"
    }
  ]
}
```

## 💬 Chat/RAG API

### POST `/api/v1/chat/ask`

Ask a question and get RAG-powered response.

**Request Body:**
```json
{
  "question": "What are the key terms in the contract?",
  "collection_ids": ["uuid1", "uuid2"],
  "options": {
    "max_results": 8,
    "include_sources": true,
    "stream": false
  }
}
```

**Response:**
```json
{
  "answer": "Based on the contract documents, the key terms include...",
  "sources": [
    {
      "document_id": "uuid",
      "document_name": "contract.pdf",
      "page_number": 5,
      "chunk_id": "uuid",
      "content": "The key terms of this agreement...",
      "relevance_score": 0.95,
      "start_offset": 1500,
      "end_offset": 2000
    }
  ],
  "confidence_score": 0.92,
  "processing_time": 1.5,
  "model_used": "gpt-4",
  "tokens_used": 1250
}
```

### POST `/api/v1/chat/stream`

Stream RAG response (WebSocket-like).

**Request Body:**
```json
{
  "question": "What are the key terms in the contract?",
  "collection_ids": ["uuid1", "uuid2"],
  "session_id": "uuid"
}
```

**Response:** (Server-Sent Events)
```
data: {"type": "start", "session_id": "uuid"}

data: {"type": "chunk", "content": "Based on the contract", "session_id": "uuid"}

data: {"type": "chunk", "content": " documents, the key", "session_id": "uuid"}

data: {"type": "sources", "sources": [...], "session_id": "uuid"}

data: {"type": "end", "session_id": "uuid"}
```

### GET `/api/v1/chat/sessions`

Get chat session history.

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 20)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "question": "What are the key terms?",
      "answer_preview": "Based on the contract documents...",
      "created_at": "2024-01-15T10:30:00Z",
      "collection_ids": ["uuid1", "uuid2"]
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

## 🔌 Connectors API

### GET `/api/v1/connectors`

List configured connectors.

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "SharePoint Legal",
      "type": "sharepoint",
      "status": "active",
      "last_sync": "2024-01-15T10:00:00Z",
      "document_count": 1250,
      "settings": {
        "site_url": "https://company.sharepoint.com/sites/legal",
        "folder_path": "/Documents"
      }
    }
  ]
}
```

### POST `/api/v1/connectors`

Create a new connector.

**Request Body:**
```json
{
  "name": "Google Drive Legal",
  "type": "google_drive",
  "settings": {
    "folder_id": "1ABC123DEF456",
    "sync_interval": 3600
  },
  "collection_id": "uuid"
}
```

### POST `/api/v1/connectors/{connector_id}/sync`

Trigger manual sync for a connector.

**Response:**
```json
{
  "sync_id": "uuid",
  "status": "started",
  "started_at": "2024-01-15T10:30:00Z"
}
```

## 👥 Admin API

### GET `/api/v1/admin/stats`

Get system statistics (admin only).

**Response:**
```json
{
  "users": {
    "total": 150,
    "active": 120,
    "new_this_month": 15
  },
  "documents": {
    "total": 50000,
    "processed": 48500,
    "processing": 1500,
    "failed": 0
  },
  "collections": {
    "total": 25,
    "active": 23
  },
  "storage": {
    "used_gb": 150.5,
    "total_gb": 1000,
    "usage_percent": 15.05
  },
  "performance": {
    "avg_response_time_ms": 1200,
    "requests_per_minute": 45,
    "error_rate_percent": 0.1
  }
}
```

### GET `/api/v1/admin/users`

List all users (admin only).

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 20)
- `search` (string, optional): Search term for user names/emails

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": "2024-01-15T09:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20
}
```

## ⚠️ Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  },
  "status_code": 400
}
```

### Common Error Codes

- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `422` - Unprocessable Entity (semantic validation errors)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

## 📊 Rate Limiting

- **Authentication endpoints**: 10 requests per minute
- **Document upload**: 5 requests per minute
- **Chat/RAG endpoints**: 60 requests per minute
- **General API**: 100 requests per minute

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642248600
```

## 🔒 Security

- All endpoints require authentication except `/health`
- JWT tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- All sensitive data is encrypted at rest
- File uploads are validated and scanned
- API keys are required for external integrations

## 📈 Monitoring

The API includes comprehensive monitoring:

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics` (Prometheus format)
- **OpenAPI Docs**: `GET /docs` (Swagger UI)
- **ReDoc**: `GET /redoc` (Alternative docs)

## 🔄 WebSocket Endpoints

### `/ws/chat/{session_id}`

Real-time chat streaming endpoint.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/session-id');
```

**Message Format:**
```json
{
  "type": "question",
  "content": "What are the key terms?",
  "collection_ids": ["uuid1", "uuid2"]
}
```

**Response Format:**
```json
{
  "type": "chunk",
  "content": "Based on the contract...",
  "session_id": "uuid"
}
```
