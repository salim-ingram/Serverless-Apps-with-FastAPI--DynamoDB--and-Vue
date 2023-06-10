import uuid
from typing import Union

import jwt
from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette import status

from config import Config
from models import Task
from schemas import APITask, CreateTask
from store import TaskStore

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
config = Config()


def get_task_store() -> TaskStore:
    return TaskStore(config.TABLE_NAME, dynamodb_url=config.DYNAMODB_URL)


def get_user_email(authorization: Union[str, None] = Header(default=None)) -> str:
    return jwt.decode(authorization, options={"verify_signature": False})[
        "cognito:username"
    ]


@app.get("/api/health-check/")
def health_check():
    return {"message": "OK"}


@app.post(
    "/api/create-task", response_model=APITask, status_code=status.HTTP_201_CREATED
)
def create_task(
    parameters: CreateTask,
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    task = Task.create(id_=uuid.uuid4(), title=parameters.title, owner=user_email)
    task_store.add(task)

    return task


handle = Mangum(app)
