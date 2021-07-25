from pydantic import BaseModel

from .groups import Group, Subgroup


class BaseSubjectName(BaseModel):
    name: str


class SubjectName(BaseSubjectName):
    id: int

    class Config:
        orm_mode = True


class BaseSubject(BaseModel):
    name: SubjectName
    group: Group
    subgroup: Subgroup


class Subject(BaseSubject):
    id: int

    class Config:
        orm_mode = True
