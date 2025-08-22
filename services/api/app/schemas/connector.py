# Connector Pydantic schemas
# Schemas for external integrations and connectors

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ConnectorConfig(BaseModel):
    """Connector configuration schema"""
    base_url: Optional[str] = None
    credentials: Dict[str, Any] = Field(default_factory=dict)
    additional_config: Dict[str, Any] = Field(default_factory=dict)

class SyncSettings(BaseModel):
    """Sync settings schema"""
    frequency: str = Field(default="manual", regex="^(manual|hourly|daily|weekly)$")
    incremental_sync: bool = Field(default=True)
    delete_removed_files: bool = Field(default=False)
    max_file_size: int = Field(default=10485760)  # 10MB

class ConnectorFilters(BaseModel):
    """Connector filters schema"""
    include_patterns: Optional[List[str]] = None
    exclude_patterns: Optional[List[str]] = None
    folder_paths: Optional[List[str]] = None
    date_modified_after: Optional[datetime] = None

class ConnectorCreate(BaseModel):
    """Schema for creating a connector"""
    name: str = Field(..., min_length=1, max_length=255)
    connector_type: str = Field(..., regex="^(sharepoint|google_drive|s3|box|confluence|jira|imap|slack)$")
    config: ConnectorConfig
    sync_settings: Optional[SyncSettings] = None
    filters: Optional[ConnectorFilters] = None

class ConnectorUpdate(BaseModel):
    """Schema for updating a connector"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    config: Optional[ConnectorConfig] = None
    status: Optional[str] = Field(None, regex="^(active|inactive|syncing|error)$")
    sync_settings: Optional[SyncSettings] = None
    filters: Optional[ConnectorFilters] = None

class ConnectorStats(BaseModel):
    """Connector statistics"""
    total_files_synced: int
    total_size_bytes: int
    last_sync_duration_ms: int
    errors_count: int
    pending_files: int

class ConnectorResponse(BaseModel):
    """Schema for connector response"""
    id: str
    name: str
    type: str
    status: str
    tenant_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    last_sync: Optional[datetime]
    config: ConnectorConfig
    sync_settings: Optional[SyncSettings]
    filters: Optional[ConnectorFilters]
    stats: ConnectorStats

class ConnectorListResponse(BaseModel):
    """Schema for connector list response"""
    items: List[ConnectorResponse]
    total: int
    page: int
    size: int
