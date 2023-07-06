from pydantic import BaseModel
from datetime import *


class EmployeeRead(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    address: str
    date_of_birth: date


class EmployeeUpdate(BaseModel):
    surname: str
    name: str
    patronymic: str
    address: str
    date_of_birth: date
