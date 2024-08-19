from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from wg_service.settings import settings

async_engine = create_async_engine(settings.get_postgres_url())
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
