from typing import List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from exceptions import PointNotFoundError
from schemas.point_scheme import CreatePointScheme, PointScheme
from models.point_model import Point


async def create(point_create: CreatePointScheme, db: AsyncSession) -> PointScheme:
    point = Point(latitude=point_create.latitude,
                  longitude=point_create.longitude,
                  address=point_create.address
                  )

    db.add(point)
    await db.commit()
    await db.refresh(point)

    point_scheme = PointScheme(**point.__dict__)

    return point_scheme



async def get(point_id: int, db: AsyncSession) -> PointScheme:
    query = select(Point).where(Point.point_id == point_id)

    result = await db.execute(query)
    point = result.scalar_one()
    if point:
        point_scheme = PointScheme(**point.__dict__)

        return point_scheme
    raise PointNotFoundError(point_id=point_id)


async def delete(point_id: int, db: AsyncSession) -> bool:
    try:
        query = select(Point).where(Point.point_id == point_id)

        result = await db.execute(query)
        point = result.scalar_one()
        if point:
            await db.delete(point)
            await db.commit()
            return True
    except NoResultFound:
        raise PointNotFoundError(point_id=point_id)
