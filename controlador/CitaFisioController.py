from fastapi import Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from modelo.CitaFisioModel import CitaFisioModel
from typing import Optional, List
import traceback
import json
from datetime import datetime, date

class CitaFisioController:
    
    @staticmethod
    async def obtener_citas_terapeuta(request: Request):
        """API endpoint para obtener las citas del terapeuta logueado"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            print(f"🔍 Buscando citas para el terapeuta: {terapeuta_actual}")
            
            citas = CitaFisioModel.obtener_citas_por_terapeuta(terapeuta_actual)
            print(f"📊 Citas obtenidas para {terapeuta_actual}: {len(citas)}")
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": citas,
                    "total": len(citas),
                    "terapeuta": terapeuta_actual
                }
            )
            
        except Exception as e:
            print(f"❌ Error en API de citas terapeuta: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener citas: {str(e)}",
                    "data": []
                }
            )

    @staticmethod
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
        """API endpoint para crear una nueva cita - VERSIÓN COMPATIBLE"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            print(f"📥 Creando nueva cita para terapeuta: {terapeuta_designado}")
            
            # Validar datos obligatorios
            if not servicio or not nombre_paciente or not fecha_cita or not hora_cita:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "Faltan campos obligatorios"
                    }
                )
            
            # Validar que la fecha sea válida
            try:
                fecha_obj = datetime.strptime(fecha_cita, "%Y-%m-%d").date()
                if fecha_obj < date.today():
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "error": "No se pueden crear citas en fechas pasadas"
                        }
                    )
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "Formato de fecha inválido. Use YYYY-MM-DD"
                    }
                )
            
            # Crear cita en la base de datos (versión simple, sin acudiente)
            resultado = CitaFisioModel.crear_cita(
                servicio=servicio,
                terapeuta_designado=terapeuta_designado,
                nombre_paciente=nombre_paciente,
                telefono=telefono,
                correo=correo,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita,
                notas_adicionales=notas_adicionales,
                tipo_pago=tipo_pago,
                estado='pending'
            )
            
            if resultado['success']:
                return JSONResponse(
                    content={
                        "success": True,
                        "message": resultado['message'],
                        "cita_id": resultado.get('cita_id')
                    }
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": resultado.get('error', 'Error al crear la cita')
                    }
                )
            
        except Exception as e:
            print(f"❌ Error al crear cita: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
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
        notas_adicionales: str = Form(None),
        tipo_pago: str = Form(...),
        acudiente_nombre: str = Form(None),
        acudiente_id: str = Form(None),
        acudiente_telefono: str = Form(None),
        acudiente_correo: str = Form(None),
        acudiente_direccion: str = Form(None),
        emails_adicionales: str = Form(None)
    ):
        """API endpoint para crear cita completa con acudiente"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            print(f"📥 Creando cita COMPLETA para terapeuta: {terapeuta_designado}")
            print(f"👥 Acudiente: {acudiente_nombre}")
            
            # Crear cita básica primero
            resultado_cita = CitaFisioModel.crear_cita(
                servicio=servicio,
                terapeuta_designado=terapeuta_designado,
                nombre_paciente=nombre_paciente,
                telefono=telefono,
                correo=correo,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita,
                notas_adicionales=notas_adicionales,
                tipo_pago=tipo_pago,
                estado='pending'
            )
            
            if not resultado_cita['success']:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": resultado_cita.get('error', 'Error al crear la cita')
                    }
                )
            
            # Si hay acudiente, crear registro en tabla acudiente y actualizar paciente
            if acudiente_nombre:
                cita_id = resultado_cita.get('cita_id')
                resultado_acudiente = CitaFisioModel.crear_acudiente_y_actualizar_paciente(
                    cita_id=cita_id,
                    acudiente_nombre=acudiente_nombre,
                    acudiente_id=acudiente_id,
                    acudiente_telefono=acudiente_telefono,
                    acudiente_correo=acudiente_correo,
                    acudiente_direccion=acudiente_direccion
                )
                
                if not resultado_acudiente['success']:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "error": resultado_acudiente.get('error', 'Error al crear acudiente')
                        }
                    )
            
            return JSONResponse(
                content={
                    "success": True,
                    "message": "Cita creada exitosamente" + (" con acudiente" if acudiente_nombre else ""),
                    "cita_id": resultado_cita.get('cita_id')
                }
            )
            
        except Exception as e:
            print(f"❌ Error al agendar cita completa: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def actualizar_estado_cita(request: Request, nombre_paciente: str = Form(...), nuevo_estado: str = Form(...)):
        """API endpoint para actualizar el estado de una cita - VERSIÓN COMPATIBLE"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            print(f"🔄 Actualizando estado de cita para paciente: {nombre_paciente} -> {nuevo_estado}")
            
            # Obtener terapeuta actual
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            # Buscar cita por nombre de paciente y terapeuta
            resultado = CitaFisioModel.actualizar_estado_cita_por_paciente(
                nombre_paciente=nombre_paciente,
                terapeuta=terapeuta_actual,
                nuevo_estado=nuevo_estado
            )
            
            if resultado['success']:
                return JSONResponse(
                    content={
                        "success": True,
                        "message": resultado['message']
                    }
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": resultado.get('error', 'Error al actualizar estado')
                    }
                )
            
        except Exception as e:
            print(f"❌ Error al actualizar estado de cita: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def filtrar_citas(
        request: Request,
        estado: str = Form(None),
        paciente: str = Form(None),
        fecha: str = Form(None)
    ):
        """API endpoint para filtrar citas - VERSIÓN COMPATIBLE"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            print(f"🔍 Filtrando citas para {terapeuta_actual}")
            
            # Filtrar citas según criterios
            citas_filtradas = CitaFisioModel.filtrar_citas_terapeuta(
                terapeuta=terapeuta_actual,
                estado=estado,
                paciente=paciente,
                fecha=fecha,
                servicio=None  # Mantener compatibilidad
            )
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": citas_filtradas,
                    "total": len(citas_filtradas),
                    "filtros_aplicados": {
                        "estado": estado,
                        "paciente": paciente,
                        "fecha": fecha
                    }
                }
            )
            
        except Exception as e:
            print(f"❌ Error al filtrar citas: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def obtener_metricas_api(request: Request):
        """API endpoint para obtener métricas"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            print(f"📊 Obteniendo métricas para {terapeuta_actual}")
            
            estadisticas = CitaFisioModel.obtener_estadisticas_citas(terapeuta_actual)
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": estadisticas,
                    "terapeuta": terapeuta_actual
                }
            )
            
        except Exception as e:
            print(f"❌ Error al obtener métricas: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener métricas: {str(e)}"
                }
            )

    @staticmethod
    async def confirmar_todas_pendientes(request: Request):
        """API endpoint para confirmar todas las citas pendientes"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            print(f"✅ Confirmando todas las citas pendientes para {terapeuta_actual}")
            
            resultado = CitaFisioModel.confirmar_todas_citas_pendientes(terapeuta_actual)
            
            if resultado['success']:
                return JSONResponse(
                    content={
                        "success": True,
                        "message": resultado['message'],
                        "actualizadas": resultado.get('actualizadas', 0)
                    }
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": resultado.get('error', 'Error al confirmar citas')
                    }
                )
            
        except Exception as e:
            print(f"❌ Error al confirmar todas las citas: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def obtener_calendario_semanal(request: Request):
        """API endpoint para obtener citas de la semana actual"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "error": "No autorizado - Inicie sesión primero"
                    }
                )
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            print(f"📅 Obteniendo calendario semanal para {terapeuta_actual}")
            
            # Obtener citas de la semana (fecha actual y 6 días siguientes)
            hoy = date.today().isoformat()
            from datetime import timedelta
            fin_semana = (date.today() + timedelta(days=6)).isoformat()
            
            citas_semana = CitaFisioModel.filtrar_citas_terapeuta(
                terapeuta=terapeuta_actual,
                fecha=None
            )
            
            # Filtrar solo citas de la semana
            citas_semana_filtradas = []
            for cita in citas_semana:
                fecha_cita = cita.get('fecha_cita', '')
                if fecha_cita and hoy <= fecha_cita <= fin_semana:
                    citas_semana_filtradas.append(cita)
            
            # Agrupar citas por día
            calendario = {}
            for cita in citas_semana_filtradas:
                fecha = cita.get('fecha_cita')
                if fecha not in calendario:
                    calendario[fecha] = []
                calendario[fecha].append(cita)
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": {
                        "calendario": calendario,
                        "rango_semana": {
                            "inicio": hoy,
                            "fin": fin_semana
                        },
                        "total_citas_semana": len(citas_semana_filtradas)
                    }
                }
            )
            
        except Exception as e:
            print(f"❌ Error al obtener calendario semanal: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def mostrar_panel_citas(request: Request):
        """Mostrar panel de citas - VERSIÓN COMPATIBLE"""
        try:
            # VERIFICAR SESIÓN
            fisioterapeuta = request.session.get('fisioterapeuta')
            
            if not fisioterapeuta or not fisioterapeuta.get('logged_in'):
                return RedirectResponse(url="/login-fisio-page", status_code=303)
            
            # Redirigir al panel principal
            return RedirectResponse(url="/panel_citas_fisio", status_code=303)
            
        except Exception as e:
            print(f"❌ Error al mostrar panel de citas: {e}")
            traceback.print_exc()
            return HTMLResponse(content="<h1>Error interno del servidor</h1>", status_code=500)