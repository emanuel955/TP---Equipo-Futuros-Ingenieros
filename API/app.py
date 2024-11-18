import querys as querys
from flask import Flask, jsonify, request, render_template

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

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug=True)
