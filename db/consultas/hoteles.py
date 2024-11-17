from db.models import Hoteles
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import select

def Select_hoteles_all():
    engine = create_engine("mysql+mysqlconnector://flask_user:flaskpassword@mysql_db:3306/flask_database")
    sesion_hoteles = Session(engine)
    stmt = select(Hoteles)
    return sesion_hoteles.scalars(stmt)

