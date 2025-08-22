# Evaluation service
# Handles RAG evaluation and testing

from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
import uuid

from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate

class EvaluationService:
    """Service for RAG evaluation and testing"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_evaluation(self, evaluation_data: EvaluationCreate, user_id: str) -> Evaluation:
        """Create a new evaluation"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create evaluation
        evaluation = Evaluation(
            name=evaluation_data.name,
            description=evaluation_data.description,
            collection_ids=evaluation_data.collection_ids,
            test_queries=evaluation_data.test_queries,
            metrics=evaluation_data.metrics,
            created_by=user_id,
            tenant_id=user.tenant_id,
            status="pending"
        )
        
        self.db.add(evaluation)
        await self.db.commit()
        await self.db.refresh(evaluation)
        
        return evaluation
    
    async def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get evaluation by ID"""
        result = await self.db.execute(
            select(Evaluation).where(Evaluation.id == evaluation_id)
        )
        evaluation = result.scalar_one_or_none()
        
        return evaluation
    
    async def list_evaluations(self, skip: int = 0, limit: int = 100) -> Tuple[List[Evaluation], int]:
        """Get evaluations with pagination"""
        # Get total count
        total_result = await self.db.execute(select(func.count(Evaluation.id)))
        total = total_result.scalar() or 0
        
        # Get evaluations
        result = await self.db.execute(
            select(Evaluation)
            .order_by(Evaluation.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        evaluations = result.scalars().all()
        
        return list(evaluations), total
    
    async def run_evaluation(self, evaluation_id: str) -> bool:
        """Run an evaluation"""
        evaluation = await self.get_evaluation(evaluation_id)
        if not evaluation:
            return False
        
        # Update status to running
        evaluation.status = "running"
        await self.db.commit()
        
        # In a real implementation, this would trigger a background task
        # For now, just return success
        
        return True
    
    async def get_evaluation_results(self, evaluation_id: str) -> Optional[dict]:
        """Get evaluation results"""
        evaluation = await self.get_evaluation(evaluation_id)
        if not evaluation:
            return None
        
        # In a real implementation, this would query results from the database
        # For now, return mock results
        return {
            "evaluation_id": evaluation_id,
            "status": evaluation.status,
            "results": {
                "accuracy": 0.85,
                "precision": 0.82,
                "recall": 0.88,
                "f1_score": 0.85
            },
            "completed_at": evaluation.updated_at.isoformat() if evaluation.status == "completed" else None
        }
