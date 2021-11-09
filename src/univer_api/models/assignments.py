import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .groups import Group, Subgroup
from .students import Student
from .subjects import LessonSubject


class BaseAssignments(BaseModel):
    subject: LessonSubject = Field(..., description="Предмет, по которому необходимо выполнить задание")
    complete_before: datetime.date = Field(..., description="Дата, до которой необходимо завершить задание")
    description: Optional[str] = Field(None, title="Описание")
    title: str = Field(..., title="Заголовок")
    is_important: bool
    archived: bool
    group: Group
    subgroup: Subgroup


class Assignment(BaseAssignments):
    """Задание для группы"""
    id: int

    class Config:
        orm_mode = True


class BaseStudentAssignment(BaseModel):
    assignment: Assignment
    student: Student
    done: bool = Field(..., description="Статус выполнения задания")


class StudentAssignment(BaseStudentAssignment):
    """Задание для группы, отслеживаемое конкретным студентом"""
    id: int

    class Config:
        orm_mode = True
