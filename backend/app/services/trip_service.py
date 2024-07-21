import datetime
from typing import List

from fastapi import Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from crud import trip_crud, trip_user_crud, trip_tag_crud, point_crud
from exceptions import UnexpectedError
from models.point_model import Point
from models.tag_model import Tag
from models.trip_model import Trip
from models.trip_tag_model import TripTag
from schemas.filter_scheme import FilterScheme
from schemas.point_scheme import CreatePointScheme
from schemas.trip_scheme import CreateTripScheme, TripScheme, TripTagsScheme, RequestTripScheme, TripResponseScheme
from services import tag_service
from services.auth_service import get_user_from_session_id
from services.geocoder_service import geocode
from services.translate_service import translate


async def create(trip_request: RequestTripScheme, request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)

    await tag_service.check_tags(trip_request.tags, db)

    pickup_address_dict = await convert_coords(trip_request.pickup.latitude, trip_request.pickup.longitude)
    dropoff_address_dict = await convert_coords(trip_request.dropoff.latitude, trip_request.dropoff.longitude)

    pickup_point = CreatePointScheme(
        address=pickup_address_dict,
        latitude=trip_request.pickup.latitude,
        longitude=trip_request.pickup.longitude,
    )

    dropoff_point = CreatePointScheme(
        address=dropoff_address_dict,
        latitude=trip_request.dropoff.latitude,
        longitude=trip_request.dropoff.longitude,
    )

    trip_create = CreateTripScheme(
        pickup=pickup_point,
        dropoff=dropoff_point,
        start_timestamp=trip_request.start_timestamp,
        end_timestamp=trip_request.end_timestamp,
        fare=trip_request.fare,
        tags=trip_request.tags,
        available_sits=trip_request.available_sits,
        driver_phone=trip_request.driver_phone,
        driver_tg=trip_request.driver_tg,
        car_number=trip_request.car_number,
        car_type=trip_request.car_type,
    )

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

    raise UnexpectedError("Trip not deleted")


async def get(trip_id: int, db: AsyncSession) -> TripResponseScheme:
    trip = await trip_user_crud.get(trip_id, db)
    creator_id = await trip_user_crud.get_trip_creator_id(trip_id, db)

    response_trip = TripResponseScheme(**trip.__dict__,
                                       creator_id=creator_id)

    return response_trip


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


async def convert_coords(latitude: float, longitude: float):
    translated_details = {}

    address_info = geocode(latitude=latitude, longitude=longitude)

    for key, value in address_info.items():
        translated_details[key] = translate(text=value)

    return translated_details
