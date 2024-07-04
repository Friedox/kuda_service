import datetime
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from sqlalchemy.orm import aliased

from . import tag_service
from ..crud import trip_crud, trip_user_crud, trip_tag_crud, point_crud
from ..exceptions import UnexpectedError
from ..models.point_model import Point
from ..models.tag_model import Tag
from ..models.trip_model import Trip
from ..models.trip_tag_model import TripTag
from ..schemas.filter_scheme import FilterScheme
from ..schemas.trip_scheme import CreateTripScheme, TripScheme, TripTagsScheme
from ..services.auth_service import get_user_from_session_id


async def create(trip_create: CreateTripScheme, request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)
    await tag_service.check_tags(trip_create.tags, db)

    trip = await trip_user_crud.create(user, trip_create, db)
    await trip_tag_crud.add_tags(trip, trip_create.tags, db)

    return {
        "message": "Trip created successfully",
        "trip_id": trip.trip_id
    }


async def delete(trip_id: int, request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)
    trip_delete = await trip_crud.get(trip_id, db)

    await trip_tag_crud.delete_tags(trip_delete, db)
    if await trip_user_crud.delete(user, trip_delete, db):
        return {"message": "Trip deleted successfully"}

    raise UnexpectedError("Trip deleted")


async def get_user_trips(request: Request, db: AsyncSession) -> List[TripScheme]:
    user = await get_user_from_session_id(request, db)

    return await trip_user_crud.get_user_trips(user, db)


async def get_upcoming(request: Request, db: AsyncSession):
    user = await get_user_from_session_id(request, db)
    now_time = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(now_time))
    return await trip_user_crud.get_upcoming_user_trips(user, timestamp, db)


async def get_filtered(trip_filter: FilterScheme, db: AsyncSession):
    query = select(Trip)

    if trip_filter.pickup:
        pickup_point = aliased(Point)
        query = query.join(pickup_point, Trip.pickup == pickup_point.point_id)
        if trip_filter.pickup_range:
            pickup_range_degrees = trip_filter.pickup_range / 111320.0  # 1 градус ≈ 111.32 км
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
            dropoff_range_degrees = trip_filter.dropoff_range / 111320.0  # 1 градус ≈ 111.32 км
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
            select([Trip.trip_id])
            .join(trip_tag_alias, Trip.trip_id == trip_tag_alias.trip_id)
            .join(tag_alias, trip_tag_alias.tag_id == tag_alias.tag_id)
            .filter(tag_alias.tag.in_(trip_filter.tags))
            .group_by(Trip.trip_id)
            .having(func.count(tag_alias.tag) == len(trip_filter.tags))
        )

        query = query.filter(Trip.trip_id.in_(subquery))

    result = await db.execute(query)
    trips = result.scalars().all()

    trip_schemas = []
    for trip in trips:
        print(trip.__dict__)

        tag_names = [tag.tag for tag in await trip_tag_crud.get_tags(trip.trip_id, db)]
        trip_dict = trip.__dict__.copy()
        trip_dict['tags'] = tag_names
        trip_dict['pickup'] = await point_crud.get(trip.pickup, db)
        trip_dict['dropoff'] = await point_crud.get(trip.dropoff, db)
        trip_schemas.append(TripTagsScheme(**trip_dict))

    return trip_schemas
