from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.tag_scheme import TagScheme
from models.tag_model import Tag


async def get_all(db: AsyncSession) -> List[TagScheme]:
    query = select(Tag)
    result = await db.execute(query)
    tags = result.scalars().all()

    if tags:
        tags_scheme = [TagScheme(**tag.__dict__) for tag in tags]
        return tags_scheme
    return []


async def is_in_table(tag: str, db: AsyncSession) -> bool:
    query = select(Tag).filter(Tag.tag == tag)
    result = await db.execute(query)
    return result.scalars().first() is not None


async def get(tag: str or int, db: AsyncSession) -> TagScheme:
    if isinstance(tag, int):
        query = select(Tag).filter(Tag.tag_id == tag)
    else:
        query = select(Tag).filter(Tag.tag == tag)
    result = await db.execute(query)
    tag = result.scalars().first()
    return TagScheme(**tag.__dict__)
