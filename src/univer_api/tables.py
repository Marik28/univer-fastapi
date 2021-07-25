import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .models.lessons import Building, LessonKind, WeekDay, Parity
from .models.groups import Subgroup

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=20), unique=True)


class Classroom(Base):
    __tablename__ = "classrooms"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    number = sa.Column(sa.SmallInteger, unique=True)
    building = sa.Column(sa.SmallInteger)

    # fixme так вообще делают?
    __table_args__ = (
        sa.CheckConstraint(
            f"building in ({', '.join([str(building.value) for building in Building])})",
            name="building_check_constraint",
        ),
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String(255))
    second_name = sa.Column(sa.String(255))
    middle_name = sa.Column(sa.String(255))

    __table_args__ = (
        sa.UniqueConstraint(
            'first_name', 'second_name', 'middle_name',
            name="unique_full_name_constraint",
        ),
    )


class SubjectName(Base):
    __tablename__ = "subject_names"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), unique=True)


class Subject(Base):
    __tablename__ = "subjects"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # todo доделать
    name_id = sa.Column(sa.Integer, sa.ForeignKey("subject_names.id"))
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))
    subgroup = sa.Column(sa.SmallInteger)

    name = relationship("SubjectName", backref="subjects")
    group = relationship("Group", backref="subjects")

    __table_args__ = (
        sa.CheckConstraint(
            f"subgroup in ({', '.join([str(subgroup.value) for subgroup in Subgroup])})",
            name="subgroup_check_constraint",
        ),
        sa.UniqueConstraint(
            "name_id", "group_id", "subgroup",
            name="unique_subject_constraint",
        ),
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.id"))
    kind = sa.Column(sa.String(50))
    day = sa.Column(sa.SmallInteger)
    parity = sa.Column(sa.SmallInteger)
    time = sa.Column(sa.Time)
    teacher_id = sa.Column(sa.Integer, sa.ForeignKey("teachers.id"))
    classroom_id = sa.Column(sa.Integer, sa.ForeignKey("classrooms.id"), nullable=True)

    subject = relationship("Subject", backref="lessons")
    teacher = relationship("Teacher", backref="lessons")
    classroom = relationship("Classroom", backref="lessons")

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
        sa.UniqueConstraint(
            "subject_id", "kind", "day", "time", "teacher_id", "classroom_id",
            name="unique_lesson_constraint",
        ),
    )
