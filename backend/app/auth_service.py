import redis.asyncio as redis
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBasicCredentials
from exceptions import UserAlreadyExistsError, InvalidSessionError, InvalidCredentialsError
from schemas import CreateUserScheme
import random
import hashlib

# Initialize Redis client
redis_client = redis.from_url("redis://localhost")


async def create_dicts():
    # No need to create dictionaries, since we're using Redis
    pass


async def authenticate_user(credentials: HTTPBasicCredentials):
    user_data = await redis_client.hgetall(f"user:{credentials.username}")
    if not user_data:
        raise InvalidCredentialsError

    # Decode byte strings to regular strings
    user_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in user_data.items()}

    if user_data["password"] != credentials.password:
        raise InvalidCredentialsError
    return user_data


async def create_session(user_id: str, username: str):
    session_id = hashlib.sha256(f"{user_id}{random.random()}".encode()).hexdigest()

    user_data = {
        "username": username,
        "user_id": user_id
    }

    await redis_client.hset(f"session:{session_id}", mapping=user_data)
    return session_id


async def get_authenticated_user_from_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise InvalidSessionError

    user = await redis_client.hget(f"session:{session_id}", "username")
    if not user:
        raise InvalidSessionError
    user_data = await get_user_from_session(user)
    return user_data


async def get_user_from_session(user):
    user_data = await redis_client.hgetall(f"user:{user.decode('utf-8')}")
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Decode byte strings to regular strings
    user_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in user_data.items()}

    return user_data


async def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or not await redis_client.exists(f"session:{session_id}"):
        raise InvalidSessionError
    return session_id


async def register_user(user_create: CreateUserScheme):
    user_exists = await redis_client.exists(f"user:{user_create.username}")
    if user_exists:
        raise UserAlreadyExistsError(user_create.username)
    user_id = hashlib.sha256(user_create.username.encode()).hexdigest()
    user_data = {
        "username": user_create.username,
        "password": user_create.password,
        "user_id": user_id
    }
    await redis_client.hset(f"user:{user_create.username}", mapping=user_data)
    return {"message": "User registered successfully"}


async def login_user(user_login: CreateUserScheme):
    user_data = await redis_client.hgetall(f"user:{user_login.username}")
    if not user_data:
        raise InvalidCredentialsError

    # Decode byte strings to regular strings
    user_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in user_data.items()}

    if user_data["password"] != user_login.password:
        raise InvalidCredentialsError

    session_id = await create_session(user_data["user_id"], user_login.username)
    return {"message": "Logged in successfully", "session_id": session_id}


async def protected(request: Request):
    user = await get_authenticated_user_from_session_id(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return {"message": "This user can connect to a protected endpoint after successfully authenticated", "user": user}


async def logout(request: Request):
    session_id = await get_session_id(request)
    await redis_client.delete(f"session:{session_id}")
    return {"message": "Logged out successfully", "session_id": session_id}
