import os
from datetime import datetime
import pytz
from fastapi import FastAPI, Request, Response, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
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
        @self.router.get("/searches", response_class=HTMLResponse)
        async def get_searches(request: Request, response: Response):
            current_user = request.session.get('user')
            if not current_user:
                return self.templates.TemplateResponse("login_page.html", {"request": request })

            user = self.user_service.get_user(current_user.get('sub'))

            searches = self.service.get_searches(user.user_id)
        
            return self.templates.TemplateResponse("searches.html", {"request": request, "searches": searches, "current_user": current_user })
        
        @self.router.get("/login_page", response_class=HTMLResponse)
        async def get_login_page(request: Request, response: Response):
            return self.templates.TemplateResponse("login_page.html", {"request": request})

    def get_local_time(date):
        utc_dt = date.replace(tzinfo=pytz.utc)

        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = utc_dt.astimezone(local_tz)

        fecha_local = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        return fecha_local
