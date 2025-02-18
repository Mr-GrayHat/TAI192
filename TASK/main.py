from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(
    title="To-Do List API",
    description="API para gestionar tareas",
    version="1.0"
)

# Modelo de datos para una tarea
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Base de datos simulada
tasks: List[Task] = []

# Obtener todas las tareas
@app.get("/tasks", tags=["Tareas"])
def get_tasks():
    return {"tasks": tasks}

