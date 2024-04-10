class Order:
    def __init__(self, order_id, user_id, order_date, total_amount, payment_method_id):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.payment_method_id = payment_method_id

class ModelOrder:
    @classmethod
    def place_order(cls, mysql, user_id, cart_items, payment_method_id):
        try:
            cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado para realizar la venta
            cursor.callproc('realizar_venta', (user_id, cart_items, payment_method_id))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al realizar la venta:", ex)
            raise Exception(ex)
        

    @classmethod
    def get_all_orders_details(cls, mysql):
        orders_info = []  # Lista para almacenar la información de todas las órdenes
        try:
            cursor = mysql.connection.cursor()
            
            # Obtener todas las órdenes
            query_orders = """
                SELECT o.id, o.user_id, o.order_date, o.total_amount, o.payment_method_id
                FROM orders o
            """
            cursor.execute(query_orders)
            orders = cursor.fetchall()  # Recuperar todas las órdenes
            
            for order_details in orders:
                # Preparar los detalles de la orden en un diccionario
                order_info = {
                    "id": order_details[0],
                    "user_id": order_details[1],
                    "order_date": order_details[2],
                    "total_amount": order_details[3],
                    "payment_method_id": order_details[4],
                    "items": []
                }
                
                # Obtener los productos vendidos en esta orden
                query_items = """
                    SELECT oi.product_id, p.name, oi.quantity, oi.price, p.image_url
                    FROM order_items oi
                    INNER JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """
                cursor.execute(query_items, (order_details[0],))  # Usar el ID de la orden actual
                products = cursor.fetchall()
                
                # Añadir los productos al diccionario de la orden
                for product in products:
                    order_info["items"].append({
                        "product_id": product[0],
                        "name": product[1],
                        "quantity": product[2],
                        "price": product[3],
                        "image_url": product[4]
                    })
                
                orders_info.append(order_info)  # Añadir la orden y sus productos a la lista
            
            return orders_info

        except Exception as ex:
            print("Error al obtener los detalles de las órdenes:", ex)
            return []

        finally:
            if cursor:
                cursor.close()
        

    @classmethod
    def get_order_details(cls, db, order_id):
        try:
            cursor = db.connection.cursor()
            
            # Obtener los detalles de la orden
            query_order = """
                SELECT o.id, o.user_id, o.order_date, o.total_amount, o.payment_method_id
                FROM orders o
                WHERE o.id = %s
            """
            cursor.execute(query_order, (order_id,))
            order_details = cursor.fetchone()
            
            if order_details:
                # Preparar los detalles de la orden en un diccionario
                order_info = {
                    "id": order_details[0],
                    "user_id": order_details[1],
                    "order_date": order_details[2],
                    "total_amount": order_details[3],
                    "payment_method_id": order_details[4],
                    "items": []
                }
                
                # Obtener los productos vendidos en la orden
                query_items = """
                    SELECT oi.product_id, p.name, oi.quantity, oi.price, p.image_url
                    FROM order_items oi
                    INNER JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """
                cursor.execute(query_items, (order_id,))
                products = cursor.fetchall()
                
                # Añadir los productos al diccionario de la orden
                for product in products:
                    order_info["items"].append({
                        "product_id": product[0],
                        "name": product[1],
                        "quantity": product[2],
                        "price": product[3],
                        "image_url": product[4]
                    })
                
                return order_info
            else:
                return None

        except Exception as ex:
            print("Error al obtener los detalles de la venta:", ex)
            raise

        finally:
            if cursor:
                cursor.close()