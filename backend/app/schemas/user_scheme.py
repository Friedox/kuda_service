from pydantic import BaseModel, EmailStr


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
    is_google_account: bool

    class Config:
        from_attributes = True
