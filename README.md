# Tienda Online - Proyecto-Unidad-IV

Este proyecto es una tienda online que incluye un sistema de inicio de sesión. A continuación, se proporciona una breve explicación del código relacionado con la página de inicio de sesión.

## Cómo Ejecutar el Proyecto
1. Entorno virtual, abrimos CMD como administrador y nos dirigimos a la carpeta donde se encuentra el proyecto y creamos el entorno virtual:

Crear un entorno virtual:
py -m venv env

Activar el entorno virtual:
env\Scripts\activate

Instalar Flask en el entorno virtual:
pip install Flask

2. Instala las dependencias del proyecto ejecutando `pip install Flask`,`pip install Flask_MySQL`,`pip install Flask-Login`,`pip install Flask_Mysqldb`,`Flask-WTF`,mysql-connector-python.

3. Nos dirigimos a donde este nuestro archivo python en este caso sera app.py .
Asignamos el archivo principal
set FLASK_APP=app.py

4. Ejecuta la aplicación con el comando `flask run.`.

5. Abre tu navegador y visita `http://127.0.0.1:5000` para acceder a la página.
