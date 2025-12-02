# modelo/CarritoModel.py
from bd.conexion_bd import get_db_connection, close_db_connection
from datetime import datetime

class CarritoModel:
    
    @staticmethod
    def agregar_al_carrito(usuario_id, producto_id, producto_tipo, cantidad=1):
        """
        Agrega un producto al carrito especificando el tipo
        producto_tipo: 'nutricion' o 'implemento'
        """
        conn = get_db_connection()
        if not conn:
            return False, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                # Verificar si el producto ya está en el carrito
                query = """
                SELECT id, cantidad FROM carrito 
                WHERE usuario_id = %s AND producto_id = %s AND producto_tipo = %s
                """
                cursor.execute(query, (usuario_id, producto_id, producto_tipo))
                item_existente = cursor.fetchone()

                if item_existente:
                    # Actualizar cantidad si ya existe
                    nueva_cantidad = item_existente['cantidad'] + cantidad
                    query = "UPDATE carrito SET cantidad = %s, actualizado_en = %s WHERE id = %s"
                    cursor.execute(query, (nueva_cantidad, datetime.now(), item_existente['id']))
                else:
                    # Insertar nuevo item
                    query = """
                    INSERT INTO carrito (usuario_id, producto_id, producto_tipo, cantidad, creado_en, actualizado_en)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (usuario_id, producto_id, producto_tipo, cantidad, datetime.now(), datetime.now()))
                
                conn.commit()
                return True, "Producto agregado al carrito"

        except Exception as e:
            print(f"Error en modelo agregar_al_carrito: {e}")
            return False, "Error interno al agregar al carrito"
        finally:
            close_db_connection(conn)


    # modelo/CarritoModel.py - VERIFICA que tenga esto
    @staticmethod
    def obtener_carrito_usuario(usuario_id):
        """
        Obtiene todos los items del carrito con información completa de ambos tipos de productos
        """
        conn = get_db_connection()
        if not conn:
            return None, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                # UNION de ambos tipos de productos - CORREGIDO
                query = """
                -- Productos de nutrición (SIN columna peso)
                SELECT 
                    c.id as carrito_id,
                    c.cantidad,
                    c.producto_tipo,
                    c.creado_en,
                    sn.codigo,
                    sn.nombre,
                    sn.descripcion,
                    sn.precio,
                    sn.porciones,
                    NULL as peso,  -- ✅ Agregar NULL para peso
                    'nutricion' as tipo
                FROM carrito c
                JOIN servicio_nutricion sn ON c.producto_id = sn.codigo
                WHERE c.usuario_id = %s AND c.producto_tipo = 'nutricion'
                
                UNION ALL
                
                -- Productos de implementos (CON columna peso)
                SELECT 
                    c.id as carrito_id,
                    c.cantidad,
                    c.producto_tipo,
                    c.creado_en,
                    si.codigo,
                    si.nombre,
                    si.descripcion,
                    si.precio,
                    NULL as porciones,  -- ✅ NULL para porciones
                    si.peso,            -- ✅ Incluir peso
                    'implemento' as tipo
                FROM carrito c
                JOIN servicio_implementos si ON c.producto_id = si.codigo
                WHERE c.usuario_id = %s AND c.producto_tipo = 'implemento'
                
                ORDER BY creado_en DESC
                """
                cursor.execute(query, (usuario_id, usuario_id))
                items = cursor.fetchall()
                
                # Convertir tipos no serializables
                for item in items:
                    # Convertir Decimal a float
                    if 'precio' in item and item['precio'] is not None:
                        item['precio'] = float(item['precio'])
                    
                    # Convertir peso si existe
                    if 'peso' in item and item['peso'] is not None:
                        item['peso'] = float(item['peso'])
                    
                    # ✅ CONVERTIR datetime a string ISO format
                    if 'creado_en' in item and item['creado_en'] is not None:
                        item['creado_en'] = item['creado_en'].isoformat() if hasattr(item['creado_en'], 'isoformat') else str(item['creado_en'])
                    
                    # Si hay otros campos datetime, convertirlos también
                    if 'actualizado_en' in item and item['actualizado_en'] is not None:
                        item['actualizado_en'] = item['actualizado_en'].isoformat() if hasattr(item['actualizado_en'], 'isoformat') else str(item['actualizado_en'])
                
                print(f"✅ Carrito obtenido: {len(items)} items")
                return items, None

        except Exception as e:
            print(f"Error en modelo obtener_carrito_usuario: {e}")
            return None, "Error interno al obtener carrito"
        finally:
            close_db_connection(conn)

    @staticmethod
    def eliminar_del_carrito(carrito_id, usuario_id):
        """
        Elimina un item del carrito
        """
        conn = get_db_connection()
        if not conn:
            return False, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM carrito WHERE id = %s AND usuario_id = %s"
                cursor.execute(query, (carrito_id, usuario_id))
                conn.commit()
                return True, "Producto eliminado del carrito"

        except Exception as e:
            print(f"Error en modelo eliminar_del_carrito: {e}")
            return False, "Error interno al eliminar del carrito"
        finally:
            close_db_connection(conn)

    @staticmethod
    def actualizar_cantidad_carrito(carrito_id, usuario_id, cantidad):
        """
        Actualiza la cantidad de un producto en el carrito
        """
        conn = get_db_connection()
        if not conn:
            return False, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                if cantidad <= 0:
                    # Si la cantidad es 0 o negativa, eliminar el item
                    return CarritoModel.eliminar_del_carrito(carrito_id, usuario_id)
                
                query = "UPDATE carrito SET cantidad = %s, actualizado_en = %s WHERE id = %s AND usuario_id = %s"
                cursor.execute(query, (cantidad, datetime.now(), carrito_id, usuario_id))
                conn.commit()
                return True, "Cantidad actualizada"

        except Exception as e:
            print(f"Error en modelo actualizar_cantidad_carrito: {e}")
            return False, "Error interno al actualizar cantidad"
        finally:
            close_db_connection(conn)

    @staticmethod
    def vaciar_carrito(usuario_id):
        """
        Vacía todo el carrito del usuario
        """
        conn = get_db_connection()
        if not conn:
            return False, "Error de conexión con la base de datos"

        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM carrito WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
                conn.commit()
                return True, "Carrito vaciado"

        except Exception as e:
            print(f"Error en modelo vaciar_carrito: {e}")
            return False, "Error interno al vaciar carrito"
        finally:
            close_db_connection(conn)