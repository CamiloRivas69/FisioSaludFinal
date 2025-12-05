# modelo/CitaFisioModel.py
import pymysql
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta
import json

class CitaFisioModel:
    
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
    def convertir_objeto_serializable(obj):
        """Convierte cualquier objeto no serializable a string"""
        if obj is None:
            return ''
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return str(obj)
        elif isinstance(obj, (int, float, str, bool)):
            return obj
        else:
            return str(obj)
    
    @staticmethod
    def obtener_citas_por_terapeuta(terapeuta_nombre: str) -> List[Dict]:
        """
        Obtiene todas las citas asignadas a un terapeuta específico
        """
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    cita_id,
                    nombre_paciente,
                    servicio,
                    terapeuta_designado,
                    telefono,
                    correo,
                    fecha_cita,
                    hora_cita,
                    notas_adicionales,
                    tipo_pago,
                    estado
                FROM cita 
                WHERE terapeuta_designado = %s
                ORDER BY fecha_cita DESC, hora_cita DESC
                """
                cursor.execute(sql, (terapeuta_nombre,))
                resultados = cursor.fetchall()
                print(f"✅ Se encontraron {len(resultados)} citas para el terapeuta: {terapeuta_nombre}")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener citas del terapeuta: {e}")
            return []
        finally:
            if connection:
                connection.close()

    
    
    
    @staticmethod
    def obtener_estadisticas_citas(terapeuta_nombre: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de citas para las cards del dashboard
        """
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {}
            
        try:
            with connection.cursor() as cursor:
                estadisticas = {}
                
                # 1. Citas de hoy
                sql_hoy = """
                SELECT COUNT(*) as total 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND fecha_cita = CURDATE()
                """
                cursor.execute(sql_hoy, (terapeuta_nombre,))
                estadisticas['hoy'] = cursor.fetchone()['total']
                
                # 2. Citas pendientes (por confirmar)
                sql_pendientes = """
                SELECT COUNT(*) as total 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND estado = 'pendiente'
                """
                cursor.execute(sql_pendientes, (terapeuta_nombre,))
                estadisticas['pendientes'] = cursor.fetchone()['total']
                
                # 3. Citas de esta semana
                sql_semana = """
                SELECT COUNT(*) as total 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND YEARWEEK(fecha_cita, 1) = YEARWEEK(CURDATE(), 1)
                """
                cursor.execute(sql_semana, (terapeuta_nombre,))
                estadisticas['semana'] = cursor.fetchone()['total']
                
                # 4. Citas confirmadas este mes
                sql_confirmadas_mes = """
                SELECT COUNT(*) as total 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND estado = 'confirmada'
                AND MONTH(fecha_cita) = MONTH(CURDATE())
                AND YEAR(fecha_cita) = YEAR(CURDATE())
                """
                cursor.execute(sql_confirmadas_mes, (terapeuta_nombre,))
                estadisticas['confirmadas_mes'] = cursor.fetchone()['total']
                
                print(f"📊 Estadísticas obtenidas para {terapeuta_nombre}: {estadisticas}")
                return estadisticas
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas de citas: {e}")
            return {}
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def filtrar_citas(terapeuta_nombre: str, filtros: Dict) -> List[Dict]:
        """
        Filtra citas según criterios especificados
        """
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                # Construir query dinámica
                sql_base = """
                SELECT 
                    cita_id,
                    nombre_paciente,
                    servicio,
                    terapeuta_designado,
                    telefono,
                    correo,
                    fecha_cita,
                    hora_cita,
                    notas_adicionales,
                    tipo_pago,
                    estado
                FROM cita 
                WHERE terapeuta_designado = %s
                """
                
                parametros = [terapeuta_nombre]
                condiciones = []
                
                # Aplicar filtros si existen
                if 'fecha' in filtros and filtros['fecha']:
                    condiciones.append("fecha_cita = %s")
                    parametros.append(filtros['fecha'])
                
                if 'paciente' in filtros and filtros['paciente']:
                    condiciones.append("nombre_paciente LIKE %s")
                    parametros.append(f"%{filtros['paciente']}%")
                
                if 'servicio' in filtros and filtros['servicio']:
                    condiciones.append("servicio = %s")
                    parametros.append(filtros['servicio'])
                
                if 'estado' in filtros and filtros['estado']:
                    condiciones.append("estado = %s")
                    parametros.append(filtros['estado'])
                
                # Agregar condiciones a la query
                if condiciones:
                    sql_base += " AND " + " AND ".join(condiciones)
                
                # Ordenar
                sql_base += " ORDER BY fecha_cita DESC, hora_cita DESC"
                
                print(f"🔍 Ejecutando filtro: {sql_base}")
                print(f"📋 Parámetros: {parametros}")
                
                cursor.execute(sql_base, tuple(parametros))
                resultados = cursor.fetchall()
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                print(f"✅ Filtro aplicado: {len(citas_serializables)} citas encontradas")
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al filtrar citas: {e}")
            return []
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def obtener_acudiente_por_cita(cita_id: str) -> Optional[Dict]:
        """
        Obtiene información del acudiente asociado a una cita
        """
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return None
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    nombre_completo,
                    telefono,
                    correo
                FROM acudiente 
                WHERE ID_cita = %s
                """
                cursor.execute(sql, (cita_id,))
                acudiente = cursor.fetchone()
                
                if acudiente:
                    # Convertir a serializable
                    acudiente_serializable = {}
                    for key, value in acudiente.items():
                        acudiente_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    return acudiente_serializable
                return None
                
        except Exception as e:
            print(f"❌ Error al obtener acudiente: {e}")
            return None
        finally:
            if connection:
                connection.close()
    @staticmethod
    def cambiar_estado_cita(cita_id: str, nuevo_estado: str, terapeuta_nombre: str) -> Dict[str, Any]:
 
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
        
        try:
            with connection.cursor() as cursor:
                # 1. Verificar que la cita pertenece al terapeutacitas
                sql_verificar = """
                SELECT cita_id, estado, nombre_paciente, telefono, correo 
                FROM cita 
                WHERE cita_id = %s AND terapeuta_designado = %s
                """
                cursor.execute(sql_verificar, (cita_id, terapeuta_nombre))
                cita_existente = cursor.fetchone()
                
                if not cita_existente:
                    return {
                        'success': False, 
                        'error': 'Cita no encontrada o no tienes permiso para modificarla'
                    }
                
                estado_actual = cita_existente['estado']
                
                # 2. Validar transición de estado válida
                estados_validos = ['pendiente', 'confirmada', 'cancelada']
                if nuevo_estado not in estados_validos:
                    return {
                        'success': False,
                        'error': f'Estado no válido. Estados permitidos: {", ".join(estados_validos)}'
                    }
                
                # 3. Si se cancela, eliminar la cita (y acudiente si existe)
                if nuevo_estado == 'cancelada':
                    # Eliminar acudiente si existe
                    sql_eliminar_acudiente = "DELETE FROM acudiente WHERE ID_cita = %s"
                    cursor.execute(sql_eliminar_acudiente, (cita_id,))
                    
                    # Eliminar cita
                    sql_eliminar_cita = "DELETE FROM cita WHERE cita_id = %s"
                    cursor.execute(sql_eliminar_cita, (cita_id,))
                    
                    connection.commit()
                    
                    return {
                        'success': True,
                        'message': 'Cita cancelada y eliminada correctamente',
                        'accion': 'eliminada'
                    }
                
                # 4. Si se confirma, también crear registro en tabla paciente
                elif nuevo_estado == 'confirmada':
                    # Primero actualizar estado en cita
                    sql_actualizar_cita = """
                    UPDATE cita 
                    SET estado = %s 
                    WHERE cita_id = %s AND terapeuta_designado = %s
                    """
                    cursor.execute(sql_actualizar_cita, (nuevo_estado, cita_id, terapeuta_nombre))
                    
                    # Obtener datos COMPLETOS de la cita para crear paciente
                    sql_datos_cita = """
                    SELECT c.*, a.ID_acudiente, a.nombre_completo as nombre_acudiente,
                        a.telefono as telefono_acudiente, a.correo as correo_acudiente
                    FROM cita c
                    LEFT JOIN acudiente a ON c.cita_id = a.ID_cita
                    WHERE c.cita_id = %s
                    """
                    cursor.execute(sql_datos_cita, (cita_id,))
                    datos_cita = cursor.fetchone()
                    
                    if not datos_cita:
                        return {
                            'success': False,
                            'error': 'No se pudieron obtener datos de la cita'
                        }
                    
                    # VERIFICAR: ¿Ya existe en paciente?
                    sql_verificar_paciente = """
                    SELECT codigo_cita FROM paciente WHERE codigo_cita = %s
                    """
                    cursor.execute(sql_verificar_paciente, (cita_id,))
                    paciente_existente = cursor.fetchone()
                    
                    if paciente_existente:
                        return {
                            'success': False,
                            'error': 'Esta cita ya está registrada en pacientes'
                        }
                    
                    # PASO CRÍTICO: Necesitamos crear un usuario primero
                    # Verificar si ya existe un usuario con ese correo
                    correo_paciente = datos_cita.get('correo')
                    if not correo_paciente:
                        return {
                            'success': False,
                            'error': 'El paciente no tiene correo registrado'
                        }
                    
                    sql_verificar_usuario = """
                    SELECT ID FROM usuario WHERE correo = %s
                    """
                    cursor.execute(sql_verificar_usuario, (correo_paciente,))
                    usuario_existente = cursor.fetchone()
                    
                    ID_usuario = None
                    
                    if usuario_existente:
                        # Usuario ya existe, usar su ID
                        ID_usuario = usuario_existente['ID']
                    else:
                        # Crear nuevo usuario
                        sql_crear_usuario = """
                        INSERT INTO usuario (
                            nombre_completo, correo, telefono, tipo_usuario, 
                            fecha_registro, contrasena_hash, estado
                        ) VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
                        """
                        # Generar contraseña temporal
                        import hashlib
                        import random
                        temp_password = str(random.randint(100000, 999999))
                        contrasena_hash = hashlib.sha256(temp_password.encode()).hexdigest()
                        
                        cursor.execute(sql_crear_usuario, (
                            datos_cita['nombre_paciente'],
                            datos_cita['correo'],
                            datos_cita['telefono'],
                            'paciente',
                            contrasena_hash,
                            'activo'
                        ))
                        
                        ID_usuario = cursor.lastrowid
                        print(f"✅ Nuevo usuario creado: ID {ID_usuario}")
                    
                    # Gestionar acudiente si existe
                    ID_acudiente = None
                    if datos_cita.get('ID_acudiente'):
                        # Acudiente ya existe
                        ID_acudiente = datos_cita['ID_acudiente']
                    elif datos_cita.get('nombre_acudiente'):
                        # Crear nuevo acudiente
                        sql_crear_acudiente = """
                        INSERT INTO acudiente (
                            ID_cita, nombre_completo, telefono, correo
                        ) VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(sql_crear_acudiente, (
                            cita_id,
                            datos_cita['nombre_acudiente'],
                            datos_cita['telefono_acudiente'],
                            datos_cita['correo_acudiente']
                        ))
                        ID_acudiente = cursor.lastrowid
                    
                    # FINALMENTE: Insertar en tabla paciente con la estructura CORRECTA
                    sql_insert_paciente = """
                    INSERT INTO paciente (
                        codigo_cita,
                        ID_usuario,
                        nombre_completo,
                        ID_acudiente,
                        terapeuta_asignado,
                        estado_cita,
                        tipo_plan,
                        precio_plan,
                        fecha_creacion_reporte
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
                    """
                    
                    valores_paciente = (
                        cita_id,                      # codigo_cita
                        ID_usuario,                   # ID_usuario (OBLIGATORIO)
                        datos_cita['nombre_paciente'], # nombre_completo
                        ID_acudiente,                 # ID_acudiente (puede ser NULL)
                        terapeuta_nombre,             # terapeuta_asignado
                        'confirmed',                  # estado_cita
                        datos_cita['tipo_pago'],      # tipo_plan (usamos tipo_pago de cita)
                        0.00                          # precio_plan (inicial 0)
                    )
                    
                    cursor.execute(sql_insert_paciente, valores_paciente)
                    connection.commit()
                    
                    return {
                        'success': True,
                        'message': 'Cita confirmada y paciente creado exitosamente',
                        'accion': 'confirmada',
                        'datos_adicionales': {
                            'id_usuario': ID_usuario,
                            'id_acudiente': ID_acudiente
                        }
                    }
                
                # 5. Para otros estados (solo actualizar pendiente a otro estado no confirmado)
                else:
                    sql_actualizar = """
                    UPDATE cita 
                    SET estado = %s 
                    WHERE cita_id = %s AND terapeuta_designado = %s
                    """
                    cursor.execute(sql_actualizar, (nuevo_estado, cita_id, terapeuta_nombre))
                    connection.commit()
                    
                    return {
                        'success': True,
                        'message': f'Estado de cita actualizado a {nuevo_estado}',
                        'accion': 'actualizada'
                    }
                    
        except pymysql.Error as e:
            print(f"❌ Error de MySQL al cambiar estado de cita: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return {
                'success': False,
                'error': f'Error de base de datos: {str(e)}'
            }
        except Exception as e:
            print(f"❌ Error al cambiar estado de cita: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return {
                'success': False,
                'error': f'Error interno: {str(e)}'
            }
        finally:
            if connection:
                connection.close()