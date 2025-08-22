# Chat models for RAG interactions and chat sessions
# Handles chat sessions, messages, citations, and metadata

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, JSON, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

from .base import Base

class HighlightSpan(Base):
    """Highlight span information for citations"""
    __tablename__ = "highlight_spans"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    citation_id: Mapped[str] = mapped_column(ForeignKey("citations.id"), nullable=False)
    start: Mapped[int] = mapped_column(Integer, nullable=False)
    end: Mapped[int] = mapped_column(Integer, nullable=False)
    page: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Relationship
    citation: Mapped["Citation"] = relationship("Citation", back_populates="highlight_spans")

class Citation(Base):
    """Citation model for source references"""
    __tablename__ = "citations"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id: Mapped[str] = mapped_column(ForeignKey("chat_messages.id"), nullable=False)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)
    chunk_id: Mapped[str] = mapped_column(ForeignKey("document_chunks.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_number: Mapped[Optional[int]] = mapped_column(Integer)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    span_start: Mapped[int] = mapped_column(Integer, nullable=False)
    span_end: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    message: Mapped["ChatMessage"] = relationship("ChatMessage", back_populates="citations")
    document: Mapped["Document"] = relationship("Document", back_populates="citations")
    chunk: Mapped["DocumentChunk"] = relationship("DocumentChunk", back_populates="citations")
    highlight_spans: Mapped[List[HighlightSpan]] = relationship("HighlightSpan", back_populates="citation")

class MessageMetadata(Base):
    """Metadata for chat messages"""
    __tablename__ = "message_metadata"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id: Mapped[str] = mapped_column(ForeignKey("chat_messages.id"), nullable=False)
    model_used: Mapped[Optional[str]] = mapped_column(String(100))
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float)
    groundedness_score: Mapped[Optional[float]] = mapped_column(Float)
    sources_retrieved: Mapped[Optional[int]] = mapped_column(Integer)
    query_type: Mapped[Optional[str]] = mapped_column(String(20))  # factual, analytical, creative
    
    # Relationship
    message: Mapped["ChatMessage"] = relationship("ChatMessage", back_populates="metadata")

class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(ForeignKey("chat_sessions.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")
    citations: Mapped[List[Citation]] = relationship("Citation", back_populates="message")
    metadata: Mapped[Optional[MessageMetadata]] = relationship("MessageMetadata", back_populates="message", uselist=False)

class ChatSettings(Base):
    """Chat session settings"""
    __tablename__ = "chat_settings"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(ForeignKey("chat_sessions.id"), nullable=False)
    model: Mapped[str] = mapped_column(String(100), default="gpt-4")
    temperature: Mapped[float] = mapped_column(Float, default=0.3)
    max_tokens: Mapped[int] = mapped_column(Integer, default=1000)
    retrieval_strategy: Mapped[str] = mapped_column(String(20), default="hybrid")  # hybrid, semantic, keyword
    reranker_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    citation_threshold: Mapped[float] = mapped_column(Float, default=0.8)
    max_sources: Mapped[int] = mapped_column(Integer, default=5)
    
    # Relationship
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="settings")

class ChatSession(Base):
    """Chat session model"""
    __tablename__ = "chat_sessions"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    collection_ids: Mapped[List[str]] = mapped_column(ARRAY(String), default=list)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    messages: Mapped[List[ChatMessage]] = relationship("ChatMessage", back_populates="session")
    
    def __repr__(self) -> str:
        return f"<ChatSession(id={self.id}, title={self.title}, user_id={self.user_id})>"
