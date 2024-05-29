from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

async def create_session() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        url="sqlite+aiosqlite:///nutritions.db",
        echo=True,
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker