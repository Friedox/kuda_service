from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from models import database_helper
from schemas.car_scheme import RequestCarScheme
from services import car_service
from services.response_service import ResponseService

router = APIRouter(tags=["Cars"])


@router.post("/")
async def create(car: RequestCarScheme, session_id: str | None = Cookie(default=None),
                 db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        car_service.create(car, session_id, db)
    )
