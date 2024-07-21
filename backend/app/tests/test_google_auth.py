import pytest
from fastapi import Request

from crud import user_crud
from exceptions import PassNotSetException, InvalidCredentialsError, UsernameInUseError
from schemas.user_scheme import CredentialsScheme
from services import auth_service
from schemas import user_scheme
from .test_auth import setup_db

mock_user = user_scheme.CreateUserScheme(
    email="test_google@mail.com",
    username="test_google",
    is_google_account=True
)

mock_login = CredentialsScheme(
    login="test_google",
    password="test_google_pass"
)


@pytest.mark.asyncio
async def test_google_register_user_without_pass():
    async for session_obj in setup_db():
        async with session_obj as session:
            user = await user_crud.create(mock_user, session)
            session_id = await auth_service.create_session(user.user_id, user.username)

            with pytest.raises(PassNotSetException):
                await auth_service.login_user(mock_login, session)
            await session.close()


@pytest.mark.asyncio
async def test_google_set_user_pass():
    async for session_obj in setup_db():
        async with session_obj as session:
            user = await user_crud.get(mock_user.username, session)

            session_id = await auth_service.create_session(user.user_id, user.username)

            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = session_id

            result = await auth_service.set_pass("new_pass", mock_request, session)
            assert result == {'message': 'Password successfully set'}
            await session.close()


@pytest.mark.asyncio
async def test_google_login_with_new_pass():
    async for session_obj in setup_db():
        async with session_obj as session:
            user = await user_crud.get(mock_user.username, session)

            session_id = await auth_service.create_session(user.user_id, user.username)

            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = session_id

            await auth_service.set_pass("new_pass", mock_request, session)

            mock_login.password = "new_pass"

            result = await auth_service.login_user(mock_login, session)
            assert result["message"] == "Logged in successfully"
            await session.close()


@pytest.mark.asyncio
async def test_google_login_with_wrong_pass():
    async for session_obj in setup_db():
        async with session_obj as session:
            user = await user_crud.get(mock_user.username, session)

            session_id = await auth_service.create_session(user.user_id, user.username)

            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = session_id

            await auth_service.set_pass("new_pass", mock_request, session)

            mock_login.password = "incorrect_password"
            with pytest.raises(InvalidCredentialsError):
                await auth_service.login_user(mock_login, session)
            await session.close()
