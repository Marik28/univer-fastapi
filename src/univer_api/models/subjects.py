from typing import Optional

from pydantic import BaseModel, Field


class BaseSubject(BaseModel):
    """Модель, описывающая предмет"""
    name: str = Field(..., description="Название предмета")


class Subject(BaseSubject):
    id: int

    class Config:
        orm_mode = True


class BaseUsefulLink(BaseModel):
    link: str
    description: Optional[str]
    subject: Subject


class UsefulLink(BaseUsefulLink):
    id: int

    class Config:
        orm_mode = True
