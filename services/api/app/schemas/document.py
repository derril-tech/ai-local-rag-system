# Document Pydantic schemas
# Schemas for document management and processing

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class DocumentMetadata(BaseModel):
    """Document metadata schema"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[List[str]] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    extracted_text_length: Optional[int] = None
    ocr_applied: bool = False
    tables_extracted: int = 0
    images_extracted: int = 0
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

class DocumentCreate(BaseModel):
    """Schema for creating a document"""
    filename: str = Field(..., description="Original filename")
    collection_id: str = Field(..., description="Collection ID")
    metadata: Optional[str] = Field("{}", description="JSON string of metadata")

class DocumentUpload(BaseModel):
    """Schema for document upload"""
    collection_id: str = Field(..., description="Collection ID")
    file: bytes = Field(..., description="File content")
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type")

class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: str
    collection_id: str
    name: str
    file_path: str
    file_size: int
    mime_type: str
    status: str
    checksum: Optional[str]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[DocumentMetadata]

class DocumentListResponse(BaseModel):
    """Schema for document list response"""
    items: List[DocumentResponse]
    total: int
    page: int
    size: int
