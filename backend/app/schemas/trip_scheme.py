from typing import List

from pydantic import BaseModel


class CreateTripScheme(BaseModel):
    pickup: str
    dropoff: str
    start_timestamp: str
    end_timestamp: str
    fare: int
    tags: List[str]


class TripScheme(BaseModel):
    pickup: str
    dropoff: str
    start_timestamp: str
    end_timestamp: str
    fare: int
    trip_id: int


class TripTagsScheme(TripScheme):
    tags: List[str]
