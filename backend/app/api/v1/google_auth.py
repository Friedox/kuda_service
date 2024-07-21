from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import auth_service
from services.response_service import ResponseService
from config import settings
from models import database_helper

router = APIRouter(tags=["Google Auth"])


@router.get('/login')
async def login_google(request: Request):
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id="
        f"{settings.google.client_id}&redirect_uri="
        f"{settings.google.redirect_uri}&scope=openid%20profile%20email&access_type=offline"
    )


@router.get('/callback')
async def auth_google(code: str, db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        auth_service.proceed_google(code, db)
    )
