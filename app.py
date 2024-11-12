from flask import Flask, jsonify, request,render_template,url_for,redirect,flash,session
from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker, scoped_session 
from flask_sqlalchemy import SQLAlchemy



#No se crear una base de datos global siendo que el codigo es local,lo que hice fue: descargar SQL + SQLworkbench
#Despues crear un usuario con nombre root,contraseña Hoteles123 y cuando se crea la base de datos con nombre Hoteles
#Todos esos datos van aca abajo en el DATABASE_URI -> root es el usuario -> Hoteles123 es la password -> /Hoteles el nombre de la base de datos
#Hay que darle connect a la base de datos y ya nos podemos conectar
#La clase usuario crea la tabla usuario, de querer crear otra tabla, hacerla antes de with app.app_context():
#                                                                                         db.create_all()
DATABASE_URI = 'mysql://root:Hoteles123@localhost/Hoteles'  
QUERY_MAIL_REPETIDO = "SELECT mail FROM usuarios WHERE mail = :mail"
QUERY_INGRESAR_USUARIO = "INSERT INTO usuarios (mail,password,nombre,apellido) VALUES (:mail,:password,:nombre,:apellido)"
QUERY_LOGIN_USUARIO = "SELECT mail FROM usuarios WHERE mail = :mail and password = :password"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'llave_secreta' 

db = SQLAlchemy(app)
class Usuario(db.Model):
    __tablename__ = 'Usuarios'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.mail}>'
    
with app.app_context():
    db.create_all()

engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

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
