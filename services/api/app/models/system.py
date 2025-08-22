# System models for system monitoring and metrics
# Handles system status, service health, and performance metrics

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base

class ServiceStatus(Base):
    """Service status and health information"""
    __tablename__ = "service_status"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # healthy, degraded, down
    response_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    error_rate: Mapped[float] = mapped_column(Float, default=0.0)
    last_check: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    details: Mapped[dict] = mapped_column(default=dict)
    
    def __repr__(self) -> str:
        return f"<ServiceStatus(name={self.name}, status={self.status}, response_time={self.response_time_ms}ms)>"

class SystemMetrics(Base):
    """System performance metrics"""
    __tablename__ = "system_metrics"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cpu_usage: Mapped[float] = mapped_column(Float, nullable=False)
    memory_usage: Mapped[float] = mapped_column(Float, nullable=False)
    disk_usage: Mapped[float] = mapped_column(Float, nullable=False)
    active_users: Mapped[int] = mapped_column(Integer, default=0)
    total_queries: Mapped[int] = mapped_column(Integer, default=0)
    average_response_time: Mapped[float] = mapped_column(Float, default=0.0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    uptime_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self) -> str:
        return f"<SystemMetrics(timestamp={self.timestamp}, cpu={self.cpu_usage}%, memory={self.memory_usage}%)>"
