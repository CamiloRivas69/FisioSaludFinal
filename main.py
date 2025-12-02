from datetime import datetime
from http.client import HTTPException
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bd.conexion_bd import close_db_connection, get_db_connection
from controlador import CarritoController, CitaPacienteController, ReporteFisioController
from controlador.AuthFisioController import AuthFisioController
from controlador.AuthController import AuthController
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
from controlador.EjercicioPacienteController import EjercicioPacienteController
from controlador.ReporteFisioController import ReporteFisioController
from controlador.CitaController import CitaController
from controlador.CitaPacienteController import CitaPacienteController 
from controlador.ServicioController import ServicioController
from controlador.ServicioNutricionController import ServicioNutricionController
from controlador.PacienteFisioController import PacienteFisioController
from controlador.ServicioImplementosController import ServicioImplementosController
from controlador.CitaFisioController import CitaFisioController
from starlette.middleware.sessions import SessionMiddleware

from fastapi import Form, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware  # ✅ IMPORTANTE: Agregar esto
import secrets
import shutil
import os
app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key="tu_clave_secreta_muy_larga_aqui_1234567890",  # 32 caracteres mínimo
    session_cookie="fisiosalud_session",
    max_age=3600,
    same_site="lax",
    https_only=False
)

templates = Jinja2Templates(directory="./vista")
templates_panel = Jinja2Templates(directory="./vista_panel")
templates_admin = Jinja2Templates(directory="./vista_admin")
templates_fisio = Jinja2Templates(directory="./vista_fisio")

@app.get("/", response_class=HTMLResponse)
def pagina_inicio(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})

@app.get("/inicio", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})


