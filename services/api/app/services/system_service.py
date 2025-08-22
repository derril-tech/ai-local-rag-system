# System service for monitoring and administration
# Handles system status, metrics, and admin operations

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.models.user import User
from app.models.audit import AuditLog
from app.models.system import ServiceStatus, SystemMetrics

class SystemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        # Get basic system metrics
        total_users = await self._get_total_users()
        total_documents = await self._get_total_documents()
        active_sessions = await self._get_active_sessions()
        
        # Get service health
        services = await self.get_service_status()
        
        return {
            "status": "healthy" if all(s["status"] == "healthy" for s in services) else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_users": total_users,
                "total_documents": total_documents,
                "active_sessions": active_sessions
            },
            "services": services
        }

    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        # Get recent metrics from database
        result = await self.db.execute(
            select(SystemMetrics)
            .order_by(SystemMetrics.timestamp.desc())
            .limit(100)
        )
        metrics = result.scalars().all()
        
        if not metrics:
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "disk_usage": 0.0,
                "active_connections": 0,
                "query_latency_ms": 0.0
            }
        
        latest = metrics[0]
        return {
            "cpu_usage": latest.cpu_usage,
            "memory_usage": latest.memory_usage,
            "disk_usage": latest.disk_usage,
            "active_connections": latest.active_connections,
            "query_latency_ms": latest.query_latency_ms,
            "timestamp": latest.timestamp.isoformat()
        }

    async def get_service_status(self) -> List[Dict[str, Any]]:
        """Get status of all system services"""
        result = await self.db.execute(
            select(ServiceStatus)
            .order_by(ServiceStatus.name)
        )
        services = result.scalars().all()
        
        if not services:
            # Return default service statuses
            return [
                {
                    "name": "database",
                    "status": "healthy",
                    "response_time_ms": 10,
                    "last_check": datetime.utcnow().isoformat()
                },
                {
                    "name": "vector_store",
                    "status": "healthy",
                    "response_time_ms": 50,
                    "last_check": datetime.utcnow().isoformat()
                },
                {
                    "name": "redis",
                    "status": "healthy",
                    "response_time_ms": 5,
                    "last_check": datetime.utcnow().isoformat()
                }
            ]
        
        return [
            {
                "name": service.name,
                "status": service.status,
                "response_time_ms": service.response_time_ms,
                "error_rate": service.error_rate,
                "last_check": service.last_check.isoformat(),
                "details": service.details
            }
            for service in services
        ]

    async def get_audit_logs(
        self, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get system audit logs"""
        query = select(AuditLog)
        
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if action:
            query = query.where(AuditLog.action == action)
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        
        query = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        logs = result.scalars().all()
        
        return [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "timestamp": log.timestamp.isoformat(),
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "session_id": log.session_id,
                "tenant_id": log.tenant_id,
                "details": log.details,
                "severity": log.severity,
                "success": log.success
            }
            for log in logs
        ]

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List all users (admin only)"""
        result = await self.db.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()
        
        return [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "tenant_id": user.tenant_id,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "is_active": user.is_active
            }
            for user in users
        ]

    async def _get_total_users(self) -> int:
        """Get total number of users"""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar() or 0

    async def _get_total_documents(self) -> int:
        """Get total number of documents"""
        from app.models.document import Document
        result = await self.db.execute(select(func.count(Document.id)))
        return result.scalar() or 0

    async def _get_active_sessions(self) -> int:
        """Get number of active chat sessions"""
        from app.models.chat import ChatSession
        result = await self.db.execute(
            select(func.count(ChatSession.id))
            .where(ChatSession.updated_at >= datetime.utcnow() - timedelta(hours=1))
        )
        return result.scalar() or 0
