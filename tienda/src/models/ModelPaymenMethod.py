from entities.paymentMethod import PaymentMethod

class ModelPaymentMethod:
    @classmethod
    def add_payment_method(cls, db, payment_method):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para agregar el método de pago
            cursor.callproc('agregar_metodo_pago', (payment_method.user_id, payment_method.payment_type, payment_method.card_number, payment_method.expiration_date, payment_method.cvv))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al agregar método de pago:", ex)
            raise Exception(ex)

    @classmethod
    def update_payment_method(cls, db, payment_method):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para actualizar el método de pago
            cursor.callproc('modificar_metodo_pago', (payment_method.id, payment_method.payment_type, payment_method.card_number, payment_method.expiration_date, payment_method.cvv))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al actualizar método de pago:", ex)
            raise Exception(ex)

    @classmethod
    def delete_payment_method(cls, db, payment_method_id):
        try:
            cursor = db.connection.cursor()

            # Llamar al procedimiento almacenado para borrar el método de pago
            cursor.callproc('borrar_metodo_pago', (payment_method_id,))

            # Confirmar los cambios en la base de datos
            db.connection.commit()

            # Cerrar el cursor
            cursor.close()

        except Exception as ex:
            print("Error al borrar método de pago:", ex)
            raise Exception(ex)
    @classmethod
    def get_user_payment_method(cls, db, user_id):
        try:
            cursor = db.connection.cursor()

            # Obtener el método de pago del usuario
            cursor.execute("SELECT id, user_id, payment_type, card_number, expiration_date, cvv FROM payment_methods WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()

            if row:
                # Si hay un método de pago registrado para el usuario, devolverlo como objeto PaymentMethod
                payment_method = PaymentMethod(row[0], row[1], row[2], row[3], row[4], row[5])
                return payment_method
            else:
                # Si no hay método de pago registrado para el usuario, devolver None
                return None

        except Exception as ex:
            print("Error al obtener método de pago del usuario:", ex)
            raise Exception(ex)

        finally:
            cursor.close()