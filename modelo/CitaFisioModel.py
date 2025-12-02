import pymysql
from typing import Dict, List, Optional, Any
from datetime import datetime, date, timedelta

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
    def obtener_citas_por_terapeuta(terapeuta: str) -> List[Dict]:
        """Obtiene todas las citas del terapeuta especificado"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at,
                    c.updated_at,
                    p.historial_medico,
                    p.tipo_plan,
                    p.precio_plan,
                    p.estado_cita as estado_paciente,
                    a.nombre_acudiente,
                    a.telefono as telefono_acudiente
                FROM cita c
                LEFT JOIN paciente p ON c.cita_id = p.codigo_cita
                LEFT JOIN acudiente a ON p.ID_acudiente = a.ID_acudiente
                WHERE c.terapeuta_designado = %s
                ORDER BY c.fecha_cita DESC, c.hora_cita DESC
                """
                cursor.execute(sql, (terapeuta,))
                resultados = cursor.fetchall()
                print(f"✅ Se encontraron {len(resultados)} citas para el terapeuta: {terapeuta}")
                
                # Convertir todas las citas a formato serializable
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
    def crear_cita(
        servicio: str,
        terapeuta_designado: str,
        nombre_paciente: str,
        telefono: str,
        correo: str,
        fecha_cita: str,
        hora_cita: str,
        notas_adicionales: Optional[str] = None,
        tipo_pago: str = 'efectivo',
        estado: str = 'pending'
    ) -> Dict[str, Any]:
        """Crea una nueva cita en la base de datos"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
            
        try:
            with connection.cursor() as cursor:
                # Validar que no haya citas duplicadas en la misma fecha/hora
                sql_verificar = """
                SELECT COUNT(*) as count 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND fecha_cita = %s 
                AND hora_cita = %s
                """
                cursor.execute(sql_verificar, (terapeuta_designado, fecha_cita, hora_cita))
                resultado = cursor.fetchone()
                
                if resultado['count'] > 0:
                    return {
                        'success': False, 
                        'error': 'Ya existe una cita programada para esa fecha y hora'
                    }
                
                # Insertar nueva cita
                sql_insert = """
                INSERT INTO cita (
                    servicio, terapeuta_designado, nombre_paciente,
                    telefono, correo, fecha_cita, hora_cita,
                    notas_adicionales, tipo_pago, estado, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """
                
                cursor.execute(sql_insert, (
                    servicio, terapeuta_designado, nombre_paciente,
                    telefono, correo, fecha_cita, hora_cita,
                    notas_adicionales, tipo_pago, estado
                ))
                
                connection.commit()
                cita_id = cursor.lastrowid
                
                print(f"✅ Cita creada exitosamente - ID: {cita_id}")
                return {
                    'success': True,
                    'cita_id': cita_id,
                    'message': 'Cita creada exitosamente'
                }
                
        except pymysql.Error as e:
            print(f"❌ Error MySQL al crear cita: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': f'Error de base de datos: {e}'}
        except Exception as e:
            print(f"❌ Error inesperado al crear cita: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': 'Error interno del servidor'}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def crear_acudiente_y_actualizar_paciente(
        cita_id: int,
        acudiente_nombre: str,
        acudiente_id: Optional[str] = None,
        acudiente_telefono: Optional[str] = None,
        acudiente_correo: Optional[str] = None,
        acudiente_direccion: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crea un acudiente y actualiza el paciente"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
            
        try:
            with connection.cursor() as cursor:
                # Insertar acudiente
                sql_acudiente = """
                INSERT INTO acudiente (
                    nombre_acudiente, telefono, correo, direccion, ID_documento
                ) VALUES (%s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql_acudiente, (
                    acudiente_nombre, acudiente_telefono, acudiente_correo,
                    acudiente_direccion, acudiente_id
                ))
                
                acudiente_id_nuevo = cursor.lastrowid
                
                # Verificar si existe paciente para esta cita
                sql_verificar_paciente = """
                SELECT COUNT(*) as count 
                FROM paciente 
                WHERE codigo_cita = %s
                """
                cursor.execute(sql_verificar_paciente, (cita_id,))
                existe_paciente = cursor.fetchone()['count'] > 0
                
                if existe_paciente:
                    # Actualizar paciente existente con el ID del acudiente
                    sql_paciente = """
                    UPDATE paciente 
                    SET ID_acudiente = %s
                    WHERE codigo_cita = %s
                    """
                    cursor.execute(sql_paciente, (acudiente_id_nuevo, cita_id))
                else:
                    # Crear paciente básico
                    sql_crear_paciente = """
                    INSERT INTO paciente (
                        codigo_cita, ID_acudiente, nombre_completo, estado_cita
                    ) VALUES (%s, %s, %s, 'pending')
                    """
                    # Necesitamos obtener el nombre del paciente de la cita
                    sql_obtener_paciente = "SELECT nombre_paciente FROM cita WHERE cita_id = %s"
                    cursor.execute(sql_obtener_paciente, (cita_id,))
                    nombre_paciente_result = cursor.fetchone()
                    nombre_paciente = nombre_paciente_result['nombre_paciente'] if nombre_paciente_result else 'Desconocido'
                    
                    cursor.execute(sql_crear_paciente, (cita_id, acudiente_id_nuevo, nombre_paciente))
                
                connection.commit()
                
                print(f"✅ Acudiente creado y paciente actualizado - Cita ID: {cita_id}")
                return {
                    'success': True,
                    'acudiente_id': acudiente_id_nuevo,
                    'message': 'Acudiente creado exitosamente'
                }
                
        except Exception as e:
            print(f"❌ Error al crear acudiente: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': f'Error: {str(e)}'}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def actualizar_estado_cita_por_paciente(
        nombre_paciente: str,
        terapeuta: str,
        nuevo_estado: str
    ) -> Dict[str, Any]:
        """Actualiza el estado de una cita por nombre de paciente"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
            
        try:
            with connection.cursor() as cursor:
                # Primero encontrar la cita
                sql_buscar = """
                SELECT cita_id 
                FROM cita 
                WHERE nombre_paciente = %s 
                AND terapeuta_designado = %s
                LIMIT 1
                """
                cursor.execute(sql_buscar, (nombre_paciente, terapeuta))
                cita = cursor.fetchone()
                
                if not cita:
                    return {
                        'success': False,
                        'error': 'No se encontró cita para este paciente y terapeuta'
                    }
                
                cita_id = cita['cita_id']
                
                # Actualizar estado
                sql_actualizar = """
                UPDATE cita 
                SET estado = %s, updated_at = NOW()
                WHERE cita_id = %s
                """
                
                cursor.execute(sql_actualizar, (nuevo_estado, cita_id))
                connection.commit()
                
                if cursor.rowcount > 0:
                    print(f"✅ Estado actualizado para cita {cita_id}: {nuevo_estado}")
                    return {
                        'success': True,
                        'message': f'Estado actualizado a {nuevo_estado}',
                        'cita_id': cita_id
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Error al actualizar estado'
                    }
                
        except Exception as e:
            print(f"❌ Error al actualizar estado de cita: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': f'Error: {str(e)}'}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def actualizar_estado_cita(cita_id: str, nuevo_estado: str) -> Dict[str, Any]:
        """Actualiza el estado de una cita por ID"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
            
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE cita 
                SET estado = %s, updated_at = NOW()
                WHERE cita_id = %s
                """
                
                cursor.execute(sql, (nuevo_estado, cita_id))
                connection.commit()
                
                if cursor.rowcount > 0:
                    print(f"✅ Estado actualizado para cita {cita_id}: {nuevo_estado}")
                    return {
                        'success': True,
                        'message': f'Estado actualizado a {nuevo_estado}'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Cita no encontrada'
                    }
                
        except Exception as e:
            print(f"❌ Error al actualizar estado de cita: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': f'Error: {str(e)}'}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def filtrar_citas_terapeuta(
        terapeuta: str,
        estado: Optional[str] = None,
        paciente: Optional[str] = None,
        fecha: Optional[str] = None,
        servicio: Optional[str] = None
    ) -> List[Dict]:
        """Filtra citas del terapeuta según criterios"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                # Construir consulta dinámica
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at,
                    c.updated_at
                FROM cita c
                WHERE c.terapeuta_designado = %s
                """
                
                params = [terapeuta]
                
                # Agregar filtros dinámicos
                if estado and estado != 'todos':
                    sql += " AND c.estado = %s"
                    params.append(estado)
                
                if paciente:
                    sql += " AND LOWER(c.nombre_paciente) LIKE LOWER(%s)"
                    params.append(f"%{paciente}%")
                
                if fecha:
                    sql += " AND c.fecha_cita = %s"
                    params.append(fecha)
                
                if servicio and servicio != 'todos':
                    sql += " AND c.servicio = %s"
                    params.append(servicio)
                
                sql += " ORDER BY c.fecha_cita DESC, c.hora_cita DESC"
                
                cursor.execute(sql, tuple(params))
                resultados = cursor.fetchall()
                
                print(f"✅ Filtradas {len(resultados)} citas para {terapeuta}")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al filtrar citas: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_estadisticas_citas(terapeuta: str) -> Dict[str, Any]:
        """Obtiene estadísticas de citas para el terapeuta"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {}
            
        try:
            with connection.cursor() as cursor:
                # Total citas
                sql_total = "SELECT COUNT(*) as total FROM cita WHERE terapeuta_designado = %s"
                cursor.execute(sql_total, (terapeuta,))
                total = cursor.fetchone()['total']
                
                # Citas por estado
                sql_estados = """
                SELECT estado, COUNT(*) as count 
                FROM cita 
                WHERE terapeuta_designado = %s
                GROUP BY estado
                """
                cursor.execute(sql_estados, (terapeuta,))
                estados = cursor.fetchall()
                distribucion_estados = {e['estado']: e['count'] for e in estados}
                
                # Citas hoy
                hoy = date.today().isoformat()
                sql_hoy = """
                SELECT COUNT(*) as hoy 
                FROM cita 
                WHERE terapeuta_designado = %s AND fecha_cita = %s
                """
                cursor.execute(sql_hoy, (terapeuta, hoy))
                hoy_count = cursor.fetchone()['hoy']
                
                # Citas pendientes hoy
                sql_pendientes_hoy = """
                SELECT COUNT(*) as pendientes_hoy 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND fecha_cita = %s 
                AND estado = 'pending'
                """
                cursor.execute(sql_pendientes_hoy, (terapeuta, hoy))
                pendientes_hoy = cursor.fetchone()['pendientes_hoy']
                
                # Citas esta semana
                fecha_inicio_semana = (date.today() - timedelta(days=date.today().weekday())).isoformat()
                fecha_fin_semana = (date.today() + timedelta(days=6 - date.today().weekday())).isoformat()
                
                sql_semana = """
                SELECT COUNT(*) as semana 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND fecha_cita BETWEEN %s AND %s
                """
                cursor.execute(sql_semana, (terapeuta, fecha_inicio_semana, fecha_fin_semana))
                semana_count = cursor.fetchone()['semana']
                
                # Citas por servicio
                sql_servicios = """
                SELECT servicio, COUNT(*) as count 
                FROM cita 
                WHERE terapeuta_designado = %s
                GROUP BY servicio
                """
                cursor.execute(sql_servicios, (terapeuta,))
                servicios = cursor.fetchall()
                distribucion_servicios = {s['servicio']: s['count'] for s in servicios if s['servicio']}
                
                # Citas completadas este mes
                fecha_inicio_mes = date.today().replace(day=1).isoformat()
                fecha_fin_mes = (date.today().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                
                sql_mes = """
                SELECT COUNT(*) as completadas_mes 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND estado = 'completed'
                AND fecha_cita BETWEEN %s AND %s
                """
                cursor.execute(sql_mes, (terapeuta, fecha_inicio_mes, fecha_fin_mes.isoformat()))
                completadas_mes = cursor.fetchone()['completadas_mes']
                
                estadisticas = {
                    'total_citas': total,
                    'distribucion_estados': distribucion_estados,
                    'citas_hoy': hoy_count,
                    'pendientes_hoy': pendientes_hoy,
                    'citas_semana': semana_count,
                    'completadas_mes': completadas_mes,
                    'distribucion_servicios': distribucion_servicios,
                    'terapeuta': terapeuta,
                    'fecha_consulta': hoy
                }
                
                print(f"📊 Estadísticas de citas obtenidas para {terapeuta}")
                return estadisticas
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas de citas: {e}")
            return {}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_cita_por_id(cita_id: str) -> Optional[Dict]:
        """Obtiene una cita específica por ID"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return None
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at,
                    c.updated_at,
                    p.historial_medico,
                    p.tipo_plan,
                    p.precio_plan,
                    p.ejercicios_registrados,
                    a.nombre_acudiente,
                    a.telefono as telefono_acudiente,
                    a.correo as correo_acudiente,
                    a.direccion as direccion_acudiente
                FROM cita c
                LEFT JOIN paciente p ON c.cita_id = p.codigo_cita
                LEFT JOIN acudiente a ON p.ID_acudiente = a.ID_acudiente
                WHERE c.cita_id = %s
                """
                cursor.execute(sql, (cita_id,))
                cita = cursor.fetchone()
                
                if cita:
                    # Convertir a formato serializable
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    return cita_serializable
                
                return None
                
        except Exception as e:
            print(f"❌ Error al obtener cita por ID: {e}")
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def confirmar_todas_citas_pendientes(terapeuta: str) -> Dict[str, Any]:
        """Confirma todas las citas pendientes del terapeuta"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return {'success': False, 'error': 'Error de conexión a BD'}
            
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE cita 
                SET estado = 'confirmed', updated_at = NOW()
                WHERE terapeuta_designado = %s 
                AND estado = 'pending'
                AND fecha_cita >= CURDATE()
                """
                
                cursor.execute(sql, (terapeuta,))
                connection.commit()
                
                actualizadas = cursor.rowcount
                print(f"✅ Confirmadas {actualizadas} citas pendientes para {terapeuta}")
                
                return {
                    'success': True,
                    'message': f'Se confirmaron {actualizadas} citas pendientes',
                    'actualizadas': actualizadas
                }
                
        except Exception as e:
            print(f"❌ Error al confirmar todas las citas: {e}")
            if connection:
                connection.rollback()
            return {'success': False, 'error': f'Error: {str(e)}'}
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_citas_hoy(terapeuta: str) -> List[Dict]:
        """Obtiene las citas de hoy para un terapeuta"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                hoy = date.today().isoformat()
                
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at
                FROM cita c
                WHERE c.terapeuta_designado = %s 
                AND c.fecha_cita = %s
                ORDER BY c.hora_cita ASC
                """
                
                cursor.execute(sql, (terapeuta, hoy))
                resultados = cursor.fetchall()
                
                print(f"✅ Se encontraron {len(resultados)} citas para hoy ({hoy})")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener citas de hoy: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_citas_pendientes(terapeuta: str) -> List[Dict]:
        """Obtiene las citas pendientes para un terapeuta"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at
                FROM cita c
                WHERE c.terapeuta_designado = %s 
                AND c.estado = 'pending'
                AND c.fecha_cita >= CURDATE()
                ORDER BY c.fecha_cita ASC, c.hora_cita ASC
                """
                
                cursor.execute(sql, (terapeuta,))
                resultados = cursor.fetchall()
                
                print(f"✅ Se encontraron {len(resultados)} citas pendientes para {terapeuta}")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener citas pendientes: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_historial_citas(terapeuta: str, limite: int = 100) -> List[Dict]:
        """Obtiene el historial de citas (completadas y canceladas)"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at,
                    c.updated_at
                FROM cita c
                WHERE c.terapeuta_designado = %s 
                AND (c.estado = 'completed' OR c.estado = 'canceled')
                ORDER BY c.fecha_cita DESC, c.hora_cita DESC
                LIMIT %s
                """
                
                cursor.execute(sql, (terapeuta, limite))
                resultados = cursor.fetchall()
                
                print(f"✅ Se encontraron {len(resultados)} citas en el historial para {terapeuta}")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al obtener historial de citas: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_disponibilidad_horaria(terapeuta: str, fecha: str) -> List[str]:
        """Obtiene horas disponibles para un terapeuta en una fecha específica"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                # Horarios estándar (puedes ajustar según tus necesidades)
                horarios_disponibles = [
                    '08:00', '09:00', '10:00', '11:00', 
                    '14:00', '15:00', '16:00', '17:00'
                ]
                
                # Obtener horas ocupadas
                sql = """
                SELECT hora_cita 
                FROM cita 
                WHERE terapeuta_designado = %s 
                AND fecha_cita = %s 
                AND estado != 'canceled'
                """
                
                cursor.execute(sql, (terapeuta, fecha))
                resultados = cursor.fetchall()
                
                horas_ocupadas = [resultado['hora_cita'][:5] for resultado in resultados if resultado['hora_cita']]
                
                # Filtrar horas disponibles
                horas_disponibles = [hora for hora in horarios_disponibles if hora not in horas_ocupadas]
                
                print(f"📅 Horas disponibles para {terapeuta} el {fecha}: {len(horas_disponibles)}")
                return horas_disponibles
                
        except Exception as e:
            print(f"❌ Error al obtener disponibilidad horaria: {e}")
            return []
        finally:
            if connection:
                connection.close()

    @staticmethod
    def exportar_citas_csv(terapeuta: str) -> str:
        """Exporta todas las citas del terapeuta a formato CSV"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return ""
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    cita_id,
                    servicio,
                    terapeuta_designado,
                    nombre_paciente,
                    telefono,
                    correo,
                    fecha_cita,
                    hora_cita,
                    tipo_pago,
                    estado,
                    created_at
                FROM cita 
                WHERE terapeuta_designado = %s
                ORDER BY fecha_cita DESC, hora_cita DESC
                """
                
                cursor.execute(sql, (terapeuta,))
                resultados = cursor.fetchall()
                
                # Crear CSV
                csv_content = "ID;Servicio;Terapeuta;Paciente;Teléfono;Correo;Fecha;Hora;Tipo Pago;Estado;Creado\n"
                
                for cita in resultados:
                    csv_content += f"{cita['cita_id']};"
                    csv_content += f"{cita['servicio']};"
                    csv_content += f"{cita['terapeuta_designado']};"
                    csv_content += f"{cita['nombre_paciente']};"
                    csv_content += f"{cita['telefono'] or ''};"
                    csv_content += f"{cita['correo'] or ''};"
                    csv_content += f"{cita['fecha_cita'].isoformat() if cita['fecha_cita'] else ''};"
                    csv_content += f"{cita['hora_cita'] or ''};"
                    csv_content += f"{cita['tipo_pago'] or ''};"
                    csv_content += f"{cita['estado'] or ''};"
                    csv_content += f"{cita['created_at'].isoformat() if cita['created_at'] else ''}\n"
                
                print(f"📤 Exportadas {len(resultados)} citas a CSV para {terapeuta}")
                return csv_content
                
        except Exception as e:
            print(f"❌ Error al exportar citas a CSV: {e}")
            return ""
        finally:
            if connection:
                connection.close()

    @staticmethod
    def buscar_citas(terapeuta: str, consulta: str) -> List[Dict]:
        """Busca citas por nombre de paciente, teléfono o correo"""
        connection = CitaFisioModel.get_db_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT 
                    c.cita_id,
                    c.servicio,
                    c.terapeuta_designado,
                    c.nombre_paciente,
                    c.telefono,
                    c.correo,
                    c.fecha_cita,
                    c.hora_cita,
                    c.notas_adicionales,
                    c.tipo_pago,
                    c.estado,
                    c.created_at
                FROM cita c
                WHERE c.terapeuta_designado = %s 
                AND (
                    LOWER(c.nombre_paciente) LIKE LOWER(%s)
                    OR c.telefono LIKE %s
                    OR LOWER(c.correo) LIKE LOWER(%s)
                )
                ORDER BY c.fecha_cita DESC, c.hora_cita DESC
                LIMIT 50
                """
                
                busqueda = f"%{consulta}%"
                cursor.execute(sql, (terapeuta, busqueda, busqueda, busqueda))
                resultados = cursor.fetchall()
                
                print(f"🔍 Se encontraron {len(resultados)} citas para la búsqueda: '{consulta}'")
                
                # Convertir a formato serializable
                citas_serializables = []
                for cita in resultados:
                    cita_serializable = {}
                    for key, value in cita.items():
                        cita_serializable[key] = CitaFisioModel.convertir_objeto_serializable(value)
                    citas_serializables.append(cita_serializable)
                
                return citas_serializables
                
        except Exception as e:
            print(f"❌ Error al buscar citas: {e}")
            return []
        finally:
            if connection:
                connection.close()