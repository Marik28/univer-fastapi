from fastapi import APIRouter, Depends

from ..models.subjects import Subject
from ..services.subjects import SubjectsService

router = APIRouter(prefix="/subjects")


@router.get("/", response_model=list[Subject])
async def get_subjects_list(
        service: SubjectsService = Depends(SubjectsService),
        with_links_only: bool = False,
):
    return service.get_list(with_links_only)
