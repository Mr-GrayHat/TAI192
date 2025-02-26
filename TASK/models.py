from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int = Field(..., gt=0, description="El ID debe ser un número entero positivo")
    nombre: str = Field(..., min_length=2, max_length=50, description="El nombre debe tener entre 2 y 50 caracteres")
    edad: int = Field(..., ge=18, le=100, description="La edad debe estar entre 18 y 100 años")
    correo: EmailStr = Field(..., description="Debe ser un correo electrónico válido")