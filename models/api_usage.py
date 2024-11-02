from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import BaseModel

class ApiUsage(BaseModel):
    """Database model for tracking API usage statistics."""
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    endpoint = Column(String, nullable=False)
    request_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    response_time = Column(Integer, nullable=False)
    status_code = Column(Integer, nullable=False)
    request_data = Column(String, nullable=True)
    response_data = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="api_usages")

    def __repr__(self):
        return f"<ApiUsage id={self.id}, user_id={self.user_id}, endpoint={self.endpoint}, request_time={self.request_time}, response_time={self.response_time}, status_code={self.status_code}>"