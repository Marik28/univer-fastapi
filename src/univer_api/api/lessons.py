from typing import Optional

from fastapi import APIRouter, Query, Depends

from ..models.groups import Subgroup
from ..models.lessons import WeekDay, Lesson, Parity, LessonKind
from ..services.lessons import LessonsService

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("/", response_model=list[Lesson])
async def get_lessons_list(
        service: LessonsService = Depends(),
        day: Optional[WeekDay] = Query(
            None,
            title="День недели"),
        parity: Optional[Parity] = Query(
            None,
            title="Четность недели",
        ),
        group: Optional[str] = Query(
            None,
            title="Группа",
            example="ЭЭ-18-4",
        ),
        subgroup: Optional[Subgroup] = Query(
            None,
            title="Подгруппа",
        ),
        kind: Optional[LessonKind] = Query(
            None,
            title="Тип пары",
        )
):
    """Эндпоинт для получения списка пар"""
    return service.get_list(day, parity, group, subgroup, kind)
