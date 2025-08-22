# Connectors API endpoints
# Handles external data source integrations

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.connector import ConnectorCreate, ConnectorUpdate, ConnectorResponse, ConnectorListResponse
from app.schemas.common import PaginationParams
from app.services.connector_service import ConnectorService

router = APIRouter(prefix="/connectors", tags=["Connectors"])

@router.post("/", response_model=ConnectorResponse, status_code=status.HTTP_201_CREATED)
async def create_connector(
    connector_data: ConnectorCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new connector"""
    connector_service = ConnectorService(db)
    connector = await connector_service.create_connector(connector_data, current_user.id)
    return connector

@router.get("/", response_model=ConnectorListResponse)
async def list_connectors(
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all connectors for the current user"""
    connector_service = ConnectorService(db)
    connectors, total = await connector_service.list_connectors(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return {
        "items": connectors,
        "total": total,
        "page": pagination.page,
        "size": pagination.size
    }

@router.get("/{connector_id}", response_model=ConnectorResponse)
async def get_connector(
    connector_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific connector by ID"""
    connector_service = ConnectorService(db)
    connector = await connector_service.get_connector(connector_id, current_user.id)
    if not connector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    return connector

@router.put("/{connector_id}", response_model=ConnectorResponse)
async def update_connector(
    connector_id: str,
    connector_data: ConnectorUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a connector"""
    connector_service = ConnectorService(db)
    connector = await connector_service.update_connector(
        connector_id, connector_data, current_user.id
    )
    if not connector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    return connector

@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(
    connector_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Delete a connector"""
    connector_service = ConnectorService(db)
    success = await connector_service.delete_connector(connector_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )

@router.post("/{connector_id}/sync")
async def sync_connector(
    connector_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Trigger a sync for a connector"""
    connector_service = ConnectorService(db)
    success = await connector_service.sync_connector(connector_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    return {"message": "Sync started successfully"}

@router.get("/{connector_id}/status")
async def get_connector_status(
    connector_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get connector sync status"""
    connector_service = ConnectorService(db)
    status = await connector_service.get_connector_status(connector_id, current_user.id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    return status

@router.get("/{connector_id}/logs")
async def get_connector_logs(
    connector_id: str,
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get connector sync logs"""
    connector_service = ConnectorService(db)
    logs = await connector_service.get_connector_logs(
        connector_id, current_user.id, pagination.skip, pagination.limit
    )
    return logs
