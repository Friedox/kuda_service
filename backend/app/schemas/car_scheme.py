from pydantic import BaseModel


class RequestCarScheme(BaseModel):
    number: str
    region_number: int
    model: str

    class Config:
        from_attributes = True


class CarScheme(RequestCarScheme):
    car_id: int
