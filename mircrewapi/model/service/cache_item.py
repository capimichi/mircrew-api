from datetime import datetime
from pydantic import BaseModel, Field


class CacheItem(BaseModel):
    key: str
    value: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
