# AI Collaboration Guide - AI Local RAG System

This document provides comprehensive guidance for AI assistants working on the AI Local RAG System project. It serves as the primary reference for understanding the project structure, coding conventions, and collaboration rules.

## 📋 Project Overview

The AI Local RAG System is a production-grade, on-premises/local-first Retrieval-Augmented Generation (RAG) platform. It enables organizations to build intelligent document search and question-answering systems that run entirely on their infrastructure.

### Key Characteristics
- **Local-First**: All processing happens on-premises, no data leaves the organization
- **Production-Ready**: Enterprise-grade security, monitoring, and scalability
- **Multi-Modal**: Supports various document types (PDF, Word, images, etc.)
- **Real-Time**: WebSocket-powered chat interface with live document interactions
- **Extensible**: Plugin architecture for external data source connectors

### Architecture Principles
1. **Separation of Concerns**: Clear boundaries between frontend, backend, and infrastructure
2. **Async-First**: Leverage async/await patterns throughout the stack
3. **Type Safety**: Comprehensive TypeScript and Pydantic type definitions
4. **Security by Design**: Authentication, authorization, and data protection built-in
5. **Observability**: Comprehensive logging, metrics, and monitoring

## 📁 Folder & File Structure

```
ai-local-rag-system/
├── apps/                          # Frontend applications
│   └── web/                      # Next.js 14 frontend
│       ├── app/                  # App Router pages and layouts
│       │   ├── (auth)/           # Authentication pages
│       │   ├── (dashboard)/      # Main dashboard pages
│       │   ├── admin/            # Admin-only pages
│       │   ├── api/              # API routes (if needed)
│       │   ├── globals.css       # Global styles
│       │   ├── layout.tsx        # Root layout
│       │   └── page.tsx          # Home page
│       ├── components/           # Reusable React components
│       │   ├── ui/              # shadcn/ui components
│       │   ├── forms/           # Form components
│       │   ├── layout/          # Layout components
│       │   └── features/        # Feature-specific components
│       ├── lib/                 # Utilities and configurations
│       │   ├── utils.ts         # General utilities
│       │   ├── api.ts           # API client configuration
│       │   ├── auth.ts          # Authentication utilities
│       │   └── store.ts         # Zustand store configuration
│       ├── types/               # TypeScript type definitions
│       │   ├── api.ts           # API response types
│       │   ├── auth.ts          # Authentication types
│       │   └── common.ts        # Shared types
│       ├── public/              # Static assets
│       ├── package.json         # Node.js dependencies
│       ├── tailwind.config.js   # Tailwind CSS configuration
│       ├── next.config.js       # Next.js configuration
│       └── tsconfig.json        # TypeScript configuration
├── services/                     # Backend services
│   └── api/                     # FastAPI backend
│       ├── app/                 # Main application code
│       │   ├── api/             # API endpoint definitions
│       │   │   └── v1/          # Version 1 API endpoints
│       │   │       ├── auth.py      # Authentication endpoints
│       │   │       ├── collections.py # Collection management
│       │   │       ├── documents.py   # Document management
│       │   │       ├── chat.py        # Chat and RAG endpoints
│       │   │       ├── connectors.py  # External connectors
│       │   │       ├── admin.py       # Admin endpoints
│       │   │       └── api.py         # Main API router
│       │   ├── core/            # Core application configuration
│       │   │   ├── config.py        # Settings and configuration
│       │   │   ├── database.py      # Database connection
│       │   │   ├── security.py      # Security utilities
│       │   │   └── celery.py        # Celery configuration
│       │   ├── models/          # SQLAlchemy ORM models
│       │   │   ├── user.py          # User model
│       │   │   ├── collection.py    # Collection model
│       │   │   ├── document.py      # Document model
│       │   │   ├── chat.py          # Chat models
│       │   │   ├── connector.py     # Connector model
│       │   │   ├── evaluation.py    # Evaluation model
│       │   │   ├── audit.py         # Audit log model
│       │   │   └── system.py        # System models
│       │   ├── schemas/         # Pydantic schemas
│       │   │   ├── auth.py          # Authentication schemas
│       │   │   ├── collection.py    # Collection schemas
│       │   │   ├── document.py      # Document schemas
│       │   │   ├── chat.py          # Chat schemas
│       │   │   ├── connector.py     # Connector schemas
│       │   │   ├── evaluation.py    # Evaluation schemas
│       │   │   └── common.py        # Common schemas
│       │   ├── services/        # Business logic services
│       │   │   ├── auth_service.py      # Authentication service
│       │   │   ├── collection_service.py # Collection service
│       │   │   ├── document_service.py   # Document service
│       │   │   ├── chat_service.py       # Chat service
│       │   │   ├── connector_service.py  # Connector service
│       │   │   ├── evaluation_service.py # Evaluation service
│       │   │   ├── rag_service.py        # RAG pipeline service
│       │   │   ├── file_service.py       # File storage service
│       │   │   ├── embedding_service.py  # Embedding service
│       │   │   └── system_service.py     # System service
│       │   └── __init__.py       # Package initialization
│       ├── alembic/             # Database migrations
│       │   ├── versions/        # Migration files
│       │   ├── env.py           # Alembic environment
│       │   └── alembic.ini      # Alembic configuration
│       ├── tests/               # Backend tests
│       │   ├── unit/            # Unit tests
│       │   ├── integration/     # Integration tests
│       │   └── conftest.py      # Test configuration
│       ├── main.py              # FastAPI application entry point
│       ├── requirements.txt     # Python dependencies
│       ├── docker-compose.yml   # Backend service orchestration
│       ├── Dockerfile           # Backend container definition
│       └── env.example          # Environment variables template
├── docs/                        # Project documentation
│   ├── CLAUDE.md               # This AI collaboration guide
│   ├── API.md                  # API documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── DEVELOPMENT.md          # Development guide
├── docker-compose.yml          # Root service orchestration
├── Makefile                    # Development commands
├── .gitignore                  # Git ignore rules
├── README.md                   # Project overview
├── README_BACKEND.md           # Backend-specific documentation
├── README_FRONTEND.md          # Frontend-specific documentation
└── PROJECT_BRIEF.md            # Original project requirements
```

