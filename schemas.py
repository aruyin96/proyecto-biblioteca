from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str
    password: str

class UsuarioLogin(BaseModel):
    nombre: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LibroBase(BaseModel):
    titulo: str
    autor: str

class LibroOut(LibroBase):
    id: int
    class Config:
        orm_mode = True

class PrestamoCreate(BaseModel):
    libro_id: int

class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime]
    class Config:
        orm_mode = True
