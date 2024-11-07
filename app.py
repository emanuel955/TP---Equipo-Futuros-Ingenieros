from flask import Flask, render_template,url_for

app = Flask(__name__)

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

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')

if __name__ == '__main__':
    app.run(debug=True)
