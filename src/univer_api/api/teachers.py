from fastapi import APIRouter, Depends

from ..models.teachers import Teacher
from ..services.teachers import TeachersService

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/", response_model=list[Teacher])
async def get_teachers_list(service: TeachersService = Depends()):
    """Эндпоинт для получения списка преподавателей"""
    return service.get_list()
