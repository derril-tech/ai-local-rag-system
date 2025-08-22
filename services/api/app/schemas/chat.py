# Chat Pydantic schemas
# Schemas for chat sessions and RAG interactions

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ChatSettings(BaseModel):
    """Chat session settings"""
    model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    retrieval_strategy: str = Field(default="hybrid", regex="^(hybrid|semantic|keyword)$")
    reranker_enabled: bool = Field(default=True)
    citation_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    max_sources: int = Field(default=5, ge=1, le=20)

class Citation(BaseModel):
    """Citation schema"""
    id: str
    document_id: str
    document_name: str
    chunk_id: str
    content: str
    page_number: Optional[int]
    confidence_score: float
    span_start: int
    span_end: int

class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    session_id: str = Field(..., description="Chat session ID")
    content: str = Field(..., min_length=1, description="Message content")
    role: str = Field(default="user", regex="^(user|assistant|system)$")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Message metadata")

class ChatSessionCreate(BaseModel):
    """Schema for creating a chat session"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    collection_ids: Optional[List[str]] = Field(None, description="Collection IDs")
    settings: Optional[ChatSettings] = None

class QueryRequest(BaseModel):
    """Schema for RAG query request"""
    query: str = Field(..., min_length=1, description="Query text")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    collection_ids: Optional[List[str]] = Field(None, description="Collection IDs")
    settings: Optional[ChatSettings] = None
    filters: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    """Schema for RAG query response"""
    answer: str
    citations: List[Citation]
    confidence_score: float
    groundedness_score: float
    processing_time_ms: int
    tokens_used: int
    sources_retrieved: int
    session_id: str
    message_id: str

class ChatResponse(BaseModel):
    """Schema for chat response"""
    id: str
    title: str
    collection_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    settings: Optional[ChatSettings]
    message_count: int
