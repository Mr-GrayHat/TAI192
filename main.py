from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(
    title="My firts API S192",
    description="Rojo Lopez Christian Eduardo",
    version="0.1"

)

users = [
    {"id": 1, "name": "Christian Rojo", "age": 20},
    {"id": 2, "name": "Alejandro Malvido", "age":48 },
    {"id": 3, "name": "Elena Tatiana", "age": 24},
    {"id": 4, "name": "Emilio Rojo", "age": 24}
]

@app.get("/", tags=["Hellow world"])
def main():
    return {"message": "Hello World"}

@app.get("/average/", tags=["Mi calificacion TAI"])
async def average(num1: float, num2: float):
    promedio = (num1 + num2) / 2
    return {"num1": num1, "num2": num2, "promedio": promedio}

@app.get("/user/{id}", tags=["parametros obligatorios"])
def userQuery(id: int):
    # database connection
    #query
    return {'the user has found': id}


# endpoint with optional parameter

@app.get("/user/", tags=["parametro opcional"])
def userQuery(id: Optional[int] = None):
   if id is not None:
        for user in users:
            if user["id"] == id:
                return user
        return {"message": "user not found"}
   else:
    return {"message": "please insert a valid id"}
   

#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    userId: Optional[int] = None,
    name: Optional[str] = None,
    age: Optional[int] = None
):
    resultados = []

    for user in users:
        if (
            (userId is None or user["id"] == userId) and
            (name is None or user["name"].lower() == name.lower()) and
            (age is None or user["age"] == age)
        ):
            resultados.append(user)

    if resultados:
        return {"usuarios_encontrados": resultados}
    return {"message": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}


@app.get('/users/', tags=['Operaciones CRUD'])
def getUsers():
    return {"the users registered are: " : users}

@app.post('/addUser/', tags=['Operaciones CRUD'])
def addUser(user: dict):
    for existing_user in users:
        if existing_user['id'] == user['id']: 
            raise HTTPException(status_code=400, detail="User already exists")
    
    users.append(user)  
    return {"message": "User added successfully", "user": user}

@app.put('/updateUser/{id}', tags=['Operaciones CRUD'])
def updateUser(id: int, user: dict):
    for existing_user in users:
        if existing_user['id'] == id:
            existing_user.update(user)  
            return {"message": "User updated successfully", "user": existing_user}
    
    raise HTTPException(status_code=404, detail="User not found") 