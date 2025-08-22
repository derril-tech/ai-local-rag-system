# AI Local RAG System

A production-grade, on-premises/local-first Retrieval-Augmented Generation (RAG) platform built with modern technologies.

## 🚀 Features

- **Local-First Architecture**: Run entirely on your infrastructure
- **Multi-Modal Document Processing**: Support for PDFs, Word docs, images, and more
- **Advanced RAG Pipeline**: Hybrid search, reranking, and intelligent answer generation
- **Real-Time Chat Interface**: WebSocket-powered conversations with your documents
- **External Connectors**: Integrate with SharePoint, Google Drive, S3, and more
- **Enterprise Security**: Role-based access control, audit logging, PII detection
- **Scalable Architecture**: Microservices with Docker and Kubernetes support

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js 14    │    │   FastAPI       │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   + pgvector    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Redis         │              │
         │              │   Cache/Queue   │              │
         │              └─────────────────┘              │
         │                       │
         │              ┌─────────────────┐
         │              │   MinIO         │
         │              │   Object Store  │
         │              └─────────────────┘
         │
┌─────────────────┐
│   Celery        │
│   Workers       │
└─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **React Query** (TanStack Query)
- **Zustand** (State Management)
- **Tailwind CSS** + **shadcn/ui**
- **TypeScript**
- **Socket.io-client** (WebSockets)

### Backend
- **FastAPI** (Async Python)
- **SQLAlchemy 2.0** (Async ORM)
- **Pydantic v2** (Data Validation)
- **Alembic** (Database Migrations)
- **LangChain** + **LangGraph** (RAG Pipeline)
- **Celery** (Background Tasks)

### Infrastructure
- **PostgreSQL** + **pgvector** (Vector Database)
- **Redis** (Cache & Message Queue)
- **MinIO** (S3-compatible Storage)
- **Docker** + **Docker Compose**
- **Kubernetes** (Production)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-local-rag-system
```

### 2. Start the System
```bash
# Start all services
make up

# Or use Docker Compose directly
docker-compose up -d
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin/minioadmin)

### 4. Create Your First User
```bash
# Access the API container
make shell-api

# Create an admin user
python -c "
from app.models.user import User
from app.core.database import get_db
from app.core.security import get_password_hash
import asyncio

async def create_admin():
    async for db in get_db():
        user = User(
            email='admin@example.com',
            name='Admin User',
            password_hash=get_password_hash('admin123'),
            role='admin',
            tenant_id='default-tenant'
        )
        db.add(user)
        await db.commit()
        break

asyncio.run(create_admin())
"
```

## 📁 Project Structure

```
ai-local-rag-system/
├── apps/
│   └── web/                    # Next.js Frontend
│       ├── app/               # App Router pages
│       ├── components/        # React components
│       ├── lib/              # Utilities and configs
│       └── types/            # TypeScript definitions
├── services/
│   └── api/                  # FastAPI Backend
│       ├── app/
│       │   ├── api/          # API endpoints
│       │   ├── core/         # Core configurations
│       │   ├── models/       # SQLAlchemy models
│       │   ├── schemas/      # Pydantic schemas
│       │   └── services/     # Business logic
│       ├── alembic/          # Database migrations
│       └── tests/            # Backend tests
├── docs/                     # Documentation
├── docker-compose.yml        # Service orchestration
├── Makefile                  # Development commands
└── README.md                 # This file
```

## 🔧 Development

### Available Commands
```bash
# See all available commands
make help

# Install dependencies
make install

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
```

### Local Development
```bash
# Backend development
cd services/api
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd apps/web
npm install
npm run dev
```

## 🔐 Security Features

- **JWT Authentication** with refresh tokens
- **Role-Based Access Control** (Admin, User, Viewer)
- **PII/PHI Detection** and anonymization
- **Audit Logging** for all operations
- **Rate Limiting** and request validation
- **Secure File Upload** with virus scanning

## 📊 Monitoring & Observability

- **Health Checks** for all services
- **Structured Logging** with structlog
- **Metrics Collection** with Prometheus
- **Distributed Tracing** with OpenTelemetry
- **Performance Monitoring** and alerting

## 🚀 Deployment

### Docker Compose (Development)
```bash
docker-compose up -d
```

### Kubernetes (Production)
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Or use Helm
helm install rag-system ./helm/
```

### Environment Variables
See `services/api/env.example` and `apps/web/env.example` for required environment variables.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🔮 Roadmap

- [ ] Advanced RAG evaluation tools
- [ ] Multi-tenant support
- [ ] Real-time collaboration
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Custom model fine-tuning
- [ ] Enterprise SSO integration