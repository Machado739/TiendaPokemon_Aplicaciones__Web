import mysql.connector

class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306  # Puerto por defecto de MySQL
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_DB = "bd_tiendapokemon"

config = {
    "development": DevelopmentConfig
}

# Obtén la configuración específica para el entorno de desarrollo
config_dev = config["development"]

# Construye la cadena de conexión según la configuración
conn_str = {
    'host': config_dev.MYSQL_HOST,
    'port': config_dev.MYSQL_PORT,  # Agrega el puerto aquí
    'user': config_dev.MYSQL_USER,
    'password': config_dev.MYSQL_PASSWORD,
    'database': config_dev.MYSQL_DB,
    'raise_on_warnings': True
}

# Intenta establecer la conexión
try:
    connection = mysql.connector.connect(**conn_str)
    print("Conexión exitosa.")
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")

