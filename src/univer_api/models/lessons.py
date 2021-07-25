from datetime import time
from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel

from .subjects import Subject
from .teachers import Teacher


class Building(IntEnum):
    """Корпус университета"""
    MAIN = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class BaseClassRoom(BaseModel):
    """Аудитория"""
    number: int
    building: Building


class ClassRoom(BaseClassRoom):
    id: int

    class Config:
        orm_mode = True


class WeekDay(IntEnum):
    """День недели"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Parity(IntEnum):
    """Четность недели"""
    NUMERATOR = 1
    DENOMINATOR = 2
    ALWAYS = 3


class LessonKind(str, Enum):
    """Тип пары"""
    LECTURE = 'Лекция'
    LAB = 'Лабораторное занятие'
    SEMINAR = 'Семинар'
    SRSP = 'СРСП'
    SRS = 'СРС'
    CURATORIAL_HOUR = 'Кураторский час'


class BaseLesson(BaseModel):
    subject: Subject
    kind: LessonKind
    day: WeekDay
    parity: Parity
    time: time
    teacher: Teacher
    classroom: Optional[ClassRoom]


class Lesson(BaseLesson):
    id: int

    class Config:
        orm_mode = True
