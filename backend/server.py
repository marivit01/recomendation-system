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
from keras import backend as K

# Para almacenar y obtener el modelo para predicciones futuras de un archivo .pkl.
from sklearn.externals import joblib

import os.path

import sys

from adaptx import adaptX # For model 2
from adaptx import adaptXModel3 # For model 3
from getAssigns import getAvailableSubjects
from adapty import adapty # For model 2
from adapty import adaptYModel3 # For model 3

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__) 
api = Api(app)

CORS(app, support_credentials=True)

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

# Función que regresa una lista de los códigos y nombres de las asignaturas que el estudiante no ha visto
@app.route('/api/getSubjects/<studentId>',methods=['POST'])
def getSubjectsCall(studentId):
    return jsonify(getAvailableSubjects(studentId)) 

@app.route('/api/predict-model-2/<studentId>',methods=['POST']) #http://localhost:8081/api/predict
def predictModel2(studentId):

    #Before prediction
    K.clear_session()

    targetTrim =  request.get_json(force=True)
    print("TARGET:",targetTrim)
    array_target_test = adapty(targetTrim)
    array_data_test = adaptX(studentId)
    print("DATA X:", array_data_test)

    print("array", array_data_test.shape, array_target_test.shape, file=sys.stderr)

    modelPath = os.path.abspath('..\\datos\modelos\\model2.pkl')
    model = joblib.load(open(modelPath,'rb'))

    output = model.predict([array_data_test, array_target_test])
    print(output, file=sys.stderr)

    #After prediction
    K.clear_session()
    return jsonify(output.tolist())

@app.route('/api/predict-model-3/<studentId>',methods=['POST']) #http://localhost:8081/api/predict
def predictModel3(studentId):

    #Before prediction
    K.clear_session()

    targetTrim = request.get_json(force=True) #subjects.split(',')
    print("TARGET:",targetTrim)
    array_target_test = adaptYModel3(targetTrim)
    array_data_test = adaptXModel3(studentId)
    print("DATA X:", array_data_test)

    print("array", array_data_test.shape, array_target_test.shape, file=sys.stderr)

    modelPath = os.path.abspath('..\\datos\modelos\\model3.pkl')
    model = joblib.load(open(modelPath,'rb'))

    output = model.predict([array_data_test, array_target_test])
    print(output, file=sys.stderr)

    #After prediction
    K.clear_session()
    return jsonify(output.tolist())

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)