from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from ..crud import trip_crud, trip_user_crud
from ..exceptions import UnexpectedError
from ..schemas.trip_scheme import CreateTripScheme
from ..services.auth_service import get_user_from_session_id


async def create(trip_create: CreateTripScheme, request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)

    trip = await trip_user_crud.create(user, trip_create, db)

    return {f"message": f"Trip created successfully, id:{trip.trip_id}"}


async def delete(trip_id: int, request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)
    trip_delete = await trip_crud.get(trip_id, db)

    if await trip_user_crud.delete(user, trip_delete, db):
        return {f"message": f"Trip deleted successfully"}
    else:
        raise UnexpectedError(f"Trip deleted")
