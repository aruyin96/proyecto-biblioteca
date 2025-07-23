from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, crud, auth, database
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# Agregar libros iniciales
from models import Libro
with SessionLocal() as db:
    if db.query(Libro).count() == 0:
        db.add_all([
            Libro(titulo="1984", autor="George Orwell"),
            Libro(titulo="Cien años de soledad", autor="Gabriel García Márquez"),
            Libro(titulo="Fahrenheit 451", autor="Ray Bradbury")
        ])
        db.commit()

app = FastAPI(title="API Biblioteca", description="Gestión de usuarios, libros y préstamos")
database.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registro", response_model=schemas.Token, summary="Registrar usuario")
def registrar(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_name(db, user.nombre):
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    user_creado = crud.create_user(db, user)
    token = auth.create_access_token({"sub": user.nombre})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token, summary="Iniciar sesión")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = auth.create_access_token({"sub": user.nombre})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/libros", response_model=list[schemas.LibroOut], summary="Listar libros")
def listar_libros(db: Session = Depends(get_db)):
    return crud.get_libros(db)

@app.post("/prestar", response_model=schemas.PrestamoOut, summary="Prestar libro")
def prestar(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db), user = Depends(auth.get_current_user)):
    resultado = crud.crear_prestamo(db, user.id, prestamo.libro_id)
    if not resultado:
        raise HTTPException(status_code=400, detail="El libro no está disponible")
    return resultado

@app.post("/devolver/{prestamo_id}", response_model=schemas.PrestamoOut, summary="Devolver libro")
def devolver(prestamo_id: int, db: Session = Depends(get_db), user = Depends(auth.get_current_user)):
    resultado = crud.devolver_prestamo(db, prestamo_id, user.id)
    if not resultado:
        raise HTTPException(status_code=400, detail="No se puede devolver este préstamo")
    return resultado
