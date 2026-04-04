from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL)


async def get_db():
    async with AsyncSession(engine) as session:
        yield session
