from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = [
    {"id": 1, "title": "Learn about FastAPI path parameters", "done": True},
    {"id": 2, "title": "Learn about FastAPI query parameters", "done": False},
    {"id": 3, "title": "Learn about FastAPI request body", "done": False}
]

@app.get("/")
def root():
    return {
            "name": "Task API",
            "version": "1.0",
            "endpoints": ["/tasks"]
        }

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/tasks/{task_id}")
def get_task_id(task_id: int, response: Response):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": f"Task {task_id} not found"}
    
    return task