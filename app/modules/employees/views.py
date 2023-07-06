from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from datetime import date

from app.core.db import get_session
from app.models import Employee
from app.modules.employees.schema import EmployeeRead, EmployeeUpdate

router = APIRouter(prefix='/employee')


@router.post('/add', response_model=EmployeeRead, status_code=status.HTTP_200_OK)
def add_employee(
        surname: str,
        name: str,
        patronymic: str,
        address: str,
        date_of_birth: date,
        db: Session = Depends(get_session)
):
    employee = Employee(surname=surname, name=name,
                        patronymic=patronymic, address=address,
                        date_of_birth=date_of_birth)

    try:
        db.add(employee)
        db.commit()
    except IntegrityError:
        db.rollback()
        return "status.HTTP_500_INTERNAL_SERVER_ERROR"

    return employee.to_dict()


@router.put('/put', status_code=status.HTTP_200_OK)
def put_employee(
        id: int,
        data: EmployeeUpdate,
        db: Session = Depends(get_session)
):
    employee = db.get(Employee, id)

    values = data.dict()
    employee.update(**values)

    try:
        db.add(employee)
        db.commit()
    except IntegrityError:
        db.rollback()

    return employee.to_dict()


@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_employees(
        name: str = None,
        db: Session = Depends(get_session)
):
    query = select(Employee)

    if name:
        query = query.where(Employee.name == name)

    all_emp = db.scalars(query).all()

    return [employee.to_dict() for employee in all_emp]


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_employee(
        id: int,
        db: Session = Depends(get_session)
):
    employee = db.get(Employee, id)

    if not employee:
        return status.HTTP_404_NOT_FOUND
    return employee.to_dict()


@router.delete('/delete', response_model=EmployeeRead, status_code=status.HTTP_200_OK)
def delete_employee(
        id: int,
        db: Session = Depends(get_session)
):
    employee = db.get(Employee, id)

    try:
        db.delete(employee)
        db.commit()
    except IntegrityError:
        db.rollback()
    return "Success delete"
