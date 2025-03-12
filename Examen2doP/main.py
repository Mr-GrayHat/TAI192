from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal

app = FastAPI(
    title="Mi primer API 192",
    description="FastAPI",
    version='1.0.1'
)

conductores = []

class ModeloConductores(BaseModel):
    noLicencia: str = Field(..., min_length=12, max_length=12 ,description="Número de licencia de conducir, 12 caracteres, debe ser único.")
    nombre: str = Field(..., min_length=3, max_length=85, description="Nombre con mínimo de 3 letras y máximo a 85.")
    tipoLicencia: Literal["A", "B", "C", "D"] = Field(..., description="Tipo de licencia de conducir (A, B, C, D)")

@app.get('/conductores', response_model=List[ModeloConductores], tags=['Operaciones CRUD'])
def leer_usuarios():
    return conductores

@app.post('/conductores/', response_model=ModeloConductores, tags=['Operaciones CRUD'])
def agregar_usuario(conductor: ModeloConductores):
    for usr in conductores:
        if usr.noLicencia == conductor.noLicencia:
            raise HTTPException(status_code=400, detail='Número de licencia ya existente.')
    
    conductores.append(conductor)    
    return conductor

@app.put('/conductores/{noLicencia}', response_model=ModeloConductores, tags=['Operaciones CRUD'])
def actualizar_conductor(noLicencia: str, usuario_actualizado: ModeloConductores):
    for index, usr in enumerate(conductores):
        if usr.noLicencia == noLicencia:
            conductores[index] = usuario_actualizado  
            return usuario_actualizado
    raise HTTPException(status_code=404, detail="El número de licencia no existe")
