# Connector models for external integrations
# Handles connectors, sync settings, and filters

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

from .base import Base

class ConnectorFilters(Base):
    """Connector filter settings"""
    __tablename__ = "connector_filters"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    connector_id: Mapped[str] = mapped_column(ForeignKey("connectors.id"), nullable=False)
    include_patterns: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    exclude_patterns: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    folder_paths: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    date_modified_after: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationship
    connector: Mapped["Connector"] = relationship("Connector", back_populates="filters")

class SyncSettings(Base):
    """Connector sync settings"""
    __tablename__ = "sync_settings"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    connector_id: Mapped[str] = mapped_column(ForeignKey("connectors.id"), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), default="manual")  # manual, hourly, daily, weekly
    last_sync: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_sync: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    incremental_sync: Mapped[bool] = mapped_column(Boolean, default=True)
    delete_removed_files: Mapped[bool] = mapped_column(Boolean, default=False)
    max_file_size: Mapped[int] = mapped_column(Integer, default=10485760)  # 10MB
    
    # Relationship
    connector: Mapped["Connector"] = relationship("Connector", back_populates="sync_settings")

class ConnectorConfig(Base):
    """Connector configuration"""
    __tablename__ = "connector_configs"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    connector_id: Mapped[str] = mapped_column(ForeignKey("connectors.id"), nullable=False)
    base_url: Mapped[Optional[str]] = mapped_column(String(500))
    credentials: Mapped[dict] = mapped_column(JSON, default=dict)
    additional_config: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    connector: Mapped["Connector"] = relationship("Connector", back_populates="config")

class Connector(Base):
    """Connector model for external integrations"""
    __tablename__ = "connectors"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    connector_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sharepoint, google_drive, s3, box, confluence, jira, imap, slack
    status: Mapped[str] = mapped_column(String(20), default="inactive")  # active, inactive, error, syncing
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    last_sync: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Statistics (cached for performance)
    total_files_synced: Mapped[int] = mapped_column(Integer, default=0)
    total_size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    last_sync_duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    errors_count: Mapped[int] = mapped_column(Integer, default=0)
    pending_files: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    created_by_user: Mapped["User"] = relationship("User", back_populates="connectors", foreign_keys=[owner_id])
    config: Mapped[Optional[ConnectorConfig]] = relationship("ConnectorConfig", back_populates="connector", uselist=False)
    sync_settings: Mapped[Optional[SyncSettings]] = relationship("SyncSettings", back_populates="connector", uselist=False)
    filters: Mapped[Optional[ConnectorFilters]] = relationship("ConnectorFilters", back_populates="connector", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Connector(id={self.id}, name={self.name}, type={self.type}, status={self.status})>"
