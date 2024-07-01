from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from . import tag_service
from ..crud import trip_crud, trip_user_crud, trip_tag_crud
from ..exceptions import UnexpectedError
from ..schemas.trip_scheme import CreateTripScheme, TripScheme
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


async def get_all(request: Request, db: AsyncSession) -> List[TripScheme]:
    user = await get_user_from_session_id(request, db)

    return await trip_user_crud.get_all(user, db)
