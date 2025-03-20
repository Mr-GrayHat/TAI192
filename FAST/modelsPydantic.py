from pydantic import BaseModel, Field, EmailStr

class modeloUsuario(BaseModel):
    name:str = Field(...,min_length=3, max_length=85, description="Nombre con mínimo de 3 letras y máximo a 85.")
    age:int = Field(..., ge=1, le=120)
    email:EmailStr = Field(..., examples=["Usuario23@gmail.com"])


class modeloAuth(BaseModel):
    email:EmailStr = Field(..., description="Correo electrónico válido", example="correo@example.com")
    passw: str = Field(..., min_length=8, strip_whitesapce=True, description="Contraseña de mínimo 8 caractéres")