from sqlalchemy.orm import Session
from contextlib import contextmanager
from .database_config import db_config
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

class ConnectionFactory:
    """Factory class for managing database connections"""
    
    def __init__(self):
        self.db_config = db_config
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session: Session = self.db_config.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session_sync(self) -> Session:
        """Get synchronous database session (remember to close it)"""
        return self.db_config.SessionLocal()
    
    def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False
    
    def initialize_database(self):
        """Initialize database with tables"""
        try:
            self.db_config.create_tables()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise

# Global connection factory instance
connection_factory = ConnectionFactory()