from pydantic import BaseModel, AnyUrl, Field, field_validator
from uuid import UUID
from typing import Optional
from datetime import datetime

class JSFileCreate(BaseModel):
    """
    Pydantic model for creating a new JS file record.
    """
    url: AnyUrl
    priority: int = Field(..., ge=1, le=5)
    company_id: UUID

    @field_validator('url')
    @classmethod
    def validate_js_file_url(cls, v):
        """
        Validator to ensure the URL ends with '.js'.
        """
        if not str(v).endswith('.js'):
            raise ValueError('URL must point to a JavaScript file (ending with .js)')
        return v

class JSFileResponse(BaseModel):
    """
    Pydantic model for the response when retrieving a JS file.
    """
    id: UUID
    url: AnyUrl
    host: str
    content: Optional[str]
    priority: int
    company_id: UUID
    last_fetched: Optional[datetime]
    last_updated: Optional[datetime]
