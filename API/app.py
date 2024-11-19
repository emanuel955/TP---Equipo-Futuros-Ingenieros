
from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
# import requests
# import requests
import querys as querys


app = Flask(__name__)

@app.route('/api/v1/testimonios', methods=['GET'])
def get_all_testimonios():
    try:
        result = querys.all_testimonion()
    except Exception as e:
        return jsonify({'error_ema': str(e)}),500
    # response=[]
    # for reo in result:
    #     response.append({'nombre':row})
    return jsonify(result),200


@app.route('/api/v1/hoteles', methods=['GET'])
def hoteles():
    responseb=[]
    try:
        response = querys.Select_hoteles_all()
    except Exception as e:
        return jsonify({'error_ema': str(e)}),500

    for row in response:
        responseb.append({'id':row[0],'name':row[1]})

    print(f"emma_t{responseb}")
    return jsonify(responseb),200


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8081, debug=True)
