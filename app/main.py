from fastapi import FastAPI
from contextlib import asynccontextmanager
from uuid import UUID
from typing import List

from app.db.database import database
from app.services.js_file_service import JSFileService
from app.models.schemas import JSFileCreate, JSFileResponse

service = JSFileService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/js-files/", response_model=List[JSFileResponse])
async def add_js_files(files: List[JSFileCreate]):
    return await service.add_files(files)

@app.get("/js-files/", response_model=List[JSFileResponse])
async def list_js_files(company_id: UUID):
    return await service.list_files_by_company(company_id)

