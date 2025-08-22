# Connector service
# Handles external integrations and connectors

from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
import uuid

from app.models.connector import Connector
from app.schemas.connector import ConnectorCreate, ConnectorUpdate

class ConnectorService:
    """Service for external integrations and connectors"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_connector(self, connector_data: ConnectorCreate, user_id: str) -> Connector:
        """Create a new connector"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create connector
        connector = Connector(
            name=connector_data.name,
            connector_type=connector_data.connector_type,
            config=connector_data.config,
            owner_id=user_id,
            tenant_id=user.tenant_id,
            status="inactive"
        )
        
        self.db.add(connector)
        await self.db.commit()
        await self.db.refresh(connector)
        
        return connector
    
    async def get_connector(self, connector_id: str, user_id: str) -> Optional[Connector]:
        """Get connector by ID"""
        result = await self.db.execute(
            select(Connector).where(Connector.id == connector_id)
        )
        connector = result.scalar_one_or_none()
        
        if not connector:
            return None
        
        # Check permissions
        from app.models.user import User
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        
        if not user or connector.tenant_id != user.tenant_id:
            return None
        
        return connector
    
    async def list_connectors(self, user_id: str, skip: int = 0, limit: int = 100) -> Tuple[List[Connector], int]:
        """Get connectors for user with pagination"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return [], 0
        
        # Get connectors for user's tenant
        query = select(Connector).where(Connector.tenant_id == user.tenant_id)
        total_result = await self.db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar() or 0
        
        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        connectors = result.scalars().all()
        
        return list(connectors), total
    
    async def update_connector(self, connector_id: str, connector_data: ConnectorUpdate, user_id: str) -> Optional[Connector]:
        """Update connector"""
        connector = await self.get_connector(connector_id, user_id)
        if not connector:
            return None
        
        # Update fields
        if connector_data.name is not None:
            connector.name = connector_data.name
        if connector_data.config is not None:
            connector.config = connector_data.config
        if connector_data.status is not None:
            connector.status = connector_data.status
        
        await self.db.commit()
        await self.db.refresh(connector)
        
        return connector
    
    async def delete_connector(self, connector_id: str, user_id: str) -> bool:
        """Delete connector"""
        connector = await self.get_connector(connector_id, user_id)
        if not connector:
            return False
        
        await self.db.delete(connector)
        await self.db.commit()
        
        return True
    
    async def sync_connector(self, connector_id: str, user_id: str) -> bool:
        """Trigger a sync for a connector"""
        connector = await self.get_connector(connector_id, user_id)
        if not connector:
            return False
        
        # Update status to syncing
        connector.status = "syncing"
        await self.db.commit()
        
        # In a real implementation, this would trigger a background task
        # For now, just return success
        
        return True
    
    async def get_connector_status(self, connector_id: str, user_id: str) -> Optional[dict]:
        """Get connector sync status"""
        connector = await self.get_connector(connector_id, user_id)
        if not connector:
            return None
        
        return {
            "id": connector.id,
            "status": connector.status,
            "last_sync": connector.last_sync.isoformat() if connector.last_sync else None,
            "sync_interval": connector.sync_interval,
            "error_message": connector.error_message
        }
    
    async def get_connector_logs(
        self, 
        connector_id: str, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """Get connector sync logs"""
        connector = await self.get_connector(connector_id, user_id)
        if not connector:
            return []
        
        # In a real implementation, this would query a logs table
        # For now, return empty list
        return []
