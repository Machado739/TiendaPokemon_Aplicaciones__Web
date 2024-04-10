from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id, username, password, fullname, usertype):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.usertype = usertype


class ModelUsers:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
            row = cursor.fetchone()
            if row:
                logged_user = User(row[0], row[1], row[2], row[3], row[4])
                return logged_user
            else:
                return None
        except Exception as ex:
            print("Error en el modelo de usuarios:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
    @classmethod
    def get_by_id(cls, mysql, id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, username, usertype, fullname FROM users WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], '', row[3], row[2])
                return user
            else:
                return None
        except Exception as ex:
            print("Error al obtener usuario por ID:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @staticmethod
    def add_user(mysql,nuevo_producto):
        try:
            cursor =  mysql.connection.cursor()

            # Llamar al procedimiento almacenado para agregar el usuario
            cursor.callproc('agregar_usuario', (nuevo_producto.username, nuevo_producto.password, nuevo_producto.fullname, nuevo_producto.usertype))

            # Obtener el resultado del procedimiento almacenado
            result = cursor.fetchone()
          

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()

            return User(id=None,username=nuevo_producto.username,password=nuevo_producto.password,fullname=nuevo_producto.fullname,usertype=nuevo_producto.usertype)
        except Exception as ex:
            print("Error al agregar producto:", ex)
            raise Exception(ex)
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()


    def get_all_users(mysql):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, username, fullname, usertype FROM users")
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = User(row[0], row[1], '', row[2], row[3])
                users.append(user)

            return users
        except Exception as ex:
            print("Error al obtener todos los usuarios:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
            
    @staticmethod
    def update_user(mysql, user):
        try:
            cursor = mysql.connection.cursor()

            # Actualizar el usuario en la tabla 'users'
            cursor.execute("UPDATE users SET username = %s, fullname = %s, usertype = %s WHERE id = %s", (user.username, user.fullname, user.usertype, user.id))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
        except Exception as e:
            # Manejar el error, si es necesario
            raise e
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()

    @staticmethod
    def delete_user(mysql, user_id):
        try:
            cursor = mysql.connection.cursor()

            # Eliminar el usuario de la tabla 'users'
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
        except Exception as e:
            # Manejar el error, si es necesario
            raise e
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()

