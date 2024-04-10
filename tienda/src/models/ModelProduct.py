from models.entities.inventory import Inventory

class Product:
    def __init__(self, id, name, price, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url


class ModelProducts:
    @classmethod
    def add_product(cls, mysql, product, cantidad):
        try:
            cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado para agregar el producto con inventario
            cursor.callproc('añadir_producto_con_inventario', (product.name, product.price, product.image_url, cantidad))

            mysql.connection.commit()

            # Obtener el ID del producto recién insertado
            cursor.execute("SELECT 'Producto añadido y asignado inventario exitosamente' AS message")
            result = cursor.fetchone()

            

            return Product(id=None, name=product.name, price=product.price, image_url=product.image_url)
        except Exception as ex:
            print("Error al agregar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()


    @classmethod
    def get_all_products(cls, mysql,category_id):
        try:
            cursor = mysql.connection.cursor()
            if category_id == 0:
                cursor.execute("""
                    SELECT products.id, products.name, products.price, products.image_url, inventory.quantity 
                    FROM products 
                    INNER JOIN inventory ON products.id = inventory.product_id 
                    INNER JOIN product_categories ON products.id = product_categories.product_id
                """)
            else:
                cursor.execute("""
                    SELECT products.id, products.name, products.price, products.image_url, inventory.quantity 
                    FROM products 
                    INNER JOIN inventory ON products.id = inventory.product_id 
                    INNER JOIN product_categories ON products.id = product_categories.product_id 
                    WHERE product_categories.category_id = %s
                """, (category_id,))
        
            
            rows = cursor.fetchall()

            products = []
            for row in rows:
                product = Product(id=row[0], name=row[1], price=row[2], image_url=row[3])
                inventory = Inventory(product_id=row[0], quantity=row[4])
                product.inventory = inventory  # Asignar el objeto de inventario al producto
                products.append(product)

            return products
        except Exception as ex:
            print("Error al obtener los productos por categoría:", ex)
            raise Exception(ex)
        finally:
            cursor.close()


    @classmethod
    def delete_product(cls, mysql, product_id):
        try:
            cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado para borrar el producto
            cursor.callproc('borrar_producto_inventario', (product_id,))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
        except Exception as ex:
            print("Error al borrar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def update_product(cls, mysql, product,quantity):
        try:
            cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado para actualizar el producto
            cursor.callproc('modificar_producto', (product.id, product.name, product.price, product.image_url, quantity))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
        except Exception as ex:
            print("Error al actualizar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @staticmethod
    def assign_category(mysql, product_id, category_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO product_categories (product_id, category_id) VALUES (%s, %s)", (product_id, category_id))
            mysql.connection.commit()
            return True
        except Exception as ex:
            print("Error al asignar categoría al producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @staticmethod
    def update_category(mysql, product_id, new_category_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE product_categories SET category_id = %s WHERE product_id = %s", (new_category_id, product_id))
            mysql.connection.commit()
            return True
        except Exception as ex:
            print("Error al modificar categoría del producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
    @staticmethod
    def add_product_with_inventory_and_category(mysql, product_name, price, image_url, quantity, category_id):
        try:
            cursor = mysql.connection.cursor()

            # Llamar al procedimiento almacenado para agregar el producto con inventario y categoría
            cursor.callproc('añadir_producto_con_inventario_y_categoria', (product_name, price, image_url, quantity, category_id))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()

            # Obtener el mensaje de éxito del procedimiento almacenado
            result = cursor.fetchone()
            if result:
                print(result['message'])
                return True
        except Exception as ex:
            print("Error al agregar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

