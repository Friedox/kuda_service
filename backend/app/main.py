from fastapi import FastAPI
from database import async_engine, create_tables
from auth_route import router
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # await async_engine.connect()
    # await create_tables()
    yield
    # await async_engine.dispose()


app = FastAPI(
    title="Kuda Service API",
    description="N/A",
    version="0.1.0",
    openapi_url="/openapi.json",
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"])],
    lifespan=lifespan
)

app.include_router(router, prefix="/auth", tags=["auth"])
