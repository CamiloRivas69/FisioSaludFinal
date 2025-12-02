from bd.conexion_bd import get_db_connection, close_db_connection

class ServicioModel:
    @staticmethod
    def obtener_servicio_por_codigo(codigo):
        """
        Obtiene un servicio por su código desde la base de datos
        """
        conn = get_db_connection()
        if not conn:
            return None, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM servicio_terapia WHERE codigo = %s"
                cursor.execute(query, (codigo,))
                servicio = cursor.fetchone()

                if not servicio:
                    return None, "Servicio no encontrado"

                return servicio, None

        except Exception as e:
            print(f"Error en modelo obtener_servicio_por_codigo: {e}")
            return None, "Error interno al obtener el servicio"
        finally:
            close_db_connection(conn)

    @staticmethod
    def obtener_todos_servicios():
        """
        Obtiene todos los servicios terapéuticos
        """
        conn = get_db_connection()
        if not conn:
            return None, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM servicio_terapia"
                cursor.execute(query)
                servicios = cursor.fetchall()
                return servicios, None

        except Exception as e:
            print(f"Error en modelo obtener_todos_servicios: {e}")
            return None, "Error interno al obtener servicios"
        finally:
            close_db_connection(conn)

    @staticmethod
    def obtener_servicios_por_categoria(categoria):
        """
        Obtiene servicios filtrados por categoría
        """
        conn = get_db_connection()
        if not conn:
            return None, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                query = "SELECT * FROM servicio_terapia WHERE categoria = %s"
                cursor.execute(query, (categoria,))
                servicios = cursor.fetchall()
                return servicios, None

        except Exception as e:
            print(f"Error en modelo obtener_servicios_por_categoria: {e}")
            return None, "Error interno al filtrar servicios"
        finally:
            close_db_connection(conn)