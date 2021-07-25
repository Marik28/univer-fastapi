import csv
from os import PathLike
from typing import Union

from sqlalchemy.orm import Session

from univer_api import tables


def insert_subject_names(
        csv_file: Union[PathLike, str],
        session: Session,
):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        subject_names = [row["name"] for row in reader]
        print(f"Список предметов: {subject_names}")

    for name in subject_names:
        new_name = tables.SubjectName(name=name)
        session.add(new_name)
    session.commit()


def insert_groups(
        csv_file: Union[PathLike, str],
        session: Session,

):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        group_names = [row["name"] for row in reader]
        print(f"Список групп: {group_names}")
    for group in group_names:
        new_group = tables.Group(name=group)
        session.add(new_group)
    session.commit()
