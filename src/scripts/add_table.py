import argparse
import csv
import datetime as dt
from os import PathLike
from typing import Union

from sqlalchemy.exc import IntegrityError

from univer_api import tables
from univer_api.database import Session

db_tables = ["lessons", "subjects", "teachers", "groups", "classrooms"]
parser = argparse.ArgumentParser()
parser.add_argument("-t", help="Таблица, которую необходимо создать", choices=db_tables)
parser.add_argument("-f", help="Путь до csv файла, из которого будут браться данные")


def insert_subjects(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                print(name)
                subject = tables.Subject(name=name)
                session.add(subject)
                try:
                    session.commit()
                except IntegrityError:
                    print(f"{subject.name} уже в БД")
                    session.rollback()


def insert_groups(
        csv_file: Union[PathLike, str],
):
    with Session() as session:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                print(name)
                group = tables.Group(name=name)
                session.add(group)
                try:
                    session.commit()
                except IntegrityError:
                    print(f"{group.name} уже в БД")
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
                print(second_name, first_name, middle_name)
                teacher = tables.Teacher(first_name=first_name, second_name=second_name, middle_name=middle_name)
                session.add(teacher)
                try:
                    session.commit()
                except IntegrityError:
                    print(f"{teacher.second_name} уже в БД")
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
                print(f"{subject.name} ({group.name})")
                try:
                    session.commit()
                except IntegrityError:
                    print(f"{lesson.subject.name} ({lesson.day} {lesson.time}) уже в БД")
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
                print(f"Корпус - {building}, кабинет")
                classroom = tables.Classroom(building=building, number=classroom_number)
                session.add(classroom)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    print("Уже в бд")
                else:
                    print("Добавлен")


flag_to_function = {
    db_tables[0]: insert_lessons,
    db_tables[1]: insert_subjects,
    db_tables[2]: insert_teachers,
    db_tables[3]: insert_groups,
    db_tables[4]: insert_classrooms,
}

if __name__ == '__main__':
    args = parser.parse_args()
    table = args.t
    file = args.f
    print('-------', table, file)
    flag_to_function[table](file)
