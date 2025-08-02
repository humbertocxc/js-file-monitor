from databases import Database

DATABASE_URL = "postgresql+asyncpg://jsuser:secret123@localhost:5432/jsmonitor"

database = Database(DATABASE_URL)

