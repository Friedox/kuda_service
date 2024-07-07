from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import TEST_SQLALCHEMY_URL, tags_fixture
from .database import Base


# async def setup_db() -> AsyncGenerator[AsyncSession, None]:
#     test_async_engine = create_async_engine(TEST_SQLALCHEMY_URL, echo=True, future=True)
#
#     async_session = sessionmaker(
#         bind=test_async_engine,
#         expire_on_commit=False,
#         class_=AsyncSession,
#         future=True
#     )
#
#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session() as session:
#         yield session
#
#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


