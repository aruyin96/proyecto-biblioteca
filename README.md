# 📚 Gestión de Biblioteca con FastAPI

La API permite gestionar préstamos de libros de una biblioteca con autenticación JWT.

## Cómo ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Demo paso a paso (Swagger)
1. POST /registro
2. POST /login
3. Click en Authorize con el token
4. GET /libros
5. POST /prestar
6. POST /devolver/{id}
