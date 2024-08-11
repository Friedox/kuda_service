from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud import trip_crud, point_crud
from exceptions import TripNotFoundError, UserTripNotFoundError, BookNotFoundError
from models.car_model import user_car_association
from models.trip_model import Trip, car_trip_association
from models.trip_user_model import TripUser
from schemas.trip_scheme import CreateTripScheme, TripScheme, TripTagsScheme
from schemas.user_scheme import UserScheme


async def create(user: UserScheme, trip_create: CreateTripScheme, db: AsyncSession) -> TripScheme:
    try:
        trip = await trip_crud.create(trip_create, db)

        stmt = insert(car_trip_association).values(trip_id=trip.trip_id, car_id=trip_create.car_id)
        await db.execute(stmt)
        await db.commit()

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


async def get(trip_id: int, db: AsyncSession) -> TripTagsScheme:
    query = (
        select(Trip)
        .join(TripUser)
        .filter(Trip.trip_id == trip_id)
        .options(selectinload(Trip.tags))
    )

    result = await db.execute(query)
    trip_object = result.scalars().first()

    if trip_object is None:
        raise TripNotFoundError

    tag_names = [tag.tag for tag in trip_object.tags]
    trip_dict = trip_object.__dict__
    trip_dict['pickup'] = await point_crud.get(trip_object.pickup, db)
    trip_dict['dropoff'] = await point_crud.get(trip_object.dropoff, db)
    trip_dict['tags'] = tag_names

    trip = TripTagsScheme(**trip_dict)

    return trip


async def get_trip_creator_id(trip_id: int, db: AsyncSession) -> int:
    query = (
        select(TripUser)
        .filter(TripUser.trip_id == trip_id)
    )

    result = await db.execute(query)

    trip_object = result.scalars().first()

    if trip_object is None:
        raise TripNotFoundError

    return trip_object.user_id


async def get_trip_users(trip_id: int, db: AsyncSession) -> list[int]:
    query = (
        select(TripUser)
        .filter(TripUser.trip_id == trip_id)
    )

    result = await db.execute(query)
    trip_objects = result.scalars().all()

    return [trip_object.user_id for trip_object in trip_objects]


async def book(user: UserScheme, trip_id: int, db: AsyncSession) -> TripScheme:
    try:
        trip = await trip_crud.get(trip_id, db)

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


async def delete_book(user: UserScheme, trip_id: int, db: AsyncSession) -> None:
    try:
        query = select(TripUser).filter(TripUser.user_id == user.user_id).filter(TripUser.trip_id == trip_id)

        result = await db.execute(query)

        link = result.scalars().first()
        if not link:
            raise BookNotFoundError

        await db.delete(link)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise e


async def delete_trip(user: UserScheme, trip_delete: TripScheme, db: AsyncSession) -> bool:
    try:
        await db.begin()

        query = (select(TripUser)
                 .filter(TripUser.user_id == user.user_id)
                 .filter(TripUser.trip_id == trip_delete.trip_id))

        result = await db.execute(query)
        trip_user = result.scalars().all()

        if not trip_user:
            await db.rollback()
            raise UserTripNotFoundError(user.user_id, trip_delete.trip_id)

        for trip in trip_user:
            await db.delete(trip)
        await trip_crud.delete(trip_delete, db)

        await db.execute(
            delete(car_trip_association).where(
                car_trip_association.c.trip_id == trip_delete.trip_id
            )
        )

        await db.commit()
        return True

    except Exception as e:
        await db.rollback()
        raise e


async def get_user_trips(user: UserScheme, db: AsyncSession) -> List[TripScheme]:
    query = (
        select(Trip)
        .join(TripUser)
        .filter(TripUser.user_id == user.user_id)
    )

    result = await db.execute(query)
    trips_objects = result.scalars().all()

    ids = [trip.trip_id for trip in trips_objects]

    return [await trip_crud.get(trip_id, db) for trip_id in ids]


async def get_upcoming_user_trips(user, timestamp, db):
    user_trips = await get_user_trips(user, db)

    upcoming_trips = [trip for trip in user_trips if trip.start_timestamp > timestamp]
    return upcoming_trips


async def get_trip_number(user_id, db):
    counter = 0
    query = (
        select(TripUser.trip_id)
        .filter(TripUser.user_id == user_id)
    )

    result = await db.execute(query)

    user_trips = result.scalars().all()

    for trip_id in user_trips:
        if await get_trip_creator_id(trip_id, db) == user_id:
            counter += 1
    return counter
