import httpx
import sqlalchemy as sa
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Optional

from app.db.database import database
from app.models.js_file_model import js_files
from app.models.schemas import JSFileResponse

class JSFileService:
    """
    Service class for managing JS files in the database.
    """
    
    async def _fetch_js_content(self, url: str) -> Optional[str]:
        """
        Fetches the content of a JavaScript file from a given URL.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, follow_redirects=True, timeout=10.0)
                response.raise_for_status() # Raises an exception for 4xx or 5xx responses
                
                # We will print the content to the console as requested.
                print(f"Fetched content from {url}:\n---\n{response.text}\n---")
                
                return response.text
            except httpx.HTTPStatusError as e:
                print(f"HTTP Error fetching {url}: {e.response.status_code}")
                return None
            except httpx.RequestError as e:
                print(f"Request Error fetching {url}: {e}")
                return None

    async def update_file_content(self, file_id: UUID) -> Optional[JSFileResponse]:
        """
        Fetches the content for a specific file from its URL and updates the database.
        """
        # First, retrieve the existing file record to get the URL
        query = js_files.select().where(js_files.c.id == file_id)
        existing_file = await database.fetch_one(query)
        
        if not existing_file:
            return None
        
        # Fetch the new content
        content = await self._fetch_js_content(existing_file.url)
        
        # If content was successfully fetched, update the database
        if content is not None:
            now = datetime.now()
            update_query = (
                js_files.update()
                .where(js_files.c.id == file_id)
                .values(content=content, last_fetched=now)
            )
            await database.execute(update_query)
            
            # Fetch the updated record to return to the client
            updated_record = await database.fetch_one(query)
            return JSFileResponse(**updated_record)
        
        # If content could not be fetched, return the existing file without updating
        return JSFileResponse(**existing_file)

    async def add_files(self, files: List[dict]):
        """
        Adds new JS files to the database.
        
        The files parameter is now a list of dictionaries from the gRPC request.
        """
        results = []
        for file in files:
            file_id = uuid4()
            now = datetime.now()
            query = js_files.insert().values(
                id=file_id,
                url=file['url'],
                host=file['url'].split('/')[2],
                content=None,
                priority=file['priority'],
                company_id=file['company_id'],
                last_fetched=None,
                last_updated=now,
            )
            await database.execute(query)
            results.append({
                "id": file_id,
                "url": file['url'],
                "host": file['url'].split('/')[2],
                "content": None,
                "priority": file['priority'],
                "company_id": file['company_id'],
                "last_fetched": None,
                "last_updated": now,
            })
        return results

    async def list_files_by_company(self, company_id: UUID, fetch_content: bool) -> List[JSFileResponse]:
        """
        Lists all JS files for a given company, optionally fetching their content.
        """
        query = js_files.select().where(js_files.c.company_id == company_id)
        records = await database.fetch_all(query)
        
        if fetch_content:
            results = []
            for record in records:
                file_dict = dict(record)
                content = await self._fetch_js_content(file_dict['url'])
                file_dict['content'] = content
                file_dict['last_fetched'] = datetime.now() if content else None
                results.append(JSFileResponse(**file_dict))
            return results
        
        return [JSFileResponse(**record) for record in records]

    async def list_all_files(self, fetch_content: bool) -> List[JSFileResponse]:
        """
        Lists all JS files in the database, optionally fetching their content.
        """
        query = js_files.select()
        records = await database.fetch_all(query)
        
        if fetch_content:
            results = []
            for record in records:
                file_dict = dict(record)
                content = await self._fetch_js_content(file_dict['url'])
                file_dict['content'] = content
                file_dict['last_fetched'] = datetime.now() if content else None
                results.append(JSFileResponse(**file_dict))
            return results

        return [JSFileResponse(**record) for record in records]