@app.get("/nosotros", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("nosotros.html", {"request": request})

@app.get("/serv_terapia", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_terapia.html", {"request": request})

@app.get("/requisitos_especiales", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("requisitos_analisis.html", {"request": request})

@app.get("/servicios_terapia", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_terapia.html", {"request": request})

@app.get("/implementos", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_implementos.html", {"request": request})

@app.get("/nutricionales", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_alimentos.html", {"request": request})

@app.get("/advertencia", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("advertencia.html", {"request": request})

@app.get("/anuncio", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("Anuncio.html", {"request": request})

@app.get("/anuncio_2", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("anuncio_2.html", {"request": request})

@app.get("/administrador", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates_admin.TemplateResponse("panel_login_admin.html", {"request": request})

@app.get("/fisioterapeuta", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates_fisio.TemplateResponse("panel_login_fisio.html", {"request": request})

@app.get("/panel_fisio", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates_fisio.TemplateResponse("panel_login_fisio.html", {"request": request})

# ─────────────────────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────────────────────

# -- Barra de navegacion -- ─────────────────────────────────────────────────────────────



@app.get("/servicios", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("servicios.html", {"request": request})

@app.get("/fisiobot", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("Fisio_AI.html", {"request": request})

@app.get("/contacto", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("info_contacto.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/registro", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

# -- Main Page -- ─────────────────────────────────────────────────────────────
@app.get("/servicios", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("servicios.html", {"request": request})

@app.get("/cita", response_class=HTMLResponse)
async def pagina_servicios(request: Request, servicio: Optional[str] = None):
    return await CitaController.mostrar_formulario_cita(request, servicio_codigo=servicio)

# -- Servicios -- ─────────────────────────────────────────────────────────────

@app.get("/servicios_terapeuticos", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_terapia.html", {"request": request})

@app.get("/servicios_alimenticios", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_alimentos.html", {"request": request})
    
@app.get("/servicios_implementos", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("serv_implementos.html", {"request": request})

# -- AI seccion -- ─────────────────────────────────────────────────────────────

@app.get("/Fisiobot", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("fisiobot.html", {"request": request})

@app.get("/contacto", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("info_contacto.html", {"request": request})

@app.get("/analisis", response_class=HTMLResponse)
def pagina_servicios(request: Request):
    return templates.TemplateResponse("analisis_previo.html", {"request": request})


# ─────────────────────────────────────────────────────────────
# lOGIN Y REGISTRO
# ─────────────────────────────────────────────────────────────


@app.get("/registro_user", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

@app.get("/inicio", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})

@app.get("/login_user", response_class=HTMLResponse)
def pagina_servicios_terapeuticos(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



# ─────────────────────────────────────────────────────────────
# RESTFULL API PARA REGISTRO DE USUARIOS
# ─────────────────────────────────────────────────────────────


@app.post("/validar_acceso", response_class=HTMLResponse)
async def validar_acceso(
    request: Request, 
    correo: str = Form(...), 
    contraseña: str = Form(...)
):
    return await AuthController.validar_acceso(request, correo, contraseña)




# ─────────────────────────────────────────────────────────────
# RESTFULL API PARA SERVICIOS
# ─────────────────────────────────────────────────────────────

@app.get("/serv_terapia", response_class=HTMLResponse)
async def pagina_servicios_terapeuticos(request: Request):
    return await ServicioController.listar_servicios_terapeuticos(request)

@app.get("/servicio/{codigo}", response_class=HTMLResponse)
async def detalle_servicio(request: Request, codigo: str):
    return await ServicioController.detalle_servicio(request, codigo)

@app.get("/servicios/filtrar/{categoria}", response_class=HTMLResponse)
async def filtrar_servicios(request: Request, categoria: str):
    return await ServicioController.filtrar_servicios(request, categoria)


@app.get("/nutricion/{codigo}", response_class=HTMLResponse)
async def detalle_nutricion(request: Request, codigo: str):
    return await ServicioNutricionController.detalle_servicio(request, codigo)

@app.get("/nutricionales", response_class=HTMLResponse)
async def pagina_servicios_nutricion(request: Request):
    return await ServicioNutricionController.listar_servicios_nutricion(request)

@app.get("/implementos/{codigo}", response_class=HTMLResponse)
async def detalle_implementos(request: Request, codigo: str):
    return await ServicioImplementosController.detalle_servicio(request, codigo)

@app.get("/implementos", response_class=HTMLResponse)
async def pagina_servicios_implementos(request: Request):
    return await ServicioImplementosController.listar_servicios_implementos(request)



# ─────────────────────────────────────────────────────────────
# RESTFULL API PARA CITAS
# ─ ────────────────────────────────────────────────────────────

@app.get("/agendar-cita", response_class=HTMLResponse)
async def mostrar_formulario_cita(request: Request):
    return await CitaController.mostrar_formulario_cita(request)

@app.get("/api/servicios-terapia")
async def obtener_servicios_terapia_api(request: Request):
    return await CitaController.obtener_servicios_api(request)

@app.post("/api/agendar-cita")
async def agendar_cita_api(
    request: Request,
    servicio: str = Form(...),
    terapeuta_designado: str = Form(...),
    nombre_paciente: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    fecha_cita: str = Form(...),
    hora_cita: str = Form(...),
    tipo_pago: str = Form(...),
    notas_adicionales: Optional[str] = Form(None),
    acudiente_nombre: Optional[str] = Form(None),
    acudiente_id: Optional[str] = Form(None),
    acudiente_telefono: Optional[str] = Form(None),
    acudiente_correo: Optional[str] = Form(None),
    emails_adicionales: Optional[str] = Form(None)
):
    return await CitaController.agendar_cita(
        request=request,
        servicio=servicio,
        terapeuta_designado=terapeuta_designado,
        nombre_paciente=nombre_paciente,
        telefono=telefono,
        correo=correo,
        fecha_cita=fecha_cita,
        hora_cita=hora_cita,
        notas_adicionales=notas_adicionales,
        tipo_pago=tipo_pago,
        acudiente_nombre=acudiente_nombre,
        acudiente_id=acudiente_id,
        acudiente_telefono=acudiente_telefono,
        acudiente_correo=acudiente_correo,
        emails_adicionales=emails_adicionales
    )


# ─────────────────────────────────────────────────────────────
# PANELES DE USUARIO
# ─────────────────────────────────────────────────────────────

@app.get("/registro")
async def registro_page(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

@app.get("/login_user")
async def login_user_page(request: Request):
    error = request.session.pop('error', None)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error_message": error
    })

@app.post("/login_user")
async def login_user(
    request: Request,
    correo: str = Form(...),
    contraseña: str = Form(...)
):
    return await AuthController.validar_acceso(request, correo, contraseña)

@app.get("/logout_user")
async def logout_user(request: Request):
    return await AuthController.cerrar_sesion(request)

@app.post("/registro_usuario")
async def registrar_usuario(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    genero: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    contraseña: str = Form(...),
    contraseña_confirmada: str = Form(...),
    ID: str = Form(...),
    historial_medico: UploadFile = File(None)
):
    from controlador.AuthController import AuthController
    return await AuthController.registrar_usuario(
        request, nombre, apellido, genero, email, telefono, 
        contraseña, contraseña_confirmada, ID, historial_medico
    )

@app.get("/panel_citas", response_class=HTMLResponse)
async def panel_citas(request: Request):
    """Panel de citas del usuario con verificación de sesión"""
    print("🔍 Accediendo a /panel_citas...")
    usuario = AuthController.verificar_sesion_usuario(request)
    
    if not usuario:
        print("❌ No hay sesión en /panel_citas, redirigiendo...")
        request.session['error'] = 'Por favor, inicie sesión primero'
        return RedirectResponse(url="/login_user", status_code=302)
    
    print(f"✅ Sesión válida para: {usuario['email']}")
    return templates_panel.TemplateResponse("panel_citas.html", {
        "request": request,
        "usuario": usuario
    })


@app.get("/panel_progreso", response_class=HTMLResponse)
async def panel_progreso(request: Request):
    """Panel de progreso del usuario con verificación de sesión"""
    usuario = AuthController.verificar_sesion_usuario(request)
    if not usuario:
        request.session['error'] = 'Por favor, inicie sesión primero'
        return RedirectResponse(url="/login_user", status_code=302)
    
    return templates_panel.TemplateResponse("panel_progreso.html", {
        "request": request,
        "usuario": usuario
    })

@app.get("/panel_ejercicios", response_class=HTMLResponse)
async def panel_ejercicios(request: Request):
    """Panel de ejercicios del usuario con verificación de sesión"""
    usuario = AuthController.verificar_sesion_usuario(request)
    if not usuario:
        request.session['error'] = 'Por favor, inicie sesión primero'
        return RedirectResponse(url="/login_user", status_code=302)
    
    return templates_panel.TemplateResponse("panel_ejercicios.html", {
        "request": request,
        "usuario": usuario
    })




# ─────────────────────────────────────────────────────────────
# PANELES DE USUARIO - CITAS
# ─────────────────────────────────────────────────────────────

@app.get("/api/citas/paciente")
async def api_obtener_citas_paciente(request: Request):
    print("🔍 [ROUTE] /api/citas/paciente llamado")
    return await CitaPacienteController.obtener_citas_paciente(request)

@app.get("/api/citas/proximas")
async def api_obtener_citas_proximas(request: Request):
    print("🔍 [ROUTE] /api/citas/proximas llamado")
    return await CitaPacienteController.obtener_citas_proximas(request)

@app.get("/api/citas/{cita_id}") 
async def api_obtener_cita_por_id(request: Request, cita_id: str):
    print(f"🔍 [ROUTE] /api/citas/{cita_id} llamado")
    return await CitaPacienteController.obtener_cita_por_id(request, cita_id)

@app.get("/api/citas/estadisticas")
async def api_obtener_estadisticas(request: Request):
    print("🔍 [ROUTE] /api/citas/estadisticas llamado")
    return await CitaPacienteController.obtener_estadisticas(request)


# ─────────────────────────────────────────────────────────────
# PANELES DE USUARIO - EJERCICIOS
# ─────────────────────────────────────────────────────────────

# Agregar estos endpoints a tu archivo principal

@app.get("/api/ejercicios/debug-ejercicios")
async def api_debug_ejercicios_bd(request: Request):
    """Endpoint para ver todos los ejercicios en la BD"""
    from bd.conexion_bd import get_db_connection
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT codigo_ejercicio, nombre_ejercicio FROM ejercicios")
            ejercicios = cursor.fetchall()
            
            print("🔍 TODOS LOS EJERCICIOS EN LA BD:")
            for ej in ejercicios:
                print(f"   - Código: '{ej['codigo_ejercicio']}', Nombre: '{ej['nombre_ejercicio']}'")
            
            return JSONResponse({
                "success": True,
                "ejercicios": ejercicios
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.get("/api/ejercicios/paciente")
async def api_obtener_ejercicios_paciente(request: Request):
    print("🔍 [ROUTE] /api/ejercicios/paciente llamado")
    return await EjercicioPacienteController.obtener_ejercicios_paciente(request)

@app.get("/api/ejercicios/completados")
async def api_obtener_ejercicios_completados(request: Request):
    print("🔍 [ROUTE] /api/ejercicios/completados llamado")
    return await EjercicioPacienteController.obtener_ejercicios_completados(request)

@app.get("/api/ejercicios/pendientes")
async def api_obtener_ejercicios_pendientes(request: Request):
    print("🔍 [ROUTE] /api/ejercicios/pendientes llamado")
    return await EjercicioPacienteController.obtener_ejercicios_pendientes(request)

@app.get("/api/ejercicios/estadisticas")
async def api_obtener_estadisticas_ejercicios(request: Request):
    print("🔍 [ROUTE] /api/ejercicios/estadisticas llamado")
    return await EjercicioPacienteController.obtener_estadisticas(request)

@app.post("/api/ejercicios/completar")
async def api_marcar_ejercicio_completado(request: Request):
    return await EjercicioPacienteController.marcar_como_completado(request)

@app.get("/api/ejercicios/{codigo_ejercicio}")
async def api_obtener_ejercicio_por_codigo(request: Request, codigo_ejercicio: str):
    print(f"🔍 [ROUTE] /api/ejercicios/{codigo_ejercicio} llamado")
    return await EjercicioPacienteController.obtener_ejercicio_por_codigo(request, codigo_ejercicio)



# ─────────────────────────────────────────────────────────────
# PANELES DE USUARIO - PRODUCTOS
# ─────────────────────────────────────────────────────────────


@app.post("/api/carrito/agregar")
async def api_agregar_carrito(request: Request):
    print("✅ RUTA /api/carrito/agregar LLAMADA")
    from controlador.CarritoController import CarritoController
    return await CarritoController.agregar_al_carrito(request)

@app.post("/api/carrito/eliminar")
async def api_eliminar_carrito(request: Request):
    print("✅ RUTA /api/carrito/eliminar LLAMADA")
    from controlador.CarritoController import CarritoController
    return await CarritoController.eliminar_del_carrito(request)

@app.post("/api/carrito/actualizar-cantidad")
async def api_actualizar_cantidad(request: Request):
    print("✅ RUTA /api/carrito/actualizar-cantidad LLAMADA")
    from controlador.CarritoController import CarritoController
    return await CarritoController.actualizar_cantidad_carrito(request)

@app.post("/api/carrito/vaciar")
async def api_vaciar_carrito(request: Request):
    print("✅ RUTA /api/carrito/vaciar LLAMADA")
    from controlador.CarritoController import CarritoController
    return await CarritoController.vaciar_carrito(request)

@app.get("/panel_mercado")
async def panel_mercado(request: Request):
    print("✅ RUTA /panel_mercado LLAMADA")
    from controlador.CarritoController import CarritoController
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="./vista_panel")
    
    try:
        data = await CarritoController.mostrar_panel_productos(request)
        if data["success"]:
            return templates.TemplateResponse("panel_producto.html", {
                "request": request,
                "usuario": data["usuario"],
                "carrito_items": data["carrito_items"],
                "productos_nutricion": data["productos_nutricion"],
                "productos_implementos": data["productos_implementos"],  # ✅ NUEVO
                "total_carrito": data["total_carrito"],
                "items_count": data["items_count"]
            })
    except Exception as e:
        print(f"Error en panel_mercado: {e}")
        return templates.TemplateResponse("panel_producto.html", {
            "request": request,
            "error": "Error al cargar el panel"
        })

# ✅ ENDPOINTS PARA CARGAR DATOS ESPECÍFICOS - AGREGAR ESTOS
@app.get("/api/productos/nutricion")
async def api_productos_nutricion(request: Request):
    from modelo.ServicioNutricionModel import ServicioNutricionModel
    
    usuario = AuthController.verificar_sesion_usuario(request)
    if not usuario:
        return JSONResponse({"success": False, "message": "No autorizado"}, status_code=401)
    
    productos, error = ServicioNutricionModel.obtener_todos_servicios()
    return JSONResponse({
        "success": True if not error else False,
        "productos": productos or [],
        "error": error
    })

@app.get("/api/productos/implementos")
async def api_productos_implementos(request: Request):
    from modelo.ServicioImplementosModel import ServicioImplementosModel
    
    usuario = AuthController.verificar_sesion_usuario(request)
    if not usuario:
        return JSONResponse({"success": False, "message": "No autorizado"}, status_code=401)
    
    productos, error = ServicioImplementosModel.obtener_todos_servicios()
    return JSONResponse({
        "success": True if not error else False,
        "productos": productos or [],
        "error": error
    })

@app.get("/api/carrito/mio")
async def api_carrito_mio(request: Request):
    from modelo.CarritoModel import CarritoModel
    
    usuario = AuthController.verificar_sesion_usuario(request)
    if not usuario:
        return JSONResponse({"success": False, "message": "No autorizado"}, status_code=401)
    
    carrito_items, error = CarritoModel.obtener_carrito_usuario(usuario['id'])
    
    # Calcular totales
    total_carrito = 0
    items_count = 0
    if carrito_items:
        for item in carrito_items:
            precio = float(item.get('precio', 0)) or 0
            cantidad = int(item.get('cantidad', 1)) or 1
            total_carrito += precio * cantidad
            items_count += cantidad
    
    return JSONResponse({
        "success": True if not error else False,
        "carrito": carrito_items or [],
        "total_carrito": total_carrito,
        "items_count": items_count,
        "error": error
    })

# ─────────────────────────────────────────────────────────────
# PANELES DE FISIOTERAPEUTA - CITA
# ─────────────────────────────────────────────────────────────

# =============================================
# RUTAS DE AUTENTICACIÓN (MANTENER EXISTENTES)
# =============================================

@app.post("/login-fisio")
async def login_fisioterapeuta(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)  
):
    """
    Endpoint para login de fisioterapeutas - CORREGIDO
    """
    try:
        # Usar el AuthFisioController CORRECTO (el que me mostraste)
        resultado = AuthFisioController.login_fisioterapeuta(email, password)
        
        if resultado['success']:
            # Credenciales válidas - crear sesión COMPLETA
            terapeuta = resultado['terapeuta']
            
            request.session['fisioterapeuta'] = {
                'codigo_trabajador': terapeuta['Codigo_trabajador'],
                'nombre_completo': terapeuta['nombre_completo'],  # ← ¡ESTO ES CLAVE!
                'email': terapeuta['fisio_correo'],
                'especializacion': terapeuta.get('especializacion', ''),
                'telefono': terapeuta.get('telefono', ''),
                'logged_in': True
            }
            
            print(f"✅ Login exitoso: {terapeuta['nombre_completo']}")
            print(f"📋 Sesión guardada: {request.session['fisioterapeuta']}")
            
            return RedirectResponse(url="/panel_citas_fisio", status_code=303)
        else:
            # Credenciales inválidas
            return templates_fisio.TemplateResponse("panel_login_fisio.html", {
                "request": request,
                "error": resultado['error']
            })
            
    except Exception as e:
        print(f"❌ Error en endpoint login-fisio: {e}")
        import traceback
        traceback.print_exc()
        return templates_fisio.TemplateResponse("panel_login_fisio.html", {
            "request": request,
            "error": 'Error interno del servidor'
        })

@app.get("/login-fisio-page")
async def login_fisio_page(request: Request):
    """
    Endpoint para mostrar la página de login de fisioterapeutas
    """
    error = request.session.pop('error', None)
    
    return templates_fisio.TemplateResponse("panel_login_fisio.html", {
        "request": request,
        "error": error
    })

def verificar_sesion_fisio(request: Request) -> dict:
    """
    Verifica la sesión del fisioterapeuta
    Retorna los datos del fisioterapeuta o None si no hay sesión
    """
    print("=" * 50)
    print("🔍 [verificar_sesion_fisio] Verificando sesión...")
    print(f"📋 Keys en sesión: {list(request.session.keys())}")
    
    fisioterapeuta = request.session.get('fisioterapeuta')
    
    if not fisioterapeuta:
        print("❌ No existe 'fisioterapeuta' en la sesión")
        request.session['error'] = 'Por favor, inicie sesión primero'
        return None
    
    if not fisioterapeuta.get('logged_in'):
        print(f"❌ logged_in es: {fisioterapeuta.get('logged_in')}")
        request.session['error'] = 'Sesión expirada'
        return None
    
    print(f"✅ Sesión válida para: {fisioterapeuta.get('nombre_completo')}")
    print("=" * 50)
    return fisioterapeuta


@app.get("/logout-fisio")
async def logout_fisioterapeuta(request: Request):
    """
    Endpoint para cerrar sesión de fisioterapeutas
    Limpia la sesión y redirige a la página de inicio
    """
    try:
        fisioterapeuta = request.session.get('fisioterapeuta')
        email = fisioterapeuta.get('email', 'Desconocido') if fisioterapeuta else 'Desconocido'
        
        request.session.clear()
        
        if 'fisioterapeuta' in request.session:
            del request.session['fisioterapeuta']
        
        request.session['success'] = 'Sesión cerrada correctamente'
        
        print(f"✅ Logout exitoso: {email} - {datetime.now()}")
        
        return RedirectResponse(url="/inicio", status_code=status.HTTP_302_FOUND)
        
    except Exception as e:
        request.session.clear()
        print(f"⚠️ Error durante logout: {e}")
        
        return RedirectResponse(url="/inicio", status_code=status.HTTP_302_FOUND)

# =============================================
# PANELES PROTEGIDOS (MANTENER EXISTENTES)
# =============================================

@app.get("/panel_citas_fisio")
async def panel_citas_fisio(request: Request):
    print("=" * 50)
    print("🔍 VERIFICANDO SESIÓN EN /panel_citas_fisio")
    print(f"📋 Todas las keys en sesión: {list(request.session.keys())}")
    print(f"👤 Datos de fisioterapeuta: {request.session.get('fisioterapeuta')}")
    print("=" * 50)
    
    fisioterapeuta = verificar_sesion_fisio(request)
    if not fisioterapeuta:
        return RedirectResponse(url="/login-fisio-page", status_code=status.HTTP_302_FOUND)
    
    return templates_fisio.TemplateResponse("panel_cita_fisio.html", {
        "request": request,
        "fisioterapeuta": fisioterapeuta
    })

@app.get("/panel_pacientes_fisio")
async def panel_pacientes_fisio(request: Request):
    fisioterapeuta = verificar_sesion_fisio(request)
    if not fisioterapeuta:
        return RedirectResponse(url="/login-fisio-page", status_code=status.HTTP_302_FOUND)
    
    return templates_fisio.TemplateResponse("panel_pacientes_fisio.html", {
        "request": request,
        "fisioterapeuta": fisioterapeuta
    })

@app.get("/panel_progreso_fisio")
async def panel_progreso_fisio(request: Request):
    fisioterapeuta = verificar_sesion_fisio(request)
    if not fisioterapeuta:
        return RedirectResponse(url="/login-fisio-page", status_code=status.HTTP_302_FOUND)
    
    return templates_fisio.TemplateResponse("panel_progreso_fisio.html", {
        "request": request,
        "fisioterapeuta": fisioterapeuta
    })



# Ruta existente - Mantener igual
app.add_api_route("/api/citas/panel_terapeuta", CitaFisioController.obtener_citas_terapeuta, methods=["GET"])

# Ruta existente - Usar la versión compatible
app.add_api_route("/api/citas/actualizar-estado", CitaFisioController.actualizar_estado_cita, methods=["POST"])

# Ruta existente - Mantener igual
@app.get("/citas", response_class=HTMLResponse)
async def mostrar_panel_citas(request: Request):
    return await CitaFisioController.mostrar_panel_citas(request)

# Ruta existente - Usar la versión compatible
@app.post("/api/citas/crear")
async def crear_cita(
    request: Request,
    servicio: str = Form(...),
    terapeuta_designado: str = Form(...),
    nombre_paciente: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    id_acudiente: str = Form(None),
    nombre_acudiente: str = Form(None),
    fecha_cita: str = Form(...),
    hora_cita: str = Form(...),
    notas_adicionales: str = Form(None),
    tipo_pago: str = Form(...)
):
    return await CitaFisioController.crear_cita( 
        request, servicio, terapeuta_designado, nombre_paciente,
        telefono, correo, id_acudiente, nombre_acudiente,
        fecha_cita, hora_cita, notas_adicionales, tipo_pago
    )

# Ruta existente - Usar la versión compatible
@app.post("/api/citas/agendar-completo")
async def agendar_cita_completa(
    request: Request,
    servicio: str = Form(...),
    terapeuta_designado: str = Form(...),
    nombre_paciente: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    fecha_cita: str = Form(...),
    hora_cita: str = Form(...),
    notas_adicionales: str = Form(None),
    tipo_pago: str = Form(...),
    acudiente_nombre: str = Form(None),
    acudiente_id: str = Form(None),
    acudiente_telefono: str = Form(None),
    acudiente_correo: str = Form(None),
    acudiente_direccion: str = Form(None),
    emails_adicionales: str = Form(None)
):
    return await CitaFisioController.agendar_cita(
        request, servicio, terapeuta_designado, nombre_paciente,
        telefono, correo, fecha_cita, hora_cita, notas_adicionales, 
        tipo_pago, acudiente_nombre, acudiente_id, acudiente_telefono,
        acudiente_correo, acudiente_direccion, emails_adicionales
    )

# =============================================
# RUTAS API ADICIONALES (NUEVAS O EXISTENTES)
# =============================================

# Ruta existente - Mantener igual
@app.get("/api/metricas")
async def obtener_metricas_api(request: Request):
    return await CitaFisioController.obtener_metricas_api(request)

# Ruta existente - Mantener igual (usa la versión compatible)
@app.post("/api/citas/confirmar-todas")
async def confirmar_todas_pendientes(request: Request):
    return await CitaFisioController.confirmar_todas_pendientes(request)

# Ruta existente - Mantener igual (usa la versión compatible)
@app.post("/api/citas/filtrar")
async def filtrar_citas(
    request: Request,
    estado: str = Form(None),
    paciente: str = Form(None),
    fecha: str = Form(None)
):
    return await CitaFisioController.filtrar_citas(request, estado, paciente, fecha)

# Ruta existente - Mantener igual
@app.get("/api/calendario")
async def obtener_calendario_semanal(request: Request):
    return await CitaFisioController.obtener_calendario_semanal(request)

# =============================================
# RUTAS NUEVAS OPCIONALES (AGREGAR SI LAS NECESITAS)
# =============================================

@app.get("/api/citas/estadisticas")
async def obtener_estadisticas_citas(request: Request):
    """Alias para /api/metricas"""
    return await CitaFisioController.obtener_metricas_api(request)

@app.get("/api/citas/detalles/{cita_id}")
async def obtener_detalles_cita(request: Request, cita_id: str):
    """Obtener detalles específicos de una cita"""
    return await CitaFisioController.obtener_detalles_cita(request, cita_id)

@app.post("/api/citas/actualizar-cita")
async def actualizar_cita_completa(
    request: Request,
    cita_id: str = Form(...),
    servicio: str = Form(None),
    fecha_cita: str = Form(None),
    hora_cita: str = Form(None),
    notas_adicionales: str = Form(None)
):
    """Actualizar información completa de una cita"""
    # Este método necesitaría ser implementado en el controlador
    pass

# ─────────────────────────────────────────────────────────────
# PANELES DE FISIOTERAPEUTA - PACIENTE
# ─────────────────────────────────────────────────────────────

app.add_api_route("/api/pacientes", PacienteFisioController.obtener_pacientes, methods=["GET"])
app.add_api_route("/api/pacientes/estadisticas", PacienteFisioController.obtener_estadisticas_pacientes, methods=["GET"])
app.add_api_route("/api/ejercicios", PacienteFisioController.obtener_ejercicios, methods=["GET"])
app.add_api_route("/api/pacientes/{codigo_cita}/ejercicios", PacienteFisioController.obtener_ejercicios_paciente, methods=["GET"])
app.add_api_route("/api/pacientes/asignar-ejercicios", PacienteFisioController.asignar_ejercicios, methods=["POST"])
app.add_api_route("/api/pacientes/{codigo_cita}", PacienteFisioController.eliminar_paciente, methods=["DELETE"])


# ─────────────────────────────────────────────────────────────
# PANELES DE FISIOTERAPEUTA - PROGRESO
# ─────────────────────────────────────────────────────────────

app.add_api_route("/api/progreso/pacientes-filtros", ReporteFisioController.obtener_pacientes_para_filtros, methods=["GET"])
app.add_api_route("/api/progreso/estadisticas", ReporteFisioController.obtener_estadisticas_progreso, methods=["GET"])
app.add_api_route("/api/reportes", ReporteFisioController.guardar_reporte, methods=["POST"])
app.add_api_route("/api/reportes", ReporteFisioController.obtener_reportes, methods=["GET"])
app.add_api_route("/api/reportes/{codigo_cita}/descargar", ReporteFisioController.descargar_reporte, methods=["GET"])

