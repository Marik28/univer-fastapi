from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    Path,
    Query,
)

from .. import tables
from ..models.assignments import StudentAssignment
from ..models.students import StudentCreate, StudentUpdate
from ..services.assignments import AssignmentsService
from ..services.students import get_current_student, StudentsService

router = APIRouter(prefix="/students")


# todo пофиксить безопасность (сейчас любой, у кого есть телеграм id пользователя, может делать, что вздумается)

@router.get("/{student_id}/assignments/", response_model=list[StudentAssignment])
async def get_student_assignments(
        done: bool = Query(False),
        student: tables.Student = Depends(get_current_student),
        service: AssignmentsService = Depends(),
):
    return service.get_list_for_student(student, done)


@router.patch("/{student_id}/assignments/{student_assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student_assignment(
        student_assignment_id: int = Path(...),
        done: bool = Body(..., embed=True),
        service: AssignmentsService = Depends(),
):
    # fixme один пользователь может достучаться до задания другого пользователя, зная его id
    service.update_student_assignment(student_assignment_id, done)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(
        student_create: StudentCreate,
        service: StudentsService = Depends(),
):
    service.create(student_create)


@router.put("/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(
        student_update: StudentUpdate,
        student: tables.Student = Depends(get_current_student),
        service: StudentsService = Depends(),
):
    service.update(student, student_update)