## 🎨 Coding Conventions

### Python (Backend)

#### General Style
- **Python Version**: 3.11+
- **Code Style**: Follow PEP 8 with Black formatting
- **Type Hints**: Use type hints everywhere, including function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes

#### FastAPI Conventions
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

# Router definition
router = APIRouter(prefix="/endpoint", tags=["Tag"])

# Endpoint with proper typing and error handling
@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: CreateModel,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new item with proper validation."""
    try:
        service = ItemService(db)
        result = await service.create_item(item_data, current_user.id)
        return result
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

#### SQLAlchemy Models
```python
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
from typing import Optional, List
import uuid

class User(Base):
    """User account model with proper relationships."""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    owned_collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="owner")
```

#### Pydantic Schemas
```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=255, description="User full name")
    password: str = Field(..., min_length=8, description="User password")
    role: str = Field(default="user", regex="^(admin|user|viewer)$")

class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    email: str
    name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Service Layer
```python
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

class ItemService:
    """Service for item management with proper error handling."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_item(self, item_data: CreateModel, user_id: str) -> Item:
        """Create a new item with validation."""
        # Validate user exists
        user = await self._get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create item
        item = Item(
            name=item_data.name,
            description=item_data.description,
            created_by=user_id,
            tenant_id=user.tenant_id
        )
        
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        
        return item
```

### TypeScript/React (Frontend)

#### General Style
- **TypeScript**: Strict mode enabled
- **React**: Functional components with hooks
- **State Management**: Zustand for global state, React Query for server state
- **Styling**: Tailwind CSS with shadcn/ui components

#### Component Structure
```typescript
import { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useToast } from '@/hooks/use-toast'
import { api } from '@/lib/api'
import type { Item, CreateItemRequest } from '@/types/api'

