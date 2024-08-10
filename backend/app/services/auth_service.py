import hashlib
import random

import bcrypt
import redis.asyncio as redis
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import user_crud, review_crud, trip_user_crud
from exceptions import InvalidSessionError, InvalidCredentialsError, EmailInUseError, UsernameInUseError, \
    GoogleException, PassNotSetException
from schemas.user_scheme import CredentialsScheme, CreateUserScheme, UserScheme, UserGetScheme


async def register_user(user_create: CreateUserScheme, db: AsyncSession) -> dict:
    await user_crud.create(user_create, db)

    return {"message": "User registered successfully"}


async def login_user(user_login: CredentialsScheme, db: AsyncSession) -> dict:
    user_data = await authenticate_user(user_login, db)
    session_id = await create_session(user_data.user_id, user_data.username)

    return {"message": "Logged in successfully", "session_id": session_id}


async def authenticate_user(credentials: CredentialsScheme, db: AsyncSession) -> UserScheme:
    user_data = await user_crud.get(credentials.login, db)

    if user_data.is_google_account:
        await authenticate_google_user(user_data, credentials, db)
    else:
        await authenticate_regular_user(user_data, credentials)

    return user_data


async def authenticate_google_user(user_data: UserScheme, credentials: CredentialsScheme, db: AsyncSession):
    """
    Authenticate a user with a Google account.
    """
    if not await user_crud.check_password(user_data.user_id, db):
        raise PassNotSetException()
    pass_hash = await user_crud.get_hash(user_data.user_id, db)
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), pass_hash):
        raise InvalidCredentialsError()


async def authenticate_regular_user(user_data: UserScheme, credentials: CredentialsScheme):
    """
    Authenticate a user with a regular account.
    """
    if not bcrypt.checkpw(credentials.password.encode('utf-8'), user_data.password_hash):
        raise InvalidCredentialsError()


async def create_session(user_id: int, username: str) -> str:
    session_id = hashlib.sha256(f"{user_id}{random.random()}".encode()).hexdigest()
    user_data = {
        "username": username,
        "user_id": user_id
    }

    redis_client = redis.from_url(f'redis://{settings.redis.host}')
    await redis_client.hset(f"session:{session_id}", mapping=user_data)
    await redis_client.expire(f"session:{session_id}", settings.redis.expire_time)
    await redis_client.aclose()

    return session_id


async def get_info(session_id: str | None, db: AsyncSession):
    print(session_id)
    user = await get_user_from_session_id(session_id=session_id, db=db)
    user.__dict__.pop('password_hash')
    return user


async def get_user_from_session_id(session_id: str | None, db: AsyncSession) -> UserScheme:
    if not session_id:
        raise InvalidSessionError

    async with redis.from_url(f'redis://{settings.redis.host}') as redis_client:
        username = await redis_client.hget(f"session:{session_id}", "username")

    if not username:
        raise InvalidSessionError

    user_data = await user_crud.get(username.decode('utf-8'), db)

    return user_data


async def logout(session_id: str | None):
    async with redis.from_url(f'redis://{settings.redis.host}') as redis_client:
        await redis_client.delete(f"session:{session_id}")

    return {"message": "Logged out successfully"}


async def proceed_google(code: str, db: AsyncSession) -> dict:
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.google.client_id,
        "client_secret": settings.google.client_secret,
        "redirect_uri": settings.google.redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise GoogleException("Failed to fetch token")

    access_token = response.json().get("access_token")
    user_info_response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                      headers={"Authorization": f"Bearer {access_token}"})
    if user_info_response.status_code != 200:
        raise GoogleException("Failed to fetch user info")

    user_info = user_info_response.json()

    try:
        user = await user_crud.create(CreateUserScheme(
            email=user_info["email"],
            username=str(user_info["email"]).split("@")[0],
            is_google_account=True
        ), db)
    except EmailInUseError:
        user = await user_crud.get(user_info["email"], db)
    except UsernameInUseError:
        user = await user_crud.get(user_info["email"].split("@")[0], db)

    session_id = await create_session(user.user_id, user.username)

    return {"message": "Logged in successfully", "session_id": session_id}


async def set_pass(new_pass: str, session_id: str | None, db: AsyncSession) -> dict:
    user = await get_user_from_session_id(session_id, db)
    user_id = user.user_id
    hashed_password = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())

    await user_crud.set_password(user_id, hashed_password, db)
    return {"message": "Password successfully set"}


async def get_user(user_id, db) -> UserGetScheme:
    user = await user_crud.get(user_id, db)
    trip_count = await trip_user_crud.get_trip_number(user_id, db)
    score = await review_crud.get_user_score(user_id, db)
    user_response = UserGetScheme(
        user_id=user.user_id,
        email=user.email,
        username=user.username,
        trip_count=trip_count,
        score=score
    )

    return user_response


async def get_score(user_id: int, db) -> dict:
    score = await review_crud.get_user_score(user_id, db)

    return {"message": score}
