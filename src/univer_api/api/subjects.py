from fastapi import APIRouter, Depends, Query

from ..models.subjects import Subject
from ..services.subjects import SubjectsService

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/", response_model=list[Subject])
async def get_subjects_list(
        service: SubjectsService = Depends(SubjectsService),
        with_links_only: bool = False,
        group: str = Query(None, example="ЭЭ-18-4"),
):
    return service.get_list(with_links_only, group)
