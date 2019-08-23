#imports
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import pandas as pd
import numpy as np
import os 

from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dropout, Dense, Flatten, Activation, LSTM, Bidirectional, Concatenate
from keras.models import Model
# to store the model for later predictions into a .pkl-file.
from sklearn.externals import joblib

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route('/api/train', methods=['POST']) #http://localhost:8081/api/train
def train():
    # # get parameters from request
    # parameters = request.get_json()
    
    # # read iris data set
    # iris = datasets.load_iris()
    # X, y = iris.data, iris.target

    # # fit model
    # clf = svm.SVC(C=float(parameters['C']),
    #               probability=True,
    #               random_state=1)
    # clf.fit(X, y)

    # # persist model
    # joblib.dump(clf, 'model.pkl')
    # return jsonify({'accuracy': round(clf.score(X, y) * 100, 2)})

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)