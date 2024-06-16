from pydantic import BaseModel


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
