from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..exceptions import TripNotFoundError, UserTripNotFoundError
from ..schemas.trip_scheme import CreateTripScheme, TripScheme
from ..schemas.user_scheme import UserScheme
from ..models.trip_user_model import TripUser
from . import trip_crud


async def create(user: UserScheme, trip_create: CreateTripScheme, db: AsyncSession) -> TripScheme:
    try:
        db.begin()

        trip = await trip_crud.create(trip_create, db)

        link = TripUser(
            user_id=user.user_id,
            trip_id=trip.trip_id
        )
        db.add(link)
        await db.commit()
        await db.refresh(link)

        return trip
    except Exception as e:
        await db.rollback()
        raise e


async def delete(user: UserScheme, trip_delete: TripScheme, db: AsyncSession) -> bool:
    try:
        db.begin()

        query = select(TripUser).filter(
            TripUser.user_id == user.user_id,
            TripUser.trip_id == trip_delete.trip_id
        )

        result = await db.execute(query)
        trip_user = result.scalars().first()

        if not trip_user:
            await db.rollback()
            raise UserTripNotFoundError(user.user_id, trip_delete.trip_id)

        await db.delete(trip_user)

        if await trip_crud.delete(trip_delete, db):
            await db.commit()
            return True
        else:
            await db.rollback()
            raise TripNotFoundError

    except Exception as e:
        await db.rollback()
        raise e
