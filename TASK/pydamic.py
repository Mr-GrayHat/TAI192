from fastapi import FastAPI, HTTPException
from models import User
from typing import List

app = FastAPI()

# Lista de ejemplo con usuarios precargados
usuarios_db = [
    User(id=1, nombre="Juan Pérez", edad=30, correo="juan.perez@example.com"),
    User(id=2, nombre="María García", edad=25, correo="maria.garcia@example.com"),
    User(id=3, nombre="Carlos López", edad=40, correo="carlos.lopez@example.com"),
]

@app.get("/usuarios", response_model=List[User])
def obtener_usuarios():
    return usuarios_db

@app.post("/usuarios", response_model=User)
def crear_usuario(usuario: User):
    # Verificar si el ID ya existe
    if any(u.id == usuario.id for u in usuarios_db):
        raise HTTPException(status_code=400, detail="El ID ya existe")
    
    usuarios_db.append(usuario)
    return usuario

@app.put("/usuarios/{user_id}", response_model=User)
def actualizar_usuario(user_id: int, usuario_actualizado: User):
    for index, usuario in enumerate(usuarios_db):
        if usuario.id == user_id:
           usuarios_db[index] = usuario_actualizado
           return usuario_actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado")