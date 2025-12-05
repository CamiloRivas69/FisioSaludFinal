# controlador/CitaFisioController.py
from fastapi import Request, Form, HTTPException
from fastapi.responses import JSONResponse
from modelo.CitaFisioModel import CitaFisioModel
from typing import Optional, Dict, Any, List
import traceback
import json

class CitaFisioController:
    
    @staticmethod
    async def obtener_citas(request: Request):
        """
        API endpoint para obtener todas las citas del terapeuta logueado
        """
        try:
            # OBTENER EL FISIOTERAPEUTA DE LA SESIÓN
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
            
            # Obtener citas del terapeuta
            citas = CitaFisioModel.obtener_citas_por_terapeuta(terapeuta_actual)
            print(f"📋 Citas obtenidas para {terapeuta_actual}: {len(citas)}")
            
            # Para cada cita, obtener info de acudiente si existe
            citas_completas = []
            for cita in citas:
                cita_completa = dict(cita)
                acudiente = CitaFisioModel.obtener_acudiente_por_cita(cita['cita_id'])
                if acudiente:
                    cita_completa['acudiente'] = acudiente
                else:
                    cita_completa['acudiente'] = None
                citas_completas.append(cita_completa)
            
            return JSONResponse(content={
                "success": True,
                "data": citas_completas,
                "total": len(citas_completas),
                "terapeuta": terapeuta_actual
            })
            
        except Exception as e:
            print(f"❌ Error en API de citas: {e}")
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
    async def cambiar_estado_cita(request: Request, cita_id: str):
        """
        API endpoint para cambiar el estado de una cita
        """
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
            
            # Obtener datos del body (JSON)
            try:
                body = await request.json()
                nuevo_estado = body.get('estado')
            except:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "Formato JSON inválido"
                    }
                )
            
            if not nuevo_estado:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "El campo 'estado' es requerido"
                    }
                )
            
            # Obtener nombre del terapeuta
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            print(f"🔄 Cambiando estado de cita {cita_id} a {nuevo_estado}")
            print(f"👨‍⚕️ Terapeuta solicitante: {terapeuta_actual}")
            
            # Llamar al modelo para cambiar estado
            resultado = CitaFisioModel.cambiar_estado_cita(cita_id, nuevo_estado, terapeuta_actual)
            
            if resultado.get('success'):
                print(f"✅ Estado cambiado exitosamente: {resultado}")
                return JSONResponse(
                    content={
                        "success": True,
                        "message": resultado.get('message', 'Estado actualizado'),
                        "accion": resultado.get('accion'),
                        "data": {
                            "cita_id": cita_id,
                            "nuevo_estado": nuevo_estado
                        }
                    }
                )
            else:
                print(f"❌ Error al cambiar estado: {resultado.get('error')}")
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": resultado.get('error', 'Error desconocido')
                    }
                )
            
        except Exception as e:
            print(f"❌ Error en API de cambio de estado: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )
    
    @staticmethod
    async def obtener_estadisticas(request: Request):
        """
        API endpoint para obtener estadísticas de citas
        """
        try:
            # OBTENER EL FISIOTERAPEUTA DE LA SESIÓN
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
            
            # Obtener estadísticas
            estadisticas = CitaFisioModel.obtener_estadisticas_citas(terapeuta_actual)
            
            return JSONResponse(content={
                "success": True,
                "data": estadisticas,
                "terapeuta": terapeuta_actual
            })
            
        except Exception as e:
            print(f"❌ Error en API de estadísticas: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener estadísticas: {str(e)}"
                }
            )
    
    @staticmethod
    async def filtrar_citas(request: Request):
        """
        API endpoint para filtrar citas según criterios
        """
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
            
            # Obtener parámetros de filtro
            try:
                body = await request.json()
            except:
                body = {}
            
            # Extraer filtros
            filtros = {
                'fecha': body.get('fecha'),
                'paciente': body.get('paciente'),
                'servicio': body.get('servicio'),
                'estado': body.get('estado')
            }
            
            print(f"🔍 Aplicando filtros: {filtros}")
            
            # Obtener nombre del terapeuta
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            # Filtrar citas
            citas_filtradas = CitaFisioModel.filtrar_citas(terapeuta_actual, filtros)
            
            # Añadir info de acudiente si existe
            citas_completas = []
            for cita in citas_filtradas:
                cita_completa = dict(cita)
                acudiente = CitaFisioModel.obtener_acudiente_por_cita(cita['cita_id'])
                if acudiente:
                    cita_completa['acudiente'] = acudiente
                else:
                    cita_completa['acudiente'] = None
                citas_completas.append(cita_completa)
            
            return JSONResponse(content={
                "success": True,
                "data": citas_completas,
                "total": len(citas_completas),
                "filtros_aplicados": {k: v for k, v in filtros.items() if v is not None and v != ''}
            })
            
        except Exception as e:
            print(f"❌ Error en API de filtrado: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al filtrar citas: {str(e)}",
                    "data": []
                }
            )
    
    @staticmethod
    async def obtener_cita_detalle(request: Request, cita_id: str):
        """
        API endpoint para obtener detalle de una cita específica
        """
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
            
            # Obtener nombre del terapeuta
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            # Obtener todas las citas del terapeuta
            todas_citas = CitaFisioModel.obtener_citas_por_terapeuta(terapeuta_actual)
            
            # Buscar la cita específica
            cita_encontrada = None
            for cita in todas_citas:
                if cita['cita_id'] == cita_id:
                    cita_encontrada = cita
                    break
            
            if not cita_encontrada:
                return JSONResponse(
                    status_code=404,
                    content={
                        "success": False,
                        "error": "Cita no encontrada o no tienes permiso para verla"
                    }
                )
            
            # Obtener info de acudiente si existe
            acudiente = CitaFisioModel.obtener_acudiente_por_cita(cita_id)
            
            cita_detalle = dict(cita_encontrada)
            if acudiente:
                cita_detalle['acudiente'] = acudiente
            else:
                cita_detalle['acudiente'] = None
            
            return JSONResponse(content={
                "success": True,
                "data": cita_detalle
            })
            
        except Exception as e:
            print(f"❌ Error en API de detalle de cita: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener detalle: {str(e)}"
                }
            )
    

