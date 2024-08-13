from fastapi import Depends, UploadFile

import pathlib
from typing import List
import uuid

from app.metadata.errors import NoExtensionSupported
from app.models import db_models
from app.repositories.TaskRepo import TaskRepo
from app.schemas import TaskSchemas
from app.configs.Settings import settings
from app.configs.Loger import log
from app.worker import detect_face


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

    async def get_task(self, task_id: int) -> TaskSchemas.Task:
        db_task: db_models.Task = self.repo.get_task(task_id)
        db_images: List[db_models.Image] = self.repo.get_images_by_task_id(db_task.id)
        images: List[TaskSchemas.Image] = []
        for image in db_images:
            db_faces = self.repo.get_faces_by_image_id(image.id)
            faces = [
                TaskSchemas.Face(
                    bbox=TaskSchemas.BoundingBox.model_validate_json(
                        face.bounding_box  # type: ignore
                    ),
                    sex=face.sex,
                    age=face.age,
                )
                for face in db_faces
            ]
            images.append(
                TaskSchemas.Image(
                    image_id=image.id, name=image.path.split("/")[-1], faces=faces
                )
            )
        task = TaskSchemas.Task(task_id=db_task.id, images=images)
        task_demographic = self.count_demographic(task)
        task.face_quantity = task_demographic.face_quantity
        task.female_and_male_qunatity = (
            task_demographic.female_qunatity + task_demographic.male_quantity
        )
        task.avg_female_age = task_demographic.avg_female_age
        task.avg_male_age = task_demographic.avg_male_age

        return task

    async def add_image(self, task_id: int, image: UploadFile) -> int:
        if image.content_type not in ["image/jpeg"]:
            log.error(f"got image with unsupported extension: {image.content_type}")
            raise NoExtensionSupported
        path_to_image = await self.save_image(image)
        image_id = self.repo.add_image(task_id, path_to_image)
        detect_face.delay(path_to_image, image_id)  # type: ignore
        return image_id

    async def delete_images(self, image_pathes: List[str]) -> None:
        for path in image_pathes:
            image = pathlib.Path(path)
            if image.is_file() and image.exists():
                image.unlink()
                log.info(f"image with path: {image.resolve()} was deleted")
            else:
                log.info(f"image with path: {image.resolve()} wasnt found")

    async def save_image(self, image: UploadFile) -> str:
        image.filename = f"{uuid.uuid4()}.jpg"
        contents = await image.read()
        with open(f"{settings.IMAGE_DIR}{image.filename}", "wb") as f:
            f.write(contents)
        return f"{settings.IMAGE_DIR}{image.filename}"

    @staticmethod
    def count_demographic(task: TaskSchemas.Task) -> TaskSchemas.TaskDemographic:
        total_faces = 0
        total_female = 0
        total_male = 0
        total_female_age = 0
        total_male_age = 0
        for image in task.images:
            total_faces += len(image.faces)
            for face in image.faces:
                if face.sex == "female":
                    total_female += 1
                    total_female_age += face.age
                elif face.sex == "male":
                    total_male += 1
                    total_male_age += face.age
        return TaskSchemas.TaskDemographic(
            face_quantity=total_faces,
            female_qunatity=total_female,
            male_quantity=total_male,
            avg_female_age=total_female_age / total_female if total_female_age else 0,
            avg_male_age=total_male_age / total_male if total_male else 0,
        )
