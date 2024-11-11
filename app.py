from flask import Flask, render_template, request,  url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms.html')
def rooms():
    return render_template('rooms.html')

@app.route('/about-us.html')
def aboutus():
    return render_template('about-us.html')

if __name__ == '__main__':
    app.run(debug=True)
