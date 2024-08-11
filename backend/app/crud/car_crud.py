from sqlalchemy import insert, select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import CarNotFoundError, UserNotAllowedError
from models import Car
from models.car_model import user_car_association
from models.trip_model import car_trip_association
from schemas.car_scheme import RequestCarScheme, CarScheme


async def create(user_id: int, car_create: RequestCarScheme, db: AsyncSession) -> CarScheme:
    try:
        new_car = Car(
            model=car_create.model,
            number=car_create.number,
            region_number=car_create.region_number
        )
        db.add(new_car)
        await db.flush()
        stmt = insert(user_car_association).values(user_id=user_id, car_id=new_car.car_id)
        await db.execute(stmt)

        await db.commit()

        await db.refresh(new_car)

        car = CarScheme(**new_car.__dict__)

        return car

    except SQLAlchemyError as e:
        print(123)
        await db.rollback()
        raise e


async def get(car_id: int, db: AsyncSession) -> CarScheme:
    car = (await db.execute(select(Car).where(Car.car_id == car_id))).scalars().first()

    if car is None:
        raise CarNotFoundError(car_id=car_id)

    car_scheme: CarScheme = CarScheme(**car.__dict__)

    return car_scheme


async def delete_car(user_id: int, car_id: int, db: AsyncSession) -> None:
    try:
        user_car = (
            await db.execute(
                select(user_car_association).where(
                    user_car_association.c.user_id == user_id,
                    user_car_association.c.car_id == car_id
                )
            )
        ).first()

        if user_car is None:
            raise UserNotAllowedError

        await db.execute(
            delete(user_car_association).where(
                user_car_association.c.user_id == user_id,
                user_car_association.c.car_id == car_id
            )
        )

        car_to_delete = (
            await db.execute(select(Car).where(Car.car_id == car_id))
        ).scalars().first()

        if car_to_delete is None:
            raise CarNotFoundError(car_id=car_id)

        await db.delete(car_to_delete)

        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_user_cars(user_id: int, db: AsyncSession) -> list[CarScheme]:
    try:
        result = await db.execute(
            select(Car).join(user_car_association).where(user_car_association.c.user_id == user_id)
        )

        cars = result.scalars().all()

        car_schemes = [CarScheme(**car.__dict__) for car in cars]

        return car_schemes

    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_trip_car(trip_id: int, db: AsyncSession) -> CarScheme:
    result = await db.execute(
        select(Car)
        .join(car_trip_association)
        .where(car_trip_association.c.trip_id == trip_id)
    )

    car = result.scalars().first()

    if car is None:
        raise CarNotFoundError

    car_scheme = CarScheme.from_orm(car)

    return car_scheme
