from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import InvalidCredentialsError, EmailInUseError, UsernameInUseError, InvalidSessionError
from models.db_helper import test_database_helper
from schemas.user_scheme import CredentialsScheme, CreateUserScheme
from services import auth_service


async def setup_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = test_database_helper.session_factory

    async with async_session() as session:
        yield session
    await test_database_helper.dispose()


@pytest.mark.asyncio
async def test_register_user():
    mock_user = CreateUserScheme(
        email="test@mail.com",
        username="test",
        password="test_pass",
        telegram="test_tg",
        phone="+77777777777",
        is_google_account=False
    )

    async for session_obj in setup_db():
        async with session_obj as session:
            result = await auth_service.register_user(mock_user, session)
            assert result == {"message": "User registered successfully"}

            with pytest.raises(UsernameInUseError):
                await auth_service.register_user(mock_user, session)

            with pytest.raises(EmailInUseError):
                mock_user.username = "new_username"
                await auth_service.register_user(mock_user, session)


@pytest.mark.asyncio
async def test_login_user():
    mock_user_login = CredentialsScheme(
        login="test@mail.com",
        password="test_pass"
    )
    async for session_obj in setup_db():
        async with session_obj as session:
            result = await auth_service.login_user(mock_user_login, session)
            assert result["message"] == "Logged in successfully"

            with pytest.raises(InvalidCredentialsError):
                mock_user_login.password = "invalid_pass"
                await auth_service.login_user(mock_user_login, session)


@pytest.mark.asyncio
async def test_logout():
    async for session_obj in setup_db():
        async with session_obj as session:
            mock_user_login = CredentialsScheme(
                login="test@mail.com",
                password="test_pass"
            )

            session_id = (await auth_service.login_user(mock_user_login, session))["session_id"]

            logout_message = await auth_service.logout(session_id)
            assert logout_message == {"message": "Logged out successfully"}


@pytest.mark.asyncio
async def test_get_info():
    async for session_obj in setup_db():
        async with session_obj as session:
            mock_user = CreateUserScheme(
                email="test@mail.com",
                username="test",
                password="test_pass",
                telegram="test_tg",
                phone="+77777777777",
                is_google_account=False
            )

            mock_user_login = CredentialsScheme(
                login="test@mail.com",
                password="test_pass"
            )

            session_id = (await auth_service.login_user(mock_user_login, session))["session_id"]

            info = await auth_service.get_info(session_id, session)

            assert info.username == mock_user.username
            assert info.email == mock_user.email


@pytest.mark.asyncio
async def test_invalid_session():
    async for session_obj in setup_db():
        async with session_obj as session:
            with pytest.raises(InvalidSessionError):
                await auth_service.get_user_from_session_id("invalid_session_id", session)
