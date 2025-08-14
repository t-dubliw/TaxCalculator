# from sqlalchemy import Column, String, Boolean, DateTime, Enum
# from sqlalchemy.dialects.postgresql import UUID
# from .base_model import BaseModel
# import uuid
# import enum

# class UserRole(str, enum.Enum):
#     ADMIN = "admin"
#     USER = "user"
#     AUDITOR = "auditor"

# class UserModel(BaseModel):
#     __tablename__ = "users"
    
#     # User identification
#     user_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, index=True)
#     username = Column(String(100), nullable=False, unique=True, index=True)
#     email = Column(String(255), nullable=False, unique=True, index=True)
    
#     # Authentication
#     password_hash = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
#     is_verified = Column(Boolean, default=False)
    
#     # Profile
#     first_name = Column(String(100), nullable=True)
#     last_name = Column(String(100), nullable=True)
#     role = Column(Enum(UserRole), default=UserRole.USER)
    
#     # Session management
#     last_login = Column(DateTime(timezone=True), nullable=True)
#     failed_login_attempts = Column(String(10), default="0")
#     locked_until = Column(DateTime(timezone=True), nullable=True)
    
#     # Tax profile defaults
#     default_country_code = Column(String(10), nullable=True)
#     default_currency = Column(String(10), default='USD')
    
#     def __repr__(self):
#         return f"<User(username='{self.username}', email='{self.email}', role='{self.role}')>"
    
#     @property
#     def full_name(self):
#         if self.first_name and self.last_name:
#             return f"{self.first_name} {self.last_name}"
#         return self.username