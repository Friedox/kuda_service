from typing import List

from pydantic import BaseModel

from .point_scheme import PointScheme, CreatePointScheme


class CreateTripScheme(BaseModel):
    pickup: CreatePointScheme
    dropoff: CreatePointScheme
    start_timestamp: int
    end_timestamp: int
    fare: int
    tags: List[str]
    available_sits: int
    driver_phone: str
    driver_tg: str
    car_number: str
    car_type: str


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


class TripTagsScheme(TripScheme):
    tags: List[str]

