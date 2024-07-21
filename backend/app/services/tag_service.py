from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from crud import tag_crud
from exceptions import InvalidTagException


async def get_available_tags(db: AsyncSession) -> dict[str, list[str]]:
    tag_collection = await tag_crud.get_all(db)

    available_tags = [tag_object.tag for tag_object in tag_collection]

    return {'available_tags': available_tags}


async def check_tags(tags: List[str], db: AsyncSession) -> None:
    for tag in tags:
        if not await tag_crud.is_in_table(tag, db):
            raise InvalidTagException(tag)

