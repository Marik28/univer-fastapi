from typing import Optional

import sqlalchemy.orm
from fastapi import Depends

from .. import tables
from ..database import get_session


class SubjectsService:
    def __init__(self, session: sqlalchemy.orm.Session = Depends(get_session)):
        self.session = session

    def get_list(self, with_links_only: Optional[bool], group: Optional[str]) -> list[tables.Subject]:
        query = (
            self.session.query(tables.Subject)
                .join(tables.Lesson)
                .join(tables.Lesson.group)
                .filter(tables.Group.name == group)
        )
        if with_links_only:
            query = query.join(tables.Subject.useful_links)
        return query.all()
