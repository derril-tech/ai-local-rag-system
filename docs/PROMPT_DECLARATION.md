# PROMPT DECLARATION FOR CLAUDE

## PROJECT OVERVIEW

You are working on a **Local Retrieval-Augmented Generation (RAG) System** - a production-grade, on-prem/local-first RAG platform for instant, trustworthy answers over private documents with strict data residency and zero-trust controls.

**Core Purpose**: Indexes PDFs, Office files, HTML, and emails; answers questions with grounded citations; runs fully local or in VPC.

**Key Value Proposition**: Deterministic retrieval + verifiable quotes + redaction pipeline → executive-trust answers.

**Target Users**: Legal, finance, research, ops teams needing compliant, air‑gapped knowledge access.

## FRONTEND ARCHITECTURE

### Tech Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: Zustand for lightweight state, React Query for server state
- **Real-time**: Socket.io-client for WebSocket connections
- **File Handling**: React Dropzone, React-PDF
- **Icons**: Lucide React
- **Date Handling**: date-fns

### Project Structure
```
apps/web/
├── app/                    # Next.js App Router pages
│   ├── globals.css        # Global styles and Tailwind
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   ├── about/             # About page
│   └── dashboard/         # Dashboard page
├── components/            # Reusable UI components
│   └── ui/               # shadcn/ui components
├── lib/                  # Utilities and helpers
│   ├── utils.ts          # Common utility functions
│   └── mock-data.ts      # Mock data for development
├── types/                # TypeScript type definitions
│   └── index.ts          # Core domain types
├── package.json          # Dependencies and scripts
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── .env.local.example    # Environment variables template
```

### Design System
- **Color Scheme**: Neutral base with accent colors for highlights
- **Typography**: Inter font family
- **Spacing**: Consistent 4px grid system
- **Components**: shadcn/ui component library
- **Themes**: Light/dark mode support
- **Accessibility**: WCAG 2.1 AA compliance

### Key Features to Implement
1. **Collections Management**: Create, view, edit collections
2. **Document Upload**: Drag-and-drop file upload with progress
3. **Chat Interface**: Real-time chat with citations
4. **Source Viewer**: PDF viewer with highlighted citations
5. **Connector Setup**: Wizard for external integrations
6. **Admin Dashboard**: System monitoring and management
7. **User Management**: Authentication and role-based access

## BACKEND ARCHITECTURE

### Tech Stack
- **Framework**: FastAPI (async) with dependency injection
- **Language**: Python 3.11+
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Task Queue**: Celery with Redis
- **File Storage**: S3-compatible (MinIO)
- **AI/ML**: LangChain, LangGraph, OpenAI, Anthropic, Cohere
- **Document Processing**: Tesseract (OCR), Pillow, OpenCV
- **Security**: JWT, Pydantic v2, Presidio (PII detection)
- **Monitoring**: structlog, Prometheus, OpenTelemetry

### Project Structure
```
services/api/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── core/             # Core configuration and setup
│   │   ├── config.py     # Settings and environment variables
│   │   ├── database.py   # Database connection and session
│   │   └── logging.py    # Structured logging setup
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── __init__.py   # Model imports
│   │   ├── base.py       # Base model class
│   │   ├── user.py       # User and auth models
│   │   ├── collection.py # Collection models
│   │   ├── document.py   # Document and chunk models
│   │   ├── chat.py       # Chat and citation models
│   │   ├── connector.py  # Connector models
│   │   ├── evaluation.py # Evaluation models
│   │   ├── audit.py      # Audit logging models
│   │   └── system.py     # System monitoring models
│   ├── schemas/          # Pydantic request/response schemas
│   │   ├── __init__.py   # Schema imports
│   │   ├── common.py     # Common schemas
│   │   ├── auth.py       # Authentication schemas
│   │   ├── collection.py # Collection schemas
│   │   ├── document.py   # Document schemas
│   │   ├── chat.py       # Chat schemas
│   │   ├── connector.py  # Connector schemas
│   │   └── evaluation.py # Evaluation schemas
│   ├── services/         # Business logic services
│   │   ├── __init__.py   # Service imports
│   │   ├── auth_service.py      # Authentication service
│   │   ├── collection_service.py # Collection management
│   │   ├── document_service.py  # Document processing
│   │   ├── chat_service.py      # Chat and RAG
│   │   ├── connector_service.py # External integrations
│   │   ├── evaluation_service.py # RAG evaluation
│   │   ├── rag_service.py       # Core RAG logic
│   │   ├── file_service.py      # File storage
│   │   └── embedding_service.py # Vector embeddings
│   └── api/              # API routes
│       └── v1/           # API version 1
│           └── api.py    # Main API router
├── requirements.txt      # Python dependencies
├── alembic.ini          # Database migration config
├── docker-compose.yml   # Local development setup
└── .env.example         # Environment variables template
```

