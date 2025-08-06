from datetime import datetime
import pytz
from fastapi import FastAPI, Request, Response, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.department_service import DepartmentService
from fastapi import APIRouter, Request, Query
from services.department_service import DepartmentService
from enumerables.reaction_type_enum import ReactionTypeEnum
from dtos.comment_request import CommentRequest
import os
from dotenv import load_dotenv

class DepartmentController:
    def __init__(self, router: APIRouter, service: DepartmentService):
        self.router = router
        self.service = service
        self.templates = Jinja2Templates(directory="templates")

        self._mount_routes()
        self._define_routes()

    def _mount_routes(self):
        pass

    def _define_routes(self):
        @self.router.get("/")
        async def index(request: Request):
            user = request.session.get('user')
            if user:
                return RedirectResponse(url='/searches')
            return RedirectResponse(url='/login_page')

        @self.router.get("/seleccionar-persona", response_class=HTMLResponse)
        async def seleccionar_persona(request: Request):
            return self.templates.TemplateResponse("departments.html", {"request": request})

        @self.router.get("/departments", response_class=HTMLResponse)
        async def get_departments(request: Request, response: Response, search_id: str = Query(None)):
            current_user = request.session.get('user')
            if current_user is None:
                return RedirectResponse(url='/login_page')
            
            user = self.service.user_service.get_user(current_user.get('sub'))
            if not user:
                return RedirectResponse(url='/logint_page')
            
            if search_id is None or search_id == "":
                return RedirectResponse(url='/searches')
            
            departmens = self.service.get_departments(search_id, user.user_id)

            return self.templates.TemplateResponse("departments.html", {"request": request, "departments": departmens, "user_id": user.user_id})

        @self.router.get('/departments/{search_departament_id}')
        async def department_detail(request: Request, search_departament_id: str, response_class=HTMLResponse):
            current_user = request.session.get('user')
            if current_user is None:
                return RedirectResponse(url='/login_page')

            user = self.service.user_service.get_user(current_user.get('sub'))
            if not user:
                return RedirectResponse(url='/login_page')
            
            search_departament = self.service.get_department_by_id(search_departament_id)

            return self.templates.TemplateResponse(
                "department_detail.html",
                {"request": request, "search_department": search_departament, "user_id": user.user_id }
            )

        @self.router.post("/reject/{search_departament_id}", response_class=JSONResponse)
        def rechazar_departamento(search_departament_id: str, request: Request):
            try:
                user = request.session.get('user')

                if user is None:
                    return JSONResponse(
                        content={"mensaje": "No autorizado"},
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

                self.service.react_department(search_departament_id, user.get('sub'), ReactionTypeEnum.REJECT)
                return JSONResponse(
                    content={"mensaje": "Departamento rechazado"},
                    status_code=status.HTTP_200_OK
                )

            except Exception as e:
                print(f"Error al rechazar el departamento: {e}")
                return JSONResponse(
                    content={"mensaje": "Error al rechazar el departamento"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        @self.router.post("/favorite/{search_departament_id}", response_class=JSONResponse)
        def resaltar_departamento(search_departament_id: str, request: Request):
            try:
                user = request.session.get('user')

                if user is None:
                    return JSONResponse(
                        content={"mensaje": "No autorizado"},
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

                self.service.react_department(search_departament_id, user.get('sub'), ReactionTypeEnum.FAVORITE)
                return JSONResponse(
                    content={"mensaje": "Departamento resaltado"},
                    status_code=status.HTTP_200_OK
                )

            except Exception as e:
                print(f"Error al resaltar el departamento: {e}")
                return JSONResponse(
                    content={"mensaje": "Error al resaltar el departamento"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        @self.router.post("/remove/{search_department_id}", response_class=JSONResponse)
        def removeDepartment(search_department_id: str, request: Request):
            try:
                user = request.session.get('user')
                if user is None:
                    return JSONResponse(
                        content={"mensaje": "No autorizado"},
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

                self.service.remove_department(search_department_id, user.get('sub'))

                return JSONResponse(
                    content={"mensaje": "Departamento removido"},
                    status_code=status.HTTP_200_OK
                )
            except Exception as e:
                print(f"Error al eliminar el departamento: {e}")
                return JSONResponse(
                    content={"mensaje": "Error al eliminar el departamento"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        @self.router.post("/comment/{search_department_id}")
        def comentar_departamento(search_department_id: str, request: Request, body: CommentRequest):
            try:
                user = request.session.get('user')
                if user is None:
                    return JSONResponse(
                        content={"mensaje": "No autorizado"},
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

                self.service.comment_department(search_department_id, user.get('sub'), body.commentary)

                return JSONResponse(
                    content={"mensaje": "Departamento comentado"},
                    status_code=status.HTTP_200_OK
                )
            except Exception as e:
                print(f"Error al comentar el departamento: {e}")
                return JSONResponse(
                    content={"mensaje": "Error al comentar el departamento"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        @self.router.get("/config")
        def get_config():
            load_dotenv('config/.env')
            env = os.getenv("APP_ENV", "development")
            load_dotenv(f"config/.{env}.env")

            return { "base_url": os.getenv("BASE_URL") }


    def get_local_time(self, create_date):
        utc_dt = create_date.replace(tzinfo=pytz.utc)
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        return utc_dt.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")

    def sort_key_nico(self, doc):
        data = doc.to_dict()
        favorito_n = data.get("favorito_n", False)
        favorito_a = data.get("favorito_a", False)
        rejected_a = data.get("rejected_a", False)
        rejected_n = data.get("rejected_n", False)
        creacion = data.get("creacion", datetime.min)
        if favorito_n or favorito_a:
            priority = 0
        elif rejected_a:
            priority = 1
        elif not rejected_n:
            priority = 2
        else:
            priority = 3
        return (priority, creacion)

    def get_app(self):
        return self.app

# Instancia y exporta el router

