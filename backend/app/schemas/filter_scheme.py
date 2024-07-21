from typing import List, Optional

from pydantic import BaseModel
from .point_scheme import PointScheme, CreatePointScheme, RequestPointScheme


class FilterScheme(BaseModel):
    pickup: Optional[RequestPointScheme] = None
    pickup_range: Optional[int] = None
    dropoff: Optional[RequestPointScheme] = None
    dropoff_range: Optional[int] = None

    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    tags: Optional[List[str]] = None
