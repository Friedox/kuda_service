from fastapi import APIRouter, Depends

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import trip_service, tag_service
from ..database import get_async_db
from ..schemas.trip_scheme import CreateTripScheme
from ..services.response_service import ResponseService

router = APIRouter()


@router.post("/create", tags=["trip"])
async def create(trip: CreateTripScheme, request: Request,
                 db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.create(trip, request, db)
    )


@router.post("/delete", tags=["trip"])
async def delete(trip_id: int, request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.delete(trip_id, request, db)
    )


@router.get("/get_all", tags=["trip"])
async def get_all(request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.get_all(request, db)
    )


@router.get("/get_available_tags", tags=["trip"])
async def get_available_tags(db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        tag_service.get_available_tags(db)
    )
