# from sqlalchemy import Column, String, Text, DateTime, Numeric, JSON, ForeignKey, Index
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from .base_model import BaseModel
# import uuid

# class AuditModel(BaseModel):
#     __tablename__ = "audit_records"
    
#     # Audit identification
#     audit_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, index=True)
#     user_id = Column(String(100), nullable=False, index=True)
#     session_id = Column(String(100), nullable=True)
    
#     # Calculation details
#     calculation_type = Column(String(50), default='tax_calculation')
#     input_data = Column(JSON, nullable=False)  # User input data
#     calculation_result = Column(JSON, nullable=False)  # Tax calculation result
    
#     # Rule version tracking
#     rule_id_used = Column(UUID(as_uuid=True), nullable=False)
#     rule_version_used = Column(String(50), nullable=False)
#     country_code = Column(String(10), nullable=False)
#     tax_year = Column(String(10), nullable=False)
    
#     # Result summary
#     total_tax_amount = Column(Numeric(15, 2), nullable=False)
#     effective_tax_rate = Column(Numeric(5, 4), nullable=True)
    
#     # Request metadata
#     request_timestamp = Column(DateTime(timezone=True), nullable=False)
#     processing_time_ms = Column(Numeric(10, 2), nullable=True)
#     client_ip = Column(String(45), nullable=True)
#     user_agent = Column(Text, nullable=True)
    
#     # Create indexes for audit queries
#     __table_args__ = (
#         Index('idx_audit_user_date', 'user_id', 'request_timestamp'),
#         Index('idx_audit_rule_version', 'rule_id_used', 'rule_version_used'),
#         Index('idx_audit_country_year', 'country_code', 'tax_year'),
#         Index('idx_audit_timestamp', 'request_timestamp'),
#     )
    
#     def __repr__(self):
#         return f"<AuditRecord(user_id='{self.user_id}', tax_amount={self.total_tax_amount}, timestamp='{self.request_timestamp}')>"