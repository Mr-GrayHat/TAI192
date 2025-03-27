from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
from modelsPydantic import modeloUsuario, modeloAuth
from middlewares import BearerVWT
from genToken import createToken
from fastapi.responses import JSONResponse
from DB.conection import Session, engine, Base
from models.modelsDB import User

app = FastAPI(
    title="API de Usuarios",
    description="API completa con CRUD de usuarios",
    version='2.0.0'
)

Base.metadata.create_all(bind=engine)

# Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'message': 'Bienvenido a la API de usuarios'}


@app.post('/auth/', tags=['Autentificación'])
def login(autorización:modeloAuth):
    if autorización.email == 'crojo@example.com' and autorización.passw == '12345678':
        token:str = createToken(autorización.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso":"El usuario no está autorizado."}

@app.get('/usuarios', 
        #  dependencies=[Depends(BearerVWT())], 
         response_model=List[modeloUsuario], 
         tags=['Operaciones CRUD'])
def get_usuarios():
    db = Session()
    try:
        usuarios = db.query(User).all()
        return usuarios
    finally:
        db.close()

@app.get('/usuarios/{id}', 
         response_model=modeloUsuario, 
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
          response_model=modeloUsuario, 
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
         response_model=modeloUsuario, 
         tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modeloUsuario):
    db = Session()
    try:
        usuario = db.query(User).get(id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar campos
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
            status_code=status.HTTP_204_NO_CONTENT,
            tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).get(id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(usuario)
        db.commit()
        return
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error eliminando usuario: {str(e)}"
        )
    finally:
        db.close()