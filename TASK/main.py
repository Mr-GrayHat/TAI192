from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(
    title="To-Do List API",
    description="API para gestionar tareas",
    version="1.0"
)

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    expiration_date: str
    completed: str

tasks: List[Task] = []

# Obtener todas las tareas
@app.get("/tasks", tags=["Tareas"])
def get_tasks():
    return {"tasks": tasks}

# Obtener una tarea específica por ID
@app.get("/tasks/{task_id}", tags=["Tareas"])
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

