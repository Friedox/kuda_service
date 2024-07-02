from pydantic import BaseModel


class CreatePointScheme(BaseModel):
    latitude: float
    longitude: float


class PointScheme(CreatePointScheme):
    point_id: int
