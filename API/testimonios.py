from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

QUERY_TODOS_LOS_TESTIMONIOS = "SELECT nombre, estrellas, resena FROM testimonios"

engine = create_engine("mysql+mysqlconnector://flask_user:flask_password@mysql_db:3306/flask_database")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()
    
    return result

def all_testimonios():
    return run_query(QUERY_TODOS_LOS_TESTIMONIOS).fetchall()