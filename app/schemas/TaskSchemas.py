from typing import List
from pydantic import BaseModel


class Face(BaseModel):
    bbox: str
    sex: str
    age: int


class Image(BaseModel):
    image_id: int
    faces: List[Face]


class Task(BaseModel):
    task_id: int
    images: List[Image]
