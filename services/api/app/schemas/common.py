# Common Pydantic schemas
# Shared schemas used across multiple endpoints

from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(default=None, description="Sort field")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$", description="Sort order")
    
    @property
    def skip(self) -> int:
        """Calculate skip value for database queries"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Get limit value for database queries"""
        return self.size

class PaginationInfo(BaseModel):
    """Pagination information in responses"""
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

class ErrorResponse(BaseModel):
    """Standard error response format"""
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseModel):
    """Standard success response format"""
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    services: Dict[str, str]

class SystemStatus(BaseModel):
    """System status information"""
    status: str
    services: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    last_updated: datetime
