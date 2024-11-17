from hashlib import new
from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
import requests
# import requests
from db import models
from db.consultas.hoteles import Select_hoteles_all
from mysql.connector import connect, Error

app = Flask(__name__)
API_URL = 'http://flask_api:8080/api/v1/'
# Configuración para conectar a MySQL
app.config['MYSQL_HOST'] = 'mysql_db'  # Nombre del servicio MySQL en Docker Compose
app.config['MYSQL_USER'] = 'flask_user'  # Usuario configurado en docker-compose.yml
app.config['MYSQL_PASSWORD'] = 'flask_password'  # Contraseña del usuario de MySQL
app.config['MYSQL_DATABASE'] = 'flask_database'  # Base de datos que usará la aplicación

# Conexión a la base de datos
def get_db_connection():
    try:
        connection = connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )
        return connection
    except Error as e:
        print("Error de conexión:", e)
        return None
    
@app.route('/test_db')
def test_db():
    connection = get_db_connection()
    if connection:
        return "Conexión a la base de datos MySQL exitosa"
    else:
        return "Error al conectar a la base de datos MySQL"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/hoteles')
def hoteles():
    models.Hoteles()
    response = Select_hoteles_all()
    return render_template('hoteles.html',response=response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
