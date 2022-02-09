from typing import Optional

from fastapi import APIRouter, Depends, Query

from ..models.assignments import Assignment
from ..models.groups import Subgroup
from ..services.assignments import AssignmentsService

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("/", response_model=list[Assignment])
async def get_assignments_list(
        service: AssignmentsService = Depends(),
        group: Optional[str] = Query(None, example="ЭЭ-18-4"),
        subgroup: Optional[Subgroup] = Query(None),
        subject: Optional[str] = Query(None),
        archived: Optional[bool] = Query(None),
):
    """Список заданий для группы, отсортированных по дате выполнения."""
    return service.get_list_for_group(group, subgroup, subject, archived)
