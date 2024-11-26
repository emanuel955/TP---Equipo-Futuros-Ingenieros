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
LEFT JOIN Reservas ON Reservas.id_habitacion = Habitaciones.id
    AND (
        (Reservas.fecha_entrada <= :fecha_salida AND Reservas.fecha_salida > :fecha_entrada)
    )
WHERE Habitaciones.hotel_id = :hotel_id
    AND Reservas.id_habitacion IS NULL;
"""
QUERY_RESERVA_EXISTENTE = "SELECT id FROM Reservas WHERE id_usuario = :id_usuario AND id_habitacion = :id_habitacion AND fecha_entrada = :fecha_entrada AND fecha_salida = :fecha_salida"
QUERY_INGRESAR_RESERVA = "INSERT INTO Reservas(id_usuario, id_habitacion, fecha_entrada, fecha_salida, precio_diario) VALUES (:id_usuario, :id_habitacion, :fecha_entrada, :fecha_salida, :precio_diario)"
QUERY_RESERVAS_BY_ID = "SELECT * FROM Reservas WHERE id_usuario = :id_usuario"
QUERY_BORRAR_RESERVA = "DELETE FROM Reservas WHERE id = :id;"
QUERY_INGRESAR_RESERVA_SERVICIOS = "INSERT INTO Reservas_Servicios(id_reserva) VALUES (:id_reserva)"
QUERY_LAST_ID = "SELECT LAST_INSERT_ID()"
QUERY_SERVICIOS_POR_RESERVA = "SELECT masaje, rio, desayuno FROM Reservas_Servicios WHERE id_reserva = :id_reserva"

engine = create_engine("mysql+mysqlconnector://root:BbiRlotkloMAGIUDbxnkuJzoVBPqzhtY@mysql.railway.internal:3306/railway")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
        if query == QUERY_INGRESAR_RESERVA:
            ultimo_id = conn.execute(text(QUERY_LAST_ID)).scalar()
            conn.close()
            return ultimo_id
    conn.close()
    return result

def all_testimonios():
    return run_query(QUERY_TODOS_LOS_TESTIMONIOS).fetchall()

def all_hoteles():
    return run_query(QUERY_TODOS_LOS_HOTELES).fetchall()

def hotel_by_id(id):
    return run_query(QUERY_HOTEL_BY_ID, {'id': id}).fetchall()

def habitaciones_disponibles(datos):
    resultado = run_query(QUERY_HABITACIONES_DISPONIBLES, datos).fetchall()
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
    
def reserva_existente(datos):
    resultado = run_query(QUERY_RESERVA_EXISTENTE, datos).fetchone()
    return resultado

def ingresar_reserva(datos):
    try:
        reserva_id = run_query(QUERY_INGRESAR_RESERVA, datos)
        return reserva_id
    except Exception as e:
        print(f"Error al agregar reserva: {e}")
        return None

def ingresar_reserva_servicios(datos):
    try:
        run_query(QUERY_INGRESAR_RESERVA_SERVICIOS, datos)
        return 201
    except Exception as e:
        print(f"Error al agregar reserva: {e}")
        return 400
    
def reservas_by_id_usuario(id_usuario):
    return run_query(QUERY_RESERVAS_BY_ID, {'id_usuario': id_usuario}).fetchall()

def delete_reserva(id):
    return run_query(QUERY_BORRAR_RESERVA, {'id': id})

def servicios_by_id_reserva(id_reserva):
    return run_query(QUERY_SERVICIOS_POR_RESERVA, {'id_reserva': id_reserva}).fetchone()
