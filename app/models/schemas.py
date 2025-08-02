from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class JSFileCreate(BaseModel):
    url: HttpUrl
    priority: int = Field(..., ge=1, le=5)
    company_id: UUID

class JSFileResponse(BaseModel):
    id: UUID
    url: HttpUrl
    host: str
    content: Optional[str]
    priority: int
    company_id: UUID
    last_fetched: Optional[datetime]
    last_updated: Optional[datetime]
