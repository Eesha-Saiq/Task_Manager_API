from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    description: str 

@app.get("/")
def home():
    return {"message": "Task Manager API Running"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added", "task": task}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    return {"message": "Task not found"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            tasks[index] = updated_task

            return {
                "message": "Task updated",
                "task": updated_task
            }

    return {"message": "Task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    return {"message": "Task not found"}