import secrets

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Annotated

from app.configs.Loger import log
from app.configs.Settings import settings
from app.metadata.errors import NoExtensionSupported
from app.services.TaskService import TaskService
from app.schemas import TaskSchemas

router = APIRouter(prefix=f"{settings.API_PREFIX}/task", tags=["Task"])

security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode()
    is_correct_username = secrets.compare_digest(
        current_username_bytes, settings.ADMIN_USERNAME.encode()
    )
    current_password_bytes = credentials.password.encode()
    is_correct_password = secrets.compare_digest(
        current_password_bytes, settings.ADMIN_PWD.encode()
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.post("/create")
async def create_task(
    _: Annotated[str, Depends(get_current_username)],
    taskService: TaskService = Depends(),
):
    task_id = await taskService.add_task()
    return {"task_id": task_id}


@router.get("/", response_model=TaskSchemas.Task)
async def get_task(
    task_id: int,
    _: Annotated[str, Depends(get_current_username)],
    taskService: TaskService = Depends(),
):
    task = await taskService.get_task(task_id)
    return task


@router.delete("/")
async def delete_task(
    task_id: int,
    _: Annotated[str, Depends(get_current_username)],
    taskService: TaskService = Depends(),
):
    task_id = await taskService.delete_task(task_id)
    return {"task_id": task_id}


@router.post("/image/add")
async def add_image_to_task(
    task_id: int,
    _: Annotated[str, Depends(get_current_username)],
    taskService: TaskService = Depends(),
    image: UploadFile = File(...),
):
    if image.content_type != "image/jpeg":
        raise NoExtensionSupported
    image_id = await taskService.add_image(task_id, image)
    return {"image_id": image_id}
