import csv
import datetime as dt
import enum
from os import PathLike
from pathlib import Path
from typing import Union

import typer
from sqlalchemy.exc import IntegrityError

from univer_api import tables
from univer_api.database import Session


class TableName(str, enum.Enum):
    LESSONS = "lessons"
    SUBJECTS = "subjects"
    TEACHERS = "teachers"
    GROUPS = "groups"
    CLASSROOMS = "classrooms"


app = typer.Typer()


def insert_subjects(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                typer.echo(name)
                subject = tables.Subject(name=name)
                session.add(subject)
                try:
                    session.commit()
                except IntegrityError:
                    typer.echo(f"{subject.name} уже в БД")
                    session.rollback()


def insert_groups(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                typer.echo(name)
                group = tables.Group(name=name)
                session.add(group)
                try:
                    session.commit()
                except IntegrityError:
                    typer.echo(f"{group.name} уже в БД")
                    session.rollback()


def insert_teachers(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row["first_name"].strip()
                second_name = row["second_name"].strip()
                middle_name = row["middle_name"].strip()
                typer.echo(second_name, first_name, middle_name)
                teacher = tables.Teacher(first_name=first_name, second_name=second_name, middle_name=middle_name)
                session.add(teacher)
                try:
                    session.commit()
                except IntegrityError:
                    typer.echo(f"{teacher.second_name} уже в БД")
                    session.rollback()


def insert_lessons(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                teacher_second_name = row["teacher"].split()[0].strip()
                name = row["name"].strip()
                parity = row["parity"].strip()
                group_name = row["group"].strip()
                subgroup = row["subgroup"].strip()
                time = dt.time.fromisoformat(row["time"].strip())
                kind = row["kind"].strip()
                day = row["day"].strip()
                classroom_number = row["classroom"].strip()
                building = row["building"].strip()

                teacher = (session.query(tables.Teacher)
                           .filter(tables.Teacher.second_name == teacher_second_name)
                           .first())
                subject = (session.query(tables.Subject)
                           .filter(tables.Subject.name == name)
                           .first())
                group = (session.query(tables.Group)
                         .filter(tables.Group.name == group_name)
                         .first())
                if classroom_number == "" and building == "":
                    classroom = None
                else:
                    classroom = (
                        session.query(tables.Classroom)
                            .filter(tables.Classroom.number == classroom_number, tables.Classroom.building == building)
                            .first()
                    )
                lesson = tables.Lesson(subject=subject, teacher=teacher, kind=kind, time=time, parity=parity,
                                       group=group, subgroup=subgroup, day=day, classroom=classroom)

                session.add(lesson)
                typer.echo(f"{subject.name} ({group.name})")
                try:
                    session.commit()
                except IntegrityError:
                    typer.echo(f"{lesson.subject.name} ({lesson.day} {lesson.time}) уже в БД")
                    session.rollback()


def insert_classrooms(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                building = row["building"]
                classroom_number = row["classroom"]
                typer.echo(f"Корпус - {building}, кабинет")
                classroom = tables.Classroom(building=building, number=classroom_number)
                session.add(classroom)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    typer.echo("Уже в бд")
                else:
                    typer.echo("Добавлен")


flag_to_function = {
    TableName.LESSONS: insert_lessons,
    TableName.SUBJECTS: insert_subjects,
    TableName.TEACHERS: insert_teachers,
    TableName.GROUPS: insert_groups,
    TableName.CLASSROOMS: insert_classrooms,
}


def table_name_autocompletion_callback() -> list[str]:
    return [v.value for v in TableName]


def validate_csv_file_callback(value: Path):
    if not value.name.endswith(".csv"):
        raise typer.BadParameter("Файл должен иметь расширение csv")
    return value


@app.command()
def main(
        table: TableName = typer.Argument(
            ...,
            show_choices=True,
            autocompletion=table_name_autocompletion_callback,
            help="Таблица, которую необходимо создать"
        ),
        file: Path = typer.Argument(
            ...,
            help="Путь до csv файла, из которого будут браться данные. "
                 "Может быть как и относительным, так и абсолютным",
            callback=validate_csv_file_callback,
            resolve_path=True,
            exists=True,
            readable=True,
        ),
):
    flag_to_function[table](file)


if __name__ == '__main__':
    app()
