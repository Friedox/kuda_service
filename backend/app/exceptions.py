class UserAlreadyExistsError(ValueError):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")


class InvalidSessionError(ValueError):
    def __init__(self):
        super().__init__(f"Invalid session ID")


class InvalidCredentialsError(ValueError):
    def __init__(self):
        super().__init__(f"Invalid credentials")
