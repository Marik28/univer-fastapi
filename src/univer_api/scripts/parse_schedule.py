import argparse
import csv
import re
from typing import Optional

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--html", help="html файл с расписанием")
parser.add_argument("--group", help="группа, у которой ведутся пары с данного расписания")
parser.add_argument("--subgroup", help="подгруппа, у которой ведутся пары с данного расписания", type=int, default=3)
parser.add_argument("--csv", help="csv-файл, в который будет сохранено расписание")


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


def parse_schedule(html: str, group: str, subgroup: int, filename):
    soup = BeautifulSoup(html, 'lxml')
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
                schedule_list.append([subject, kind, teacher, parity, time, day, group, subgroup, building, classroom])
        with open(filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["name", "kind", "teacher", "parity", "time", "day", "group", "subgroup", "building", "classroom"]
            )
            writer.writerows(schedule_list)


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.html) as f:
        html = f.read()
    parse_schedule(html, args.group, args.subgroup, args.csv)
