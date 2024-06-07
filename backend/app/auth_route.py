from fastapi import APIRouter

from fastapi import Request

from schemas import UserScheme, CreateUserScheme
from response_service import ResponseService
import auth_service

router = APIRouter()


@router.post("/signup", tags=["auth"])
async def sign_up(user: CreateUserScheme):
    return await ResponseService.response(
        auth_service.register_user(user)
    )


# Login endpoint - Creates a new session
@router.post("/login")
async def login(user: CreateUserScheme):
    return await ResponseService.response(
        auth_service.login_user(user)
    )


# Get current user endpoint - Returns the user corresponding to the session ID
@router.get("/getusers/me")
async def read_current_user(request: Request):
    return await ResponseService.response(
        auth_service.get_authenticated_user_from_session_id(request)
    )


@router.get("/protected")
async def protected_endpoint(request: Request):
    return await ResponseService.response(
        auth_service.protected(request)
    )


@router.post("/logout")
async def logout(request: Request):
    return await ResponseService.response(
        auth_service.logout(request)
    )
