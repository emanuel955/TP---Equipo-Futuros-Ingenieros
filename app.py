from flask import Flask, jsonify, request,render_template,url_for,redirect,flash,session
from mysql.connector import connect, Error
from datetime import datetime
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'usuario' not in session: 
            flash('Por favor, inicia sesión para continuar.')
            return redirect(url_for('login'))
        else:
            hotel_id = request.form['hotel']
            fecha_entrada = request.form['fecha_entrada']
            fecha_salida = request.form['fecha_salida']

            hoy = datetime.today().date()
            fecha_entrada_date = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
            fecha_salida_date = datetime.strptime(fecha_salida, '%Y-%m-%d').date()


            if fecha_entrada_date < hoy:
                flash('La fecha de entrada no puede ser anterior a hoy.')
                return redirect(url_for('index'))

            # Validar la fecha de salida (no debe ser anterior a la fecha de entrada)
            if fecha_salida_date < fecha_entrada_date:
                flash('La fecha de salida no puede ser anterior a la fecha de entrada.')
                return redirect(url_for('index'))

            try:
                datos = {'hotel_id':hotel_id,
                        'fecha_entrada':fecha_entrada,
                        'fecha_salida':fecha_salida
                        }
                response = requests.post(API_URL+'habitaciones-disponibles', json=datos)
                response.raise_for_status()
                habitaciones = response.json()
                session['fechas']={'fecha_entrada': fecha_entrada, 'fecha_salida': fecha_salida}
                session['habitaciones']=habitaciones
                return redirect(url_for('rooms'))
            except Exception as e:
                print (f"Error sending data: {e}")
                return render_template('index.html')

    try:
        response = requests.get(API_URL+'hoteles')
        response.raise_for_status()
        hoteles = response.json()

        response = requests.get(API_URL+'testimonios')
        response.raise_for_status()
        testimonios = response.json()

    except Exception as e:
        print (f"Error fetching data: {e}")
        hoteles = []
        testimonios = []
    return render_template('index.html', hoteles=hoteles, testimonios=testimonios)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if 'usuario' not in session: 
        flash('Por favor, inicia sesión para continuar.')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            usuario = session.get('usuario')
            id_usuario = usuario['id']

            fechas = session.get('fechas')
            fecha_entrada = fechas['fecha_entrada']
            fecha_salida = fechas['fecha_salida']

            id_habitacion = request.form.get('id_habitacion')
            datos = {'id_usuario': id_usuario,
                    'id_habitacion': id_habitacion,
                    'fecha_entrada': fecha_entrada,
                    'fecha_salida': fecha_salida
                    }
            try:
                response = requests.post(API_URL+'reservas/ingresar',json=datos)
                if response.status_code == 201:
                    return redirect(url_for('index'))
                if response.status_code == 400:
                    flash("The reservation you are trying to make already exists.")
                    return redirect(url_for('index'))
            except requests.exceptions.RequestException as e:
                print (f"Error sending data: {e}")
        habitaciones = session.get('habitaciones', [])
            
        if not habitaciones:
            return redirect(url_for('index'))

    return render_template('rooms.html', habitaciones=habitaciones)

@app.route('/hotel/<int:id>')
def hotel_details(id):
    try:
        response = requests.get(API_URL+'hoteles/'+str(id))
        response.raise_for_status()
        hotel = response.json()
    except requests.exceptions.RequestException as e:
        print (f"Error fetching data: {e}")
        hotel = []
    return render_template('hotel-details.html', hotel=hotel)

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
                try:
                    response = requests.get(API_URL+'usuarios', json={'mail':mail})
                    response.raise_for_status()
                    id = response.json()
                except Exception as e:
                    print (f"Error fetching data: {e}")
                    id = []
                usuario = {'mail': mail, 'id': id[0]['id']}
                session['usuario'] = usuario
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
