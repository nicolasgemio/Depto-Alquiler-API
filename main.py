import os
from dotenv import load_dotenv

load_dotenv('config/.env')
env = os.getenv("APP_ENV", "development")
load_dotenv(f"config/.{env}.env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from utils.containers import Container
from controllers.department_controller import DepartmentController
from controllers.auth_controller import AuthController
from controllers.search_controller import SearchController
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models  # <--- Esto importa todos los modelos definidos en models/__init__.py
from fastapi import APIRouter

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# vercel --prod

# Comando para permitir scripts firmados
#  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser