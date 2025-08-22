# Collections API endpoints
# Handles collection CRUD operations and management

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionListResponse
from app.schemas.common import PaginationParams
from app.services.collection_service import CollectionService

router = APIRouter(prefix="/collections", tags=["Collections"])

@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection_data: CollectionCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new collection"""
    collection_service = CollectionService(db)
    collection = await collection_service.create_collection(collection_data, current_user.id)
    return collection

@router.get("/", response_model=CollectionListResponse)
async def list_collections(
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all collections for the current user"""
    collection_service = CollectionService(db)
    collections, total = await collection_service.list_collections(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return {
        "items": collections,
        "total": total,
        "page": pagination.page,
        "size": pagination.size
    }

@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific collection by ID"""
    collection_service = CollectionService(db)
    collection = await collection_service.get_collection(collection_id, current_user.id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    return collection

@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: str,
    collection_data: CollectionUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a collection"""
    collection_service = CollectionService(db)
    collection = await collection_service.update_collection(
        collection_id, collection_data, current_user.id
    )
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    return collection

@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Delete a collection"""
    collection_service = CollectionService(db)
    success = await collection_service.delete_collection(collection_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )

@router.get("/{collection_id}/stats")
async def get_collection_stats(
    collection_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get collection statistics"""
    collection_service = CollectionService(db)
    stats = await collection_service.get_collection_stats(collection_id, current_user.id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    return stats
