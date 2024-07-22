from typing import List

from pydantic import BaseModel

from .point_scheme import PointScheme, CreatePointScheme, RequestPointScheme


class RequestTripScheme(BaseModel):
    pickup: RequestPointScheme
    dropoff: RequestPointScheme
    start_timestamp: int
    end_timestamp: int
    fare: int
    tags: List[str]
    available_sits: int
    driver_phone: str
    driver_tg: str
    car_number: str
    car_type: str


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
    driver_phone: str
    driver_tg: str
    car_number: str
    car_type: str
    is_active: bool
    travel_time: float


class TripTagsScheme(TripScheme):
    tags: List[str]


class TripResponseScheme(TripTagsScheme):
    creator_id: int
    trip_users: list[int]
