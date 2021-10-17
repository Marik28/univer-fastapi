import csv
import re
import time
from pathlib import Path
from typing import Optional

import typer
from bs4 import BeautifulSoup

from univer_api.models.groups import Subgroup

app = typer.Typer()


def default_csv_name() -> str:
    return f"schedule-{int(time.time())}.csv"


def parse_subject(text: str) -> tuple[Optional[str], Optional[str]]:
    pattern = re.compile(
        r"(?P<name>[\w ,]+)\((?P<kind>[\w ]+)\)"
    )
    result = pattern.match(text)
    if result is not None:
        return result.group("name").strip(), result.group("kind").strip()
    return None, None


def parse_classroom(text: str) -> tuple[Optional[str], Optional[str]]:
    """ -> building, classroom"""
    pattern = re.compile(r"Ауд\.: (?P<building>\w)к(?P<classroom>[\w]+)")
    result = pattern.match(text)
    if result is not None:
        building = result.group("building")
        return building if building.isdigit() else "0", result.group("classroom")
    return None, None


def get_parity_from_string(parity: Optional[str]) -> int:
    return {
        "числитель": 1,
        "знаменатель": 2,
    }[parity.lower().strip()]


def parse_schedule(page_content: str, group: str, subgroup: Subgroup, filename):
    soup = BeautifulSoup(page_content, 'lxml')
    schedule = soup.select_one("tr#files_list table.schedule")

    schedule_list = []
    for row in schedule.select("tr")[1:]:
        continuation = row.select_one("td.time div.divIE")
        time = continuation.text.split("-")[0]
        lessons = row.select("td.field")
        for day, lesson_group in enumerate(lessons, start=1):
            if len(lesson_group.text.strip()) == 0:
                continue
            for lesson in lesson_group.select("div.groups div"):
                lesson_info = lesson.select("p.teacher")
                subject, kind = parse_subject(lesson_info[0].text.strip())
                teacher = lesson_info[1].text.split()[0]
                classroom_info = lesson.select_one("p.params").select("span")[-1].text.strip()
                building, classroom = parse_classroom(classroom_info)
                parity_info = lesson.select_one("p.params span.denominator")
                parity = get_parity_from_string(parity_info.text) if parity_info is not None else 3
                schedule_list.append(
                    [subject, kind, teacher, parity, time, day, group, subgroup.value, building, classroom]
                )
        with open(filename, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["name", "kind", "teacher", "parity", "time", "day", "group", "subgroup", "building", "classroom"]
            )
            writer.writerows(schedule_list)


@app.command()
def main(
        html: Path = typer.Argument(
            ...,
            resolve_path=True,
            exists=True,
            readable=True,
            help='html файл с расписанием'
        ),
        csv_file: Optional[Path] = typer.Argument(
            None,
            resolve_path=True,
            show_default="schedule-{timestamp}.csv",
        ),
        group: str = typer.Option(
            "ЭЭ-18-4",
            help="группа, у которой ведутся пары с данного расписания"
        ),
        subgroup: Subgroup = typer.Option(
            Subgroup.BOTH,
            help="подгруппа, у которой ведутся пары с данного расписания"
        ),

):
    with open(html, encoding="urf-8") as f:
        html_content = f.read()

    if csv_file is None:
        csv_file = default_csv_name()

    parse_schedule(html_content, group, subgroup, csv_file)


if __name__ == '__main__':
    app()
