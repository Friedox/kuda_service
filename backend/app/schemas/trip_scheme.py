from typing import List

from pydantic import BaseModel

from .car_scheme import CarScheme
from .point_scheme import PointScheme, CreatePointScheme, RequestPointScheme
from .user_scheme import UserGetScheme


class RequestTripScheme(BaseModel):
    pickup: RequestPointScheme
    dropoff: RequestPointScheme
    start_timestamp: int
    end_timestamp: int
    fare: int
    tags: List[str]
    available_sits: int
    car_id: int


class CreateTripScheme(RequestTripScheme):
    pickup: CreatePointScheme
    dropoff: CreatePointScheme
    travel_time: float


class TripScheme(BaseModel):
    pickup: PointScheme
    dropoff: PointScheme
    start_timestamp: int
    end_timestamp: int
    fare: int
    trip_id: int
    available_sits: int
    is_active: bool
    travel_time: float


class TripTagsScheme(TripScheme):
    tags: List[str]


class TripResponseScheme(TripTagsScheme):
    car: CarScheme
    creator: UserGetScheme
    trip_users: list[int]


class TripScoreResponseScheme(TripResponseScheme):
    creator_score: float
    creator_username: str