### Core Integrations
- **LLMs**: OpenAI GPT-4 family, Anthropic Claude via LangChain
- **Embeddings**: OpenAI text-embedding-3-large, local E5-large
- **Rerankers**: Cohere, local bge-reranker
- **Storage**: S3/MinIO for blobs, PostgreSQL for metadata, pgvector for embeddings
- **Auth**: JWT sessions, RBAC scoped to collections
- **Connectors**: SharePoint, Google Drive, Box, Confluence, Jira, Slack, IMAP/SMTP
- **Observability**: LangSmith, OpenTelemetry, SIEM export

## DESIGN REQUIREMENTS

### UI/UX Principles
- **Information-first Layout**: Left nav (Collections/Connectors), main chat, right sidebar (Sources/Citations)
- **Visual Trust Cues**: Source logos, timestamps, confidence badges
- **Micro-interactions**: Hover-to-preview citations, click-to-scroll to page spans
- **Responsive Design**: Mobile-first approach with breakpoints
- **Accessibility**: Keyboard navigation, screen reader support, high contrast mode

### Color Tokens
- **Primary**: Blue (#3B82F6) for main actions
- **Success**: Green (#10B981) for positive states
- **Warning**: Yellow (#F59E0B) for caution states
- **Error**: Red (#EF4444) for error states
- **Citation**: Purple (#8B5CF6) for source references
- **Neutral**: Gray scale for text and backgrounds

### Component Guidelines
- Use shadcn/ui components as base
- Maintain consistent spacing (4px grid)
- Implement proper loading states
- Add error boundaries and retry mechanisms
- Support keyboard navigation
- Include proper ARIA labels

## PERFORMANCE BUDGETS

### Frontend
- **Bundle Size**: < 500KB initial load, < 2MB total
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3s
- **Core Web Vitals**: All metrics in "Good" range

### Backend
- **API Response Time**: < 2s P95 for RAG queries
- **Database Queries**: < 100ms P95
- **File Upload**: < 30s for 100MB files
- **Vector Search**: < 500ms P95 for 1M chunks
- **Memory Usage**: < 4GB per service instance

## SECURITY CONSTRAINTS

### Authentication & Authorization
- JWT tokens with short expiration (15min access, 7 days refresh)
- Role-based access control (admin, user, viewer)
- Tenant isolation for multi-tenant deployments
- Row-level security in PostgreSQL

### Data Protection
- PII/PHI detection and redaction pipeline
- Envelope encryption for sensitive data
- Zero-trust architecture with per-tenant KMS keys
- Audit logging for all data access

### API Security
- Rate limiting (100 requests/minute per user)
- Input validation with Pydantic
- CORS configuration for frontend
- HTTPS enforcement in production

## TESTING EXPECTATIONS

### Frontend Testing
- **Unit Tests**: Component testing with Jest + React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: Critical user flows with Playwright
- **Accessibility Tests**: Automated a11y testing
- **Visual Regression**: Component visual testing

### Backend Testing
- **Unit Tests**: Service and utility function testing
- **Integration Tests**: Database and external service integration
- **API Tests**: Endpoint testing with pytest
- **Performance Tests**: Load testing for RAG pipeline
- **Security Tests**: Authentication and authorization testing

### Test Coverage Targets
- **Frontend**: > 80% code coverage
- **Backend**: > 85% code coverage
- **Critical Paths**: 100% test coverage

## CODING CONVENTIONS

### Frontend (TypeScript/React)
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use React Query for server state management
- Implement proper error boundaries
- Follow ESLint and Prettier configurations
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

### Backend (Python/FastAPI)
- Use type hints for all functions
- Follow PEP 8 style guidelines
- Use async/await for I/O operations
- Implement proper error handling
- Use dependency injection for services
- Add docstrings for all public methods
- Use Pydantic for data validation

### Database
- Use UUIDs for primary keys
- Implement soft deletes where appropriate
- Add proper indexes for performance
- Use foreign key constraints
- Implement audit trails for sensitive data

## DEPLOYMENT & INFRASTRUCTURE

### Local Development
- Docker Compose for local services
- Hot reload for both frontend and backend
- Local PostgreSQL with pgvector
- MinIO for S3-compatible storage
- Redis for caching and task queue

### Production Deployment
- Containerized deployment with Docker
- Kubernetes orchestration
- Helm charts for deployment
- CI/CD pipeline with automated testing
- Monitoring with Prometheus and Grafana
- Logging with structured logs

## SUCCESS CRITERIA

### Functional Requirements
- Groundedness >= 0.9 on internal eval set
- Citation coverage >= 95% for factual answers
- Sub-2s P95 retrieval latency on 1M-chunk corpus
- Zero egress of document text in local mode
- Deterministic reruns with same corpus snapshot

### User Experience
- Intuitive document upload and management
- Real-time chat with instant citations
- Responsive design across all devices
- Fast search and retrieval
- Clear visual feedback for all actions

### Technical Requirements
- Scalable architecture supporting 1000+ concurrent users
- 99.9% uptime SLA
- Comprehensive audit logging
- GDPR/CCPA compliance ready
- Air-gap deployment capability

## EDITING BOUNDARIES

### What Claude Can Edit
- Frontend components and pages
- Backend services and API endpoints
- Database models and schemas
- Configuration files
- Documentation and README files
- Test files and test data

### What Claude Cannot Edit
- Environment-specific configuration
- Production secrets and API keys
- Infrastructure as Code (Terraform, Kubernetes)
- Third-party library code
- Generated files (migrations, build artifacts)

### File Naming Conventions
- Use kebab-case for file names
- Use PascalCase for React components
- Use snake_case for Python files
- Use UPPER_CASE for constants
- Use camelCase for JavaScript variables

## AMBIGUITY HANDLING

When faced with ambiguous requirements:
1. **Ask for clarification** on specific requirements
2. **Provide multiple options** with pros/cons
3. **Follow established patterns** in the codebase
4. **Default to security-first** approach
5. **Document decisions** in code comments
6. **Implement with extensibility** in mind

## RESPONSE FORMAT

When implementing features:
1. **Explain the approach** before coding
2. **Show the code** with clear comments
3. **Include error handling** and edge cases
4. **Add tests** for critical functionality
5. **Update documentation** as needed
6. **Consider performance** implications

## EXAMPLES

### Good Implementation
```typescript
// Clear component with proper typing and error handling
interface DocumentUploadProps {
  collectionId: string;
  onUpload: (file: File) => Promise<void>;
  maxSize?: number;
}

export function DocumentUpload({ collectionId, onUpload, maxSize = 10485760 }: DocumentUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    try {
      setIsUploading(true);
      setError(null);
      await onUpload(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Component implementation */}
    </div>
  );
}
```

### Bad Implementation
```typescript
// Poor typing, no error handling, unclear naming
export function Upload({ id, cb, size }: any) {
  const [loading, setLoading] = useState(false);

  const upload = async (f: any) => {
    setLoading(true);
    await cb(f);
    setLoading(false);
  };

  return <div>{/* Implementation */}</div>;
}
```

This prompt declaration provides comprehensive guidance for implementing the Local RAG System with clear boundaries, conventions, and expectations for both frontend and backend development.
