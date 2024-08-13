# Task Manager API

## About project
API built as parf of a test case. Service can create "Task" and take images in .jpg format as part of "Task". This API connect Client-side with FaceCloud API for face recognition on images.


## Features
- Stack: Python3.12, FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Celery, Flower
- Integrated with FaceCloud API
- HTTP Basic Auth (username:password set in .env file)

## Getting started

### Prerequisites
- Docker, docker-compose

### How to build
```zsh
# clone project to your machine
git clone https://github.com/algakz06/task_manager_api.git && cd task_manager_api

# clone .env.example to .env and configure it
cp .env.example .env
vi .env

# make sure docker daemon running on and launch the project
docker compose up -d
```
## Usage
After launching project you can go Swagger with `http://localhost:3333/docs` and Flower wtih `http://localhost:5001`.
### Endpoints
| Method | Endpoint | Decription |
| --- | --- | --- |
| POST | /api/v1/task/add | task creating |
| GET | /api/v1/task | get task with images and detected faces via task_id |
| DELETE | /api/v1/task | task deleting via task_id |
| POST | /api/v1/task/image/add | add image to task via task_id|

## TO-DO
- [X] POST api/v1/task/add
- [X] GET api/v1/task
- [X] DELETE api/v1/task
- [X] POST api/v1/task/image/add
- [X] Link API to FaceCloud
