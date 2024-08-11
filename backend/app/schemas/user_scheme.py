from typing import Optional
from pydantic import BaseModel, EmailStr


class CredentialsScheme(BaseModel):
    login: str
    password: str


class CreateUserScheme(BaseModel):
    email: EmailStr
    username: str
    password: str = None
    phone: str = None
    telegram: str = None
    is_google_account: bool = False


class UserScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    password_hash: Optional[bytes] = None
    phone: str = None
    telegram: str = None
    is_google_account: bool


class UserGetScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    trip_count: int
    phone: str
    telegram: str
    score: float

