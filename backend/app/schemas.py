from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    message: str = None


class SuccessResponse(BaseModel):
    status: str = "ok"
    detail: Any = None


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: Message


class CredentialsScheme(BaseModel):
    login: str
    password: str


class CreateUserScheme(BaseModel):
    email: str
    username: str
    password: str


class UserScheme(BaseModel):
    email: str
    username: str
    password_hash: bytes
    user_id: int
