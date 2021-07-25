from pydantic import BaseModel


class BaseTeacher(BaseModel):
    first_name: str
    second_name: str
    middle_name: str


class Teacher(BaseTeacher):
    id: int

    class Config:
        orm_mode = True
