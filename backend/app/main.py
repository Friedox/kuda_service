from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from .database import async_engine, create_tables, insert_fixture_data
from .routes.auth_route import router as auth_router
from .routes.trip_route import router as trip_router
from .routes.google_auth_route import router as google_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_engine.connect()
    await create_tables()
    await insert_fixture_data()
    yield
    await async_engine.dispose()


app = FastAPI(
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

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

app.include_router(google_auth_router, prefix="/api/auth/google", tags=["google"])

app.include_router(trip_router, prefix="/api/trip", tags=["trip"])
