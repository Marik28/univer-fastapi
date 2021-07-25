from fastapi import APIRouter

from . import groups, lessons, teachers

router = APIRouter()
router.include_router(lessons.router)
router.include_router(groups.router)
router.include_router(teachers.router)
