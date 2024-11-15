# Usa Python como imagen base
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /api

# Copia todos los archivos de la carpeta actual en el contenedor
COPY . /api

# Instala las dependencias del proyecto
RUN pip install flask mysql-connector-python
RUN pip install -U Flask-SQLAlchemy

# Expone el puerto 8080 para Flask
EXPOSE 8080

# Comando para ejecutar Flask
CMD ["python", "app.py"]
