# Collection models for document organization
# Handles collections, settings, permissions, and retention policies

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base

class CollectionSettings(Base):
    """Collection configuration and settings"""
    __tablename__ = "collection_settings"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id: Mapped[str] = mapped_column(ForeignKey("collections.id"), nullable=False)
    chunk_size: Mapped[int] = mapped_column(Integer, default=1000)
    chunk_overlap: Mapped[int] = mapped_column(Integer, default=150)
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-large")
    retrieval_strategy: Mapped[str] = mapped_column(String(20), default="hybrid")  # hybrid, semantic, keyword
    reranker_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    pii_redaction: Mapped[bool] = mapped_column(Boolean, default=False)
    retention_policy: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    collection: Mapped["Collection"] = relationship("Collection", back_populates="settings")

class RetentionPolicy(Base):
    """Document retention policy settings"""
    __tablename__ = "retention_policies"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id: Mapped[str] = mapped_column(ForeignKey("collections.id"), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    days: Mapped[int] = mapped_column(Integer, default=0)
    action: Mapped[str] = mapped_column(String(20), default="delete")  # delete, archive
    
    # Relationship
    collection: Mapped["Collection"] = relationship("Collection", back_populates="retention_policy")

class CollectionPermissions(Base):
    """User permissions for collections"""
    __tablename__ = "collection_permissions"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id: Mapped[str] = mapped_column(ForeignKey("collections.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # owner, editor, viewer
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    granted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    collection: Mapped["Collection"] = relationship("Collection", back_populates="permissions")
    user: Mapped["User"] = relationship("User")
    granted_by_user: Mapped["User"] = relationship("User", foreign_keys=[granted_by])

class Collection(Base):
    """Document collection model"""
    __tablename__ = "collections"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Statistics (cached for performance)
    total_documents: Mapped[int] = mapped_column(Integer, default=0)
    total_chunks: Mapped[int] = mapped_column(Integer, default=0)
    total_size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    last_ingestion: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_query: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="owned_collections", foreign_keys=[owner_id])
    settings: Mapped[Optional[CollectionSettings]] = relationship("CollectionSettings", back_populates="collection", uselist=False)
    retention_policy: Mapped[Optional[RetentionPolicy]] = relationship("RetentionPolicy", back_populates="collection", uselist=False)
    permissions: Mapped[List[CollectionPermissions]] = relationship("CollectionPermissions", back_populates="collection")
    
    # Documents in this collection
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="collection")
    
    # Chat sessions for this collection
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="collection")
    
    # Evaluations for this collection
    evaluations: Mapped[List["Evaluation"]] = relationship("Evaluation", back_populates="collection")
    
    def __repr__(self) -> str:
        return f"<Collection(id={self.id}, name={self.name}, tenant_id={self.tenant_id})>"
