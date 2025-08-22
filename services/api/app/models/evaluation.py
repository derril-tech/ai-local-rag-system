# Evaluation models for RAG evaluation and testing
# Handles evaluations, metrics, test queries, and results

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, JSON, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base

class EvaluationMetric(Base):
    """Evaluation metric definition"""
    __tablename__ = "evaluation_metrics"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    threshold: Mapped[float] = mapped_column(Float, default=0.8)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationship
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="metrics")

class TestQuery(Base):
    """Test query for evaluation"""
    __tablename__ = "test_queries"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[Optional[str]] = mapped_column(Text)
    expected_sources: Mapped[Optional[List[str]]] = mapped_column(JSON)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")  # easy, medium, hard
    
    # Relationship
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="test_queries")

class ModelConfig(Base):
    """Model configuration for evaluation"""
    __tablename__ = "model_configs"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.3)
    max_tokens: Mapped[int] = mapped_column(Integer, default=1000)
    retrieval_strategy: Mapped[str] = mapped_column(String(20), default="hybrid")
    
    # Relationship
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="model_config")

class QueryResult(Base):
    """Result of a test query"""
    __tablename__ = "query_results"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    query_id: Mapped[str] = mapped_column(ForeignKey("test_queries.id"), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    processing_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="query_results")
    test_query: Mapped[TestQuery] = relationship("TestQuery")

class MetricResult(Base):
    """Result of an evaluation metric"""
    __tablename__ = "metric_results"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    weighted_score: Mapped[float] = mapped_column(Float, nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationship
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="metric_results")

class EvaluationSummary(Base):
    """Summary of evaluation results"""
    __tablename__ = "evaluation_summaries"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    total_queries: Mapped[int] = mapped_column(Integer, default=0)
    successful_queries: Mapped[int] = mapped_column(Integer, default=0)
    average_groundedness: Mapped[float] = mapped_column(Float, default=0.0)
    average_citation_coverage: Mapped[float] = mapped_column(Float, default=0.0)
    average_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    common_issues: Mapped[List[str]] = mapped_column(JSON, default=list)
    recommendations: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # Relationship
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="summary")

class EvaluationResults(Base):
    """Complete evaluation results"""
    __tablename__ = "evaluation_results"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluations.id"), nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    evaluation: Mapped["Evaluation"] = relationship("Evaluation", back_populates="results")

class Evaluation(Base):
    """Evaluation model for RAG testing"""
    __tablename__ = "evaluations"
    
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    collection_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed, failed
    
    # Relationships
    created_by_user: Mapped["User"] = relationship("User", back_populates="evaluations")
    metrics: Mapped[List[EvaluationMetric]] = relationship("EvaluationMetric", back_populates="evaluation")
    test_queries: Mapped[List[TestQuery]] = relationship("TestQuery", back_populates="evaluation")
    model_config: Mapped[Optional[ModelConfig]] = relationship("ModelConfig", back_populates="evaluation", uselist=False)
    results: Mapped[Optional[EvaluationResults]] = relationship("EvaluationResults", back_populates="evaluation", uselist=False)
    metric_results: Mapped[List[MetricResult]] = relationship("MetricResult", back_populates="evaluation")
    query_results: Mapped[List[QueryResult]] = relationship("QueryResult", back_populates="evaluation")
    summary: Mapped[Optional[EvaluationSummary]] = relationship("EvaluationSummary", back_populates="evaluation", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Evaluation(id={self.id}, name={self.name}, status={self.status})>"
