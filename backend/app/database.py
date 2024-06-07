from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
from config import SQLALCHEMY_URL
from sqlalchemy.ext.declarative import declarative_base

async_engine = create_async_engine(SQLALCHEMY_URL, echo=True)

database = Database(SQLALCHEMY_URL)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


async def get_async_db():
    async with async_session() as session:
        yield session


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
