import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JsFileCreate(_message.Message):
    __slots__ = ("url", "priority", "company_id")
    URL_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    priority: int
    company_id: str
    def __init__(self, url: _Optional[str] = ..., priority: _Optional[int] = ..., company_id: _Optional[str] = ...) -> None: ...

class AddJsFilesRequest(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[JsFileCreate]
    def __init__(self, files: _Optional[_Iterable[_Union[JsFileCreate, _Mapping]]] = ...) -> None: ...

class AddJsFilesResponse(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[JsFileResponse]
    def __init__(self, files: _Optional[_Iterable[_Union[JsFileResponse, _Mapping]]] = ...) -> None: ...

class FetchAndUpdateJsFileContentRequest(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    def __init__(self, file_id: _Optional[str] = ...) -> None: ...

class ListJsFilesRequest(_message.Message):
    __slots__ = ("company_id", "fetch_content")
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    FETCH_CONTENT_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    fetch_content: bool
    def __init__(self, company_id: _Optional[str] = ..., fetch_content: bool = ...) -> None: ...

class ListJsFilesResponse(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[JsFileResponse]
    def __init__(self, files: _Optional[_Iterable[_Union[JsFileResponse, _Mapping]]] = ...) -> None: ...

class JsFileResponse(_message.Message):
    __slots__ = ("id", "url", "host", "content", "priority", "company_id", "last_fetched", "last_updated")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_FETCHED_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    host: str
    content: str
    priority: int
    company_id: str
    last_fetched: _timestamp_pb2.Timestamp
    last_updated: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., host: _Optional[str] = ..., content: _Optional[str] = ..., priority: _Optional[int] = ..., company_id: _Optional[str] = ..., last_fetched: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_updated: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
