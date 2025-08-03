import os
from dotenv import load_dotenv

load_dotenv('config/.env')
env = os.getenv("APP_ENV", "development")
load_dotenv(f"config/.{env}.env")

import firebase_admin
import pytz
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from utils.containers import Container
from controllers.department_controller import DepartmentController
from controllers.auth_controller import AuthController
from controllers.search_controller import SearchController
from fastapi.responses import RedirectResponse
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models  # <--- Esto importa todos los modelos definidos en models/__init__.py
from fastapi import APIRouter, Request


cred = credentials.Certificate("scrapping-deptos-2-firebase-adminsdk-fbsvc-0d283c648f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

container = Container()  # creamos el contenedor
app = FastAPI()
router = APIRouter()
app.container = container

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test")
def test_db(db: Session = Depends(get_db)):
    # Solo para testear conexión
    return {"message": "Conexión exitosa con la base de datos"}

auth_controller = AuthController(router, container.user_service())
search_controller = SearchController(router, container.search_service(), container.user_service())
department_controller = DepartmentController(router, container.department_service())


app.include_router(router, prefix="/auth")
app.include_router(department_controller.router)
app.include_router(search_controller.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

def sort_key_ampi(doc):
    data = doc.to_dict()
    rejected_n = data.get("rejected_n", False)
    rejected_a = data.get("rejected_a", False)
    favorito_n = data.get("favorito_n", False)
    favorito_a = data.get("favorito_a", False)
    creacion = data.get("creacion", datetime.min)  # Si no tiene fecha, usa datetime.min
    
    # Asignamos prioridad (valores más pequeños van primeros en sorted)
    if favorito_n or favorito_a:
        priority = 0  # Favoritos primero
    elif rejected_n:
        priority = 1  # Luego los rechazados por Nico
    elif not rejected_a:
        priority = 2  # Los que no están rechazados por nadie en el medio
    else:
        priority = 3  # Los rechazados por Ampi al final

    return (priority, creacion)

def sort_key_nico(doc):
    data = doc.to_dict()
    rejected_n = data.get("rejected_n", False)
    rejected_a = data.get("rejected_a", False)
    favorito_n = data.get("favorito_n", False)
    favorito_a = data.get("favorito_a", False)
    creacion = data.get("creacion", datetime.min)  # Si no tiene fecha, usa datetime.min

    # Asignamos prioridad (valores más pequeños van primeros en sorted)
    if favorito_n or favorito_a:
        priority = 0  # Favoritos primero
    elif rejected_a:
        priority = 1  # Luego los rechazados por Nico
    elif not rejected_n:
        priority = 2  # Los que no están rechazados por nadie en el medio
    else:
        priority = 3  # Los rechazados por Ampi al final

    return (priority, creacion)


class CommentRequest(BaseModel):
    comentario: str

@app.post("/comment/{departamento_id}")
def comentar_departamento(departamento_id: str, request: Request, body: CommentRequest):
    comentario = body.comentario

    person = request.cookies.get("person")
    if not person:
        return templates.TemplateResponse("seleccionar_persona.html", {"request": request })

    if person not in ['nico', 'ampi']:
        raise HTTPException(status_code=400, detail="Persona no válida")

    campo = "comentario_n" if person == "nico" else "comentario_a"
    
    db.collection("deptos").document(departamento_id).update({campo: comentario})
    
    return {"mensaje": "Departamento comentado"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# vercel --prod

# Comando para permitir scripts firmados
#  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser