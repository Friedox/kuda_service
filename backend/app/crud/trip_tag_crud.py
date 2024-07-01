from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from ..models.trip_tag_model import TripTag
from ..schemas.tag_scheme import TagScheme
from ..schemas.trip_scheme import TripScheme
from . import tag_crud


async def add_tags(trip: TripScheme, tags: List[str], db: AsyncSession) -> TripScheme:
    try:
        db.begin()

        for tag in tags:
            tag_object = await tag_crud.get(tag, db)

            link = TripTag(
                tag_id=tag_object.tag_id,
                trip_id=trip.trip_id
            )

            db.add(link)
        await db.commit()

        return trip
    except Exception as e:
        await db.rollback()
        raise e


async def get_tags(trip: TripScheme, db: AsyncSession) -> List[TagScheme]:
    query = select(TripTag).filter(TripTag.trip_id == trip.trip_id)

    result = await db.execute(query)
    tag_objects = result.scalars().all()

    tags = [await tag_crud.get(tag.tag, db) for tag in tag_objects]

    return tags


async def delete_tags(trip: TripScheme, db: AsyncSession):
    query = delete(TripTag).where(TripTag.trip_id == trip.trip_id)
    await db.execute(query)
    await db.commit()
