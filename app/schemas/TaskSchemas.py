from typing import List, NamedTuple
from pydantic import BaseModel


class BoundingBox(BaseModel):
    height: int
    width: int
    x: int
    y: int

class Face(BaseModel):
    bbox: BoundingBox
    sex: str
    age: int


class Image(BaseModel):
    image_id: int
    name: str
    faces: List[Face]


class Task(BaseModel):
    task_id: int
    images: List[Image]
    face_quantity: int = 0
    female_and_male_qunatity: int = 0
    avg_female_age: float = 0
    avg_male_age: float = 0


class TaskDemographic(NamedTuple):
    face_quantity: int
    female_qunatity: int
    male_quantity: int
    avg_female_age: float
    avg_male_age: float
