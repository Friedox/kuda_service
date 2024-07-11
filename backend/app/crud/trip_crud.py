from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import point_crud
from ..exceptions import TripNotFoundError
from ..schemas.trip_scheme import CreateTripScheme, TripScheme
from ..models.trip_model import Trip


async def create(trip_create: CreateTripScheme, db: AsyncSession) -> TripScheme:
    pickup_point = await point_crud.create(trip_create.pickup, db)
    dropoff_point = await point_crud.create(trip_create.dropoff, db)

    new_trip = Trip(
        pickup=pickup_point.point_id,
        dropoff=dropoff_point.point_id,
        start_timestamp=trip_create.start_timestamp,
        end_timestamp=trip_create.end_timestamp,
        fare=trip_create.fare,
        available_sits=trip_create.available_sits,
        driver_tg=trip_create.driver_tg,
        driver_phone=trip_create.driver_phone
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)

    trip = TripScheme(pickup=pickup_point,
                      dropoff=dropoff_point,
                      start_timestamp=new_trip.start_timestamp,
                      end_timestamp=new_trip.end_timestamp,
                      fare=new_trip.fare,
                      trip_id=new_trip.trip_id,
                      available_sits=new_trip.available_sits,
                      driver_tg=new_trip.driver_tg,
                      driver_phone=new_trip.driver_phone
                      )

    return trip


async def get(trip_id: int, db: AsyncSession) -> TripScheme:
    query = select(Trip).filter(Trip.trip_id == trip_id)
    result = await db.execute(query)
    trip = result.scalars().first()

    pickup_point = await point_crud.get(trip.pickup, db)
    dropoff_point = await point_crud.get(trip.dropoff, db)

    if trip:
        trip_scheme = TripScheme(
            pickup=pickup_point,
            dropoff=dropoff_point,
            start_timestamp=trip.start_timestamp,
            end_timestamp=trip.end_timestamp,
            fare=trip.fare,
            trip_id=trip.trip_id
        )
        return trip_scheme
    raise TripNotFoundError


async def delete(trip_delete: TripScheme, db: AsyncSession) -> bool:
    query = select(Trip).filter(Trip.trip_id == trip_delete.trip_id)

    result = await db.execute(query)
    trip = result.scalars().first()

    if trip:
        await db.delete(trip)
        await db.commit()
        await point_crud.delete(trip.pickup, db)
        await point_crud.delete(trip.dropoff, db)
        return True

    raise TripNotFoundError