interface ItemFormProps {
  onSuccess?: () => void
  initialData?: Partial<Item>
}

export function ItemForm({ onSuccess, initialData }: ItemFormProps) {
  const [formData, setFormData] = useState<CreateItemRequest>({
    name: initialData?.name || '',
    description: initialData?.description || ''
  })
  
  const { toast } = useToast()
  
  const createMutation = useMutation({
    mutationFn: (data: CreateItemRequest) => api.post('/items', data),
    onSuccess: () => {
      toast({
        title: 'Success',
        description: 'Item created successfully'
      })
      onSuccess?.()
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive'
      })
    }
  })
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData)
  }
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Name"
        value={formData.name}
        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        required
      />
      <Button type="submit" disabled={createMutation.isPending}>
        {createMutation.isPending ? 'Creating...' : 'Create Item'}
      </Button>
    </form>
  )
}
```

#### API Client
```typescript
import axios from 'axios'
import type { ApiResponse, PaginatedResponse } from '@/types/api'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for authentication
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or logout
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export { api }
```

#### Type Definitions
```typescript
// types/api.ts
export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user' | 'viewer'
  is_active: boolean
  created_at: string
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

export interface CreateCollectionRequest {
  name: string
  description?: string
  is_public?: boolean
}
```

## 🤖 AI Collaboration Rules

### 1. Code Generation Guidelines

#### When Creating New Files
- Always include proper imports and type definitions
- Follow the established file structure and naming conventions
- Include comprehensive docstrings and comments
- Implement proper error handling and validation
- Add appropriate tests when creating new functionality

#### When Modifying Existing Files
- Preserve existing functionality unless explicitly requested to change
- Maintain backward compatibility when possible
- Update related tests and documentation
- Follow the established patterns in the file

#### Error Handling
- Always implement proper error handling with meaningful error messages
- Use appropriate HTTP status codes for API endpoints
- Log errors appropriately for debugging
- Provide user-friendly error messages in the frontend

### 2. Database and Schema Changes

#### Model Changes
- Always create Alembic migrations for database schema changes
- Update related Pydantic schemas to match model changes
- Consider backward compatibility and data migration needs
- Update API endpoints to handle new/removed fields

#### Migration Guidelines
```python
# Example migration
"""Add user preferences field

Revision ID: 001_add_user_preferences
Revises: 000_initial
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.add_column('users', sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'preferences')
```

### 3. API Design Principles

#### RESTful Endpoints
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Implement consistent URL patterns
- Return appropriate HTTP status codes
- Include proper response models and validation

#### Pagination
- Always implement pagination for list endpoints
- Use consistent pagination parameters (page, size)
- Include total count and pagination metadata

#### Authentication & Authorization
- Implement proper JWT token validation
- Check user permissions for protected endpoints
- Use role-based access control (RBAC)
- Log authentication events for security

### 4. Frontend Development

#### Component Design
- Create reusable, composable components
- Use proper TypeScript types for all props and state
- Implement proper loading and error states
- Follow accessibility best practices

#### State Management
- Use React Query for server state
- Use Zustand for global client state
- Minimize prop drilling with proper state organization
- Implement optimistic updates where appropriate

#### Performance
- Implement proper memoization (useMemo, useCallback)
- Use Next.js Image component for optimized images
- Implement proper code splitting
- Optimize bundle size with tree shaking

## 📝 Editing Rules

### 1. File Modification Guidelines

#### Before Making Changes
- Read the existing code thoroughly to understand the current implementation
- Check for related files that might be affected
- Consider the impact on existing functionality
- Plan the changes to maintain consistency

#### During Implementation
- Follow the established coding patterns
- Add comprehensive comments for complex logic
- Implement proper error handling
- Write or update tests for new functionality

#### After Changes
- Verify that all imports are correct
- Check that the code compiles/runs without errors
- Update related documentation if needed
- Test the functionality manually if possible

### 2. Code Review Checklist

#### Backend Code
- [ ] Proper type hints and docstrings
- [ ] Error handling and validation
- [ ] Database query optimization
- [ ] Security considerations
- [ ] Test coverage
- [ ] API documentation

#### Frontend Code
- [ ] TypeScript types and interfaces
- [ ] Component reusability
- [ ] Performance optimization
- [ ] Accessibility compliance
- [ ] Error boundaries
- [ ] Responsive design

### 3. Documentation Updates

#### When to Update Documentation
- Adding new features or endpoints
- Changing API contracts
- Modifying database schemas
- Updating deployment procedures
- Adding new configuration options

#### Documentation Standards
- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Keep documentation up-to-date with code changes

## 🔧 Dependencies & Setup

### Backend Dependencies (Python)
```txt
# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Database
sqlalchemy>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.0

# Authentication & Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# RAG & AI
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-community>=0.0.10
openai>=1.3.0
anthropic>=0.7.0
sentence-transformers>=2.2.0

# File Processing
python-docx>=1.1.0
PyPDF2>=3.0.0
Pillow>=10.1.0
opencv-python>=4.8.0
pytesseract>=0.3.10

# Storage & Infrastructure
boto3>=1.34.0
redis>=5.0.0
celery>=5.3.0

# Monitoring & Logging
structlog>=23.2.0
prometheus-client>=0.19.0
opentelemetry-api>=1.21.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.25.0
```

### Frontend Dependencies (Node.js)
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.0",
    "react-dropzone": "^14.2.0",
    "react-pdf": "^7.0.0",
    "date-fns": "^2.30.0",
    "lucide-react": "^0.294.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  }
}
```

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rag_system

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage
S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=rag-system

# AI Services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
EMBEDDING_MODEL=text-embedding-3-large

# Monitoring
LOG_LEVEL=INFO
ENVIRONMENT=development
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_APP_NAME="AI Local RAG System"
```

## 🔄 Workflow & Tools

### Development Workflow

#### 1. Local Development Setup
```bash
# Clone repository
git clone <repository-url>
cd ai-local-rag-system

# Install dependencies
make install

# Start services
make up

# Run migrations
make db-migrate
```

#### 2. Development Commands
```bash
# View available commands
make help

# Start development environment
make up

# View logs
make logs

# Run tests
make test

# Code formatting
make format

# Database operations
make db-migrate
make db-reset  # WARNING: destroys data
```

#### 3. Testing Strategy
- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test API endpoints and database operations
- **E2E Tests**: Test complete user workflows
- **Performance Tests**: Test system under load

### Code Quality Tools

#### Backend
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

#### Frontend
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **Jest**: Testing

### Git Workflow

#### Branch Naming
- `feature/feature-name`: New features
- `bugfix/bug-description`: Bug fixes
- `hotfix/urgent-fix`: Critical fixes
- `refactor/component-name`: Code refactoring

#### Commit Messages
```
type(scope): description

feat(auth): add JWT token refresh functionality
fix(api): resolve pagination issue in collections endpoint
refactor(ui): extract reusable form components
docs(readme): update installation instructions
```

## 🧠 Contextual Knowledge

### Key Concepts

#### RAG Pipeline
1. **Document Ingestion**: Upload and process documents
2. **Chunking**: Split documents into manageable pieces
3. **Embedding**: Convert text to vector representations
4. **Indexing**: Store vectors in vector database
5. **Query Processing**: Convert user questions to vectors
6. **Retrieval**: Find relevant document chunks
7. **Reranking**: Improve relevance of retrieved chunks
8. **Answer Generation**: Generate answers using LLM
9. **Citation**: Provide source references

#### Security Model
- **Authentication**: JWT-based token authentication
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: PII/PHI detection and anonymization
- **Audit Logging**: Comprehensive activity tracking
- **Rate Limiting**: Prevent abuse and ensure performance

#### Performance Considerations
- **Async Processing**: Use async/await throughout
- **Caching**: Redis for frequently accessed data
- **Database Optimization**: Proper indexing and query optimization
- **File Storage**: Efficient document storage and retrieval
- **Background Tasks**: Celery for long-running operations

### Common Patterns

#### API Response Pattern
```python
@router.get("/items", response_model=PaginatedResponse[ItemResponse])
async def list_items(
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List items with pagination and filtering."""
    service = ItemService(db)
    items, total = await service.list_items(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size
    )
