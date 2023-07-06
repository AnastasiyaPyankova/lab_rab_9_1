from fastapi import APIRouter, Depends
# from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Position
from app.modules.positions.schema import PositionRead

router = APIRouter(prefix='/position')


@router.post('/create', status_code=status.HTTP_200_OK)
def add_position(
        position: str,
        db: Session = Depends(get_session)):
    new_position = Position(position=position)

    try:
        db.add(new_position)
        db.commit()
    except IntegrityError:
        db.rollback()
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return new_position.to_dict()


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_position(
        id: int,
        db: Session = Depends(get_session)):
    get_position = db.get(Position, id)

    if not get_position:
        return status.HTTP_404_NOT_FOUND

    return get_position.to_dict()


@router.delete('/delete', response_model=PositionRead, status_code=status.HTTP_200_OK)
def delete_position(
        id: int,
        db: Session = Depends(get_session)):
    del_position = db.get(Position, id)

    try:
        db.delete(del_position)
        db.commit()
    except IntegrityError:
        db.rollback()
    return 'Success delete'
