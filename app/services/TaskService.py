import pathlib
from typing import List
from fastapi import Depends, UploadFile

import uuid

from app.repositories.TaskRepo import TaskRepo
from app.schemas.TaskSchemas import Task
from app.configs.Settings import settings
from app.configs.Loger import log


class TaskService:
    repo: TaskRepo

    def __init__(self, repo: TaskRepo = Depends()):
        self.repo = repo

    async def add_task(self) -> int:
        return self.repo.add_task()

    async def delete_task(self, task_id: int) -> int:
        image_pathes = self.repo.get_image_pathes_by_task_id(task_id)
        await self.delete_images(image_pathes)
        return self.repo.delete_task(task_id)

    async def get_task(self, task_id: int) -> Task:
        task = self.repo.get_task(task_id)
        return task

    async def add_image(self, task_id: int, image: UploadFile) -> int:
        path_to_image = await self.save_image(image)
        image_id = self.repo.add_image(task_id, path_to_image)
        return image_id

    async def detect_faces(self, image: bytes): ...

    async def delete_images(self, image_pathes: List[str]) -> None:
        for path in image_pathes:
            image = pathlib.Path(path)
            if image.is_file() and image.exists():
                image.unlink()
                log.info(f"image with path: {image.resolve()} was deleted")
            else:
                log.info(f"image with path: {image.resolve()} wasnt found")
                continue

    async def save_image(self, image: UploadFile) -> str:
        image.filename = f"{uuid.uuid4()}.jpg"
        contents = await image.read()
        with open(f"{settings.IMAGE_DIR}{image.filename}", "wb") as f:
            f.write(contents)
        return f"{settings.IMAGE_DIR}{image.filename}"
