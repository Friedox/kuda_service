from sqlalchemy.ext.asyncio import AsyncSession

from crud import car_crud
from schemas.car_scheme import RequestCarScheme, CarScheme
from services.auth_service import get_user_from_session_id


async def create(car_create: RequestCarScheme, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    car = await car_crud.create(user.user_id, car_create, db)

    return {
        "message": "Car created successfully",
        "trip_id": car.car_id
    }


async def get_user_cars(session_id: str | None, db: AsyncSession) -> list[CarScheme]:
    user = await get_user_from_session_id(session_id=session_id, db=db)

    return await car_crud.get_user_cars(user.user_id, db)


async def get(car_id: int, db: AsyncSession) -> CarScheme:
    car = await car_crud.get(car_id, db)

    return car


async def delete(car_id, session_id, db):
    user = await get_user_from_session_id(session_id=session_id, db=db)

    await car_crud.delete_car(user.user_id, car_id, db)

    return {
        "message": "Car deleted successfully",
        "trip_id": car_id
    }
