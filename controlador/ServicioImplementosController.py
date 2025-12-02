from modelo.ServicioImplementosModel import ServicioImplementosModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./vista")

class ServicioImplementosController:
    
    @staticmethod
    async def detalle_servicio(request, codigo: str):
        """
        Controla la obtención y presentación del detalle de un implemento
        """
        servicio, mensaje_error = ServicioImplementosModel.obtener_servicio_por_codigo(codigo)
        
        if mensaje_error:
            return templates.TemplateResponse("serv_implementos.html", {
                "request": request,
                "mensaje": mensaje_error
            })

        return templates.TemplateResponse("detalle_implementos.html", {
            "request": request,
            "servicio_implementos": servicio
        })

    @staticmethod
    async def listar_servicios_implementos(request):
        """
        Controla la presentación de la página de implementos
        """
        return templates.TemplateResponse("serv_implementos.html", {
            "request": request
        })