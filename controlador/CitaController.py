from fastapi import Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from modelo.CitaModel import CitaModel
from typing import Optional
import json
from datetime import datetime

class CitaController:
    
    @staticmethod
    async def mostrar_formulario_cita(request: Request, servicio_codigo: Optional[str] = None):
        """Muestra el formulario para agendar citas de terapia"""
        try:
            servicios = CitaModel.obtener_servicios_terapia()
            
            # Si viene un código de servicio, buscar ese servicio específico
            servicio_seleccionado = None
            if servicio_codigo:
                servicio_seleccionado = next(
                    (s for s in servicios if s['codigo'] == servicio_codigo), 
                    None
                )
            
            from fastapi.templating import Jinja2Templates
            templates = Jinja2Templates(directory="./vista")
            
            return templates.TemplateResponse(
                "cita.html",  # Asegúrate que este es el nombre correcto del template
                {
                    "request": request,
                    "servicios": servicios,
                    "servicio_seleccionado": servicio_seleccionado
                }
            )
        except Exception as e:
            print(f"Error al mostrar formulario de cita: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    @staticmethod
    async def obtener_servicios_api(request: Request):
        """API endpoint para obtener servicios de terapia"""
        try:
            servicios = CitaModel.obtener_servicios_terapia()
            
            return JSONResponse(content={"servicios": servicios})
            
        except Exception as e:
            print(f"Error en API de servicios: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Error al obtener servicios"}
            )

    @staticmethod
    async def agendar_cita(
        request: Request,
        servicio: str = Form(...),
        terapeuta_designado: str = Form(...),
        nombre_paciente: str = Form(...),
        telefono: str = Form(...),
        correo: str = Form(...),
        fecha_cita: str = Form(...),
        hora_cita: str = Form(...),
        notas_adicionales: Optional[str] = Form(None),
        tipo_pago: str = Form(...),
        acudiente_nombre: Optional[str] = Form(None),
        acudiente_id: Optional[str] = Form(None),
        acudiente_telefono: Optional[str] = Form(None),
        acudiente_correo: Optional[str] = Form(None),
        acudiente_direccion: Optional[str] = Form(None),
        emails_adicionales: Optional[str] = Form(None)
    ):
        """Procesa el agendamiento de una nueva cita"""
        try:
            print(f"Iniciando agendamiento para: {nombre_paciente}")
            
            # Validaciones básicas
            if not all([servicio, terapeuta_designado, nombre_paciente, telefono, correo, fecha_cita, hora_cita, tipo_pago]):
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "error": "Todos los campos obligatorios deben ser completados"}
                )

            # Validar fecha
            try:
                fecha_obj = datetime.strptime(fecha_cita, '%Y-%m-%d')
                if fecha_obj.date() < datetime.now().date():
                    return JSONResponse(
                        status_code=400,
                        content={"success": False, "error": "No se pueden agendar citas en fechas pasadas"}
                    )
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "error": "Formato de fecha inválido"}
                )

            # 1. VERIFICAR DISPONIBILIDAD
            disponible = CitaModel.verificar_disponibilidad_cita(
                fecha_cita, hora_cita, terapeuta_designado
            )
            
            if not disponible:
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "error": "El horario seleccionado no está disponible para este terapeuta"}
                )
            
            # 2. CREAR LA CITA
            datos_cita = {
                'servicio': servicio,
                'terapeuta_designado': terapeuta_designado,
                'nombre_paciente': nombre_paciente,
                'telefono': telefono,
                'correo': correo,
                'fecha_cita': fecha_cita,
                'hora_cita': hora_cita,
                'notas_adicionales': notas_adicionales or '',
                'tipo_pago': tipo_pago
            }
            
            codigo_cita = CitaModel.crear_cita(datos_cita)
            
            if not codigo_cita:
                return JSONResponse(
                    status_code=500,
                    content={"success": False, "error": "Error al crear la cita en el sistema"}
                )
            
            # 3. CREAR ACUDIENTE SI EXISTE
            acudiente_creado = False
            if acudiente_nombre and acudiente_id:
                datos_acudiente = {
                    'nombre_completo': acudiente_nombre,
                    'identificacion': acudiente_id,
                    'telefono': acudiente_telefono or '',
                    'correo': acudiente_correo or '',
                    'direccion': acudiente_direccion or ''
                }
                
                acudiente_creado = CitaModel.crear_acudiente(codigo_cita, datos_acudiente)
                if not acudiente_creado:
                    print(f"Advertencia: No se pudo crear el acudiente para la cita {codigo_cita}")
            
            # 4. PROCESAR EMAILS ADICIONALES
            emails_list = []
            if emails_adicionales:
                try:
                    emails_data = json.loads(emails_adicionales)
                    if isinstance(emails_data, list):
                        emails_list = [email for email in emails_data if email.strip()]
                except json.JSONDecodeError:
                    # Si no es JSON válido, tratar como string simple
                    if emails_adicionales.strip():
                        emails_list = [emails_adicionales.strip()]
            
            # 5. RESPUESTA EXITOSA
            response_data = {
                "success": True,
                "message": "Cita agendada exitosamente",
                "codigo_cita": codigo_cita,  # Código alfanumérico (FS-0001)
                "cita": {
                    "servicio": servicio,
                    "terapeuta_designado": terapeuta_designado,
                    "fecha_cita": fecha_cita,
                    "hora_cita": hora_cita,
                    "nombre_paciente": nombre_paciente
                },
                "acudiente_creado": acudiente_creado,
                "emails_adicionales": emails_list
            }
            
            print(f"Cita agendada exitosamente: {codigo_cita}")
            return JSONResponse(content=response_data)
            
        except Exception as e:
            print(f"Error al agendar cita: {e}")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Error interno del servidor al procesar la cita"}
            )