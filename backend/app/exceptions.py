from fastapi import HTTPException


class InvalidSessionError(ValueError):
    def __init__(self):
        super().__init__("Invalid session ID")


class InvalidCredentialsError(ValueError):
    def __init__(self):
        super().__init__("Invalid credentials")


class UsernameInUseError(ValueError):
    def __init__(self):
        super().__init__("The username is already taken")


class EmailInUseError(ValueError):
    def __init__(self):
        super().__init__("The email is already taken")


class UserNotFoundError(ValueError):
    def __init__(self):
        super().__init__("User not found")


class TripNotFoundError(ValueError):
    def __init__(self):
        super().__init__("Trip not found")


class UserTripNotFoundError(ValueError):
    def __init__(self, user_id, trip_id):
        super().__init__(f"User {user_id} do not have trip {trip_id}")


class UnexpectedError(ValueError):
    def __init__(self, operation: str):
        super().__init__(f"Unexpected error while operation: {operation}")


class InvalidTagException(ValueError):
    def __init__(self, tag: str):
        super().__init__(f"Tag '{tag}' is not a valid tag")


class GoogleException(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class PassNotSetException(ValueError):
    def __init__(self):
        super().__init__('There is no password set for this account. Please set your password in settings')


class PointNotFoundError(ValueError):
    def __init__(self, point_id):
        super().__init__(f"Point {point_id} not found")


class GeocoderServiceError(ValueError):
    def __init__(self, error_message: str):
        super().__init__(f"Error '{error_message}' while trying to geocode")


class UserAlreadyBookedError(ValueError):
    def __init__(self: str):
        super().__init__("User already booked")


class UserNotBookedError(ValueError):
    def __init__(self: str):
        super().__init__("User even not booked yet")


class NotEnoughSitsError(ValueError):
    def __init__(self: str):
        super().__init__("Not enough sits")


class BookNotFoundError(ValueError):
    def __init__(self: str):
        super().__init__("Book not found")


class TripEndedError(ValueError):
    def __init__(self: str):
        super().__init__("Trip already ended")


class UserNotAllowedError(ValueError):
    def __init__(self: str):
        super().__init__("This operation is not allowed for user")


class ReviewNotAllowedError(ValueError):
    def __init__(self: str, text: str):
        super().__init__(f"This operation is not allowed for user, message: {text}")


class FindPathError(ValueError):
    def __init__(self: str):
        super().__init__("Path not found")


exceptions_list = (TripNotFoundError,
                   UserNotFoundError,
                   EmailInUseError,
                   UsernameInUseError,
                   InvalidCredentialsError,
                   InvalidSessionError,
                   UnexpectedError,
                   UserTripNotFoundError,
                   InvalidTagException,
                   GoogleException,
                   PassNotSetException,
                   PointNotFoundError,
                   GeocoderServiceError,
                   UserAlreadyBookedError,
                   NotEnoughSitsError,
                   UserNotBookedError,
                   BookNotFoundError,
                   TripEndedError,
                   UserNotAllowedError,
                   ReviewNotAllowedError,
                   FindPathError
                   )
