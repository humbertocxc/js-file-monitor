from fastapi import APIRouter, Query, HTTPException
from uuid import UUID
from typing import List, Optional

from app.services.js_file_service import JSFileService
from app.models.schemas import JSFileCreate, JSFileResponse

router = APIRouter()
service = JSFileService()

@router.post("/js-files/", response_model=List[JSFileResponse])
async def add_js_files(files: List[JSFileCreate], fetch_content: bool = Query(True)):
    """
    Endpoint to add one or more new JavaScript files to the database,
    optionally fetching their content immediately.
    
    - `fetch_content`: Set to `False` to prevent content from being fetched on creation.
    """
    return await service.add_files(files, fetch_content=fetch_content)

@router.put("/js-files/{file_id}/fetch-content", response_model=JSFileResponse)
async def fetch_and_update_js_file_content(file_id: UUID):
    """
    Endpoint to fetch the content of a specific JavaScript file from its URL
    and update its record in the database.
    """
    updated_file = await service.update_file_content(file_id)
    if not updated_file:
        raise HTTPException(status_code=404, detail=f"File with id {file_id} not found.")
    return updated_file

@router.get("/js-files/", response_model=List[JSFileResponse])
async def list_js_files(company_id: Optional[UUID] = Query(None)):
    """
    Endpoint to list all JavaScript files, optionally filtered by company ID.
    """
    if company_id:
        return await service.list_files_by_company(company_id)
    return await service.list_all_files()