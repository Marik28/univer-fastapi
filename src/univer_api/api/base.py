from typing import Optional

import sqlalchemy.orm

from univer_api import tables
from univer_api.models.groups import Subgroup


class GroupFilterHelper:
    subgroup_exclusion_dict = {
        Subgroup.FIRST_GROUP.value: Subgroup.SECOND_GROUP.value,
        Subgroup.SECOND_GROUP.value: Subgroup.FIRST_GROUP.value,
    }

    def exclude_subgroup(self, subgroup: str) -> int:
        return self.subgroup_exclusion_dict[subgroup]

    def filter_group_and_subgroup(self, query: sqlalchemy.orm.Query, group: Optional[str], subgroup: Optional[str]):
        if group is not None:
            query = query.filter(tables.Group.name == group)
            if subgroup is not None and subgroup != Subgroup.BOTH:
                subgroup_to_exclude = self.exclude_subgroup(subgroup)
                query = query.filter(tables.Lesson.subgroup != subgroup_to_exclude)
        return query
