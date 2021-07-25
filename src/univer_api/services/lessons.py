from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.groups import Subgroup
from ..models.lessons import Parity


class LessonsService:
    parity_exclusion_dict = {
        Parity.NUMERATOR.value: Parity.DENOMINATOR.value,
        Parity.DENOMINATOR.value: Parity.NUMERATOR.value,
    }

    subgroup_exclusion_dict = {
        Subgroup.FIRST_GROUP.value: Subgroup.SECOND_GROUP.value,
        Subgroup.SECOND_GROUP.value: Subgroup.FIRST_GROUP.value,
    }

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self,
                 day: Optional[int],
                 parity: Optional[int],
                 group: Optional[str],
                 subgroup: Optional[int],
                 kind: Optional[str]) -> list[tables.Lesson]:
        query = self.session.query(tables.Lesson)

        if day is not None:
            query = query.filter(tables.Lesson.day == day)

        if parity is not None and parity != Parity.ALWAYS:
            parity_to_exclude = self.exclude_parity(parity)
            query = query.filter(tables.Lesson.parity != parity_to_exclude)

        if kind is not None:
            query = query.filter(tables.Lesson.kind == kind)

        if group is not None:
            query = query.join(tables.Lesson.group).filter(tables.Group.name == group)
            if subgroup is not None and subgroup != Subgroup.BOTH:
                subgroup_to_exclude = self.exclude_subgroup(subgroup)
                query = query.filter(tables.Subject.subgroup != subgroup_to_exclude)

        return query.all().order_by(tables.Lesson.day.asc())

    # TODO придумать что-то поумнее?
    def exclude_parity(self, parity: int) -> Optional[int]:
        return self.parity_exclusion_dict[parity]

    def exclude_subgroup(self, subgroup: int) -> int:
        return self.subgroup_exclusion_dict[subgroup]
