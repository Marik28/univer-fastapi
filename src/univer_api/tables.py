import sqlalchemy as sa
import sqlalchemy.sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.models import generic_repr

from .models.groups import Subgroup
from .models.lessons import Building, LessonKind, WeekDay, Parity

Base = declarative_base()


def get_enum_values(enum) -> list[str]:
    return [str(e.value) for e in enum]


class Group(Base):
    __tablename__ = "groups"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=20), unique=True, nullable=False)

    def __str__(self):
        return f"{self.name}"


@generic_repr("building", "number")
class Classroom(Base):
    __tablename__ = "classrooms"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    number = sa.Column(sa.String(10), unique=True, nullable=False)
    building = sa.Column(sa.Enum(Building, create_constraint=True, values_callable=get_enum_values), nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String(255), nullable=False)
    second_name = sa.Column(sa.String(255), nullable=False)
    middle_name = sa.Column(sa.String(255), nullable=False)

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.middle_name}"

    __table_args__ = (
        sa.UniqueConstraint(
            'first_name', 'second_name', 'middle_name',
            name="unique_full_name_constraint",
        ),
    )


class Subject(Base):
    __tablename__ = "subjects"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)

    def __str__(self):
        return f"{self.name}"


@generic_repr("link", "subject")
class UsefulLink(Base):
    __tablename__ = "useful_links"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    link = sa.Column(sa.String(500), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    subject = relationship("Subject", backref="useful_links")


@generic_repr
class Lesson(Base):
    __tablename__ = "lessons"

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    subject_id = sa.Column(sa.Integer(), sa.ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    teacher_id = sa.Column(sa.Integer(), sa.ForeignKey("teachers.id", ondelete="RESTRICT"), nullable=False)
    classroom_id = sa.Column(sa.Integer(), sa.ForeignKey("classrooms.id", ondelete="SET NULL"), nullable=True)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False)
    subgroup = sa.Column(sa.Enum(Subgroup, create_constraint=True, values_callable=get_enum_values), nullable=False)
    kind = sa.Column(sa.Enum(LessonKind, create_constraint=True, values_callable=get_enum_values), nullable=False)
    day = sa.Column(sa.Enum(WeekDay, create_constraint=True, values_callable=get_enum_values), nullable=False)
    parity = sa.Column(sa.Enum(Parity, create_constraint=True, values_callable=get_enum_values), nullable=False)
    time = sa.Column(sa.Time(), nullable=False)

    subject = relationship("Subject", backref="lessons")
    teacher = relationship("Teacher", backref="lessons")
    classroom = relationship("Classroom", backref="lessons")
    group = relationship("Group", backref="lessons")

    __table_args__ = (
        sa.UniqueConstraint(
            "subject_id", "kind", "day", "time", "teacher_id", "group_id", "subgroup",
            name="unique_lesson_constraint",
        ),
    )


@generic_repr
class Assignment(Base):
    __tablename__ = 'assignments'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    complete_before = sa.Column(sa.Date(), nullable=False)
    is_important = sa.Column(sa.Boolean(), nullable=False)
    archived = sa.Column(sa.Boolean(), nullable=False, server_default=sqlalchemy.sql.text("0"))
    title = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text(), nullable=True)
    subject_id = sa.Column(sa.Integer(), sa.ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False)
    subgroup = sa.Column(sa.Enum(Subgroup, create_constraint=True, values_callable=get_enum_values), nullable=False)

    subject = relationship("Subject", backref="assignments")
    group = relationship("Group", backref="assignments")


@generic_repr
class Student(Base):
    __tablename__ = "students"
    telegram_id = sa.Column(sa.Integer(), primary_key=True)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    subgroup = sa.Column(sa.Enum(Subgroup, create_constraint=True, values_callable=get_enum_values), nullable=False)

    group = relationship("Group", backref="students")


@generic_repr
class StudentAssignment(Base):
    __tablename__ = "student_assignments"
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    student_id = sa.Column(sa.Integer(), sa.ForeignKey("students.telegram_id", ondelete="CASCADE"), nullable=False)
    assignment_id = sa.Column(sa.Integer(), sa.ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    done = sa.Column(sa.Boolean(), nullable=False, default=False)

    student = relationship("Student", backref="assignments")
    assignment = relationship("Assignment")
