from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from crud import point_crud
from exceptions import TripNotFoundError, TripAlreadyEndedError
from models.point_model import Point
from models.tag_model import Tag
from models.trip_model import Trip
from models.trip_tag_model import TripTag
from schemas.trip_scheme import CreateTripScheme
from schemas.trip_scheme import TripScheme


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
        is_active=True,
        travel_time=trip_create.travel_time
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)

    trip = TripScheme(
        pickup=pickup_point,
        dropoff=dropoff_point,
        start_timestamp=new_trip.start_timestamp,
        end_timestamp=new_trip.end_timestamp,
        fare=new_trip.fare,
        trip_id=new_trip.trip_id,
        available_sits=new_trip.available_sits,
        is_active=new_trip.is_active,
        travel_time=new_trip.travel_time
    )

    return trip


async def get(trip_id: int, db: AsyncSession) -> TripScheme:
    trip = (
        await db.execute(
            select(Trip)
            .filter(Trip.trip_id == trip_id)
        )
    ).scalars().first()

    if trip is None:
        raise TripNotFoundError

    pickup_point = await point_crud.get(trip.pickup, db)
    dropoff_point = await point_crud.get(trip.dropoff, db)

    trip_scheme = TripScheme(
        pickup=pickup_point,
        dropoff=dropoff_point,
        start_timestamp=trip.start_timestamp,
        end_timestamp=trip.end_timestamp,
        fare=trip.fare,
        trip_id=trip.trip_id,
        available_sits=trip.available_sits,
        is_active=trip.is_active,
        travel_time=trip.travel_time
    )
    return trip_scheme


async def delete(trip_delete: TripScheme, db: AsyncSession) -> None:
    query = select(Trip).filter(Trip.trip_id == trip_delete.trip_id)

    result = await db.execute(query)
    trip = result.scalars().first()

    if not trip:
        raise TripNotFoundError

    await db.delete(trip)
    await db.commit()


async def set_ended(trip_id, db) -> None:
    trip = (
        await db.execute(
            select(Trip)
            .filter(Trip.trip_id == trip_id))
    ).scalars().first()

    if trip is None:
        raise TripNotFoundError

    if not trip.is_active:
        raise TripAlreadyEndedError

    trip.is_active = False

    await db.commit()


async def get_filtered(trip_filter, db):
    query = select(Trip)

    if trip_filter.pickup:
        pickup_point = aliased(Point)
        query = query.join(pickup_point, Trip.pickup == pickup_point.point_id)
        if trip_filter.pickup_range:
            pickup_range_degrees = trip_filter.pickup_range / 111320.0  # 1 degree ≈ 111.32 km
            query = query.filter(
                func.sqrt(
                    func.pow(pickup_point.latitude - trip_filter.pickup.latitude, 2) +
                    func.pow(pickup_point.longitude - trip_filter.pickup.longitude, 2)
                ) <= pickup_range_degrees
            )
        else:
            query = query.filter(
                pickup_point.latitude == trip_filter.pickup.latitude,
                pickup_point.longitude == trip_filter.pickup.longitude
            )

    if trip_filter.dropoff:
        dropoff_point = aliased(Point)
        query = query.join(dropoff_point, Trip.dropoff == dropoff_point.point_id)
        if trip_filter.dropoff_range:
            dropoff_range_degrees = trip_filter.dropoff_range / 111320.0  # 1 degree ≈ 111.32 km
            query = query.filter(
                func.sqrt(
                    func.pow(dropoff_point.latitude - trip_filter.dropoff.latitude, 2) +
                    func.pow(dropoff_point.longitude - trip_filter.dropoff.longitude, 2)
                ) <= dropoff_range_degrees
            )
        else:
            query = query.filter(
                dropoff_point.latitude == trip_filter.dropoff.latitude,
                dropoff_point.longitude == trip_filter.dropoff.longitude
            )

    if trip_filter.start_timestamp:
        query = query.filter(Trip.start_timestamp >= trip_filter.start_timestamp)

    if trip_filter.end_timestamp:
        query = query.filter(Trip.end_timestamp <= trip_filter.end_timestamp)

    if trip_filter.tags:
        tag_alias = aliased(Tag)
        trip_tag_alias = aliased(TripTag)

        subquery = (
            select(Trip.trip_id)
            .join(trip_tag_alias, Trip.trip_id == trip_tag_alias.trip_id)
            .join(tag_alias, trip_tag_alias.tag_id == tag_alias.tag_id)
            .filter(tag_alias.tag.in_(trip_filter.tags))
            .group_by(Trip.trip_id)
            .having(func.count(tag_alias.tag) == len(trip_filter.tags))
        )

        query = query.filter(Trip.trip_id.in_(subquery))

    result = await db.execute(query)
    trips = result.scalars().all()

    trip_ids = [trip.trip_id for trip in trips]

    return trip_ids
