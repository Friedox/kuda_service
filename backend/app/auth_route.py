from fastapi import APIRouter, Depends

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import auth_service
from .database import get_async_db
from .schemas import UserScheme, CreateUserScheme, CredentialsScheme
from .response_service import ResponseService

router = APIRouter()


@router.post("/signup", tags=["auth"])
async def sign_up(user: CreateUserScheme, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        auth_service.register_user(user, db)
    )


@router.post("/login")
async def login(user: CredentialsScheme, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        auth_service.login_user(user, db)
    )


@router.get("/getusers/me")
async def read_current_user(request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        auth_service.get_user_from_session_id(request, db)
    )


@router.get("/protected")
async def protected_endpoint(request: Request, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        auth_service.protected(request, db)
    )


@router.post("/logout")
async def logout(request: Request):
    return await ResponseService.response(
        auth_service.logout(request)
    )
