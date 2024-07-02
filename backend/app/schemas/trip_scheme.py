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


class TripScheme(BaseModel):
    pickup: PointScheme
    dropoff: PointScheme
    start_timestamp: int
    end_timestamp: int
    fare: int
    trip_id: int


class TripTagsScheme(TripScheme):
    tags: List[str]
