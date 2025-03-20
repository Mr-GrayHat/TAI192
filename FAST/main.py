from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from middlewares import BearerVWT
from genToken import createToken
from fastapi.responses import JSONResponse
from DB.conection import Session,engine,Base
from models.modelsDB import User

app = FastAPI(
    title="Mi primer API 192",
    description="fastAPI",
    version='1.0.1'
)

Base.metadata.create_all(bind=engine)

# usuarios = [
#     {"id": 1, "name": "Christian Rojo", "age": 20, "email": "crojo@example.com"},
#     {"id": 2, "name": "Alejandro Malvido", "age":48, "email": "Amal@example.com"},
#     {"id": 3, "name": "Elena Tatiana", "age": 24, "email": "Etat@example.com"},
#     {"id": 4, "name": "Emilio Rojo", "age": 24, "email": "Erojo@example.com"},
# ]

#Endpoint home
@app.get('/', tags=['Hola mundo'])
def home():
    return {'hello':'world fastAPI'}

# Endpoint Autenticación
@app.post('/auth/', tags=['Autentificación'])
def login(autorización:modeloAuth):
    if autorización.email == 'crojo@example.com' and autorización.passw == '12345678':
        token:str = createToken(autorización.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso":"El usuario no está autorizado."}


#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios',dependencies=[Depends(BearerVWT())], response_model = List[modeloUsuario], tags=['Operaciones CRUD'])
def leerUsuarios():
    return usuarios

# Endpoint - Agregar nuevos usuarios
@app.post('/usuarios/', response_model=modeloUsuario, status_code=201, tags=['Operaciones CRUD'])
def agregarUsuario(usuario: modeloUsuario):
    # Crear sesión de base de datos correctamente (ajusta SessionLocal según tu configuración)
    db = Session()
    try:
        # 1. Crear instancia del modelo de base de datos
        db_user = User(**usuario.model_dump())
        
        # 2. Agregar y confirmar transacción
        db.add(db_user)
        db.commit()
        
        # 3. Refrescar para obtener datos generados (como ID)
        db.refresh(db_user)
        
        # 4. Convertir a modelo Pydantic y retornar
        return modeloUsuario.model_validate(db_user, from_attributes=True)
    
    except Exception as e:
        db.rollback()
        # Usar HTTPException para manejo de errores estándar
        raise HTTPException(
            status_code=400,
            detail=f"Error al agregar usuario: {str(e)}"
        )
    
    finally:
        # Asegurar cierre de sesión
        db.close()

# Endpoint - Modificar usuario
@app.put('/usuariosPut/{id}', response_model=modeloUsuario, tags=['Operaciones CRUD'])
def usuariosPut(id:int, usuarioActualizado:modeloUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]=usuarioActualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=400, detail="El id no existe")

# Endpoint - Eliminar usuario
@app.delete('/usuarioDelete/{id}', tags=['Operaciones CRUD'])
def usuariosDelete(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) 
            return {"message": "Usuario eliminado", "usuarios": usuarios}
    raise HTTPException(status_code=404, detail='Id no existente.')
    
