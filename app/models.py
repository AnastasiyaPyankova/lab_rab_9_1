from sqlalchemy import inspect, Integer, Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.core.db import Base


class BaseMixin(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in
                inspect(self).mapper.column_attrs}


class Employee(BaseMixin):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    surname = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    patronymic = Column(String(30), nullable=False)
    address = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)


class Position(BaseMixin):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    position = Column(String(50), nullable=False)


class Division(BaseMixin):
    __tablename__ = 'divisions'

    id = Column(Integer, primary_key=True)
    division = Column(String, nullable=False)


class Job(BaseMixin):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('Employee')
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=True)
    position = relationship('Position')
    division_id = Column(Integer, ForeignKey('divisions.id'), nullable=True)
    division = relationship('Division')
    date_of_employment = Column(Date, nullable=False)
    date_of_dismissal = Column(Date, nullable=True)
