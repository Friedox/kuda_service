from pydantic import BaseModel, conint, constr


class ReviewRequestScheme(BaseModel):
    trip_id: int
    score: conint(ge=0, le=5)
    text: constr(max_length=250)


class ReviewScheme(ReviewRequestScheme):
    review_id: int
