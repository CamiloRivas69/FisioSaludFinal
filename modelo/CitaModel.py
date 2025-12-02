import pymysql
from bd.conexion_bd import get_db_connection, close_db_connection
from typing import List, Dict, Any, Optional
from datetime import timedelta

class CitaModel:
    
    @staticmethod
    def generar_codigo_cita() -> str:
        """Genera un código único para la cita en formato FS-0001"""
        conn = get_db_connection()
        if conn is None:
            return ""
        
        try:
            with conn.cursor() as cursor:
                # Obtener el último código de cita
                sql = "SELECT cita_id FROM cita ORDER BY cita_id DESC LIMIT 1"
                cursor.execute(sql)
                ultima_cita = cursor.fetchone()
                
                if ultima_cita:
                    try:
                        # Extraer el número y incrementar
                        ultimo_numero = int(ultima_cita['cita_id'].split('-')[1])
                        nuevo_numero = ultimo_numero + 1
                    except (ValueError, IndexError):
                        # Si hay formato incorrecto, empezar desde 1
                        nuevo_numero = 1
                else:
                    # Primera cita
                    nuevo_numero = 1
                
                return f"FS-{nuevo_numero:04d}"
                
        except Exception as e:
            print(f"Error al generar código de cita: {e}")
            return f"FS-{1:04d}"  # Fallback
        finally:
            close_db_connection(conn)

    @staticmethod
    def obtener_servicios_terapia() -> List[Dict[str, Any]]:
        """Obtiene todos los servicios de terapia disponibles"""
        conn = get_db_connection()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT codigo, nombre, descripcion, terapeuta_disponible, 
                       inicio_jornada, final_jornada, duracion, modalidad, 
                       precio, beneficios
                FROM servicio_terapia 
                WHERE codigo IS NOT NULL
                """
                cursor.execute(sql)
                servicios = cursor.fetchall()
                
                # Convertir a diccionarios y formatear datos
                servicios_formateados = []
                for servicio in servicios:
                    servicio_dict = dict(servicio)
                    
                    # Convertir timedelta a string legible
                    if isinstance(servicio_dict.get('duracion'), timedelta):
                        total_minutes = servicio_dict['duracion'].total_seconds() / 60
                        horas = int(total_minutes // 60)
                        minutos = int(total_minutes % 60)
                        if horas > 0:
                            servicio_dict['duracion'] = f"{horas}h {minutos}min"
                        else:
                            servicio_dict['duracion'] = f"{minutos} min"
                    
                    # Convertir time a string
                    for time_field in ['inicio_jornada', 'final_jornada']:
                        if servicio_dict.get(time_field):
                            servicio_dict[time_field] = str(servicio_dict[time_field])
                    
                    # Asegurar que el precio sea float
                    if servicio_dict.get('precio'):
                        servicio_dict['precio'] = float(servicio_dict['precio'])
                    
                    servicios_formateados.append(servicio_dict)
                
                return servicios_formateados
                
        except Exception as e:
            print(f"Error al obtener servicios de terapia: {e}")
            return []
        finally:
            close_db_connection(conn)

    @staticmethod
    def crear_cita(datos_cita: Dict[str, Any]) -> str:
        """Crea una nueva cita y retorna el código de la cita creada"""
        conn = get_db_connection()
        if conn is None:
            return ""
        
        try:
            with conn.cursor() as cursor:
                # Generar código único para la cita
                codigo_cita = CitaModel.generar_codigo_cita()
                
                if not codigo_cita:
                    raise Exception("No se pudo generar el código de cita")
                
                sql = """
                INSERT INTO cita (cita_id, servicio, terapeuta_designado, nombre_paciente, 
                                telefono, correo, fecha_cita, hora_cita, 
                                notas_adicionales, tipo_pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql, (
                    codigo_cita,  # Código alfanumérico (FS-0001)
                    datos_cita['servicio'],
                    datos_cita['terapeuta_designado'],
                    datos_cita['nombre_paciente'],
                    datos_cita['telefono'],
                    datos_cita['correo'],
                    datos_cita['fecha_cita'],
                    datos_cita['hora_cita'],
                    datos_cita.get('notas_adicionales', ''),
                    datos_cita['tipo_pago']
                ))
                
                conn.commit()
                
                # Verificar que se insertó correctamente
                cursor.execute("SELECT cita_id FROM cita WHERE cita_id = %s", (codigo_cita,))
                cita_verificada = cursor.fetchone()
                
                if cita_verificada:
                    print(f"Cita creada exitosamente: {codigo_cita}")
                    return codigo_cita
                else:
                    raise Exception("No se pudo verificar la creación de la cita")
                    
        except Exception as e:
            print(f"Error al crear cita: {e}")
            if conn:
                conn.rollback()
            return ""
        finally:
            close_db_connection(conn)

    @staticmethod
    def crear_acudiente(codigo_cita: str, datos_acudiente: Dict[str, Any]) -> bool:
        """Crea un nuevo registro de acudiente vinculado a una cita"""
        conn = get_db_connection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                # Verificar que la cita existe
                cursor.execute("SELECT cita_id FROM cita WHERE cita_id = %s", (codigo_cita,))
                if not cursor.fetchone():
                    print(f"Error: No existe la cita {codigo_cita} para vincular acudiente")
                    return False
                
                sql = """
                INSERT INTO acudiente (cita_id, nombre_completo, identificacion, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    codigo_cita,
                    datos_acudiente['nombre_completo'],
                    datos_acudiente['identificacion'],
                    datos_acudiente.get('telefono', ''),
                    datos_acudiente.get('correo', ''),
                    datos_acudiente.get('direccion', '')
                ))
                conn.commit()
                print(f"Acudiente creado exitosamente para cita: {codigo_cita}")
                return True
                
        except Exception as e:
            print(f"Error al crear acudiente: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            close_db_connection(conn)

    @staticmethod
    def verificar_disponibilidad_cita(fecha: str, hora: str, terapeuta: str) -> bool:
        """Verifica si la hora y fecha están disponibles para el terapeuta"""
        conn = get_db_connection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT COUNT(*) as count 
                FROM cita 
                WHERE fecha_cita = %s AND hora_cita = %s AND terapeuta_designado = %s
                """
                cursor.execute(sql, (fecha, hora, terapeuta))
                resultado = cursor.fetchone()
                disponible = resultado['count'] == 0
                print(f"Disponibilidad para {terapeuta} el {fecha} a las {hora}: {'Sí' if disponible else 'No'}")
                return disponible
                
        except Exception as e:
            print(f"Error al verificar disponibilidad: {e}")
            return False
        finally:
            close_db_connection(conn)