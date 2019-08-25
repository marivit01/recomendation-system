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

import os.path

import sys

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__) 
api = Api(app)

CORS(app)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

@app.route('/api/predict',methods=['POST']) #http://localhost:8081/api/predict
def predict():
    #Esto será sustituido por los parametros que se pasará. Se supone debe preprocesarse la data
    dataTestPath = os.path.abspath('..\\recomendation-system\\datos\modelos\\array_data_df.npy')
    targetTestPath = os.path.abspath('..\\recomendation-system\\datos\modelos\\array_target_df.npy')
    array_data_test = np.load(dataTestPath)
    array_target_test = np.load(targetTestPath)

    print("array", array_data_test.shape, array_target_test.shape, file=sys.stderr)

    modelPath = os.path.abspath('..\\recomendation-system\\datos\modelos\\model2.pkl')
    model = joblib.load(open(modelPath,'rb'))
    print('model', file=sys.stderr)
    print('modellll',model.summary(), file=sys.stderr)
    # data = request.get_json(force=True)
    output = model.predict([array_data_test, array_target_test])
    # output = prediction[0]
    print(output, file=sys.stderr)
    return jsonify(output.tolist())

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)