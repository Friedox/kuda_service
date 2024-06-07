from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
import random
from fastapi import Request

from exceptions import UserAlreadyExistsError, InvalidSessionError, InvalidCredentialsError
from schemas import UserScheme, CreateUserScheme

# User Database (for demonstration purposes)
users = {}

# In-memory session storage (for demonstration purposes)
sessions = {}


async def create_dicts():
    global users
    global sessions
    users = {}
    sessions = {}


def authenticate_user(credentials: HTTPBasicCredentials):
    user = users.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise InvalidCredentialsError
    return user


def create_session(user_id: int):
    session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = user_id
    return session_id


async def get_authenticated_user_from_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is None or int(session_id) not in sessions:
        raise InvalidSessionError
    # Get the user from the session
    user = get_user_from_session(int(session_id))
    return user


# Use the valid session id to get the corresponding user from the users dictionary
def get_user_from_session(session_id: int):
    user = None
    for user_data in users.values():
        if user_data == sessions.get(session_id):
            user = user_data
            break
    print(user)
    return user


def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is None or int(session_id) not in sessions:
        raise InvalidSessionError
    return int(session_id)


async def register_user(user_create: CreateUserScheme):
    user = users.get(user_create.username)
    if user:
        raise UserAlreadyExistsError(user_create.username)
    new_user_id = len(users) + 1
    new_user = {
        "username": user_create.username,
        "password": user_create.password,
        "user_id": new_user_id
    }
    users[user_create.username] = new_user
    return {"message": "User registered successfully"}


async def login_user(user_login: CreateUserScheme):
    user = users.get(user_login.username)
    print(1111)
    print(user)
    if user is None or user["password"] != user_login.password:
        raise InvalidCredentialsError
    session_id = create_session(users[user_login.username])
    return {"message": "Logged in successfully", "session_id": session_id}


async def protected(request: Request):
    user = await get_authenticated_user_from_session_id(request)

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return {"message": "This user can connect to a protected endpoint after successfully autheticated", "user": user}


async def logout(request: Request):
    session_id = get_session_id(request)

    if session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    sessions.pop(session_id)
    return {"message": "Logged out successfully", "session_id": session_id}
