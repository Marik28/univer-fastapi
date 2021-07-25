from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session


class TeachersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> list[tables.Teacher]:
        teachers = self.session.query(tables.Teacher).order_by(tables.Teacher.second_name.asc()).all()
        return teachers
