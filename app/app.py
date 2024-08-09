from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


async def on_startup(): ...


async def on_shutdown(): ...


def create_app() -> FastAPI:
    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app
