import sqlalchemy.orm
from fastapi import Depends, HTTPException, status, Path

from .groups import GroupsService
from .. import tables
from ..database import get_session
from ..models.students import StudentCreate, StudentUpdate


def get_current_student(
        student_id: int = Path(...),
        session: sqlalchemy.orm.Session = Depends(get_session),
) -> tables.Student:
    student = session.query(tables.Student).filter(tables.Student.telegram_id == student_id).first()
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
    return student


class StudentsService:

    def __init__(
            self,
            session: sqlalchemy.orm.Session = Depends(get_session),
            group_service: GroupsService = Depends(),
    ):
        self.session = session
        self.group_service = group_service

    def validate_group(self, group_name) -> tables.Group:
        group = self.group_service.get_by_name(group_name)
        if group is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Group was not found")
        return group

    def create(self, student_create: StudentCreate):
        group = self.validate_group(student_create.group_name)
        new_student = tables.Student(
            telegram_id=student_create.telegram_id,
            group_id=group.id,
            subgroup=student_create.subgroup
        )
        self.session.add(new_student)
        self.session.commit()

    def update(self, student: tables.Student, student_update: StudentUpdate):
        group = self.validate_group(student_update.group_name)
        student.group = group
        student.subgroup = student_update.subgroup
        self.session.add(student)
        self.session.commit()
