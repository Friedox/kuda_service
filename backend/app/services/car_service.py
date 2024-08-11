from sqlalchemy.ext.asyncio import AsyncSession

from crud import car_crud
from schemas.car_scheme import RequestCarScheme
from services.auth_service import get_user_from_session_id


async def create(car_create: RequestCarScheme, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    car = await car_crud.create(user, car_create, db)

    return {
        "message": "Car created successfully",
        "trip_id": car.car_id
    }
