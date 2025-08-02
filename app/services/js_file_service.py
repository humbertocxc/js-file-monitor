from uuid import uuid4, UUID
from datetime import datetime
from typing import List

from app.db.database import database
from app.models.js_file_model import js_files
from app.models.schemas import JSFileCreate

class JSFileService:
    async def add_files(self, files: List[JSFileCreate]):
        results = []
        for file in files:
            file_id = uuid4()
            now = datetime.now()
            query = js_files.insert().values(
                id=file_id,
                url=str(file.url),
                host=file.url.host,
                content=None,
                priority=file.priority,
                company_id=file.company_id,
                last_fetched=None,
                last_updated=now,
            )
            await database.execute(query)
            results.append({
                "id": file_id,
                "url": str(file.url),
                "host": file.url.host,
                "content": None,
                "priority": file.priority,
                "company_id": file.company_id,
                "last_fetched": None,
                "last_updated": now,
            })
        return results

    async def list_files_by_company(self, company_id: UUID):
        query = js_files.select().where(js_files.c.company_id == company_id)
        return await database.fetch_all(query)
