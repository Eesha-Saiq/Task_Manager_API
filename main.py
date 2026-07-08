from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI()

tasks = []

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    completed: bool = False

class Task(BaseModel):
    id: str 
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    completed: bool = False

@app.get("/")
def home():
    return {"message": "Task Manager API Running"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TaskCreate):

    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    tasks.append(new_task)

    return {
        "message": "Task added",
        "task": new_task
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}")
def update_task(task_id: str, updated_task: TaskUpdate):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            updated = Task(
                id=task.id,
                title=updated_task.title,
                description=updated_task.description,
                completed=updated_task.completed
            )

            tasks[index] = updated

            return {
                "message": "Task updated successfully",
                "task": updated
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }
    raise HTTPException(status_code=404, detail="Task not found")
