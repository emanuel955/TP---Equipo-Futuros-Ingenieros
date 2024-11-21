from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_TODOS_LOS_TESTIMONIOS = "SELECT nombre, estrellas, resena FROM testimonios"
QUERY_TODOS_LOS_HOTELES = "SELECT name_hotel from Hoteles"
QUERY_USUARIO_EXISTENTE = "SELECT mail FROM Usuarios WHERE mail = :mail "
QUERY_INGRESAR_USUARIO = "INSERT INTO Usuarios(mail,password,nombre,apellido) VALUES (:mail,:password,:nombre,:apellido)"
QUERY_LOGEAR_USUARIO = "SELECT * FROM Usuarios WHERE mail = :mail AND password = :password"
QUERY_TODAS_LAS_HABITACIONES = "SELECT id, hotel_id, nombre, camas, precio_diario, imagen, caracteristicas, disponibilidad FROM Habitaciones WHERE disponibilidad = TRUE"


engine = create_engine("mysql+mysqlconnector://flask_user:flask_password@mysql_db:3306/flask_database")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    
    return result

def all_testimonios():
    return run_query(QUERY_TODOS_LOS_TESTIMONIOS).fetchall()

def all_hoteles():
    return run_query(QUERY_TODOS_LOS_HOTELES).fetchall()

def usuario_existente(datos):
    resultado = run_query(QUERY_USUARIO_EXISTENTE,{'mail':datos['mail']}).fetchone()
    return resultado

def ingresar_usuario(datos):
    try:
        run_query(QUERY_INGRESAR_USUARIO,datos)
        return 201
    except Exception as e:
        print(f"Error al agregar al usuario: {e}")
        return 400

def existencia_credenciales(mail,password):
    try:
        return run_query(QUERY_LOGEAR_USUARIO,{'mail':mail,'password':password}).fetchone() 
    except Exception as e:
        print(f"Error al intentar iniciar sesion: {e}")
        return None

def todas_habitaciones():
    try:
        return run_query(QUERY_TODAS_LAS_HABITACIONES).fetchall()
    except Exception as e:
        print(f"Error al obtener las habitaciones: {e}")
        return None

