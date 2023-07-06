from pydantic import BaseModel


class PositionRead(BaseModel):
    id: int
    position: str
