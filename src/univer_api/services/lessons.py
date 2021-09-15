from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..api.base import GroupFilterHelper
from ..database import get_session
from ..models.lessons import Parity


class LessonsService(GroupFilterHelper):
    parity_exclusion_dict = {
        Parity.NUMERATOR.value: Parity.DENOMINATOR.value,
        Parity.DENOMINATOR.value: Parity.NUMERATOR.value,
    }

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self,
                 day: Optional[int],
                 parity: Optional[int],
                 group: Optional[str],
                 subgroup: Optional[int],
                 kind: Optional[str]) -> list[tables.Lesson]:
        query = self.session.query(tables.Lesson).join(tables.Lesson.group)

        if day is not None:
            query = query.filter(tables.Lesson.day == day)

        if parity is not None and parity != Parity.ALWAYS:
            parity_to_exclude = self.exclude_parity(parity)
            query = query.filter(tables.Lesson.parity != parity_to_exclude)

        if kind is not None:
            query = query.filter(tables.Lesson.kind == kind)

        query = self.filter_group_and_subgroup(query, group, subgroup)

        return query.order_by(tables.Group.name.asc(), tables.Lesson.day.asc(), tables.Lesson.time.asc()).all()

    # TODO придумать что-то поумнее?
    def exclude_parity(self, parity: int) -> Optional[int]:
        return self.parity_exclusion_dict[parity]
