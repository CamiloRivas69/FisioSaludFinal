from datetime import datetime
from fastapi import Request, Form, HTTPException, UploadFile
from fastapi.params import File
from fastapi.responses import JSONResponse, Response
from modelo.ReporteFisioModel import ReporteFisioModel
from typing import Optional
import traceback
import base64


class ReporteFisioController:
    
    @staticmethod
    async def obtener_pacientes_para_filtros(request: Request):
        """API endpoint para obtener pacientes del terapeuta para filtros"""
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
            print(f"🔍 Buscando pacientes para filtros del terapeuta: {terapeuta_actual}")
            
            pacientes = ReporteFisioModel.obtener_pacientes_por_terapeuta(terapeuta_actual)
            
            return JSONResponse(content={
                "success": True,
                "data": pacientes,
                "total": len(pacientes)
            })
            
        except Exception as e:
            print(f"Error en API de pacientes para filtros: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener pacientes: {str(e)}",
                    "data": []
                }
            )

    @staticmethod
    async def guardar_reporte(
        request: Request,
        ID: str = Form(...),
        reporte: UploadFile = File(...)  # Cambiar a "reporte" (singular)
    ):
        """API endpoint para guardar reporte PDF en la base de datos"""
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
            
            print(f"📥 Guardando reporte para paciente ID: {ID}")
            print(f"📄 Nombre del archivo: {reporte.filename}")
            print(f"📊 Tipo MIME: {reporte.content_type}")
            
            # Leer el contenido del archivo
            pdf_content = await reporte.read()
            print(f"📦 Tamaño del PDF leído: {len(pdf_content)} bytes")
            
            # Obtener el nombre del terapeuta de la sesión
            terapeuta_actual = fisioterapeuta.get('nombre_completo')
            
            # Por ahora usamos un nombre genérico, podrías obtenerlo de otra tabla
            nombre_paciente = f"Paciente {ID}"
            
            # Guardar el reporte en la base de datos
            guardado = ReporteFisioModel.guardar_reporte_paciente(ID, pdf_content, nombre_paciente)
            
            if guardado:
                print("✅ Reporte guardado exitosamente en la BD")
                return JSONResponse(
                    content={
                        "success": True,
                        "message": "Reporte guardado exitosamente",
                        "data": {
                            "codigo_cita": ID,
                            "tamaño_pdf": len(pdf_content),
                            "fecha_guardado": datetime.now().isoformat()
                        }
                    }
                )
            else:
                print("❌ Error al guardar reporte en el modelo")
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "error": "Error al guardar el reporte en la base de datos"
                    }
                )
            
        except Exception as e:
            print(f"❌ Error al guardar reporte: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error interno del servidor: {str(e)}"
                }
            )

    @staticmethod
    async def obtener_reportes(request: Request):
        """API endpoint para obtener todos los reportes del terapeuta"""
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
            print(f"🔍 Buscando reportes del terapeuta: {terapeuta_actual}")
            
            reportes = ReporteFisioModel.obtener_reportes_por_terapeuta(terapeuta_actual)
            
            return JSONResponse(content={
                "success": True,
                "data": reportes,
                "total": len(reportes)
            })
            
        except Exception as e:
            print(f"Error en API de reportes: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener reportes: {str(e)}",
                    "data": []
                }
            )

    @staticmethod
    async def descargar_reporte(request: Request, codigo_cita: str):
        """API endpoint para descargar un reporte específico"""
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
            
            reporte = ReporteFisioModel.descargar_reporte(codigo_cita)
            
            if not reporte:
                return JSONResponse(
                    status_code=404,
                    content={
                        "success": False,
                        "error": "Reporte no encontrado"
                    }
                )
            
            # Devolver el PDF como respuesta
            return Response(
                content=reporte['pdf_data'],
                media_type='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename="reporte_{codigo_cita}.pdf"',
                    'Content-Type': 'application/pdf'
                }
            )
            
        except Exception as e:
            print(f"Error al descargar reporte: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Error interno del servidor"
                }
            )

    @staticmethod
    async def obtener_estadisticas_progreso(request: Request):
        """API endpoint para obtener estadísticas del dashboard"""
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
            
            estadisticas = ReporteFisioModel.obtener_estadisticas_progreso(terapeuta_actual)
            
            return JSONResponse(content={
                "success": True,
                "data": estadisticas
            })
            
        except Exception as e:
            print(f"Error en API de estadísticas: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Error al obtener estadísticas: {str(e)}"
                }
            )