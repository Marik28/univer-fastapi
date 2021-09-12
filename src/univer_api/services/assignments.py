from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session


class AssignmentsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(
            self,
            group: Optional[str] = None,
            subgroup: Optional[int] = None,
            subject: Optional[str] = None,
    ) -> list[tables.Assignment]:
        query = self.session.query(tables.Assignment).join(tables.Assignment.group).join(tables.Assignment.subject)

        if group is not None:
            query = query.filter(tables.Group.name == group)

        if subject is not None:
            query = query.filter(tables.Subject.name == subject)

        return query.order_by(tables.Group.name.asc(), tables.Assignment.complete_before.asc()).all()
