from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session


class GroupsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> list[tables.Group]:
        groups = self.session.query(tables.Group).order_by(tables.Group.name.asc()).all()
        return groups
