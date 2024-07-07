from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from .config import SQLALCHEMY_URL, tags_fixture

async_engine = create_async_engine(SQLALCHEMY_URL, echo=True, future=True)

database = Database(SQLALCHEMY_URL)

async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)

Base = declarative_base()


async def get_async_db():
    async with async_session() as session:
        yield session


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_fixture_data():
    from .crud import tag_crud
    from .models.tag_model import Tag

    async with async_session() as session:
        existing_tags = await tag_crud.get_all(session)
        existing_tag_names = {tag.tag for tag in existing_tags}

        for tag_name in tags_fixture:
            if tag_name not in existing_tag_names:
                new_tag = Tag(tag=tag_name)
                session.add(new_tag)

        await session.commit()
