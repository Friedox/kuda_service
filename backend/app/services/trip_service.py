from datetime import datetime
from typing import List

import requests
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import trip_crud, trip_user_crud, trip_tag_crud, point_crud, review_crud, message_crud, car_crud
from exceptions import (UserAlreadyBookedError, NotEnoughSitsError, TripEndedError,
                        UserNotAllowedError)
from schemas.filter_scheme import FilterScheme
from schemas.point_scheme import CreatePointScheme
from schemas.review_scheme import ReviewRequestScheme, ReviewScheme
from schemas.trip_scheme import CreateTripScheme, RequestTripScheme, TripResponseScheme
from schemas.user_scheme import UserScheme
from services import tag_service, auth_service
from services.auth_service import get_user_from_session_id
from services.geocoder_service import geocode
from services.translate_service import translate


async def create(trip_request: RequestTripScheme, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    await tag_service.check_tags(trip_request.tags, db)
    await car_crud.get(trip_request.car_id, db)

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

    travel_time: float = await get_trip_time(pickup_point, dropoff_point)

    trip_create = CreateTripScheme(
        pickup=pickup_point,
        dropoff=dropoff_point,
        start_timestamp=trip_request.start_timestamp,
        end_timestamp=trip_request.end_timestamp,
        fare=trip_request.fare,
        tags=trip_request.tags,
        available_sits=trip_request.available_sits,
        travel_time=travel_time,
        car_id=trip_request.car_id
    )

    trip = await trip_user_crud.create(user, trip_create, db)

    await trip_tag_crud.add_tags(trip, trip_create.tags, db)

    return {
        "message": "Trip created successfully",
        "trip_id": trip.trip_id
    }


async def delete(trip_id: int, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)
    trip_delete = await trip_crud.get(trip_id, db)

    await trip_tag_crud.delete_tags(trip_delete, db)
    await message_crud.delete_messages(trip_delete, db)
    await trip_user_crud.delete_trip(user, trip_delete, db)

    await point_crud.delete(trip_delete.pickup.point_id, db)
    await point_crud.delete(trip_delete.dropoff.point_id, db)
    return {"message": "Trip deleted successfully"}


async def get(trip_id: int, db: AsyncSession) -> TripResponseScheme:
    trip = await trip_crud.get(trip_id, db)
    tags = [tag.tag for tag in await trip_tag_crud.get_tags(trip_id=trip_id, db=db)]
    car = await car_crud.get_trip_car(trip_id, db)

    creator_id = await trip_user_crud.get_trip_creator_id(trip_id, db)
    creator = await auth_service.get_user(creator_id, db)

    response_trip = TripResponseScheme(**trip.__dict__,
                                       tags=tags,
                                       car=car,
                                       creator=creator,
                                       trip_users=await trip_user_crud.get_trip_users(trip_id, db))

    return response_trip


async def get_user_trips(session_id: str | None, db: AsyncSession) -> List[TripResponseScheme]:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    trips = await trip_user_crud.get_user_trips(user, db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            tags=[tag.tag for tag in await trip_tag_crud.get_tags(trip_id=trip.trip_id, db=db)],
            car=await car_crud.get_trip_car(trip.trip_id, db),
            trip_users=await trip_user_crud.get_trip_users(trip.trip_id, db),
            creator=await auth_service.get_user(
                await trip_user_crud.get_trip_creator_id(trip.trip_id, db)
                , db
            )
        ) for
        trip in trips]

    return response_trips


async def get_upcoming(session_id: str | None, db: AsyncSession) -> list[TripResponseScheme]:
    user = await get_user_from_session_id(session_id, db)
    now_time = datetime.now()
    timestamp = int(datetime.timestamp(now_time))
    trips = await trip_user_crud.get_upcoming_user_trips(user, timestamp, db)

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            tags=[tag.tag for tag in await trip_tag_crud.get_tags(trip_id=trip.trip_id, db=db)],
            car=await car_crud.get_trip_car(trip.trip_id, db),
            trip_users=await trip_user_crud.get_trip_users(trip.trip_id, db),
            creator=await auth_service.get_user(
                await trip_user_crud.get_trip_creator_id(trip.trip_id, db)
                , db
            )
        ) for
        trip in trips]

    return response_trips


