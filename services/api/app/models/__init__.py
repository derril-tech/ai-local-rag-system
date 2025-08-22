# Database models package
# This package contains all SQLAlchemy ORM models for the RAG system

from .base import Base
from .user import User, UserPreferences, NotificationSettings
from .collection import Collection, CollectionSettings, CollectionPermissions, RetentionPolicy
from .document import Document, DocumentMetadata, DocumentChunk, ChunkMetadata, CitationSpan, ProcessingInfo, ProcessingStep
from .chat import ChatSession, ChatMessage, Citation, HighlightSpan, MessageMetadata, ChatSettings
from .connector import Connector, ConnectorConfig, SyncSettings, ConnectorFilters
from .evaluation import Evaluation, EvaluationSettings, EvaluationMetric, TestQuery, ModelConfig, EvaluationResults, MetricResult, QueryResult, EvaluationSummary
from .audit import AuditLog
from .system import SystemMetrics, ServiceStatus

__all__ = [
    # Base
    'Base',
    
    # User models
    'User',
    'UserPreferences', 
    'NotificationSettings',
    
    # Collection models
    'Collection',
    'CollectionSettings',
    'CollectionPermissions',
    'RetentionPolicy',
    
    # Document models
    'Document',
    'DocumentMetadata',
    'DocumentChunk',
    'ChunkMetadata',
    'CitationSpan',
    'ProcessingInfo',
    'ProcessingStep',
    
    # Chat models
    'ChatSession',
    'ChatMessage',
    'Citation',
    'HighlightSpan',
    'MessageMetadata',
    'ChatSettings',
    
    # Connector models
    'Connector',
    'ConnectorConfig',
    'SyncSettings',
    'ConnectorFilters',
    
    # Evaluation models
    'Evaluation',
    'EvaluationSettings',
    'EvaluationMetric',
    'TestQuery',
    'ModelConfig',
    'EvaluationResults',
    'MetricResult',
    'QueryResult',
    'EvaluationSummary',
    
    # Audit models
    'AuditLog',
    
    # System models
    'SystemMetrics',
    'ServiceStatus',
]
