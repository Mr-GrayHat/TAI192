from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List
from models import modeloUsuario, modeloAuth
from middlewares import BearerVWT
from genToken import createToken
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Mi primer API 192",
    description="fastAPI",
    version='1.0.1'
)


usuarios = [
    {"id": 1, "name": "Christian Rojo", "age": 20, "email": "crojo@example.com"},
    {"id": 2, "name": "Alejandro Malvido", "age":48, "email": "Amal@example.com"},
    {"id": 3, "name": "Elena Tatiana", "age": 24, "email": "Etat@example.com"},
    {"id": 4, "name": "Emilio Rojo", "age": 24, "email": "Erojo@example.com"},
]

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
@app.post('/usuarios/', response_model=modeloUsuario, tags = ['Operaciones CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail='Id ya existente.')
    usuarios.append(usuario)    
    return usuario

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
    
