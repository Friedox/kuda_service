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


class TripNotFoundError(ValueError):
    def __init__(self):
        super().__init__(f"Trip not found")


class UserTripNotFoundError(ValueError):
    def __init__(self, user_id, trip_id):
        super().__init__(f"User {user_id} do not have trip {trip_id}")


class UnexpectedError(ValueError):
    def __init__(self, operation: str):
        super().__init__(f"Unexpected error while operation: {operation}")


exceptions_list = (TripNotFoundError,
                   UserNotFoundError,
                   EmailInUseError,
                   UsernameInUseError,
                   InvalidCredentialsError,
                   InvalidSessionError,
                   UnexpectedError,
                   UserTripNotFoundError
                   )
