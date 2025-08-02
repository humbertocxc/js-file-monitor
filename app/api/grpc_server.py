import asyncio
import grpc
from concurrent import futures
from datetime import datetime
from uuid import UUID

from app.db.database import database
from app.services.js_file_service import JSFileService
from protos import js_monitor_pb2
from protos import js_monitor_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

class JSMonitorServicer(js_monitor_pb2_grpc.JSMonitorServiceServicer):
    """
    Implements the gRPC service for JSMonitor.
    """
    def __init__(self):
        self.service = JSFileService()

    async def AddJsFiles(self, request, context):
        """
        Handles the gRPC call to add new JS files.
        """
        files_to_add = []
        for file in request.files:
            # We will perform the validation here since we are not using pydantic anymore for the API
            if not file.url.endswith('.js'):
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "URL must point to a JavaScript file (ending with .js)")
            files_to_add.append({
                "url": file.url,
                "priority": file.priority,
                "company_id": UUID(file.company_id)
            })

        results = await self.service.add_files(files_to_add)
        
        response_files = []
        for result in results:
            last_updated_ts = Timestamp()
            last_updated_ts.FromDatetime(result['last_updated'])
            response_files.append(js_monitor_pb2.JsFileResponse(
                id=str(result['id']),
                url=result['url'],
                host=result['host'],
                content=result.get('content', ''),
                priority=result['priority'],
                company_id=str(result['company_id']),
                last_fetched=Timestamp(),
                last_updated=last_updated_ts
            ))
        
        return js_monitor_pb2.AddJsFilesResponse(files=response_files)

    async def FetchAndUpdateJsFileContent(self, request, context):
        """
        Handles the gRPC call to fetch and update file content.
        """
        try:
            file_id = UUID(request.file_id)
        except ValueError:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid file ID format.")

        updated_file = await self.service.update_file_content(file_id)
        
        if not updated_file:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"File with id {file_id} not found.")

        last_fetched_ts = Timestamp()
        if updated_file.last_fetched:
            last_fetched_ts.FromDatetime(updated_file.last_fetched)
        
        last_updated_ts = Timestamp()
        if updated_file.last_updated:
            last_updated_ts.FromDatetime(updated_file.last_updated)

        return js_monitor_pb2.JsFileResponse(
            id=str(updated_file.id),
            url=str(updated_file.url),
            host=updated_file.host,
            content=updated_file.content or '',
            priority=updated_file.priority,
            company_id=str(updated_file.company_id),
            last_fetched=last_fetched_ts,
            last_updated=last_updated_ts,
        )

    async def ListJsFiles(self, request, context):
        """
        Handles the gRPC call to list JS files.
        """
        company_id = UUID(request.company_id) if request.company_id else None
        fetch_content = request.fetch_content
        
        if company_id:
            files = await self.service.list_files_by_company(company_id, fetch_content=fetch_content)
        else:
            files = await self.service.list_all_files(fetch_content=fetch_content)
        
        response_files = []
        for file in files:
            last_fetched_ts = Timestamp()
            if file.last_fetched:
                last_fetched_ts.FromDatetime(file.last_fetched)
            
            last_updated_ts = Timestamp()
            if file.last_updated:
                last_updated_ts.FromDatetime(file.last_updated)
            
            response_files.append(js_monitor_pb2.JsFileResponse(
                id=str(file.id),
                url=str(file.url),
                host=file.host,
                content=file.content or '',
                priority=file.priority,
                company_id=str(file.company_id),
                last_fetched=last_fetched_ts,
                last_updated=last_updated_ts,
            ))
            
        return js_monitor_pb2.ListJsFilesResponse(files=response_files)


async def serve():
    """
    Main function to run the gRPC server.
    """
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    js_monitor_pb2_grpc.add_JSMonitorServiceServicer_to_server(JSMonitorServicer(), server)
    server.add_insecure_port('[::]:50051')
    
    await database.connect()
    
    print("gRPC server starting on port 50051...")
    await server.start()
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down gRPC server...")
    finally:
        await database.disconnect()
