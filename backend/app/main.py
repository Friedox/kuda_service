from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router_api_v1
from config import settings
from models import database_helper


# from .database import async_engine, create_tables, insert_fixture_data
# from .api.auth_route import router as auth_router
# from .api.trip_route import router as trip_router
# from .api.google_auth_route import router as google_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database_helper.dispose()


main_app = FastAPI(
    title="Kuda Service API",
    description="N/A",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    middleware=[Middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3001", "http://localhost:3000", "https://kuda-trip.ru", "http://localhost",
                       "http://kuda-trip.ru"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )],
    lifespan=lifespan
)

main_app.include_router(router_api_v1, prefix=settings.api.prefix)
# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
#
# app.include_router(google_auth_router, prefix="/api/auth/google", tags=["google"])
#
# app.include_router(trip_router, prefix="/api/trips", tags=["trip"])

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
