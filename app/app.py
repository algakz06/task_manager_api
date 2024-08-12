from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.db_models import init
from app.configs.Loger import log


async def on_startup():
    try:
        init()
    except Exception as e:
        log.error(f"Error occured while starting up db: {e}")


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_event_handler("startup", on_startup)

    from app.routers.TaskRouter import router as taskRouter

    _app.include_router(taskRouter)

    return _app
