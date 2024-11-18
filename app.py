from flask import Flask, jsonify, request,render_template,url_for,redirect,flash,session
from mysql.connector import connect, Error

app = Flask(__name__)

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

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')
        try:
            conn = Session()
            usuario = conn.execute(text(QUERY_LOGIN_USUARIO),{'mail': mail,'password': password},).first()
            if usuario:
                session['user'] = mail
                return render_template('index.html')
            else:
                flash("The email or the password is incorrect, try again.")
                return render_template('login.html')
        except Exception as e:
            return str(e),500
        finally:
            conn.close()
    else:
        return render_template('login.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/registrarse',methods=['POST', 'GET'])
def registrarse():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        try:
            conn = Session()
            usuario_existente = conn.execute(text(QUERY_MAIL_REPETIDO),{'mail': mail}).first()
            if usuario_existente:
                flash("The email is already registered. Please use a different one.")
                return render_template('registro.html',mail=mail,nombre=nombre,apellido=apellido) 
        except Exception as e:
            return str(e)
        finally:
            conn.close()
        
        nuevo_usuario = Usuario(mail=mail, password=password, nombre=nombre, apellido=apellido)

        try:
            conn = Session()
            conn.execute(text(QUERY_INGRESAR_USUARIO),{'mail':nuevo_usuario.mail,'password':nuevo_usuario.password,'nombre':nuevo_usuario.nombre,'apellido':nuevo_usuario.apellido})
            conn.commit()
        except Exception as e:
            return str(e)
        finally:
            conn.close()
        
        return redirect('/login')
            
    else:
        return render_template('registro.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/logout')
def logout():
    session.pop('user', None) 
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
