from pydantic import BaseModel


class DivisionRead(BaseModel):
    id: int
    division: str
