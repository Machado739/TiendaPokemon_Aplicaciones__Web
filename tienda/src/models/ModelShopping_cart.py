
class CartItem:
    def __init__(self, id, user_id, product_id, quantity):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

class CartItems:
    def __init__(self, cart_item_id, user_id, product_id, quantity,product_name,unit_price,image_url):
        self.cart_item_id = cart_item_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.product_name = product_name  # Nombre del producto
        self.unit_price = unit_price    # Precio unitario del producto
        self.image_url = image_url      # URL de la imagen del producto
        
class ShoppingCartModel:
    @classmethod
    def add_to_cart(cls, mysql, user_id, product_id, quantity):
        try:
            cursor = mysql.connection.cursor()
            # Primero, verifica la cantidad disponible en el inventario
            cursor.execute("SELECT quantity FROM inventory WHERE product_id = %s", (product_id,))
            stock = cursor.fetchone()
            if stock and stock[0] >= quantity:
                # Si hay suficiente stock, procede a añadir al carrito
                cursor.execute("INSERT INTO shopping_cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, quantity))
                mysql.connection.commit()
            else:
                # Maneja el caso de no tener suficiente stock
                print("Cantidad solicitada no disponible en el inventario.")
                return False
        except Exception as ex:
            print("Error al agregar al carrito:", ex)
            raise
        finally:
            cursor.close()
        return True


    @classmethod
    def update_cart_item_quantity(cls, mysql, cart_item_id,product_id, new_quantity):
        try:
            cursor = mysql.connection.cursor()
            # Obtén el product_id para este cart_item_id
            cursor.execute("SELECT product_id FROM shopping_cart WHERE id = %s", (cart_item_id,))
            product_info = cursor.fetchone()
            if product_info:
                product_id = product_info[0]
                # Verifica la cantidad disponible en el inventario
                cursor.execute("SELECT quantity FROM inventory WHERE product_id = %s", (product_id,))
                stock = cursor.fetchone()
                if stock and stock[0] >= new_quantity:
                    # Si hay suficiente stock, procede a actualizar la cantidad en el carrito
                    cursor.execute("UPDATE shopping_cart SET quantity = %s WHERE id = %s", (new_quantity, cart_item_id))
                    mysql.connection.commit()
                else:
                    # Maneja el caso de no tener suficiente stock
                    print("Cantidad solicitada no disponible en el inventario.")
                    return False
            else:
                print("Producto no encontrado en el carrito.")
                return False
        except Exception as ex:
            print("Error al actualizar la cantidad del elemento del carrito:", ex)
            raise
        finally:
            cursor.close()
        return True


    @classmethod
    def remove_cart(cls, mysql, cart_item_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM shopping_cart WHERE id = %s", (cart_item_id,))

            mysql.connection.commit()
        except Exception as ex:
            print("Error al eliminar el producto específico del carrito:", ex)
            raise
        finally:
            cursor.close()

    @classmethod
    def clear_cart_for_user(cls, mysql, user_id):
        try:
            cursor = mysql.connection.cursor()
            # Elimina todos los elementos del carrito para el usuario especificado
            cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", (user_id,))
            mysql.connection.commit()
        except Exception as ex:
            print("Error al limpiar el carrito del usuario:", ex)
            raise
        finally:
            cursor.close()

    @classmethod
    def realizar_venta(cls, mysql,user_id ):
        try:
            # Conectar a la base de datos
            cursor = mysql.connection.cursor()
            payment_method_id="4"
            # Llamar al procedimiento almacenado
            cursor.callproc('realizar_venta', [user_id, payment_method_id])
           
        except Exception as e:
            # En caso de error, imprimir mensaje de error y revertir la transacción
            print("Error al realizar lsssa venta:", e)
            

        finally:
            # Cerrar la conexión a la base de datos
            cursor.close()
       


    @classmethod
    def get_cart_items(cls, mysql, user_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.callproc('GetCartItems', (user_id,))
            rows = cursor.fetchall()

            cart_items = []
            for row in rows:
                cart_item = CartItems(
                    cart_item_id=row[0],
                    user_id=row[1],
                    product_id=row[2],
                    quantity=row[3],
                    product_name=row[4],  # Nombre del producto
                    unit_price=row[5],     # Precio unitario del producto
                    image_url=row[6]       # URL de la imagen del producto
                )
                cart_items.append(cart_item)

            return cart_items
        except Exception as ex:
            print("Error al obtener elementos del carrito:", ex)
            raise
        finally:
            cursor.close()


