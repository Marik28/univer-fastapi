from fastapi import APIRouter, Depends, status

from .. import tables
from ..models.students import StudentCreate, StudentUpdate
from ..services.assignments import AssignmentsService
from ..services.students import get_current_student, StudentsService

router = APIRouter(prefix="/students")


@router.get("/{id}/assignments/")
async def get_student_assignments(
        student: tables.Student = Depends(get_current_student),
        service: AssignmentsService = Depends(),
):
    return student


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(
        student_create: StudentCreate,
        service: StudentsService = Depends(),
):
    service.create(student_create)


@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(
        student_update: StudentUpdate,
        student: tables.Student = Depends(get_current_student),
        service: StudentsService = Depends(),
):
    service.update(student, student_update)
