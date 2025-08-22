# Chat service
# Handles chat sessions and RAG interactions

from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
import uuid

from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate

class ChatService:
    """Service for chat sessions and RAG interactions"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_session(self, session_data: ChatSessionCreate, user_id: str) -> ChatSession:
        """Create a new chat session"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create chat session
        session = ChatSession(
            title=session_data.title or "New Chat",
            user_id=user_id,
            tenant_id=user.tenant_id,
            collection_ids=session_data.collection_ids or [],
            settings=session_data.settings or {}
        )
        
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        
        return session
    
    async def get_session(self, session_id: str, user_id: str) -> Optional[ChatSession]:
        """Get chat session by ID"""
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return None
        
        # Check permissions
        from app.models.user import User
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        
        if not user or session.tenant_id != user.tenant_id:
            return None
        
        return session
    
    async def list_sessions(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        """Get chat sessions for user"""
        from app.models.user import User
        
        # Get user to get tenant_id
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return []
        
        # Get sessions for user's tenant
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.tenant_id == user.tenant_id)
            .order_by(ChatSession.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        sessions = result.scalars().all()
        
        return list(sessions)
    
    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete chat session"""
        session = await self.get_session(session_id, user_id)
        if not session:
            return False
        
        await self.db.delete(session)
        await self.db.commit()
        
        return True
    
    async def add_message(self, message_data: ChatMessageCreate, user_id: str) -> ChatMessage:
        """Add a message to a chat session"""
        # Verify session exists and user has access
        session = await self.get_session(message_data.session_id, user_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
        
        # Create message
        message = ChatMessage(
            session_id=message_data.session_id,
            role=message_data.role,
            content=message_data.content,
            metadata=message_data.metadata or {}
        )
        
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        
        return message
    
    async def get_messages(
        self, 
        session_id: str, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get messages for a chat session"""
        # Verify session exists and user has access
        session = await self.get_session(session_id, user_id)
        if not session:
            return []
        
        # Get messages
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        messages = result.scalars().all()
        
        return list(messages)
