from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn about FastAPI path parameters", "done": True},
    {"id": 2, "title": "Learn about FastAPI query parameters", "done": False},
    {"id": 3, "title": "Learn about FastAPI request body", "done": False},
]


class TaskCreate(BaseModel):
    title: str | None = None


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks/{task_id}")
def get_task_id(task_id: int, response: Response):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Task {task_id} not found"}

    return task


@app.post("/tasks")
def create_task(task_in: TaskCreate, response: Response):
    if not task_in.title or not task_in.title.strip():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Title is required and cannot be empty"}

    next_id = max((t["id"] for t in tasks), default=0) + 1

    new_task = {"id": next_id, "title": task_in.title.strip(), "done": False}

    tasks.append(new_task)

    response.status_code = status.HTTP_201_CREATED
    return new_task
