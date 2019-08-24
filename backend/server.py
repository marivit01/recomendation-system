#imports
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import pandas as pd
import numpy as np
# import os 

from keras.layers import Input, Dropout, Dense, Flatten, Activation, LSTM, Bidirectional, Concatenate
from keras.models import Model

# Para almacenar y obtener el modelo para predicciones futuras de un archivo .pkl.
from sklearn.externals import joblib

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__) 
api = Api(app)

CORS(app)

@app.route('/api/predict',methods=['POST']) #http://localhost:8081/api/predict
def predict():
    model = joblib.load(open('..datos/modelos/model2.pkl','rb'))
    data = request.get_json(force=True)
    output = model.predict([array_data_test, array_target_test])
    # output = prediction[0]
    print(output)
    return jsonify(output)

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)