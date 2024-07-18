from fastapi import APIRouter, Depends

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.filter_scheme import FilterScheme
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


@router.delete("/delete", tags=["trip"])
async def delete(trip_id: int, request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.delete(trip_id, request, db)
    )


@router.get("/get_user_trips", tags=["trip"])
async def get_all(request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.get_user_trips(request, db)
    )


@router.get("/get_available_tags", tags=["trip"])
async def get_available_tags(db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        tag_service.get_available_tags(db)
    )


@router.post("/get_filtered", tags=["trip"])
async def get_filtered(trip_filter: FilterScheme, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.get_filtered(trip_filter, db)
    )


@router.get("/get_upcoming", tags=["trip"])
async def get_upcoming(request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        trip_service.get_upcoming(request, db)
    )


@router.get("/convert_coords", tags=["trip"])
async def create(latitude: float, longitude: float):
    return await ResponseService.response(
        trip_service.convert_coords(latitude, longitude)
    )
