from flask import Flask, jsonify, request,render_template,url_for # type: ignore
from sqlalchemy import create_engine, text # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session # type: ignore

app = Flask(__name__)
# Replace with your actual database credentials
username = 'root'  # MySQL username
password = 'Hoteles123'  # MySQL password
host = 'localhost'  # Database host (use '127.0.0.1' if 'localhost' doesn't work)
port = 3306         # MySQL port, default is 3306
database_name = 'hoteles_db'  # Name of your database

DATABASE_URL = f"mysql://{username}:{password}@{host}:{port}/{database_name}"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
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

@app.route('/registrarse')
def registrarse():
    return render_template('registro.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """Fetch all users"""
    try:
        session = Session()
        result = session.execute(text("SELECT * FROM usuarios")).fetchall()
        session.close()
        
        users = [{'id': row[0], 'username': row[1], 'password': row[2]} for row in result]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/reservations', methods=['GET'])
def get_all_reservations():
    """Fetch all reservations"""
    try:
        session = Session()
        result = session.execute(text("SELECT * FROM reservations")).fetchall()
        session.close()
        
        reservations = [{'reserva_num': row[0], 'user_id': row[1], 'check_in_date': row[2], 'check_out_date': row[3], 'room_type': row[4], 'total_cost': row[5]} for row in result]
        return jsonify(reservations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
