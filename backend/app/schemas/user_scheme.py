from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class CredentialsScheme(BaseModel):
    login: str
    password: str


class CreateUserScheme(BaseModel):
    email: EmailStr
    username: str
    password: str = None
    is_google_account: bool = False


class UserScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    password_hash: Optional[bytes] = None
    is_google_account: bool


class UserGetScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
