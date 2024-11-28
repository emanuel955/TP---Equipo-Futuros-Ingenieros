from flask import Flask, jsonify, request,render_template,url_for,redirect,flash,session
from mysql.connector import connect, Error
from datetime import datetime
import requests
API_URL = 'http://flask_api:8080/api/v1/'


app = Flask(__name__)
app.secret_key = "clave_ultra_secreta"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'usuario' not in session: 
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        else:
            hotel_id = request.form['hotel']
            fecha_entrada = request.form['fecha_entrada']
            fecha_salida = request.form['fecha_salida']

            hoy = datetime.today().date()
            fecha_entrada_date = datetime.strptime(fecha_entrada, '%Y-%m-%d').date()
            fecha_salida_date = datetime.strptime(fecha_salida, '%Y-%m-%d').date()


            if fecha_entrada_date < hoy:
                flash("The check-in date cannot be earlier than today.", 'error')
                return redirect(url_for('index'))

            # Validar la fecha de salida (no debe ser anterior a la fecha de entrada)
            if fecha_salida_date < fecha_entrada_date:
                flash("The check-out date cannot be earlier than the check-in date.", 'error')
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

        response = requests.get(API_URL+'servicios')
        response.raise_for_status()
        servicios = response.json()

    except Exception as e:
        print (f"Error fetching data: {e}")
        hoteles = []
        testimonios = []
        servicios = []

    return render_template('index.html', hoteles=hoteles, testimonios=testimonios, servicios=servicios)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if 'usuario' not in session: 
        flash('Please log in to continue.', 'error')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            usuario = session.get('usuario')
            id_usuario = usuario['id']

            fechas = session.get('fechas')
            fecha_entrada = fechas['fecha_entrada']
            fecha_salida = fechas['fecha_salida']

            id_habitacion = request.form.get('id_habitacion')
            precio_diario = request.form.get('precio_diario')
            datos = {'id_usuario': id_usuario,
                    'id_habitacion': id_habitacion,
                    'fecha_entrada': fecha_entrada,
                    'fecha_salida': fecha_salida,
                    'precio_diario': precio_diario
                    }
            try:
                response = requests.post(API_URL+'reservas/ingresar',json=datos)
                if response.status_code == 201:
                    flash("Reservation made successfully", 'success')
                    return redirect(url_for('index'))
                if response.status_code == 400:
                    flash("The reservation you are trying to make already exists.", 'error')
                    return redirect(url_for('index'))
            except requests.exceptions.RequestException as e:
                print (f"Error sending data: {e}")
        habitaciones = session.get('habitaciones', [])
            
        if not habitaciones:
            return redirect(url_for('index'))

    return render_template('rooms.html', habitaciones=habitaciones)

@app.route('/hotel/<string:nombre>')
def hotel_details(nombre):
    try:
        id = request.args.get('id')
        response = requests.get(API_URL+'hoteles/'+str(id))
        response.raise_for_status()
        hotel = response.json()

        response = requests.get(API_URL+'servicios')
        response.raise_for_status()
        servicios = response.json()
    except requests.exceptions.RequestException as e:
        print (f"Error fetching data: {e}")
        hotel = []
        servicios = []

    return render_template('hotel-details.html', hotel=hotel, servicios=servicios)

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reservas', methods=['GET','POST'])
def reservas():
    usuario = session.get('usuario')
    id_usuario = usuario['id']
    if request.method == 'POST':
        id = request.form.get('id')
        datos = {'id': id}
        try:
            response = requests.delete(API_URL+'reservas/borrar', json=datos)
            response.raise_for_status()
            if response.status_code == 200:
                flash("Reservation successfully canceled.", 'success')
            else:
                flash("Could not cancel the reservation.", 'error')
        except Exception as e:
            flash(f"Error canceling the reservation: {e}", 'error')
        redirect(url_for('reservas'))

    try:
        response = requests.get(API_URL+'reservas/'+str(id_usuario))
        response.raise_for_status()
        reservas = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        reservas = []
        
    return render_template('reservas.html', reservas=reservas)

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
                flash("Incorrect email or password.", 'error')
        except Exception as e:
            flash(f"Server connection error. {e}", 'error')

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
                flash("The email you entered is already registered. Please enter a different one.", 'error')
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
