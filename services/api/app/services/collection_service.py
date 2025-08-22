# Collection service
# Handles collection management and operations

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException, status

from app.models.collection import Collection, CollectionSettings, RetentionPolicy
from app.schemas.collection import CollectionCreate, CollectionUpdate

class CollectionService:
    """Service for collection management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_collection(self, collection_data: CollectionCreate, user_id: str) -> Collection:
        """Create a new collection"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create collection
        collection = Collection(
            name=collection_data.name,
            description=collection_data.description,
            owner_id=user_id,
            tenant_id=user.tenant_id,
            is_public=collection_data.is_public,
            settings=collection_data.settings
        )
        
        self.db.add(collection)
        await self.db.commit()
        await self.db.refresh(collection)
        
        return collection
    
    async def get_collection(self, collection_id: str, user_id: str) -> Optional[Collection]:
        """Get collection by ID with permission check"""
        result = await self.db.execute(
            select(Collection).where(Collection.id == collection_id)
        )
        collection = result.scalar_one_or_none()
        
        if not collection:
            return None
        
        # Check permissions
        if not await self.check_collection_permission(collection_id, user_id):
            return None
        
        return collection
    
    async def list_collections(self, user_id: str, skip: int = 0, limit: int = 100) -> tuple[List[Collection], int]:
        """Get collections for user with pagination"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return [], 0
        
        # Get collections for user's tenant
        query = select(Collection).where(Collection.tenant_id == user.tenant_id)
        total_result = await self.db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar() or 0
        
        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        collections = result.scalars().all()
        
        return list(collections), total
    
    async def update_collection(self, collection_id: str, collection_data: CollectionUpdate, user_id: str) -> Optional[Collection]:
        """Update collection"""
        collection = await self.get_collection(collection_id, user_id)
        if not collection:
            return None
        
        # Update fields
        if collection_data.name is not None:
            collection.name = collection_data.name
        if collection_data.description is not None:
            collection.description = collection_data.description
        if collection_data.is_public is not None:
            collection.is_public = collection_data.is_public
        if collection_data.settings is not None:
            collection.settings = collection_data.settings
        
        await self.db.commit()
        await self.db.refresh(collection)
        
        return collection
    
    async def delete_collection(self, collection_id: str, user_id: str) -> bool:
        """Delete collection"""
        collection = await self.get_collection(collection_id, user_id)
        if not collection:
            return False
        
        await self.db.delete(collection)
        await self.db.commit()
        
        return True
    
    async def get_collection_stats(self, collection_id: str, user_id: str) -> Optional[dict]:
        """Get collection statistics"""
        collection = await self.get_collection(collection_id, user_id)
        if not collection:
            return None
        
        # Get document count
        from app.models.document import Document
        doc_result = await self.db.execute(
            select(func.count(Document.id)).where(Document.collection_id == collection_id)
        )
        document_count = doc_result.scalar() or 0
        
        # Get total size
        size_result = await self.db.execute(
            select(func.sum(Document.file_size)).where(Document.collection_id == collection_id)
        )
        total_size = size_result.scalar() or 0
        
        return {
            "collection_id": collection_id,
            "document_count": document_count,
            "total_size": total_size,
            "created_at": collection.created_at.isoformat(),
            "updated_at": collection.updated_at.isoformat()
        }
    
    async def check_collection_permission(self, collection_id: str, user_id: str, required_role: str = "viewer") -> bool:
        """Check if user has permission to access collection"""
        from app.models.user import User
        
        # Get user
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return False
        
        # Get collection
        result = await self.db.execute(select(Collection).where(Collection.id == collection_id))
        collection = result.scalar_one_or_none()
        if not collection:
            return False
        
        # Admin can access everything
        if user.role == "admin":
            return True
        
        # Owner can access their collections
        if collection.owner_id == user_id:
            return True
        
        # Public collections can be accessed by viewers
        if collection.is_public and required_role == "viewer":
            return True
        
        # Check tenant access
        if collection.tenant_id == user.tenant_id:
            return True
        
        return False
