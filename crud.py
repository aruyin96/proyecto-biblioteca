from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash, verify_password
from datetime import datetime

def get_user_by_name(db: Session, nombre: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()

def create_user(db: Session, user: schemas.UsuarioCreate):
    db_user = models.Usuario(nombre=user.nombre, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, nombre: str, password: str):
    user = get_user_by_name(db, nombre)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_libros(db: Session):
    return db.query(models.Libro).all()

def crear_prestamo(db: Session, user_id: int, libro_id: int):
    prestamo_existente = db.query(models.Prestamo).filter_by(libro_id=libro_id, fecha_devolucion=None).first()
    if prestamo_existente:
        return None
    prestamo = models.Prestamo(usuario_id=user_id, libro_id=libro_id)
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo

def devolver_prestamo(db: Session, prestamo_id: int, user_id: int):
    prestamo = db.query(models.Prestamo).filter_by(id=prestamo_id, usuario_id=user_id).first()
    if not prestamo or prestamo.fecha_devolucion:
        return None
    prestamo.fecha_devolucion = datetime.utcnow()
    db.commit()
    return prestamo
