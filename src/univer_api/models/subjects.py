from pydantic import BaseModel


class BaseSubject(BaseModel):
    name: str


class Subject(BaseSubject):
    id: int

    class Config:
        orm_mode = True
