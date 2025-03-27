from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
from pydantic import BaseModel, Field, EmailStr
from DB.conection import Session, engine, Base
from models.modelsDB import User
from genToken import createToken
from fastapi.responses import JSONResponse

# Creación de la app
app = FastAPI(
    title="API de Usuarios",
    description="API completa con CRUD de usuarios",
    version='2.0.0'
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# --------------------------------------
# Modelos Pydantic
# --------------------------------------
class modeloUsuario(BaseModel):
    name: str = Field(..., min_length=3, max_length=85, description="Nombre con mínimo de 3 letras y máximo a 85.")
    age: int = Field(..., ge=1, le=120)
    email: EmailStr = Field(..., examples=["Usuario23@gmail.com"])

class modeloUsuarioResponse(modeloUsuario):
    id: int

class modeloAuth(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico válido", example="correo@example.com")
    passw: str = Field(..., min_length=8, description="Contraseña de mínimo 8 caractéres")

# --------------------------------------
# Endpoints
# --------------------------------------
@app.get('/', tags=['Hola mundo'])
def home():
    return {'message': 'Bienvenido a la API de usuarios'}

@app.post('/auth/', tags=['Autentificación'])
def login(autorización: modeloAuth):
    if autorización.email == 'crojo@example.com' and autorización.passw == '12345678':
        token: str = createToken(autorización.model_dump())
        return JSONResponse(content=token)
    else:
        return {"Aviso": "El usuario no está autorizado."}

@app.get('/usuarios', 
         response_model=List[modeloUsuarioResponse], 
         tags=['Operaciones CRUD'])
def get_usuarios():
    db = Session()
    try:
        usuarios = db.query(User).all()
        return usuarios
    finally:
        db.close()

@app.get('/usuarios/{id}', 
         response_model=modeloUsuarioResponse, 
         tags=['Operaciones CRUD'])
def get_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).get(id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    finally:
        db.close()

@app.post('/usuarios/', 
          response_model=modeloUsuarioResponse, 
          status_code=status.HTTP_201_CREATED,
          tags=['Operaciones CRUD'])
def crear_usuario(usuario: modeloUsuario):
    db = Session()
    try:
        db_user = User(**usuario.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creando usuario: {str(e)}"
        )
    finally:
        db.close()

@app.put('/usuarios/{id}', 
         response_model=modeloUsuarioResponse, 
         tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modeloUsuario):
    db = Session()
    try:
        usuario = db.query(User).get(id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        for key, value in usuario_actualizado.model_dump().items():
            setattr(usuario, key, value)
            
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error actualizando usuario: {str(e)}"
        )
    finally:
        db.close()

@app.delete('/usuarios/{id}', 
            status_code=status.HTTP_200_OK, 
            tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).get(id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(usuario)
        db.commit()
        return {"detail": "Usuario eliminado exitosamente"}  
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error eliminando usuario: {str(e)}"
        )
    finally:
        db.close()