```

#### Error Handling Pattern
```python
async def process_document(document_id: str, file: UploadFile) -> None:
    """Process uploaded document with comprehensive error handling."""
    try:
        # Validate file
        if not is_valid_file(file):
            raise ValidationError("Invalid file type")
        
        # Process document
        await extract_text(file)
        await generate_embeddings(document_id)
        await update_document_status(document_id, "completed")
        
    except ValidationError as e:
        await update_document_status(document_id, "failed", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        await update_document_status(document_id, "failed", str(e))
        raise HTTPException(status_code=500, detail="Processing failed")
    except Exception as e:
        await update_document_status(document_id, "failed", "Unknown error")
        logger.error(f"Unexpected error processing document {document_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### Frontend State Management Pattern
```typescript
// Zustand store
interface AppState {
  user: User | null
  collections: Collection[]
  isLoading: boolean
  error: string | null
  
  // Actions
  setUser: (user: User | null) => void
  setCollections: (collections: Collection[]) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  logout: () => void
}

const useAppStore = create<AppState>((set) => ({
  user: null,
  collections: [],
  isLoading: false,
  error: null,
  
  setUser: (user) => set({ user }),
  setCollections: (collections) => set({ collections }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  logout: () => set({ user: null, collections: [] })
}))
```

## 📚 Examples

### Complete API Endpoint Example
```python
# app/api/v1/collections.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionListResponse
from app.schemas.common import PaginationParams
from app.services.collection_service import CollectionService

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection_data: CollectionCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new collection."""
    try:
        collection_service = CollectionService(db)
        collection = await collection_service.create_collection(collection_data, current_user.id)
        return collection
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=CollectionListResponse)
async def list_collections(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search collections by name"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List collections with pagination and search."""
    collection_service = CollectionService(db)
    collections, total = await collection_service.list_collections(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit,
        search=search
    )
    
    return CollectionListResponse(
        items=collections,
        total=total,
        page=pagination.page,
        size=pagination.size
    )
```

### Complete React Component Example
```typescript
// components/features/collections/CollectionList.tsx
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { api } from '@/lib/api'
import type { Collection } from '@/types/api'

export function CollectionList() {
  const [searchTerm, setSearchTerm] = useState('')
  const [page, setPage] = useState(1)
  const { toast } = useToast()
  const queryClient = useQueryClient()
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['collections', page, searchTerm],
    queryFn: () => api.get('/collections', {
      params: { page, size: 10, search: searchTerm || undefined }
    }).then(res => res.data)
  })
  
  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/collections/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['collections'] })
      toast({
        title: 'Success',
        description: 'Collection deleted successfully'
      })
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive'
      })
    }
  })
  
  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this collection?')) {
      deleteMutation.mutate(id)
    }
  }
  
  if (isLoading) return <div>Loading collections...</div>
  if (error) return <div>Error loading collections: {error.message}</div>
  
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Search className="h-4 w-4 text-gray-500" />
          <Input
            placeholder="Search collections..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-64"
          />
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Collection
        </Button>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data?.items.map((collection: Collection) => (
          <Card key={collection.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                {collection.name}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(collection.id)}
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-2">
                {collection.description || 'No description'}
              </p>
              <div className="flex items-center justify-between">
                <Badge variant={collection.is_public ? 'default' : 'secondary'}>
                  {collection.is_public ? 'Public' : 'Private'}
                </Badge>
                <span className="text-sm text-gray-500">
                  {collection.document_count} documents
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      {data?.items.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No collections found
        </div>
      )}
    </div>
  )
}
```

This comprehensive guide should provide AI assistants with all the necessary information to effectively work on the AI Local RAG System project while maintaining consistency and quality standards.




