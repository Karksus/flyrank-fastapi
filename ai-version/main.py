from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

# Initialize FastAPI app with documentation metadata
app = FastAPI(
    title="FastAPI Task Manager Toy API",
    description="A fully-featured toy CRUD application managing FastAPI learning tasks with input validation and error handling.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Mock Database ---
fake_db = [
    {"id": 1, "title": "Learn FastAPI Basics and Routing", "done": True},
    {"id": 2, "title": "Implement Pydantic Models & Validation", "done": False},
    {"id": 3, "title": "Write Complete CRUD Endpoints", "done": False},
]

# --- Pydantic Models for Input Validation & Serialization ---
class TaskBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="The title of the FastAPI task",
        examples=["Master Dependency Injection"]
    )
    done: bool = Field(
        False, 
        description="Indicates whether the task has been completed"
    )

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=100, 
        description="Updated title for the task"
    )
    done: Optional[bool] = Field(
        None, 
        description="Updated completion status"
    )

class Task(TaskBase):
    id: int = Field(
        ..., 
        description="Unique identifier for the task"
    )

    class Config:
        from_attributes = True

# --- Root & Health Check Endpoints ---
@app.get(
    "/", 
    tags=["Root"], 
    summary="Welcome Root Endpoint",
    status_code=status.HTTP_200_OK
)
def read_root():
    """
    Returns a welcoming JSON message and directs developers to the interactive documentation.
    """
    return {
        "message": "Welcome to the FastAPI Toy CRUD API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get(
    "/health", 
    tags=["Health Check"], 
    summary="Application Health Check",
    status_code=status.HTTP_200_OK
)
def health_check():
    """
    Checks if the application is running smoothly.
    """
    return {"status": "healthy", "database": "connected (mock)"}

# --- CRUD Operations ---

@app.get(
    "/tasks", 
    response_model=List[Task], 
    tags=["Tasks"], 
    summary="Retrieve all tasks"
)
def get_tasks():
    """
    Retrieve a full list of all FastAPI-related tasks stored in the mock database.
    """
    return fake_db

@app.get(
    "/tasks/{task_id}", 
    response_model=Task, 
    tags=["Tasks"], 
    summary="Retrieve a single task by ID"
)
def get_task(task_id: int):
    """
    Fetch a specific task using its unique integer ID. 
    Raises a **404 Not Found** error if the task doesn't exist.
    """
    task = next((t for t in fake_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} could not be found."
        )
    return task

@app.post(
    "/tasks", 
    response_model=Task, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Tasks"], 
    summary="Create a new task"
)
def create_task(task: TaskCreate):
    """
    Create a new task. 
    - Automatically assigns an auto-incremented `id`.
    - Validates input length (3–100 characters) via Pydantic.
    """
    new_id = max((t["id"] for t in fake_db), default=0) + 1
    new_task = {"id": new_id, "title": task.title, "done": task.done}
    fake_db.append(new_task)
    return new_task

@app.put(
    "/tasks/{task_id}", 
    response_model=Task, 
    tags=["Tasks"], 
    summary="Update an existing task"
)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Partially or fully update an existing task by ID. 
    - Validates incoming fields.
    - Raises a **404 Not Found** error if the task ID doesn't exist.
    """
    task = next((t for t in fake_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} could not be found for updating."
        )
    
    # Update only fields provided in the request payload
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        task[key] = value
        
    return task

@app.delete(
    "/tasks/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    tags=["Tasks"], 
    summary="Delete a task"
)
def delete_task(task_id: int):
    """
    Delete a specific task from the mock database by ID.
    - Returns **204 No Content** upon success.
    - Raises a **404 Not Found** if the ID is missing.
    """
    task_index = next((i for i, t in enumerate(fake_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} could not be found for deletion."
        )
    
    fake_db.pop(task_index)
    return None