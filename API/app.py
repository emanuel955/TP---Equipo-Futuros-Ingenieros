import querys as querys
from flask import Flask, jsonify, request, render_template,flash

app = Flask(__name__)

@app.route('/api/v1/testimonios', methods=['GET'])
def get_all_testimonios():
    try:
        result = querys.all_testimonios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = []
    for row in result:
        response.append({'nombre':row[0], 'estrellas': row[1], 'resena': row[2]})
    
    return jsonify(response), 200

@app.route('/api/v1/hoteles', methods=['GET'])
def get_all_hoteles():
    try:
        result = querys.all_hoteles()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    print (result)
    response = []
    for row in result:
        response.append({'name_hotel':row[0]})
    
    return jsonify(response), 200

@app.route('/api/v1/registrarse',methods=['POST'])
def registrarse():
    try:
        datos = request.get_json()
        mail = datos['mail']
        password = datos['password']
        nombre = datos['nombre']
        apellido = datos['apellido']

        usuario_existe = querys.usuario_existente({'mail':mail})
        if usuario_existe:
            return '',400
        else:
            respuesta = querys.ingresar_usuario(datos)
            if respuesta == 201:
                return '',201
            
    except Exception as e:
        return jsonify({"Error":str(e)}),400

@app.route('/api/v1/login',methods=['POST'])
def api_login():
    try:
        datos = request.get_json()
        mail = datos['mail']
        password = datos['password']
        credenciales = querys.existencia_credenciales(mail,password)
        if credenciales:
            return '',201
        else:
            return jsonify({"Error": "Credenciales incorrectas"}), 400
    except Exception as e:
        return jsonify({"Error":str(e)}),400
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug=True)
