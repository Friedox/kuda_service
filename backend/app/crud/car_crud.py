from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from models import Car
from models.car_model import user_car_association
from schemas.car_scheme import RequestCarScheme, CarScheme
from schemas.user_scheme import UserScheme


async def create(user: UserScheme, car_create: RequestCarScheme, db: AsyncSession) -> CarScheme:
    try:
        new_car = Car(
            model=car_create.model,
            number=car_create.number,
            region_number=car_create.region_number
        )
        db.add(new_car)
        await db.flush()
        stmt = insert(user_car_association).values(user_id=user.user_id, car_id=new_car.car_id)
        await db.execute(stmt)

        await db.commit()

        await db.refresh(new_car)

        car = CarScheme(**new_car.__dict__)

        return car

    except SQLAlchemyError as e:
        print(123)
        await db.rollback()
        raise e
