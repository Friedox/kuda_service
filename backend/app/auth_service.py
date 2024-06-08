import bcrypt
import redis.asyncio as redis
from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import InvalidSessionError, InvalidCredentialsError
from .schemas import CreateUserScheme, CredentialsScheme
import random
import hashlib
from .config import REDIS_HOST, SESSION_EXPIRE_TIME
from .crud import UserCrud

redis_client = redis.from_url(f'redis://{REDIS_HOST}')


async def register_user(user_create: CreateUserScheme, db: AsyncSession) -> dict:
    await UserCrud.create(user_create, db)

    return {"message": "User registered successfully"}


async def login_user(user_login: CredentialsScheme, db: AsyncSession) -> dict:
    user_data = await authenticate_user(user_login, db)
    session_id = await create_session(user_data.user_id, user_data.username)

    return {"message": "Logged in successfully", "session_id": session_id}


async def authenticate_user(credentials: CredentialsScheme, db: AsyncSession):
    user_data = await UserCrud.get(credentials.login, db)
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user_data.password_hash):
        raise InvalidCredentialsError

    return user_data


async def create_session(user_id: int, username: str):
    session_id = hashlib.sha256(f"{user_id}{random.random()}".encode()).hexdigest()
    user_data = {
        "username": username,
        "user_id": user_id
    }
    await redis_client.hset(f"session:{session_id}", mapping=user_data)
    await redis_client.expire(f"session:{session_id}", SESSION_EXPIRE_TIME)

    return session_id


async def protected(request: Request, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")

    return {"message": "This user can connect to a protected endpoint after successfully authenticated", "user": user}


async def get_user_from_session_id(request: Request, db: AsyncSession):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise InvalidSessionError

    username = await redis_client.hget(f"session:{session_id}", "username")
    if not username:
        raise InvalidSessionError
    user_data = await UserCrud.get(username.decode('utf-8'), db)

    return user_data


async def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or not await redis_client.exists(f"session:{session_id}"):
        raise InvalidSessionError
    return session_id


async def logout(request: Request):
    session_id = await get_session_id(request)
    await redis_client.delete(f"session:{session_id}")
    return {"message": "Logged out successfully", "session_id": session_id}
