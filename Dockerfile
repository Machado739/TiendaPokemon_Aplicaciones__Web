# Utiliza una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al directorio de trabajo en el contenedor
COPY ./Proyecto/src /app

# Instala las dependencias del proyecto
RUN pip install Flask Flask_MySQL Flask-Login Flask_Mysqldb Flask-WTF mysql-connector-python

# Expone el puerto en el que la aplicación Flask escucha dentro del contenedor
EXPOSE 5000

# Define el comando para iniciar tu aplicación
CMD ["python", "app.py"]
