from enum import IntEnum

from pydantic import BaseModel


class BaseGroup(BaseModel):
    name: str


class Group(BaseGroup):
    id: int

    class Config:
        orm_mode = True


class Subgroup(IntEnum):
    FIRST_GROUP = 1
    SECOND_GROUP = 2
    BOTH = 3
