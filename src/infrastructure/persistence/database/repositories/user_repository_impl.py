from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, or_
from datetime import datetime, timezone

from ..models.user_model import UserModel, UserRole
from ..config.connection_factory import connection_factory
import logging

logger = logging.getLogger(__name__)

class UserRepositoryImpl:
    """Implementation of user repository"""
    
    def __init__(self):
        self.connection_factory = connection_factory
    
    def create_user(self, user_data: Dict[str, Any]) -> UserModel:
        """Create a new user"""
        with self.connection_factory.get_session() as session:
            user = UserModel(**user_data)
            session.add(user)
            session.flush()
            session.refresh(user)
            return user
    
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID"""
        with self.connection_factory.get_session() as session:
            return session.query(UserModel).filter(
                UserModel.id == user_id
            ).first()
    
    def get_user_by_uuid(self, user_uuid: str) -> Optional[UserModel]:
        """Get user by UUID"""
        with self.connection_factory.get_session() as session:
            return session.query(UserModel).filter(
                UserModel.user_uuid == user_uuid
            ).first()
    
    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        with self.connection_factory.get_session() as session:
            return session.query(UserModel).filter(
                UserModel.username == username
            ).first()
    