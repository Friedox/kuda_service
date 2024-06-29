from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..exceptions import TripNotFoundError
from ..schemas.trip_scheme import CreateTripScheme, TripScheme
from ..models.trip_model import Trip


async def create(trip_create: CreateTripScheme, db: AsyncSession) -> TripScheme:
    new_trip = Trip(
        pickup=trip_create.pickup,
        dropoff=trip_create.dropoff,
        start_timestamp=trip_create.start_timestamp,
        end_timestamp=trip_create.end_timestamp,
        fare=trip_create.fare
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)

    trip = TripScheme(**new_trip.__dict__)

    return trip


async def get(trip_id: int, db: AsyncSession) -> TripScheme:
    query = select(Trip).filter(Trip.trip_id == trip_id)
    result = await db.execute(query)
    trip = result.scalars().first()

    if trip:
        trip_scheme = TripScheme(**trip.__dict__)
        return trip_scheme
    raise TripNotFoundError


async def delete(trip_delete: TripScheme, db: AsyncSession) -> bool:
    query = select(Trip).filter(Trip.trip_id == trip_delete.trip_id)

    result = await db.execute(query)
    trip = result.scalars().first()

    if trip:
        await db.delete(trip)
        await db.commit()
        return True

    raise TripNotFoundError
