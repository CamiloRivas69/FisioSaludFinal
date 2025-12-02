import pymysql
from typing import Dict, List, Optional
from datetime import datetime, date
import base64

class ReporteFisioModel:
    
    @staticmethod
    def get_db_connection():
        """Obtiene conexión a la base de datos"""
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="fisiosalud-2",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except pymysql.Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")
            return None

    @staticmethod
    def guardar_reporte_paciente(codigo_cita: str, pdf_blob: bytes, nombre_paciente: str) -> bool:
        """Guarda el reporte PDF en la tabla paciente"""
        connection = ReporteFisioModel.get_db_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE paciente 
                SET reporte = %s, 
                    fecha_creacion_reporte = %s,
                    nombre_completo = %s
                WHERE codigo_cita = %s
                """
                
                fecha_actual = date.today()
                
                cursor.execute(sql, (
                    pdf_blob,
                    fecha_actual,
                    nombre_paciente,
                    codigo_cita
                ))
                connection.commit()
                print(f"✅ Reporte guardado para paciente {codigo_cita} - {nombre_paciente}")
                return True
                
        except Exception as e:
            print(f"❌ Error al guardar reporte: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_pacientes_por_terapeuta(terapeuta: str) -> List[Dict]:
        """Obtiene pacientes del terapeuta para los filtros"""
        connection = ReporteFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    codigo_cita,
                    nombre_completo,
                    terapeuta_asignado
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND estado_cita = 'confirmed'
                ORDER BY nombre_completo
                """
                cursor.execute(sql, (terapeuta,))
                resultados = cursor.fetchall()
                
                # Convertir a formato serializable
                pacientes_serializables = []
                for paciente in resultados:
                    paciente_serializable = {}
                    for key, value in paciente.items():
                        if value is None:
                            paciente_serializable[key] = ''
                        elif isinstance(value, (date, datetime)):
                            paciente_serializable[key] = value.isoformat()
                        else:
                            paciente_serializable[key] = str(value)
                    pacientes_serializables.append(paciente_serializable)
                
                return pacientes_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener pacientes: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_reportes_por_terapeuta(terapeuta: str) -> List[Dict]:
        """Obtiene todos los reportes generados por el terapeuta"""
        connection = ReporteFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    codigo_cita,
                    nombre_completo,
                    fecha_creacion_reporte,
                    tipo_plan,
                    estado_cita,
                    reporte IS NOT NULL as tiene_reporte
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND fecha_creacion_reporte IS NOT NULL
                ORDER BY fecha_creacion_reporte DESC
                """
                cursor.execute(sql, (terapeuta,))
                resultados = cursor.fetchall()
                
                # Convertir a formato serializable
                reportes_serializables = []
                for reporte in resultados:
                    reporte_serializable = {}
                    for key, value in reporte.items():
                        if value is None:
                            reporte_serializable[key] = ''
                        elif isinstance(value, (date, datetime)):
                            reporte_serializable[key] = value.isoformat()
                        else:
                            reporte_serializable[key] = str(value)
                    reportes_serializables.append(reporte_serializable)
                
                return reportes_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener reportes: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def descargar_reporte(codigo_cita: str) -> Optional[Dict]:
        """Obtiene el reporte PDF para descargar"""
        connection = ReporteFisioModel.get_db_connection()
        if not connection:
            return None
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    reporte,
                    nombre_completo,
                    fecha_creacion_reporte
                FROM paciente 
                WHERE codigo_cita = %s 
                AND reporte IS NOT NULL
                """
                cursor.execute(sql, (codigo_cita,))
                resultado = cursor.fetchone()
                
                if resultado and resultado['reporte']:
                    return {
                        'pdf_data': resultado['reporte'],
                        'nombre_paciente': resultado['nombre_completo'],
                        'fecha_reporte': resultado['fecha_creacion_reporte'].isoformat() if resultado['fecha_creacion_reporte'] else ''
                    }
                return None
                
        except Exception as e:
            print(f"❌ Error al descargar reporte: {e}")
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_estadisticas_progreso(terapeuta: str) -> Dict:
        """Obtiene estadísticas para las tarjetas del dashboard"""
        connection = ReporteFisioModel.get_db_connection()
        if not connection:
            return {}
            
        try:
            with connection.cursor() as cursor:
                # Pacientes en seguimiento (con estado confirmed)
                sql_pacientes = """
                SELECT COUNT(*) as total 
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND estado_cita = 'confirmed'
                """
                cursor.execute(sql_pacientes, (terapeuta,))
                total_pacientes = cursor.fetchone()['total']
                
                # Evaluaciones este mes
                sql_evaluaciones_mes = """
                SELECT COUNT(*) as total 
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND fecha_creacion_reporte IS NOT NULL
                AND MONTH(fecha_creacion_reporte) = MONTH(CURDATE())
                AND YEAR(fecha_creacion_reporte) = YEAR(CURDATE())
                """
                cursor.execute(sql_evaluaciones_mes, (terapeuta,))
                evaluaciones_mes = cursor.fetchone()['total']
                
                # Pacientes con reportes
                sql_con_reportes = """
                SELECT COUNT(*) as total 
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND reporte IS NOT NULL
                """
                cursor.execute(sql_con_reportes, (terapeuta,))
                con_reportes = cursor.fetchone()['total']
                
                # Alertas (pacientes sin reportes recientes)
                sql_sin_reportes_recientes = """
                SELECT COUNT(*) as total 
                FROM paciente 
                WHERE terapeuta_asignado = %s 
                AND estado_cita = 'confirmed'
                AND (fecha_creacion_reporte IS NULL 
                     OR fecha_creacion_reporte < DATE_SUB(CURDATE(), INTERVAL 30 DAY))
                """
                cursor.execute(sql_sin_reportes_recientes, (terapeuta,))
                alertas = cursor.fetchone()['total']
                
                estadisticas = {
                    'pacientes_seguimiento': total_pacientes,
                    'evaluaciones_mes': evaluaciones_mes,
                    'pacientes_con_reportes': con_reportes,
                    'alertas_activas': alertas,
                    'progreso_promedio': round((con_reportes / total_pacientes * 100) if total_pacientes > 0 else 0, 1)
                }
                
                print(f"📊 Estadísticas obtenidas para {terapeuta}: {estadisticas}")
                return estadisticas
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return {}
        finally:
            if connection:
                connection.close()