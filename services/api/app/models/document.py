# Document models for document processing and storage
# Handles documents, chunks, metadata, and processing information

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, JSON, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

from .base import Base

class DocumentMetadata(Base):
    """Document metadata and extracted information"""
    __tablename__ = "document_metadata"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    author: Mapped[Optional[str]] = mapped_column(String(255))
    subject: Mapped[Optional[str]] = mapped_column(String(500))
    keywords: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    language: Mapped[Optional[str]] = mapped_column(String(10))
    page_count: Mapped[Optional[int]] = mapped_column(Integer)
    extracted_text_length: Mapped[Optional[int]] = mapped_column(Integer)
    ocr_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    tables_extracted: Mapped[int] = mapped_column(Integer, default=0)
    images_extracted: Mapped[int] = mapped_column(Integer, default=0)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="metadata")

class ProcessingStep(Base):
    """Individual processing step information"""
    __tablename__ = "processing_steps"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pending, running, completed, failed
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="processing_steps")

class ProcessingInfo(Base):
    """Document processing information"""
    __tablename__ = "processing_info"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationship
    document: Mapped["Document"] = relationship("Document", back_populates="processing_info")

class CitationSpan(Base):
    """Citation span information for document chunks"""
    __tablename__ = "citation_spans"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_id: Mapped[str] = mapped_column(ForeignKey("document_chunks.id"), nullable=False)
    start: Mapped[int] = mapped_column(Integer, nullable=False)
    end: Mapped[int] = mapped_column(Integer, nullable=False)
    page: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[str]] = mapped_column(String(255))
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    # Relationship
    chunk: Mapped["DocumentChunk"] = relationship("DocumentChunk", back_populates="citation_spans")

class ChunkMetadata(Base):
    """Metadata for document chunks"""
    __tablename__ = "chunk_metadata"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_id: Mapped[str] = mapped_column(ForeignKey("document_chunks.id"), nullable=False)
    heading: Mapped[Optional[str]] = mapped_column(String(500))
    table_data: Mapped[Optional[dict]] = mapped_column(JSON)
    image_caption: Mapped[Optional[str]] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    # Relationship
    chunk: Mapped["DocumentChunk"] = relationship("DocumentChunk", back_populates="metadata")

class DocumentChunk(Base):
    """Document chunk model for RAG processing"""
    __tablename__ = "document_chunks"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    page_number: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[str]] = mapped_column(String(255))
    embeddings: Mapped[Optional[List[float]]] = mapped_column(ARRAY(Float))
    
    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
    metadata: Mapped[Optional[ChunkMetadata]] = relationship("ChunkMetadata", back_populates="chunk", uselist=False)
    citation_spans: Mapped[List[CitationSpan]] = relationship("CitationSpan", back_populates="chunk")
    
    # Citations that reference this chunk
    citations: Mapped[List["Citation"]] = relationship("Citation", back_populates="chunk")

class Document(Base):
    """Document model for file storage and processing"""
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id: Mapped[str] = mapped_column(ForeignKey("collections.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, processing, completed, failed, archived
    checksum: Mapped[Optional[str]] = mapped_column(String(64))  # SHA-256 hash
    uploaded_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    processing_progress: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationships
    collection: Mapped["Collection"] = relationship("Collection", back_populates="documents")
    metadata: Mapped[Optional[DocumentMetadata]] = relationship("DocumentMetadata", back_populates="document", uselist=False)
    processing_info: Mapped[Optional[ProcessingInfo]] = relationship("ProcessingInfo", back_populates="document", uselist=False)
    processing_steps: Mapped[List[ProcessingStep]] = relationship("ProcessingStep", back_populates="document")
    chunks: Mapped[List[DocumentChunk]] = relationship("DocumentChunk", back_populates="document")
    
    # Citations that reference this document
    citations: Mapped[List["Citation"]] = relationship("Citation", back_populates="document")
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"
