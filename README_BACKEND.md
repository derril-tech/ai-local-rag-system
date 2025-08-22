# AI Local RAG System - Backend API

This is the FastAPI backend service for the AI Local RAG System, providing a comprehensive RESTful API for document processing, RAG functionality, and system management.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Redis 6+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-local-rag-system/services/api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create database
   createdb rag_system
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API documentation**
   Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)

## 🏗️ Architecture

### Tech Stack

- **Framework**: FastAPI with async support
- **Language**: Python 3.11+
- **Database**: PostgreSQL with pgvector
- **ORM**: SQLAlchemy 2.0 with async support
- **Authentication**: JWT with refresh tokens
- **Task Queue**: Celery with Redis
- **File Storage**: S3/MinIO compatible
- **AI Integration**: LangChain + LangGraph
- **Monitoring**: OpenTelemetry + Prometheus

### Project Structure

```
services/api/
├── app/                    # Main application code
│   ├── api/               # API route handlers
│   │   └── v1/           # Version 1 API endpoints
│   ├── core/              # Core application modules
│   │   ├── config.py     # Configuration settings
│   │   ├── database.py   # Database connection
│   │   ├── security.py   # Authentication & authorization
│   │   └── logging.py    # Logging configuration
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic services
│   │   ├── rag/          # RAG pipeline services
│   │   ├── embedding/    # Embedding services
│   │   ├── storage/      # File storage services
│   │   └── connectors/   # Connector services
│   └── utils/             # Utility functions
├── alembic/               # Database migrations
├── tests/                 # Test files
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Environment
ENVIRONMENT=development
DEBUG=true

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/rag_system
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=rag_system
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379

# AI Models
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
COHERE_API_KEY=your-cohere-api-key

# File Storage
STORAGE_TYPE=local
S3_BUCKET_NAME=rag-documents

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
MAX_RETRIEVAL_RESULTS=40
MAX_FINAL_RESULTS=8
```

### Database Setup

1. **Install PostgreSQL with pgvector**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Install pgvector extension
   # Follow instructions at: https://github.com/pgvector/pgvector
   ```

2. **Create database and user**
   ```sql
   CREATE DATABASE rag_system;
   CREATE USER rag_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE rag_system TO rag_user;
   ```

3. **Enable pgvector extension**
   ```sql
   \c rag_system
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

## 📚 API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Collections

- `GET /api/v1/collections` - List collections
- `POST /api/v1/collections` - Create collection
- `GET /api/v1/collections/{id}` - Get collection details
- `PUT /api/v1/collections/{id}` - Update collection
- `DELETE /api/v1/collections/{id}` - Delete collection

### Documents

- `POST /api/v1/collections/{id}/documents` - Upload documents
- `GET /api/v1/collections/{id}/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Chat/RAG

- `POST /api/v1/chat/ask` - Ask questions
- `POST /api/v1/chat/stream` - Stream responses
- `GET /api/v1/chat/sessions` - Chat history

### Connectors

- `GET /api/v1/connectors` - List connectors
- `POST /api/v1/connectors` - Create connector
- `POST /api/v1/connectors/{id}/sync` - Trigger sync

### Admin

- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/users` - User management
- `GET /api/v1/admin/logs` - Audit logs

## 🔄 RAG Pipeline

### Document Processing Flow

1. **Upload**: File validation and storage
2. **Parsing**: Extract text and metadata
3. **Chunking**: Split into manageable chunks
4. **Embedding**: Generate vector embeddings
5. **Indexing**: Store in vector database

### Retrieval Flow

1. **Query Processing**: Parse and enhance user query
2. **Hybrid Search**: BM25 + vector similarity
3. **Reranking**: Improve result relevance
4. **Context Assembly**: Prepare for LLM

### Generation Flow

1. **Prompt Engineering**: Create RAG prompts
2. **LLM Generation**: Generate response
3. **Citation Extraction**: Link to sources
4. **Verification**: Validate response accuracy

## 🔐 Security

### Authentication

- JWT tokens with proper expiration
- Refresh token rotation
- Secure password hashing
- Session management

### Authorization

- Role-based access control (RBAC)
- Collection-level permissions
- Document-level access control
- Admin role management

### Data Protection

- Encrypt sensitive data at rest
- Secure API communication (HTTPS)
- Input validation and sanitization
- SQL injection prevention

## 📊 Performance

### Database Optimization

- Connection pooling
- Proper indexing
- Query optimization
- Database partitioning

### Caching Strategy

