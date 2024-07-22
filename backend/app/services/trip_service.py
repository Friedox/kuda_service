import datetime
from typing import List

import requests
from fastapi import Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from crud import trip_crud, trip_user_crud, trip_tag_crud, point_crud, review_crud
from exceptions import UnexpectedError, UserAlreadyBookedError, NotEnoughSitsError, TripEndedError, UserNotAllowedError
from models.point_model import Point
from models.tag_model import Tag
from models.trip_model import Trip
from models.trip_tag_model import TripTag
from schemas.filter_scheme import FilterScheme
from schemas.point_scheme import CreatePointScheme
from schemas.review_scheme import ReviewRequestScheme, ReviewScheme
from schemas.trip_scheme import CreateTripScheme, TripScheme, TripTagsScheme, RequestTripScheme, TripResponseScheme
from schemas.user_scheme import UserScheme
from services import tag_service
from services.auth_service import get_user_from_session_id
from services.geocoder_service import geocode
from services.translate_service import translate

from datetime import datetime


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
                                       creator_id=creator_id,
                                       trip_users=await trip_user_crud.get_trip_users(trip_id, db))

    return response_trip


async def get_user_trips(request: Request, db: AsyncSession) -> List[TripResponseScheme]:
    user = await get_user_from_session_id(request, db)

    trips = await trip_user_crud.get_user_trips(user, db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            creator_id=await trip_user_crud.get_trip_creator_id(trip.trip_id, db),
            trip_users=await trip_user_crud.get_trip_users(trip.trip_id, db)
        ) for
        trip in trips]

    return response_trips


async def get_upcoming(request: Request, db: AsyncSession) -> List[TripResponseScheme]:
    user = await get_user_from_session_id(request, db)
    now_time = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(now_time))
    trips = await trip_user_crud.get_upcoming_user_trips(user, timestamp, db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            creator_id=await trip_user_crud.get_trip_creator_id(trip.trip_id, db),
            trip_users=await trip_user_crud.get_trip_users(trip.trip_id, db)
        ) for
        trip in trips]

    return response_trips


async def get_filtered(trip_filter: FilterScheme, db: AsyncSession) -> List[TripResponseScheme]:
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
        trip_dict['creator_id'] = await trip_user_crud.get_trip_creator_id(trip.trip_id, db)
        trip_dict['trip_users'] = await trip_user_crud.get_trip_users(trip.trip_id, db)

        trip_schemas.append(TripResponseScheme(**trip_dict))

    return trip_schemas


async def convert_coords(latitude: float, longitude: float):
    translated_details = {}

    address_info = geocode(latitude=latitude, longitude=longitude)

    for key, value in address_info.items():
        translated_details[key] = translate(text=value)

    return translated_details


async def book(trip_id: int, request: Request, db: AsyncSession):
    user = await get_user_from_session_id(request, db)
    trip = await trip_user_crud.get(trip_id, db)
    users = await trip_user_crud.get_trip_users(trip_id, db)

    if not trip.is_active:
        raise TripEndedError

    if user.user_id in users:
        raise UserAlreadyBookedError

    if len(users) - 1 >= trip.available_sits:
        raise NotEnoughSitsError

    await trip_user_crud.book(user, trip_id, db)

    return {"message": "Booked successfully"}


async def delete_book(trip_id: int, request: Request, db: AsyncSession):
    user = await get_user_from_session_id(request, db)
    trip = await trip_user_crud.get(trip_id, db)
    users = await trip_user_crud.get_trip_users(trip_id, db)

    if user.user_id not in users:
        raise UserAlreadyBookedError

    await trip_user_crud.delete_book(user, trip_id, db)

    return {"message": "Book deleted successfully"}


async def end_trip(trip_id: int, request: Request, db: AsyncSession) -> None:
    user: UserScheme = await get_user_from_session_id(request, db)
    creator_id: int = await trip_user_crud.get_trip_creator_id(trip_id, db)

    if user.user_id != creator_id:
        raise UserNotAllowedError

    await trip_crud.set_ended(trip_id, db)


async def set_review(review: ReviewRequestScheme, request: Request, db: AsyncSession) -> ReviewScheme:
    user: UserScheme = await get_user_from_session_id(request, db)
    await trip_user_crud.get(review.trip_id, db)

    creator_id: int = await trip_user_crud.get_trip_creator_id(review.trip_id, db)
    trip_users: list[int] = await trip_user_crud.get_trip_users(review.trip_id, db)

    if user.user_id not in trip_users or user.user_id == creator_id:
        raise UserNotAllowedError

    response = await review_crud.create(review, user.user_id, db)

    return response


async def get_trip_time(db):
    pick_up_latitude = 55.754671
    pick_up_longitude = 48.741960
    drop_off_latitude = 55.793490
    drop_off_longitude = 49.118317
    time_trip_api = "hFD5DYJTQxkwl7LFdk87-KL3UIx8kUSPY8kqP0fam_s"

    response = requests.get(f"https://router.hereapi.com/v8/routes?transportMode=car&origin={pick_up_latitude},"
                            f"{pick_up_longitude}&destination={drop_off_latitude},"
                            f"{drop_off_longitude}&return=summary&apikey={time_trip_api}")
    route_data = response.json()
    durations = []
    for route in route_data['routes']:
        total_duration = 0

        for section in route['sections']:
            departure_time = section['departure']['time']
            arrival_time = section['arrival']['time']
            duration = (datetime.fromisoformat(arrival_time) - datetime.fromisoformat(
                departure_time)).total_seconds() / 60
            total_duration += duration

        durations.append(total_duration)

    smallest_duration = min(durations)

    return smallest_duration
