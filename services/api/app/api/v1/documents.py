# Documents API endpoints
# Handles document upload, processing, and management

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentListResponse
from app.schemas.common import PaginationParams
from app.services.document_service import DocumentService
from app.services.file_service import FileService

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    collection_id: str = Form(...),
    metadata: str = Form("{}"),  # JSON string
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Upload and process a new document"""
    document_service = DocumentService(db)
    file_service = FileService()
    
    # Validate file
    if not file_service.is_supported_file_type(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type"
        )
    
    # Create document record
    document_data = DocumentCreate(
        filename=file.filename,
        collection_id=collection_id,
        metadata=metadata
    )
    
    document = await document_service.create_document(document_data, current_user.id)
    
    # Process document asynchronously
    await document_service.process_document(document.id, file)
    
    return document

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    collection_id: str = None,
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List documents with optional collection filter"""
    document_service = DocumentService(db)
    documents, total = await document_service.list_documents(
        user_id=current_user.id,
        collection_id=collection_id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return {
        "items": documents,
        "total": total,
        "page": pagination.page,
        "size": pagination.size
    }

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific document by ID"""
    document_service = DocumentService(db)
    document = await document_service.get_document(document_id, current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Delete a document"""
    document_service = DocumentService(db)
    success = await document_service.delete_document(document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

@router.get("/{document_id}/content")
async def get_document_content(
    document_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get document content and chunks"""
    document_service = DocumentService(db)
    content = await document_service.get_document_content(document_id, current_user.id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return content

@router.post("/{document_id}/reprocess")
async def reprocess_document(
    document_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Reprocess a document"""
    document_service = DocumentService(db)
    success = await document_service.reprocess_document(document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return {"message": "Document reprocessing started"}

@router.get("/{document_id}/status")
async def get_document_status(
    document_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get document processing status"""
    document_service = DocumentService(db)
    status = await document_service.get_document_status(document_id, current_user.id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return status
