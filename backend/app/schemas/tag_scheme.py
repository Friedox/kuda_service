from pydantic import BaseModel


class TagScheme(BaseModel):
    tag_id: int
    tag: str
