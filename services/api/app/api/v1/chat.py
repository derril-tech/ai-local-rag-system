# Chat API endpoints
# Handles RAG interactions and chat sessions

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate, QueryRequest, QueryResponse, ChatResponse
from app.schemas.common import PaginationParams
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/sessions", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new chat session"""
    chat_service = ChatService(db)
    session = await chat_service.create_session(session_data, current_user.id)
    return session

@router.get("/sessions", response_model=List[ChatResponse])
async def list_chat_sessions(
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List chat sessions for the current user"""
    chat_service = ChatService(db)
    sessions = await chat_service.list_sessions(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return sessions

@router.get("/sessions/{session_id}", response_model=ChatResponse)
async def get_chat_session(
    session_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific chat session"""
    chat_service = ChatService(db)
    session = await chat_service.get_session(session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    return session

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    session_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Delete a chat session"""
    chat_service = ChatService(db)
    success = await chat_service.delete_session(session_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

@router.post("/query", response_model=QueryResponse)
async def query_rag(
    query_data: QueryRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Query the RAG system"""
    rag_service = RAGService(db)
    chat_service = ChatService(db)
    
    # Process query through RAG pipeline
    response = await rag_service.process_query(
        query=query_data.query,
        collection_ids=query_data.collection_ids,
        session_id=query_data.session_id,
        user_id=current_user.id
    )
    
    # Save message to chat session if provided
    if query_data.session_id:
        message_data = ChatMessageCreate(
            content=query_data.query,
            role="user",
            session_id=query_data.session_id
        )
        await chat_service.add_message(message_data, current_user.id)
    
    return response

@router.get("/sessions/{session_id}/messages")
async def get_chat_messages(
    session_id: str,
    pagination: PaginationParams = Depends(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get messages for a chat session"""
    chat_service = ChatService(db)
    messages = await chat_service.get_messages(
        session_id=session_id,
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return messages

@router.post("/sessions/{session_id}/messages")
async def add_chat_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Add a message to a chat session"""
    chat_service = ChatService(db)
    message = await chat_service.add_message(message_data, current_user.id)
    return message
