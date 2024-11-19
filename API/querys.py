from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine("mysql+mysqlconnector://flask_user:flask_password@mysql_db:3306/flask_database")

def run_query(query,parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query),parameters)
        conn.commit

    return result

def all_testimonios():
    return run_query("select nombre,estrellas,resena from testimonions")

def Select_hoteles_all():
    return run_query("select * from Hoteles")