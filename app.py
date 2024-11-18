from flask import Flask, jsonify, request,render_template,url_for,redirect,flash,session
from mysql.connector import connect, Error
import requests
API_URL = 'http://flask_api:8080/api/v1/'


app = Flask(__name__)
app.secret_key = "clave_ultra_secreta"

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
    #if 'usuario' not in session:  
    #    flash('Por favor, inicia sesión para continuar.')
    #    return redirect(url_for('login'))
    #Usar para cuando se mande el POST request para ver la disponibilidad de los hoteles
    #Si no esta el usuario -> al login, de lo contrario se hace la request de POST
    try:
        response = requests.get(API_URL+'hoteles')
        response.raise_for_status()
        hoteles = response.json()

        #response = requests.get(API_URL+'testimonios')
        #response.raise_for_status()
        #testimonios = response.json()
        testimonios = []

    except requests.exceptions.RequestException as e:
        print (f"Error fetching data: {e}")
        hoteles = []
        testimonios = []
    return render_template('index.html', hoteles=hoteles, testimonios=testimonios)

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        datos = {'mail':mail,'password':password}

        try:
            usuario = requests.post(API_URL+'login',json=datos)
            if usuario.status_code == 201:
                session['usuario'] = mail
                return redirect(url_for('index'))
            else:
                flash('Correo o contraseña incorrectos.')
        except Exception as e:
            flash(f'Error de conexión al servidor: {e}')

    return render_template('login.html')

@app.route('/registrarse',methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        datos = {'mail': mail,
                 'password': password,
                 'nombre': nombre,
                 'apellido': apellido
                } 
        try:
            response = requests.post(API_URL+'registrarse',json=datos)
            if response.status_code == 201:
                return redirect(url_for('login'))
            if response.status_code == 400:
                flash("El email que ingreso ya esta registrado. Ingrese uno diferente.")
                return render_template('registro.html',mail = mail,nombre = nombre,apellido = apellido)

        except requests.exceptions.RequestException as e:
            print (f"Error sending data: {e}")
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None) 
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
