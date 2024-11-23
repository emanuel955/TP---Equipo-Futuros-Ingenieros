import querys as querys
from flask import Flask, jsonify, request, render_template,flash
import logging
import sys

# IMPRIMIR LOGS EN DOCKER (borrar en produccion)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)

@app.route('/api/v1/testimonios', methods=['GET'])
def get_all_testimonios():
    try:
        result = querys.all_testimonios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = []
    for row in result:
        response.append({'nombre': row[0], 'estrellas': row[1], 'resena': row[2]})
    
    return jsonify(response), 200

@app.route('/api/v1/hoteles', methods=['GET'])
def get_all_hoteles():
    try:
        result = querys.all_hoteles()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = []
    for row in result:
        response.append({'id':row[0], 'nombre':row[1]})
    
    return jsonify(response), 200

@app.route('/api/v1/hoteles/<int:id>', methods=['GET'])
def get_hotel_by_id(id):
    try:
        result = querys.hotel_by_id(id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = []
    for row in result:
        response.append({'id':row[0], 'nombre':row[1], 'descripcion':row[2], 'estrellas': row[3], 'servicios': row[4], 'ubicacion':row[5], 'latitud':row[6], 'longitud':row[7], 'imagen': row[8]})
    
    return jsonify(response), 200

@app.route('/api/v1/habitaciones-disponibles', methods=['POST'])
def get_habitaciones_disponibles():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se recibieron datos JSON válidos'}), 400

        hotel_id = datos.get('hotel_id')
        fecha_entrada = datos.get('fecha_entrada')
        fecha_salida = datos.get('fecha_salida')

        if not hotel_id or not fecha_entrada or not fecha_salida:
            return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

        # Verifica datos en logs (borrar en produccion)
        print(f"Hotel ID: {hotel_id}, Fecha Entrada: {fecha_entrada}, Fecha Salida: {fecha_salida}")

        result = querys.habitaciones_disponibles(hotel_id, fecha_entrada, fecha_salida)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    response = []

    if not result:
        response.append({'rooms': [], 'message': 'There are no rooms available for the hotel and date you selected.'})

    else:
        for row in result:
            response.append({'id': row[0], 'hotel_id': row[1], 'nombre': row[2], 'camas': row[3], 'precio_diario': row[4], 'imagen': row[5]})
    
    return jsonify(response), 200

@app.route('/api/v1/usuarios', methods=['GET'])
def get_usuario_by_mail(mail):
    try:
        result = querys.usuario_by_mail(mail)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = []
    for row in result:
        response.append({'id':row[0]})
    
    return jsonify(response), 200

@app.route('/api/v1/reservas/ingresar', methods=['POST'])
def ingresar_reserva():
    try:
        datos = request.get_json()
        querys.ingresar_reserva(datos)
    except Exception as e:
        return jsonify({"Error":str(e)}),400


@app.route('/api/v1/registrarse', methods=['POST'])
def registrarse():
    try:
        datos = request.get_json()
        mail = datos['mail']
        password = datos['password']
        nombre = datos['nombre']
        apellido = datos['apellido']

        usuario_existe = querys.usuario_existente({'mail': mail})
        if usuario_existe:
            return '', 400
        else:
            respuesta = querys.ingresar_usuario(datos)
            if respuesta == 201:
                return '', 201
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

@app.route('/api/v1/login', methods=['POST'])
def api_login():
    try:
        datos = request.get_json()
        mail = datos['mail']
        password = datos['password']
        credenciales = querys.existencia_credenciales(mail, password)
        if credenciales:
            return '', 201
        else:
            return jsonify({"Error": "Credenciales incorrectas"}), 400
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
