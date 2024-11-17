from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String

# class Base (DeclarationBase):
#     pass

Base = declarative_base()

class Hoteles(Base):
    __tablename__ = "hoteles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


engine = create_engine("mysql+mysqlconnector://flask_user:flaskpassword@mysql_db:3306/flask_database")

Base.metadata.create_all(engine)

with Session(engine) as session:
    hilton = Hoteles(name = "Hilton")

    session.add_all(hilton)
    session.commit()

