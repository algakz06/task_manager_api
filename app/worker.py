from celery import Celery

from app.configs.Database import get_db
from app.repositories.TaskRepo import TaskRepo
from app.configs.Settings import settings
from app.utils.CVManager import CVManager

celery = Celery("worker", broker=settings.BROKER_URI)
cvManager = CVManager(
    settings.FACECLOUD_EMAIL, settings.FACECLOUD_PWD, settings.FACECLOUD_URL
)


@celery.task(name="face_detection")
def detect_face(
    path_to_image: str,
    image_id: int,
    taskRepo: TaskRepo = TaskRepo(db_conn=next(get_db())), #type: ignore
):
    faces = cvManager.detect(path_to_image)
    taskRepo.add_faces(image_id=image_id, faces=faces)
