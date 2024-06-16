from pydantic import BaseModel


class CreateTripScheme(BaseModel):
    pickup: str
    dropoff: str
    start_timestamp: str
    end_timestamp: str
    fare: int


class TripScheme(CreateTripScheme):
    trip_id: int
