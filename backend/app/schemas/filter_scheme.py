from typing import List, Optional

from pydantic import BaseModel
from .point_scheme import PointScheme, CreatePointScheme


class FilterScheme(BaseModel):
    pickup: Optional[CreatePointScheme] = None
    pickup_range: Optional[int] = None
    dropoff: Optional[CreatePointScheme] = None
    dropoff_range: Optional[int] = None

    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    tags: Optional[List[str]] = None
