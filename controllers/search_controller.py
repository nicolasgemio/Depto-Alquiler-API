import os
from datetime import datetime
import pytz
from fastapi import FastAPI, Request, Response, HTTPException, Depends, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from repositories.department_repository import DepartmentRepository
from services.search_service import SearchService
from services.user_service import UserService

class SearchController:
    def __init__(self, router: APIRouter, service: SearchService, user_service: UserService):
        self.router = router
        self.service = service
        self.user_service = user_service
        self.templates = Jinja2Templates(directory="templates")

        self._define_routes()

    def _define_routes(self):

        @self.router.get("/all", response_class=JSONResponse)
        async def get_all(request: Request, response: Response):
            """
            Obtener todas las búsquedas
            """
            try:
                searches = self.service.get_all()
                return JSONResponse(content={"message": "busquedas obtenidas", "searches": [search.model_dump() for search in searches]}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"message": f"Error al obtener el busquedas: {e}"}, status_code=500)

        @self.router.get("/searches", response_class=HTMLResponse)
        async def get_searches(request: Request, response: Response):
            current_user = request.session.get('user')
            if not current_user:
                return self.templates.TemplateResponse("login_page.html", {"request": request })

            user = self.user_service.get_user(current_user.get('sub'))
            searches = self.service.get_searches(user.user_id)
        
            return self.templates.TemplateResponse("searches.html", {"request": request, "searches": searches, "current_user": current_user })
        
        @self.router.get("/searches/exists/search/{search_id}/department/{department_code}", response_class=JSONResponse)
        async def get_if_exists(search_id: str, department_code: str, request: Request, response: Response):
            department_id, is_loaded = self.service.get_if_exists(search_id, department_code)
            
            return JSONResponse(content={"message": "resultado obtenido", "is_loaded": is_loaded, "department_id": str(department_id)}, status_code=200)

        @self.router.get("/login_page", response_class=HTMLResponse)
        async def get_login_page(request: Request, response: Response):
            return self.templates.TemplateResponse("login_page.html", {"request": request})
        
        @self.router.post("/searches/search/{search_id}/department/{department_id}")
        async def create_search_department(search_id: str, department_id: str, request: Request, response: Response):
            created_search_department = self.service.insert_search_department(search_id, department_id)
            
            return JSONResponse(
                content={"mensaje": "Departamento vinculado", "search_department_id": str(created_search_department.search_department_id)},
                status_code=status.HTTP_200_OK
            )
        
        @self.router.post("/searches/notloaded/search/{search_id}", response_class=JSONResponse)
        async def get_not_loaded(search_id: str, request: Request, response: Response):
            body = await request.json()
            codes = body.get("codes", [])
            if not isinstance(codes, list):
                return JSONResponse(content={"message": "El campo codes debe ser una lista"}, status_code=400)
            departamentos = self.service.get_not_loaded(search_id, codes)
            return JSONResponse(content={"message": "resultado obtenido", "departments": [dpt.model_dump() for dpt in departamentos]}, status_code=200)

    def get_local_time(date):
        utc_dt = date.replace(tzinfo=pytz.utc)

        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = utc_dt.astimezone(local_tz)

        fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_local
