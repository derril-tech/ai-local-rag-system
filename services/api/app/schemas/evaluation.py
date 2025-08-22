# Evaluation Pydantic schemas
# Schemas for RAG evaluation and testing

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class EvaluationMetric(BaseModel):
    """Evaluation metric schema"""
    name: str = Field(..., min_length=1, max_length=100)
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    description: Optional[str] = None

class TestQuery(BaseModel):
    """Test query schema"""
    query: str = Field(..., min_length=1)
    expected_answer: Optional[str] = None
    expected_sources: Optional[List[str]] = None
    category: str = Field(..., min_length=1, max_length=100)
    difficulty: str = Field(default="medium", regex="^(easy|medium|hard)$")

class ModelConfig(BaseModel):
    """Model configuration for evaluation"""
    model: str = Field(..., min_length=1, max_length=100)
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    retrieval_strategy: str = Field(default="hybrid", regex="^(hybrid|semantic|keyword)$")

class EvaluationCreate(BaseModel):
    """Schema for creating an evaluation"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    collection_ids: List[str] = Field(..., description="Collection IDs")
    test_queries: List[TestQuery]
    metrics: List[EvaluationMetric]

class EvaluationResponse(BaseModel):
    """Schema for evaluation response"""
    id: str
    name: str
    description: Optional[str]
    created_by: str
    collection_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    metrics: List[EvaluationMetric]
    test_queries: List[TestQuery]
    model_config: ModelConfig

class EvaluationListResponse(BaseModel):
    """Schema for evaluation list response"""
    items: List[EvaluationResponse]
    total: int
    page: int
    size: int
