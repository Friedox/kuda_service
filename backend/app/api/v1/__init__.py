from fastapi import APIRouter

from config import settings
from .trips import router as trips_router
from .auth import router as auth_router
from .google_auth import router as auth_google_router
from .chat import router as chat_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)
router.include_router(
    trips_router,
    prefix=settings.api.v1.trips
)

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth
)

router.include_router(
    auth_google_router,
    prefix=settings.api.v1.google
)

router.include_router(
    chat_router,
    prefix=settings.api.v1.chat
)
