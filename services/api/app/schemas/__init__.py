# Pydantic schemas package
# This package contains all request/response schemas for the API

from .auth import UserCreate, UserLogin, UserResponse, TokenResponse, TokenData
from .collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionListResponse
from .document import DocumentCreate, DocumentResponse, DocumentListResponse, DocumentUpload
from .chat import ChatSessionCreate, ChatMessageCreate, QueryRequest, QueryResponse, ChatResponse
from .connector import ConnectorCreate, ConnectorUpdate, ConnectorResponse, ConnectorListResponse
from .evaluation import EvaluationCreate, EvaluationResponse, EvaluationListResponse
from .common import PaginationParams, ErrorResponse, SuccessResponse

__all__ = [
    # Auth schemas
    'UserCreate',
    'UserLogin', 
    'UserResponse',
    'TokenResponse',
    'TokenData',
    
    # Collection schemas
    'CollectionCreate',
    'CollectionUpdate',
    'CollectionResponse',
    'CollectionListResponse',
    
    # Document schemas
    'DocumentCreate',
    'DocumentResponse',
    'DocumentListResponse',
    'DocumentUpload',
    
    # Chat schemas
    'ChatSessionCreate',
    'ChatMessageCreate',
    'QueryRequest',
    'QueryResponse',
    'ChatResponse',
    
    # Connector schemas
    'ConnectorCreate',
    'ConnectorUpdate',
    'ConnectorResponse',
    'ConnectorListResponse',
    
    # Evaluation schemas
    'EvaluationCreate',
    'EvaluationResponse',
    'EvaluationListResponse',
    
    # Common schemas
    'PaginationParams',
    'ErrorResponse',
    'SuccessResponse',
]
