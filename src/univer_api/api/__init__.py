from fastapi import APIRouter

from . import groups, lessons, teachers, assignments, subjects

router = APIRouter()
router.include_router(lessons.router)
router.include_router(groups.router)
router.include_router(teachers.router)
router.include_router(assignments.router)
router.include_router(subjects.router)
