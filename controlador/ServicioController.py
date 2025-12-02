from modelo.ServicioModel import ServicioModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./vista")

class ServicioController:
    
    @staticmethod
    async def detalle_servicio(request, codigo: str):
        """
        Controla la obtención y presentación del detalle de un servicio
        """
        # Obtener servicio a través del modelo
        servicio, mensaje_error = ServicioModel.obtener_servicio_por_codigo(codigo)
        
        if mensaje_error:
            # Si hay un error, mostramos la página de error
            return templates.TemplateResponse("error.html", {
                "request": request,
                "mensaje": mensaje_error
            })

        # Si encontramos el servicio, mostramos el detalle
        return templates.TemplateResponse("detalle_servicio.html", {
            "request": request,
            "servicio": servicio
        })

    @staticmethod
    async def listar_servicios_terapeuticos(request):
        """
        Controla la obtención y presentación de todos los servicios
        """
        servicios, mensaje_error = ServicioModel.obtener_todos_servicios()
        
        if mensaje_error:
            return templates.TemplateResponse("serv_terapia.html", {
                "request": request,
                "error_message": mensaje_error
            })

        return templates.TemplateResponse("serv_terapia.html", {
            "request": request,
            "servicios": servicios  # Por si quieres mostrar dinámicamente
        })

    @staticmethod
    async def filtrar_servicios(request, categoria: str):
        """
        Controla el filtrado de servicios por categoría
        """
        servicios, mensaje_error = ServicioModel.obtener_servicios_por_categoria(categoria)
        
        if mensaje_error:
            return templates.TemplateResponse("serv_terapia.html", {
                "request": request,
                "error_message": mensaje_error
            })

        return templates.TemplateResponse("serv_terapia.html", {
            "request": request,
            "servicios": servicios,
            "categoria_activa": categoria
        })