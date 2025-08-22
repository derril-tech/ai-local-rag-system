# Repository Map - AI Local RAG System

This document provides a comprehensive overview of the repository structure and the purpose of each folder and file.

## 📁 Root Structure

```
ai-local-rag-system/
├── apps/                    # Frontend applications
│   └── web/                # Next.js frontend application
├── services/               # Backend services
│   ├── api/               # FastAPI backend service
│   └── workers/           # Celery workers for background tasks
├── docs/                  # Documentation
├── scripts/               # Development and deployment scripts
├── docker/                # Docker configuration files
└── infrastructure/        # Infrastructure as Code (IaC)
```

## 🎯 Frontend (`apps/web/`)

The Next.js frontend application with App Router, TypeScript, and Tailwind CSS.

### Key Directories:
- **`app/`** - Next.js App Router pages and layouts
  - `layout.tsx` - Root layout with providers
  - `page.tsx` - Landing page
  - `globals.css` - Global styles and design tokens
  - `dashboard/` - Dashboard pages
  - `collections/` - Collection management
  - `connectors/` - Connector setup
  - `admin/` - Admin interface

- **`components/`** - Reusable React components
  - `ui/` - shadcn/ui components
  - `chat/` - Chat interface components
  - `upload/` - File upload components
  - `viewer/` - Document viewer components
  - `providers/` - React context providers

- **`lib/`** - Utility functions and configurations
  - `api.ts` - API client functions
  - `utils.ts` - General utilities
  - `types.ts` - TypeScript type definitions
  - `hooks/` - Custom React hooks

- **`public/`** - Static assets

### Configuration Files:
- `package.json` - Dependencies and scripts
- `next.config.js` - Next.js configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `tsconfig.json` - TypeScript configuration

## 🔧 Backend (`services/api/`)

The FastAPI backend service with comprehensive RAG functionality.

### Key Directories:
- **`app/`** - Main application code
  - `api/` - API route handlers
    - `v1/` - Version 1 API endpoints
      - `auth.py` - Authentication endpoints
      - `collections.py` - Collection management
      - `documents.py` - Document operations
      - `chat.py` - Chat/RAG endpoints
      - `connectors.py` - Connector management
      - `admin.py` - Admin endpoints
  - `core/` - Core application modules
    - `config.py` - Configuration settings
    - `database.py` - Database connection and models
    - `security.py` - Authentication and authorization
    - `logging.py` - Logging configuration
  - `models/` - Database models
    - `user.py` - User model
    - `collection.py` - Collection model
    - `document.py` - Document model
    - `chat.py` - Chat session model
  - `schemas/` - Pydantic schemas
    - `user.py` - User schemas
    - `collection.py` - Collection schemas
    - `document.py` - Document schemas
    - `chat.py` - Chat schemas
  - `services/` - Business logic services
    - `rag/` - RAG pipeline services
    - `embedding/` - Embedding services
    - `storage/` - File storage services
    - `connectors/` - Connector services
  - `utils/` - Utility functions

- **`alembic/`** - Database migration files
- **`tests/`** - Test files
  - `unit/` - Unit tests
  - `integration/` - Integration tests
  - `fixtures/` - Test data

### Configuration Files:
- `main.py` - FastAPI application entry point
- `requirements.txt` - Python dependencies
- `alembic.ini` - Alembic configuration
- `Dockerfile` - Container configuration

## 🔄 Workers (`services/workers/`)

Celery workers for background task processing.

### Key Directories:
- **`app/`** - Worker application code
  - `tasks/` - Celery task definitions
    - `document_processing.py` - Document ingestion tasks
    - `embedding.py` - Embedding generation tasks
    - `ocr.py` - OCR processing tasks
    - `sync.py` - Connector sync tasks
  - `processors/` - Document processors
    - `pdf.py` - PDF processing
    - `docx.py` - Word document processing
    - `excel.py` - Excel processing
    - `html.py` - HTML processing
  - `utils/` - Worker utilities

### Configuration Files:
- `celery.py` - Celery configuration
- `requirements.txt` - Worker dependencies
- `Dockerfile` - Worker container configuration

## 📚 Documentation (`docs/`)

Comprehensive documentation for the project.

### Key Files:
- **`REPO_MAP.md`** - This file, repository structure overview
- **`API_SPEC.md`** - API specification and endpoints
- **`CLAUDE.md`** - AI collaboration guidelines and project context
- **`PROMPT_DECLARATION.md`** - Project requirements and specifications
- **`DEPLOYMENT.md`** - Deployment instructions
- **`SECURITY.md`** - Security guidelines and compliance

## 🛠️ Scripts (`scripts/`)

Development and deployment automation scripts.

### Key Files:
- `dev.sh` - Development environment setup
- `deploy.sh` - Deployment script
- `setup.sh` - Initial project setup
- `test.sh` - Test execution script
- `migrate.sh` - Database migration script

## 🐳 Docker (`docker/`)

Docker configuration for containerized deployment.

### Key Files:
- `docker-compose.yml` - Local development environment
- `docker-compose.prod.yml` - Production environment
- `Dockerfile.api` - API service container
- `Dockerfile.workers` - Workers container
- `Dockerfile.frontend` - Frontend container

## ☁️ Infrastructure (`infrastructure/`)

Infrastructure as Code for cloud deployment.

### Key Directories:
- **`terraform/`** - Terraform configurations
- **`kubernetes/`** - Kubernetes manifests
- **`helm/`** - Helm charts
- **`monitoring/`** - Monitoring and observability

## 🔍 Key Features by Directory

### Frontend Features:
- **Real-time Chat Interface** - WebSocket-based chat with streaming responses
- **Document Upload** - Drag-and-drop file upload with progress tracking
- **Source Viewer** - PDF viewer with citation highlighting
- **Collection Management** - Create and manage document collections
- **Connector Setup** - Wizard for setting up external connectors
- **Admin Dashboard** - System monitoring and user management

### Backend Features:
- **RAG Pipeline** - Complete retrieval-augmented generation pipeline
- **Document Processing** - Multi-format document ingestion with OCR
- **Vector Search** - Hybrid search with BM25 and embeddings
- **Authentication** - JWT-based authentication with RBAC
- **File Storage** - S3/MinIO compatible storage
- **Connector Framework** - Extensible connector system
- **Audit Logging** - Comprehensive audit trail
- **Rate Limiting** - API rate limiting and quotas

### Worker Features:
- **Background Processing** - Asynchronous document processing
- **OCR Processing** - Optical character recognition
- **Embedding Generation** - Vector embedding creation
- **Connector Sync** - Periodic synchronization with external systems

## 🚀 Getting Started

1. **Frontend Development**: `cd apps/web && npm run dev`
2. **Backend Development**: `cd services/api && uvicorn main:app --reload`
3. **Worker Development**: `cd services/workers && celery -A app.celery worker --loglevel=info`
4. **Full Stack**: Use `scripts/dev.sh` for complete development environment

## 📝 Development Guidelines

- **Frontend**: Follow Next.js App Router patterns and use shadcn/ui components
- **Backend**: Use FastAPI with dependency injection and Pydantic models
- **Database**: Use SQLAlchemy with async support and Alembic migrations
- **Testing**: Maintain high test coverage with pytest
- **Documentation**: Keep all documentation up to date with code changes

## 🔒 Security Considerations

- All sensitive data is encrypted at rest and in transit
- Authentication uses JWT tokens with proper expiration
- File uploads are validated and scanned for malware
- API endpoints are rate-limited and protected
- Audit logging tracks all user actions
- PII detection and redaction capabilities included
