#engine_db.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from sqlalchemy import text
from config import settings

engine = create_async_engine(settings.db.uri, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";"""))
        await conn.run_sync(Base.metadata.create_all)