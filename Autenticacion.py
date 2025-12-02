from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rutas que no requieren autenticación
        public_routes = ["/", "/login_user", "/registro_user", "/validar_acceso", "/registro_usuario"]
        
        # Si la ruta no es pública y no hay usuario en sesión, redirigir al login
        if (not any(request.url.path.startswith(route) for route in public_routes) and 
            "usuario" not in request.session):
            return RedirectResponse(url="/login_user")
        
        response = await call_next(request)
        return response

# Agrega el middleware a la app
app.add_middleware(AuthMiddleware)