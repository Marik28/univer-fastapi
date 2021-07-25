import csv
import datetime as dt
from os import PathLike
from typing import Union

import sqlalchemy.exc
from sqlalchemy.orm import Session

from univer_api import tables


def insert_subject_names(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            print(name)
            subject_name = tables.SubjectName(name=name)
            session.add(subject_name)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f"{subject_name.name} уже в БД")
                session.rollback()


def insert_groups(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            print(name)
            group = tables.Group(name=name)
            session.add(group)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f"{group.name} уже в БД")
                session.rollback()


def insert_teachers(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            first_name = row["first_name"].strip()
            second_name = row["second_name"].strip()
            middle_name = row["middle_name"].strip()
            print(second_name, first_name, middle_name)
            teacher = tables.Teacher(first_name=first_name, second_name=second_name, middle_name=middle_name)
            session.add(teacher)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f"{teacher.second_name} уже в БД")
                session.rollback()


def insert_subjects(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            group_name = row["group"].strip()
            subgroup = int(row["subgroup"])
            group = session.query(tables.Group).filter(tables.Group.name == group_name).first()
            subject_name = session.query(tables.SubjectName).filter(tables.SubjectName.name == name).first()

            subject = tables.Subject(name=subject_name, subgroup=subgroup, group=group)
            session.add(subject)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f"{subject.name} ({subject.group.name}) уже в БД")
                session.rollback()


def insert_lessons(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            teacher_second_name = row["teacher"].split()[0].strip()
            name = row["name"].strip()
            parity = int(row["parity"])
            group_name = row["group"].strip()
            time = dt.time.fromisoformat(row["time"].strip())
            kind = row["kind"].strip()
            teacher = (session.query(tables.Teacher)
                       .filter(tables.Teacher.second_name == teacher_second_name)
                       .first())
            subgroup = int(row["subgroup"])
            subject = (session.query(tables.Subject)
                       .join(tables.SubjectName)
                       .join(tables.Group)
                       .filter(
                tables.Subject.subgroup == subgroup,
                tables.SubjectName.name == name,
                tables.Group.name == group_name,
            )
                       .first())
            lesson = tables.Lesson(subject=subject, teacher=teacher, kind=kind, time=time, parity=parity)
            session.add(lesson)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print(f"{lesson.subject.name} ({lesson.day} {lesson.time}) уже в БД")
                session.rollback()

