from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from services.user_service import UserService
from fastapi.templating import Jinja2Templates

import os


from config.oauth import oauth

class AuthController:
    def __init__(self, router: APIRouter, service: UserService) -> None:
        self.router = router
        self.service = service

        self.templates = Jinja2Templates(directory="templates")


        self.base_uri = os.getenv("BASE_URI")

        # Rutas
        self.router.add_api_route("/login", self.login, methods=["GET"])
        self.router.add_api_route("/", self.auth, methods=["GET"])
        self.router.add_api_route("/logout", self.logout, methods=["GET"])

    # Métodos handler
    async def login(self, request: Request):
        redirect_uri = f"{self.base_uri}/auth"
        return await oauth.google.authorize_redirect(request, redirect_uri)

    async def auth(self, request: Request):
        token = await oauth.google.authorize_access_token(request)
        userinfo = await oauth.google.userinfo(token=token)
        userinfo_dic = request.session["user"] = dict(userinfo)
        
        current_user = self.service.get_user(userinfo_dic.get('sub'))
        if current_user is None:
            self.service.create_user(userinfo_dic)

        return RedirectResponse(url="/searches")

    async def logout(self, request: Request):
        request.session.pop("user", None)
        return RedirectResponse(url="/login_page")

# Instancia y exporta el router
