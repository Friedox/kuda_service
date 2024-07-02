from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import GOOGLE_CLIENT_ID, REDIRECT_URI
from ..database import get_async_db
from ..services import auth_service
from ..services.response_service import ResponseService

router = APIRouter()


@router.get('/login')
async def login_google(request: Request):
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id="
        f"{GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    )


@router.get('/callback')
async def auth_google(code: str, db: AsyncSession = Depends(get_async_db)):
    return await ResponseService.response(
        auth_service.proceed_google(code, db)
    )
