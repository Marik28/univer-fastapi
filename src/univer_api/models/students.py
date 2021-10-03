from typing import Optional

from pydantic import BaseModel

from .groups import Group, Subgroup


class BaseStudent(BaseModel):
    telegram_id: Optional[int]
    subgroup: Subgroup


class StudentCreate(BaseStudent):
    group_name: str


class StudentUpdate(BaseModel):
    group_name: str
    subgroup: Subgroup


class Student(BaseStudent):
    id: int
    group: Group

    class Config:
        orm_mode = True
