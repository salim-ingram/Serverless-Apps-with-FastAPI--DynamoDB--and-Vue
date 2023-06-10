from uuid import UUID

from models import TaskStatus
from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str


class APITask(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    class Config:
        orm_mode = True


class APITasksList(BaseModel):
    results: list[APITask]

    class Config:
        orm_mode = True


class CloseTask(BaseModel):
    id: UUID
