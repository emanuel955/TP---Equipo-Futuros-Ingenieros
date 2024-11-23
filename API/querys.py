from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_TODOS_LOS_TESTIMONIOS = "SELECT nombre, estrellas, resena FROM Testimonios"
QUERY_TODOS_LOS_HOTELES = "SELECT id, nombre FROM Hoteles"
QUERY_HOTEL_BY_ID = "SELECT * FROM Hoteles WHERE id = :id"
QUERY_USUARIO_BY_MAIL = "SELECT id FROM Usuarios WHERE mail = :mail"
QUERY_USUARIO_EXISTENTE = "SELECT mail FROM Usuarios WHERE mail = :mail "
QUERY_INGRESAR_USUARIO = "INSERT INTO Usuarios(mail,password,nombre,apellido) VALUES (:mail,:password,:nombre,:apellido)"
QUERY_LOGEAR_USUARIO = "SELECT * FROM Usuarios WHERE mail = :mail AND password = :password"
QUERY_HABITACIONES_DISPONIBLES = """
SELECT
    Habitaciones.id,
    Habitaciones.hotel_id,
    Habitaciones.nombre,
    Habitaciones.camas,
    Habitaciones.precio_diario,
    Habitaciones.imagen
FROM Habitaciones
LEFT JOIN Reservas ON Reservas.id = Habitaciones.id
    AND (
        (Reservas.fecha_entrada <= :fecha_salida AND Reservas.fecha_salida > :fecha_entrada) OR
        (Reservas.fecha_entrada < :fecha_salida AND Reservas.fecha_salida >= :fecha_entrada) OR
        (Reservas.fecha_entrada >= :fecha_entrada AND Reservas.fecha_salida <= :fecha_salida)
    )
WHERE Habitaciones.hotel_id = :hotel_id
    AND Reservas.id IS NULL;
"""
QUERY_INGRESAR_RESERVA = "INSERT INTO Reservas(id_usuario, id_habitacion, fecha_entrada, fecha_salida) VALUES (:id_usuario, :id_habitacion, :fecha_entrada, :fecha_salida)"

engine = create_engine("mysql+mysqlconnector://flask_user:flask_password@mysql_db:3306/flask_database")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    conn.close()
    return result

def all_testimonios():
    return run_query(QUERY_TODOS_LOS_TESTIMONIOS).fetchall()

def all_hoteles():
    return run_query(QUERY_TODOS_LOS_HOTELES).fetchall()

def hotel_by_id(id):
    return run_query(QUERY_HOTEL_BY_ID, {'id': id}).fetchall()

def habitaciones_disponibles(hotel_id, fecha_entrada, fecha_salida):
    resultado = run_query(QUERY_HABITACIONES_DISPONIBLES, {'hotel_id': hotel_id, 'fecha_entrada': fecha_entrada, 'fecha_salida': fecha_salida}).fetchall()
    return resultado
    
def usuario_by_mail(mail):
    return run_query(QUERY_USUARIO_BY_MAIL, {'mail': mail}).fetchall()

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

def ingresar_reserva(datos):
    try:
        run_query(QUERY_INGRESAR_RESERVA, datos)
        return 201
    except Exception as e:
        print(f"Error al agregar al usuario: {e}")
        return 400