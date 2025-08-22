"""
Configuration settings for AI Local RAG System
"""
from typing import List, Optional
from pydantic import BaseSettings, Field, validator
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Local RAG System"
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    ALGORITHM: str = "HS256"
    
    # CORS and Hosts
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    POSTGRES_SERVER: str = Field(default="localhost", env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="rag_system", env="POSTGRES_DB")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # File Storage (S3/MinIO)
    STORAGE_TYPE: str = Field(default="local", env="STORAGE_TYPE")  # local, s3, minio
    S3_ENDPOINT_URL: Optional[str] = Field(default=None, env="S3_ENDPOINT_URL")
    S3_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="S3_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME: str = Field(default="rag-documents", env="S3_BUCKET_NAME")
    S3_REGION: str = Field(default="us-east-1", env="S3_REGION")
    
    # AI Models
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    COHERE_API_KEY: Optional[str] = Field(default=None, env="COHERE_API_KEY")
    
    # Model Configuration
    DEFAULT_LLM_PROVIDER: str = Field(default="openai", env="DEFAULT_LLM_PROVIDER")
    DEFAULT_EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", env="DEFAULT_EMBEDDING_MODEL")
    DEFAULT_RERANKER_MODEL: str = Field(default="rerank-english-v2.0", env="DEFAULT_RERANKER_MODEL")
    
    # Local Models (for air-gapped mode)
    USE_LOCAL_MODELS: bool = Field(default=False, env="USE_LOCAL_MODELS")
    LOCAL_LLM_PATH: Optional[str] = Field(default=None, env="LOCAL_LLM_PATH")
    LOCAL_EMBEDDING_PATH: Optional[str] = Field(default=None, env="LOCAL_EMBEDDING_PATH")
    
    # RAG Configuration
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=150, env="CHUNK_OVERLAP")
    MAX_RETRIEVAL_RESULTS: int = Field(default=40, env="MAX_RETRIEVAL_RESULTS")
    MAX_FINAL_RESULTS: int = Field(default=8, env="MAX_FINAL_RESULTS")
    
    # Security and Compliance
    ENABLE_PII_DETECTION: bool = Field(default=True, env="ENABLE_PII_DETECTION")
    ENABLE_REDACTION: bool = Field(default=False, env="ENABLE_REDACTION")
    AUDIT_LOG_ENABLED: bool = Field(default=True, env="AUDIT_LOG_ENABLED")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    ENABLE_TRACING: bool = Field(default=True, env="ENABLE_TRACING")
    LANGSMITH_API_KEY: Optional[str] = Field(default=None, env="LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: Optional[str] = Field(default=None, env="LANGSMITH_PROJECT")
    
    # File Upload Limits
    MAX_FILE_SIZE: int = Field(default=100 * 1024 * 1024, env="MAX_FILE_SIZE")  # 100MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[".pdf", ".docx", ".doc", ".txt", ".csv", ".xlsx", ".xls", ".html", ".eml"],
        env="ALLOWED_FILE_TYPES"
    )
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        """Assemble database URL from components if not provided"""
        if isinstance(v, str):
            return v
        
        return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from comma-separated string"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_TYPES", pre=True)
    def parse_file_types(cls, v):
        """Parse allowed file types from comma-separated string"""
        if isinstance(v, str):
            return [ftype.strip() for ftype in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Validate critical settings
def validate_settings():
    """Validate critical settings are present"""
    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY must be set")
    
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL must be set")
    
    if settings.USE_LOCAL_MODELS and not settings.LOCAL_LLM_PATH:
        raise ValueError("LOCAL_LLM_PATH must be set when USE_LOCAL_MODELS is True")
    
    # Validate at least one AI provider is configured
    if not any([
        settings.OPENAI_API_KEY,
        settings.ANTHROPIC_API_KEY,
        settings.USE_LOCAL_MODELS
    ]):
        raise ValueError("At least one AI provider must be configured (OpenAI, Anthropic, or Local Models)")

# Validate settings on import
validate_settings()
