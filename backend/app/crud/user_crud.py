import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import EMAIL_PATTERN
from ..exceptions import UsernameInUseError, EmailInUseError, UserNotFoundError
from ..schemas.user_scheme import CreateUserScheme, UserScheme
from ..models.user_model import User
import bcrypt


async def create(user_create: CreateUserScheme, db: AsyncSession) -> UserScheme:
    async def check_username(username: str):
        query = select(User).filter(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            raise UsernameInUseError

    async def check_email(email: str):
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            raise EmailInUseError

    await check_username(user_create.username)
    await check_email(user_create.email)

    hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        email=user_create.email,
        username=user_create.username,
        password_hash=hashed_password
    )

    db.add(new_user)
    await db.flush()
    await db.commit()

    user_scheme = UserScheme(**new_user.__dict__)

    return user_scheme


async def get(param, db: AsyncSession) -> UserScheme:
    if type(param) is int:
        query = select(User).filter(User.user_id == param)
    else:
        if re.match(EMAIL_PATTERN, param) is not None:
            query = select(User).filter(User.email == param)
        else:
            query = select(User).filter(User.username == param)

    result = await db.execute(query)
    user = result.scalars().first()

    if user:
        user_scheme = UserScheme(**user.__dict__)
        return user_scheme
    else:
        raise UserNotFoundError