async def get_filtered(trip_filter: FilterScheme, db: AsyncSession) -> List[TripResponseScheme]:
    filtered_trip_ids = await trip_crud.get_filtered(trip_filter, db)

    filtered_trips = [await trip_crud.get(trip_id, db) for trip_id in filtered_trip_ids]

    response_trips = [
        TripResponseScheme(
            **trip.__dict__,
            tags=[tag.tag for tag in await trip_tag_crud.get_tags(trip_id=trip.trip_id, db=db)],
            car=await car_crud.get_trip_car(trip.trip_id, db),
            trip_users=await trip_user_crud.get_trip_users(trip.trip_id, db),
            creator=await auth_service.get_user(
                await trip_user_crud.get_trip_creator_id(trip.trip_id, db)
                , db
            )
        ) for
        trip in filtered_trips]

    return response_trips


async def convert_coords(latitude: float, longitude: float):
    translated_details = {}

    address_info = geocode(latitude=latitude, longitude=longitude)

    for key, value in address_info.items():
        translated_details[key] = translate(text=value)

    return translated_details


async def book(trip_id: int, session_id: str | None, db: AsyncSession):
    user = await get_user_from_session_id(session_id=session_id, db=db)
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


async def delete_book(trip_id: int, session_id: str | None, db: AsyncSession):
    user = await get_user_from_session_id(session_id=session_id, db=db)
    await trip_user_crud.get(trip_id, db)
    users = await trip_user_crud.get_trip_users(trip_id, db)

    if user.user_id not in users:
        raise UserAlreadyBookedError

    await trip_user_crud.delete_book(user, trip_id, db)

    return {"message": "Book deleted successfully"}


async def end_trip(trip_id: int, session_id: str | None, db: AsyncSession) -> None:
    user: UserScheme = await get_user_from_session_id(session_id=session_id, db=db)
    creator_id: int = await trip_user_crud.get_trip_creator_id(trip_id, db)

    if user.user_id != creator_id:
        raise UserNotAllowedError

    await trip_crud.set_ended(trip_id, db)


async def set_review(review: ReviewRequestScheme, session_id: str | None, db: AsyncSession) -> ReviewScheme:
    user: UserScheme = await get_user_from_session_id(session_id=session_id, db=db)
    await trip_user_crud.get(review.trip_id, db)

    creator_id: int = await trip_user_crud.get_trip_creator_id(review.trip_id, db)
    trip_users: list[int] = await trip_user_crud.get_trip_users(review.trip_id, db)

    if user.user_id not in trip_users or user.user_id == creator_id:
        raise UserNotAllowedError

    response = await review_crud.create(review, user.user_id, db)

    return response


async def get_trip_time(pickup_point: CreatePointScheme, dropoff_point: CreatePointScheme):
    pick_up_latitude = pickup_point.latitude
    pick_up_longitude = pickup_point.longitude
    drop_off_latitude = dropoff_point.latitude
    drop_off_longitude = dropoff_point.longitude
    time_trip_api = settings.geocoder.path_api_key

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

    if len(durations) <= 0:
        return -1
        # raise FindPathError
    smallest_duration = min(durations)

    return smallest_duration


async def check_user(trip_id: int, session_id: str | None, db: AsyncSession):
    user: UserScheme = await get_user_from_session_id(session_id=session_id, db=db)

    users = await trip_user_crud.get_trip_users(trip_id, db)
    creator_id = await trip_user_crud.get_trip_creator_id(trip_id, db)

    is_in_trip = user.user_id in users
    is_creator = user.user_id == creator_id

    return {"is_in_trip": is_in_trip, "is_creator": is_creator}
