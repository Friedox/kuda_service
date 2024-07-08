from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncTransaction, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..crud import user_crud
from ..exceptions import InvalidCredentialsError, EmailInUseError, UsernameInUseError, PassNotSetException, \
    InvalidSessionError
from ..main import app
from ..schemas.user_scheme import CredentialsScheme, CreateUserScheme
from ..services import auth_service
from ..schemas import user_scheme
from ..database import Base
from ..config import TEST_SQLALCHEMY_URL, tags_fixture


async def setup_db() -> AsyncGenerator[AsyncSession, None]:
    test_async_engine = create_async_engine(TEST_SQLALCHEMY_URL, echo=True, future=True)

    async_session = sessionmaker(
        bind=test_async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True
    )

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        from ..crud import tag_crud
        from ..models.tag_model import Tag
        existing_tags = await tag_crud.get_all(session)
        existing_tag_names = {tag.tag for tag in existing_tags}

        for tag_name in tags_fixture:
            if tag_name not in existing_tag_names:
                new_tag = Tag(tag=tag_name)
                session.add(new_tag)

        await session.commit()
        yield session

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_register_user():
    mock_user = CreateUserScheme(
        email="test@mail.com",
        username="test",
        password="test_pass",
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
            await session.close()


@pytest.mark.asyncio
async def test_login_user():
    mock_user = CreateUserScheme(
        email="test@mail.com",
        username="test",
        password="test_pass",
        is_google_account=False
    )

    mock_user_login = CredentialsScheme(
        login="test@mail.com",
        password="test_pass"
    )
    async for session_obj in setup_db():
        async with session_obj as session:
            await auth_service.register_user(mock_user, session)

            result = await auth_service.login_user(mock_user_login, session)
            assert result["message"] == "Logged in successfully"

            with pytest.raises(InvalidCredentialsError):
                mock_user_login.password = "invalid_pass"
                await auth_service.login_user(mock_user_login, session)

            await session.close()


@pytest.mark.asyncio
async def test_logout():
    async for session_obj in setup_db():
        async with session_obj as session:
            mock_user = CreateUserScheme(
                email="test@mail.com",
                username="test",
                password="test_pass",
                is_google_account=False
            )

            mock_user_login = CredentialsScheme(
                login="test@mail.com",
                password="test_pass"
            )

            await auth_service.register_user(mock_user, session)
            session_id = (await auth_service.login_user(mock_user_login, session))["session_id"]

            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = session_id

            logout_message = await auth_service.logout(mock_request)
            assert logout_message == {"message": "Logged out successfully"}
            await session.close()


@pytest.mark.asyncio
async def test_get_info():
    async for session_obj in setup_db():
        async with session_obj as session:
            mock_user = CreateUserScheme(
                email="test@mail.com",
                username="test",
                password="test_pass",
                is_google_account=False
            )

            mock_user_login = CredentialsScheme(
                login="test@mail.com",
                password="test_pass"
            )

            await auth_service.register_user(mock_user, session)
            session_id = (await auth_service.login_user(mock_user_login, session))["session_id"]

            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = session_id

            info = await auth_service.get_info(mock_request, session)

            assert info.username == mock_user.username
            assert info.email == mock_user.email
            await session.close()


@pytest.mark.asyncio
async def test_invalid_session():
    async for session_obj in setup_db():
        async with session_obj as session:
            mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
            mock_request.cookies["session_id"] = "invalid_session_id"

            with pytest.raises(InvalidSessionError):
                await auth_service.get_session_id(mock_request)

            with pytest.raises(InvalidSessionError):
                mock_request = Request(scope={"type": "http", "method": "GET", "headers": {}})
                await auth_service.get_user_from_session_id(mock_request, session)
            await session.close()
