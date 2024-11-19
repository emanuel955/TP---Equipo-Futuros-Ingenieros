# Usa Python como imagen base
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /api

# Copia todos los archivos de la carpeta actual en el contenedor
COPY . /api

# Instala las dependencias del proyecto
RUN pip install flask mysql-connector-python
RUN pip install -U Flask-SQLAlchemy

# Expone el puerto 5000 para Flask 3600 para MySQL
EXPOSE 8081

# Comando para ejecutar Flask
CMD ["python", "app.py"]
