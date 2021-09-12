import datetime
from typing import Optional

from pydantic import BaseModel

from .groups import Group, Subgroup
from .subjects import Subject


class BaseAssignments(BaseModel):
    subject: Subject
    complete_before: datetime.date
    description: Optional[str]
    title: str
    is_important: bool
    group: Group
    subgroup: Subgroup


class Assignment(BaseAssignments):
    id: int

    class Config:
        orm_mode = True
