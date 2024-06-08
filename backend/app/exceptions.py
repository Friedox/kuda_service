class InvalidSessionError(ValueError):
    def __init__(self):
        super().__init__(f"Invalid session ID")


class InvalidCredentialsError(ValueError):
    def __init__(self):
        super().__init__(f"Invalid credentials")


class UsernameInUseError(ValueError):
    def __init__(self):
        super().__init__(f"The username is already taken")


class EmailInUseError(ValueError):
    def __init__(self):
        super().__init__(f"The email is already taken")


class UserNotFoundError(ValueError):
    def __init__(self):
        super().__init__(f"User not found")
