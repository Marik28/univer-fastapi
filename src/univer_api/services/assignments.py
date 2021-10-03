from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..api.base import GroupFilterHelper
from ..database import get_session


class AssignmentsService(GroupFilterHelper):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list_for_group(
            self,
            group: Optional[str] = None,
            subgroup: Optional[int] = None,
            subject: Optional[str] = None,
            archived: Optional[bool] = None,
    ) -> list[tables.Assignment]:
        query = self.session.query(tables.Assignment).join(tables.Assignment.group).join(tables.Assignment.subject)

        if subject is not None:
            query = query.filter(tables.Subject.name == subject)

        if archived is not None:
            query = query.filter(tables.Assignment.archived == archived)

        query = self.filter_group_and_subgroup(query, group, subgroup)

        return query.order_by(tables.Group.name.asc(), tables.Assignment.complete_before.asc()).all()

    def get_list_for_student(self, student: tables.Student, done: bool = False) -> list[tables.StudentAssignment]:
        # todo оптимизировать

        not_created_group_assignments = (
            self.session.query(tables.Assignment)
                .filter(
                tables.Assignment.id.notin_(
                    self.session.query(tables.StudentAssignment.id)
                    .filter(tables.StudentAssignment.student_id == student.telegram_id)
                )
            )
                .all()
        )

        if not_created_group_assignments:
            self.create_many_for_student(student, not_created_group_assignments)

        student_assignments = (
            self.session.query(tables.StudentAssignment)
                .join(tables.Assignment)
                .filter(tables.StudentAssignment.student_id == student.telegram_id)
                .filter(tables.StudentAssignment.done.is_(done))
                .all()
        )
        return student_assignments

    def create_many_for_student(self, student: tables.Student, assignments: list[tables.Assignment]):
        new_assignments = [
            tables.StudentAssignment(assignment_id=assignment.id, student_id=student.telegram_id)
            for assignment in assignments
        ]
        self.session.add_all(new_assignments)
        self.session.commit()

    def _get_student_assignment(self, assignment_id: int) -> tables.StudentAssignment:
        student_assignment = (
            self.session.query(tables.StudentAssignment)
                .filter(tables.StudentAssignment.id == assignment_id)
                .first()
        )
        if student_assignment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return student_assignment

    def update_student_assignment(self, student_assignment_id: int, done: bool):
        student_assignment = self._get_student_assignment(student_assignment_id)
        student_assignment.done = done
        self.session.add(student_assignment)
        self.session.commit()
