# Document service
# Handles document management and processing

from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from fastapi import UploadFile
import uuid

from app.models.document import Document
from app.schemas.document import DocumentCreate

class DocumentService:
    """Service for document management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_document(self, document_data: DocumentCreate, user_id: str) -> Document:
        """Create a new document"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create document
        document = Document(
            filename=document_data.filename,
            collection_id=document_data.collection_id,
            uploaded_by=user_id,
            tenant_id=user.tenant_id,
            file_size=0,  # Will be updated after file upload
            status="pending"
        )
        
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        
        return document
    
    async def get_document(self, document_id: str, user_id: str) -> Optional[Document]:
        """Get document by ID"""
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()
        
        if not document:
            return None
        
        # Check permissions (simplified - in real app, check collection permissions)
        from app.models.user import User
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        
        if not user or document.tenant_id != user.tenant_id:
            return None
        
        return document
    
    async def list_documents(
        self, 
        user_id: str, 
        collection_id: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> Tuple[List[Document], int]:
        """Get documents with pagination"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return [], 0
        
        # Build query
        query = select(Document).where(Document.tenant_id == user.tenant_id)
        if collection_id:
            query = query.where(Document.collection_id == collection_id)
        
        # Get total count
        total_result = await self.db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar() or 0
        
        # Get documents
        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        documents = result.scalars().all()
        
        return list(documents), total
    
    async def delete_document(self, document_id: str, user_id: str) -> bool:
        """Delete document"""
        document = await self.get_document(document_id, user_id)
        if not document:
            return False
        
        await self.db.delete(document)
        await self.db.commit()
        
        return True
    
    async def process_document(self, document_id: str, file: UploadFile) -> None:
        """Process document asynchronously"""
        # This would typically be handled by a background task
        # For now, just update the status
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        document = result.scalar_one_or_none()
        
        if document:
            document.status = "processing"
            document.file_size = len(await file.read())
            await self.db.commit()
    
    async def get_document_content(self, document_id: str, user_id: str) -> Optional[dict]:
        """Get document content and chunks"""
        document = await self.get_document(document_id, user_id)
        if not document:
            return None
        
        # Get document chunks
        from app.models.document import DocumentChunk
        result = await self.db.execute(
            select(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )
        chunks = result.scalars().all()
        
        return {
            "document": document,
            "chunks": [chunk.to_dict() for chunk in chunks]
        }
    
    async def reprocess_document(self, document_id: str, user_id: str) -> bool:
        """Reprocess a document"""
        document = await self.get_document(document_id, user_id)
        if not document:
            return False
        
        document.status = "processing"
        await self.db.commit()
        
        return True
    
    async def get_document_status(self, document_id: str, user_id: str) -> Optional[dict]:
        """Get document processing status"""
        document = await self.get_document(document_id, user_id)
        if not document:
            return None
        
        return {
            "id": document.id,
            "status": document.status,
            "progress": document.processing_progress or 0,
            "error_message": document.error_message
        }
