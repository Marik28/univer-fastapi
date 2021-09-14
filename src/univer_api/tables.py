import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.models import generic_repr

from .models.groups import Subgroup
from .models.lessons import Building, LessonKind, WeekDay, Parity

Base = declarative_base()

subgroup_check_constraint = sa.CheckConstraint(
    f"subgroup in ({', '.join([str(subgroup.value) for subgroup in Subgroup])})",
    name="subgroup_check_constraint",
),


@generic_repr
class Group(Base):
    __tablename__ = "groups"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=20), unique=True, nullable=False)


@generic_repr
class Classroom(Base):
    __tablename__ = "classrooms"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    number = sa.Column(sa.String(10), unique=True, nullable=False)
    building = sa.Column(sa.SmallInteger, nullable=False)

    # fixme так вообще делают?
    __table_args__ = (
        sa.CheckConstraint(
            f"building in ({', '.join([str(building.value) for building in Building])})",
            name="building_check_constraint",
        ),
    )


@generic_repr
class Teacher(Base):
    __tablename__ = "teachers"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String(255), nullable=False)
    second_name = sa.Column(sa.String(255), nullable=False)
    middle_name = sa.Column(sa.String(255), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint(
            'first_name', 'second_name', 'middle_name',
            name="unique_full_name_constraint",
        ),
    )


@generic_repr
class Subject(Base):
    __tablename__ = "subjects"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)


@generic_repr
class UsefulLink(Base):
    __tablename__ = "useful_links"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    link = sa.Column(sa.String(500), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.id"), nullable=False)

    subject = relationship("Subject", backref="links")


@generic_repr
class Lesson(Base):
    __tablename__ = "lessons"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    teacher_id = sa.Column(sa.Integer, sa.ForeignKey("teachers.id", ondelete="RESTRICT"), nullable=False)
    classroom_id = sa.Column(sa.Integer, sa.ForeignKey("classrooms.id", ondelete="SET NULL"), nullable=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False)
    subgroup = sa.Column(sa.SmallInteger, nullable=False)
    kind = sa.Column(sa.String(50), nullable=False)
    day = sa.Column(sa.SmallInteger, nullable=False)
    parity = sa.Column(sa.SmallInteger, nullable=False)
    time = sa.Column(sa.Time, nullable=False)

    subject = relationship("Subject", backref="lessons")
    teacher = relationship("Teacher", backref="lessons")
    classroom = relationship("Classroom", backref="lessons")
    group = relationship("Group", backref="lessons")

    __table_args__ = (
        sa.CheckConstraint(
            f"""kind in ({', '.join([f'"{kind.value}"' for kind in LessonKind])})""",
            name="unique_lesson_kind_constraint",
        ),
        sa.CheckConstraint(
            f"day in ({', '.join([str(day.value) for day in WeekDay])})",
            name="unique_week_day_constraint",
        ),
        sa.CheckConstraint(
            f"parity in ({', '.join([str(parity.value) for parity in Parity])})",
            name="parity_check_constraint",
        ),
        subgroup_check_constraint,
        sa.UniqueConstraint(
            "subject_id", "kind", "day", "time", "teacher_id", "group_id", "subgroup",
            name="unique_lesson_constraint",
        ),
    )


@generic_repr
class Assignment(Base):
    __tablename__ = 'assignments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    complete_before = sa.Column(sa.Date, nullable=False)
    is_important = sa.Column(sa.Boolean)
    title = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.id", ondelete="RESTRICT"))
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id", ondelete="RESTRICT"))
    subgroup = sa.Column(sa.String, nullable=False)

    subject = relationship("Subject", backref="assignments")
    group = relationship("Group", backref="assignments")

    __table_args__ = (
        subgroup_check_constraint,
    )
