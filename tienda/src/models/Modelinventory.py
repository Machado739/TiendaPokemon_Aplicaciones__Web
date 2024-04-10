class Inventory:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

class ModelInventory:
    @classmethod
    def replenish_inventory(cls, db, product_id, quantity):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para reponer el inventario
            cursor.callproc('reponer_inventario', (product_id, quantity))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al reponer el inventario:", ex)
            raise Exception(ex)

    @classmethod
    def add_product_with_inventory(cls, db, name, price, image_url, quantity):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para agregar un producto con inventario
            cursor.callproc('añadir_producto_con_inventario', (name, price, image_url, quantity))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al agregar un producto con inventario:", ex)
            raise Exception(ex)
    @classmethod
    def delete_product_from_inventory(cls, db, product_id):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para borrar el producto del inventario
            cursor.callproc('borrar_producto_inventario', (product_id,))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al borrar producto del inventario:", ex)
            raise Exception(ex)