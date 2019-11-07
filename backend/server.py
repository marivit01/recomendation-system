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

from adaptx import adaptX, adaptX_test # For model 2 an 3
from getAssigns import getAvailableSubjects, getAvailableSubjects_test, createCombinations
from adapty import adapty, adaptYModel5 # For model 2, 3 and 4

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

    # UNCOMMENT THE NEXT LINE TO USE THE STUDENTS IN TEST SET
    # return jsonify(getAvailableSubjects_test(studentId))

# Función que regresa todas las combinaciones de materias posibles para un estudiante especifico
@app.route('/api/getCombinations/<assignsNumber>',methods=['POST'])
def getCombinationsCall(assignsNumber):
    data = request.get_json(force=True)
    # print('data for combinations', data, data.get('availables'))
    return jsonify(createCombinations(data.get('availables'), data.get('preselected'), assignsNumber).tolist()) 


@app.route('/api/predict-model-2/<studentId>',methods=['POST']) #http://localhost:8081/api/predict
def predictModel2(studentId):

    #Before prediction
    K.clear_session()

    targetTrim = request.get_json(force=True)
    print("TARGET:",targetTrim)
    array_target_test = adapty(targetTrim)
    array_data_test = adaptX(studentId)
    print("DATA X:", array_data_test, len(array_data_test))

    print("array", array_data_test.shape, array_target_test.shape, file=sys.stderr)

    modelPath = os.path.abspath('..\\datos\ordenados\\model2.pkl')
    model = joblib.load(open(modelPath,'rb'))

    output = model.predict([array_data_test, array_target_test])
    print(output, file=sys.stderr)

    #After prediction
    K.clear_session()
    return jsonify(output.tolist())

@app.route('/api/predict-model/<studentId>',methods=['POST']) #http://localhost:8081/api/predict
def predictModel(studentId):

    #Before prediction
    K.clear_session()

    targetTrim =  request.get_json(force=True)

    # print("TARGET:",targetTrim)

    # UNCOMMENT THE NEXT LINE TO TEST WITH KNOWN TRIMESTRES
    # array_data_test = adaptX_test(studentId)

    array_data_test = adaptX(studentId)

    # print("DATA X:", array_data_test[0][0], array_data_test[0][29], array_data_test.shape)

    array_target_test, array_data_test = adaptYModel5(targetTrim, array_data_test)

    # print("array", array_data_test.shape, array_target_test[0].shape, file=sys.stderr)
    # print("target result:", array_target_test, file=sys.stderr)

    modelPath = os.path.abspath("../datos/modelos/model-5.0.pkl")
    model = joblib.load(open(modelPath,'rb'))

    output = model.predict([array_data_test, array_target_test])

    print(output, file=sys.stderr)

    outputs = []
    for o in output:
        outputs.append(o[0])

    order_index = np.argsort(outputs)[::-1][:10]

    final_subjects = []

    for oi in order_index:
        final_subjects.append({'subjects': targetTrim[oi], 'prediction': str(output[oi][0])})
    
    print("final subjects", final_subjects)

    #After prediction
    K.clear_session()
    return jsonify(final_subjects)


if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT) 



#Modelo 5 testeo con split
# TEST DATA: [array([10068854]) array([10087881]) array([10077126]) array([10078660])
#  array([10066589]) array([10079147]) array([10091723]) array([10074639])
#  array([10091471]) array([10061223]) array([10088866]) array([10082111])
#  array([10065078])]
