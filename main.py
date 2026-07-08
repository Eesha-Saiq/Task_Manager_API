from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import uuid
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
print("API TOKEN =", API_TOKEN)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="my_session_secret"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []

def verify_token(
    request: Request,
    authorization: str = Header(None)
):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    request.session["authenticated"] = True

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
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.get("/")
def home():
    return {"message": "Task Manager API Running"}


@app.get("/tasks")
def get_tasks(token: str = Depends(verify_token)):
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: str, token: str = Depends(verify_token)):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.post("/tasks")
def create_task(task: TaskCreate, token: str = Depends(verify_token)):

    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    tasks.append(new_task)

    return {
        "message": "Task added successfully",
        "task": new_task
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: str, updated_task: TaskUpdate, token: str = Depends(verify_token)):

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
def delete_task(task_id: str, token: str = Depends(verify_token)):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.get("/me")
def get_me(request: Request):

    if "authenticated" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="No active session"
        )

    return {
        "message": "Session Active",
        "session": request.session
    }

@app.post("/logout")
def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logged out successfully"
    }