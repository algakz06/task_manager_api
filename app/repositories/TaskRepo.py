from fastapi import Depends
from sqlalchemy.orm import Session

from typing import List

from app.configs.Database import get_db
from app.metadata.errors import NoTaskFound
from app.models import db_models
from app.schemas.TaskSchemas import Image, Task, Face


class TaskRepo:
    db_conn: Session

    def __init__(self, db_conn: Session = Depends(get_db)):
        self.db_conn = db_conn

    def add_task(self) -> int:
        task = db_models.Task()
        self.db_conn.add(task)
        self.db_conn.commit()
        return task.id

    def delete_task(self, task_id: int) -> int:
        task = (
            self.db_conn.query(db_models.Task)
            .filter(db_models.Task.id == task_id)
            .first()
        )
        if task is None:
            raise NoTaskFound
        self.db_conn.delete(task)
        self.db_conn.commit()
        return task.id

    def get_task(self, task_id: int) -> Task:
        db_task = (
            self.db_conn.query(db_models.Task)
            .filter(db_models.Task.id == task_id)
            .first()
        )
        if not db_task:
            raise NoTaskFound
        images = self.get_images_by_task_id(db_task.id)
        return Task(task_id=db_task.id, images=images)

    def get_images_by_task_id(self, task_id: int) -> List[Image]:
        db_images = (
            self.db_conn.query(db_models.Image)
            .filter(db_models.Image.task_id == task_id)
            .all()
        )
        return [
            Image(
                image_id=image.id,
                faces=self.get_faces_by_image_id(image.id),
            )
            for image in db_images
        ]

    def get_image_pathes_by_task_id(self, task_id: int) -> List[str]:
        db_images = (
            self.db_conn.query(db_models.Image)
            .filter(db_models.Image.task_id == task_id)
            .all()
        )
        return [image.path for image in db_images]

    def get_faces_by_image_id(self, image_id: int) -> List[Face]:
        db_faces = (
            self.db_conn.query(db_models.Face)
            .filter(db_models.Face.image_id == image_id)
            .all()
        )
        return [
            Face(
                bbox=face.bbox,
                sex=face.sex,
                age=face.age,
            )
            for face in db_faces
        ]

    def add_image(self, task_id: int, path_to_image: str):
        db_image = db_models.Image(task_id=task_id, path=path_to_image)
        self.db_conn.add(db_image)
        self.db_conn.commit()

        return db_image.id

    def add_face(self, image_id: int, face: Face):
        db_face = db_models.Face(
            image_id=image_id, sex=face.sex, bbox=face.bbox, age=face.age
        )
        self.db_conn.add(db_face)

    def add_many_faces(self, image_id: int, faces: List[Face]):
        for face in faces:
            self.add_face(image_id, face)
        self.db_conn.commit()
