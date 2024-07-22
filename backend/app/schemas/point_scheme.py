from pydantic import BaseModel


class RequestPointScheme(BaseModel):
    latitude: float
    longitude: float


class CreatePointScheme(RequestPointScheme):
    address: dict


class PointScheme(CreatePointScheme):
    point_id: int


class PathRequestScheme(BaseModel):
    pick_up: RequestPointScheme
    drop_off: RequestPointScheme
