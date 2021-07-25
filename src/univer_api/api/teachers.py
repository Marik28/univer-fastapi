from fastapi import APIRouter, Depends

from ..models.teachers import Teacher
from ..services.teachers import TeachersService

router = APIRouter(prefix="/teachers")


@router.get("/", response_model=list[Teacher])
async def get_teachers_list(service: TeachersService = Depends()):
    return service.get_list()
