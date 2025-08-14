# infrastructure/configuration/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from src.infrastructure.configuration.app_settings import settings


class DatabaseConfig:
    def __init__(self):
        self.database_url: str = self._get_database_url()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def _get_database_url(self) -> str:
        """Construct database URL from settings"""
        if settings.db_type.lower() == "postgresql":
            return (
                f"postgresql://{settings.db_user}:{settings.db_password}"
                f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
            )
        else:
            raise ValueError(f"Unsupported DB_TYPE: {settings.db_type}")

    def _create_engine(self):
        """Create SQLAlchemy engine"""
        return create_engine(self.database_url, echo=settings.debug)
        # return create_engine("postgresql://myuser:mypassword@localhost:6543/tax_residency_db", echo=settings.debug)

    def get_session(self) -> Generator[Session, None, None]:
        """Yield a database session"""
        session: Session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def create_tables(self) -> None:
        """Create all tables"""
        from ..models.base_model import Base
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Drop all tables (use with caution)"""
        from ..models.base_model import Base
        Base.metadata.drop_all(bind=self.engine)


# Global database instance
db_config = DatabaseConfig()
