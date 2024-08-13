from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, ForeignKey

from app.configs.Database import Engine


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    path: Mapped[str]


class Face(Base):
    __tablename__ = "face"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id", ondelete="CASCADE"))
    sex: Mapped[str]
    bounding_box: Mapped[dict[str, Any]]
    age: Mapped[int]


def init():
    Base.metadata.create_all(Engine)
