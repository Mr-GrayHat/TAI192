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
    status: str

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

# Crear una nueva tarea
@app.post("/tasks", tags=["Tareas"])
def create_task(task: Task):
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="El ID de la tarea ya existe")
    tasks.append(task)
    return {"message": "Tarea creada exitosamente", "task": task}

# Actualizar una tarea existente
@app.put("/tasks/{task_id}", tags=["Tareas"])
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return {"message": "Tarea actualizada exitosamente", "task": updated_task}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Eliminar una tarea
@app.delete("/tasks/{task_id}", tags=["Tareas"])
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Tarea eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

