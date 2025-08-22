# Collection Pydantic schemas
# Schemas for collection management

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class CollectionSettings(BaseModel):
    """Collection settings schema"""
    chunk_size: int = Field(default=1000, ge=100, le=2000)
    chunk_overlap: int = Field(default=150, ge=0, le=500)
    embedding_model: str = Field(default="text-embedding-3-large")
    retrieval_strategy: str = Field(default="hybrid", regex="^(hybrid|semantic|keyword)$")
    reranker_enabled: bool = Field(default=True)
    pii_redaction: bool = Field(default=False)

class RetentionPolicy(BaseModel):
    """Retention policy schema"""
    enabled: bool = Field(default=False)
    days: int = Field(default=0, ge=0)
    action: str = Field(default="delete", regex="^(delete|archive)$")

class CollectionCreate(BaseModel):
    """Schema for creating a collection"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_public: bool = Field(default=False)
    settings: Optional[CollectionSettings] = None
    retention_policy: Optional[RetentionPolicy] = None

class CollectionUpdate(BaseModel):
    """Schema for updating a collection"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_public: Optional[bool] = None
    settings: Optional[CollectionSettings] = None
    retention_policy: Optional[RetentionPolicy] = None

class CollectionStats(BaseModel):
    """Collection statistics"""
    total_documents: int
    total_chunks: int
    total_size_bytes: int
    last_ingestion: Optional[datetime]
    last_query: Optional[datetime]

class CollectionResponse(BaseModel):
    """Schema for collection response"""
    id: str
    name: str
    description: Optional[str]
    tenant_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    is_public: bool
    is_archived: bool
    settings: Optional[CollectionSettings]
    retention_policy: Optional[RetentionPolicy]
    stats: CollectionStats

class CollectionListResponse(BaseModel):
    """Schema for collection list response"""
    items: List[CollectionResponse]
    total: int
    page: int
    size: int
