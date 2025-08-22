# Admin API endpoints
# Handles system administration and monitoring

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_admin_role
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse, EvaluationListResponse
from app.schemas.common import PaginationParams
from app.services.evaluation_service import EvaluationService
from app.services.system_service import SystemService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/system/status")
async def get_system_status(
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get overall system status"""
    system_service = SystemService(db)
    status = await system_service.get_system_status()
    return status

@router.get("/system/metrics")
async def get_system_metrics(
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get system performance metrics"""
    system_service = SystemService(db)
    metrics = await system_service.get_system_metrics()
    return metrics

@router.get("/system/services")
async def get_service_status(
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get status of all system services"""
    system_service = SystemService(db)
    services = await system_service.get_service_status()
    return services

@router.post("/evaluations", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    evaluation_data: EvaluationCreate,
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new RAG evaluation"""
    evaluation_service = EvaluationService(db)
    evaluation = await evaluation_service.create_evaluation(evaluation_data, current_user.id)
    return evaluation

@router.get("/evaluations", response_model=EvaluationListResponse)
async def list_evaluations(
    pagination: PaginationParams = Depends(),
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all evaluations"""
    evaluation_service = EvaluationService(db)
    evaluations, total = await evaluation_service.list_evaluations(
        skip=pagination.skip,
        limit=pagination.limit
    )
    return {
        "items": evaluations,
        "total": total,
        "page": pagination.page,
        "size": pagination.size
    }

@router.get("/evaluations/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: str,
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific evaluation"""
    evaluation_service = EvaluationService(db)
    evaluation = await evaluation_service.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    return evaluation

@router.post("/evaluations/{evaluation_id}/run")
async def run_evaluation(
    evaluation_id: str,
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Run an evaluation"""
    evaluation_service = EvaluationService(db)
    success = await evaluation_service.run_evaluation(evaluation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    return {"message": "Evaluation started successfully"}

@router.get("/evaluations/{evaluation_id}/results")
async def get_evaluation_results(
    evaluation_id: str,
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get evaluation results"""
    evaluation_service = EvaluationService(db)
    results = await evaluation_service.get_evaluation_results(evaluation_id)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    return results

@router.get("/audit-logs")
async def get_audit_logs(
    pagination: PaginationParams = Depends(),
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get system audit logs"""
    system_service = SystemService(db)
    logs = await system_service.get_audit_logs(
        skip=pagination.skip,
        limit=pagination.limit
    )
    return logs

@router.get("/users")
async def list_users(
    pagination: PaginationParams = Depends(),
    current_user = Depends(require_admin_role),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all users (admin only)"""
    system_service = SystemService(db)
    users = await system_service.list_users(
        skip=pagination.skip,
        limit=pagination.limit
    )
    return users