- Redis for session storage
- Cache frequently accessed data
- Implement cache invalidation
- Use CDN for static assets

### API Performance

- Implement pagination
- Use async/await properly
- Optimize response serialization
- Add response compression

## 🧪 Testing

### Testing Strategy

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API endpoints
- **Performance Tests**: Load and stress testing
- **Security Tests**: Authentication and authorization

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run performance tests
pytest tests/performance/
```

## 📈 Monitoring

### Logging

- Structured logging with structlog
- Log levels and filtering
- Log aggregation
- Error tracking

### Metrics

- Prometheus metrics
- Custom business metrics
- Performance monitoring
- Health checks

### Tracing

- OpenTelemetry integration
- Request tracing
- Performance profiling
- Distributed tracing

## 🔄 Background Tasks

### Celery Integration

- Document processing tasks
- Embedding generation
- Connector synchronization
- Cleanup tasks

### Task Management

- Task queuing and scheduling
- Error handling and retries
- Progress tracking
- Resource management

## 🌐 External Integrations

### AI Services

- OpenAI API integration
- Anthropic Claude integration
- Local model support
- Embedding service integration

### Storage Services

- S3/MinIO integration
- File upload/download
- Backup and recovery
- Storage optimization

### Connector Services

- SharePoint integration
- Google Drive integration
- Email integration
- Custom connector framework

## 🚀 Deployment

### Docker Deployment

1. **Build image**
   ```bash
   docker build -t rag-api .
   ```

2. **Run container**
   ```bash
   docker run -p 8000:8000 rag-api
   ```

### Production Deployment

1. **Environment setup**
   ```bash
   export ENVIRONMENT=production
   export DEBUG=false
   ```

2. **Database migration**
   ```bash
   alembic upgrade head
   ```

3. **Start application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Kubernetes Deployment

- Use provided Helm charts
- Configure resource limits
- Set up monitoring
- Implement auto-scaling

## 📝 Development

### Code Style

- Follow PEP 8
- Use type hints
- Document functions
- Write clean code

### Code Review

- Peer review process
- Automated checks
- Security review
- Performance review

### Documentation

- API documentation (OpenAPI/Swagger)
- Code documentation
- Architecture documentation
- Deployment guides

## 🔒 Security Best Practices

### Input Validation

- Validate all inputs
- Sanitize user data
- Prevent injection attacks
- Use parameterized queries

### Authentication

- Secure token storage
- Implement proper logout
- Session timeout
- Multi-factor authentication

### Data Protection

- Encrypt sensitive data
- Implement data retention
- Secure data transmission
- Regular security audits

## 🎯 Success Metrics

### Performance

- API response time < 2 seconds
- 99.9% uptime
- Handle 1000+ concurrent users
- Process 100MB+ documents

### Quality

- 90%+ test coverage
- Zero critical security vulnerabilities
- Comprehensive error handling
- Excellent user experience

### Scalability

- Horizontal scaling capability
- Efficient resource usage
- Database optimization
- Caching effectiveness

## 🚨 Common Issues & Solutions

### Database Issues

- **Connection pool exhaustion**: Increase pool size
- **Slow query performance**: Add proper indexes
- **Migration conflicts**: Use Alembic properly
- **Data consistency**: Implement transactions

### API Issues

- **Rate limiting problems**: Configure Redis properly
- **Authentication errors**: Check JWT configuration
- **CORS issues**: Verify CORS settings
- **Response timeouts**: Optimize database queries

### Integration Issues

- **External API failures**: Implement retry logic
- **File upload problems**: Check storage configuration
- **Connector synchronization**: Monitor task queue
- **Embedding generation errors**: Verify AI service keys

## 📚 Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

### Tools

- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryproject.org/)
- [Alembic](https://alembic.sqlalchemy.org/)

### Best Practices

- [Python Best Practices](https://docs.python-guide.org/)
- [API Design Best Practices](https://restfulapi.net/)
- [Security Best Practices](https://owasp.org/)
- [Performance Best Practices](https://fastapi.tiangolo.com/tutorial/performance/)

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Review

- Automated checks (linting, testing)
- Peer review process
- Security review
- Performance review

## 🆘 Support

### Getting Help

1. **Documentation**: Check the docs first
2. **Issues**: Search existing issues
3. **Discussions**: Community discussions
4. **Contact**: Direct support for enterprise

### Common Issues

- **Installation**: Check Python version and dependencies
- **Database**: Verify PostgreSQL and pgvector setup
- **API**: Check environment variables and configuration
- **Performance**: Monitor logs and metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
