# User models for authentication and user management
# Handles user accounts, preferences, and authentication state

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base

class UserPreferences(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    theme: Mapped[str] = mapped_column(String(20), default="system")  # light, dark, system
    language: Mapped[str] = mapped_column(String(10), default="en")
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    notifications: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="preferences")

class NotificationSettings(Base):
    """User notification preferences"""
    __tablename__ = "notification_settings"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    email: Mapped[bool] = mapped_column(Boolean, default=True)
    push: Mapped[bool] = mapped_column(Boolean, default=True)
    chat_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    ingestion_complete: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="notification_settings")

class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")  # admin, user, viewer
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    preferences: Mapped[Optional[UserPreferences]] = relationship("UserPreferences", back_populates="user", uselist=False)
    notification_settings: Mapped[Optional[NotificationSettings]] = relationship("NotificationSettings", back_populates="user", uselist=False)
    
    # Collections (as owner/editor/viewer)
    owned_collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="owner", foreign_keys="Collection.created_by")
    
    # Chat sessions
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    
    # Connectors
    connectors: Mapped[List["Connector"]] = relationship("Connector", back_populates="created_by_user")
    
    # Evaluations
    evaluations: Mapped[List["Evaluation"]] = relationship("Evaluation", back_populates="created_by_user")
    
    # Audit logs
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
