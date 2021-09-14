from typing import Optional

import sqlalchemy.orm
from fastapi import Depends

from .. import tables
from ..database import get_session


class SubjectsService:
    def __init__(self, session: sqlalchemy.orm.Session = Depends(get_session)):
        self.session = session

    def get_list(self, with_links_only: Optional[bool]) -> list[tables.Subject]:
        query = self.session.query(tables.Subject)
        if with_links_only:
            query = query.join(tables.Subject.useful_links)
        return query.all()
