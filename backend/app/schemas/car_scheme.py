from pydantic import BaseModel


class RequestCarScheme(BaseModel):
    number: str
    region_number: int
    model: str


class CarScheme(RequestCarScheme):
    car_id: int
