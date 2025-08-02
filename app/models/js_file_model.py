import sqlalchemy
from sqlalchemy import Table, Column, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

metadata = sqlalchemy.MetaData()

js_files = Table(
    "js_files",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("url", Text, nullable=False),
    Column("host", Text, nullable=False),
    Column("content", Text),
    Column("priority", Integer),
    Column("company_id", UUID(as_uuid=True), nullable=False),
    Column("last_fetched", DateTime),
    Column("last_updated", DateTime),
)

