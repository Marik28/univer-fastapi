import csv
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
