import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.model_selection import train_test_split

def adaptX(studentId):
    studentId = int(studentId)
    one_hot_path = os.path.abspath('..\\datos\\ordenados\\one_hot_modificado.csv')
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    print('grouped', grouped, file=sys.stderr)

    array_data = []

    max_number_trim = 30
    max_number_assigns = 10

    # out_estudiante = display(progress(0, len(grouped)), display_id=True)
    i_estudiante = 0

    # out_trim = display(progress(0, len(grouped)), display_id=True)

    for est, est_group in grouped:
        i_estudiante += 1
        # out_estudiante.update(progress(i_estudiante, len(grouped)))
        count = 0
        
        count += 1
        # out_trim.update(progress(count, est_group.shape[0]))
        row_trim = []

        for num_empty in range(max_number_trim): #Se agarran todos los trimestres
            row_trim.append(np.zeros((264), dtype=int))

        start_trim = max_number_trim - est_group.shape[0]

        for num in range(est_group.shape[0]): #Aquí es cuando se ponen los valores en los trimestres.
            row_trim[start_trim + num ] = est_group.iloc[ num , 3:].values
        array_data.append(np.asarray(row_trim))

    return np.asarray(array_data)

def adaptXModel3(studentId):
    studentId = int(studentId)
    one_hot_path = os.path.abspath('..\\datos\\one_hot_model_3.csv')
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    print('grouped', grouped, file=sys.stderr)

    array_data = []

    max_number_trim = 30
    max_number_assigns = 10

    # out_estudiante = display(progress(0, len(grouped)), display_id=True)
    i_estudiante = 0

    # out_trim = display(progress(0, len(grouped)), display_id=True)

    for est, est_group in grouped:
        i_estudiante += 1
        # out_estudiante.update(progress(i_estudiante, len(grouped)))
        count = 0
        
        count += 1
        # out_trim.update(progress(count, est_group.shape[0]))
        row_trim = []

        for num_empty in range(max_number_trim): #Se agarran todos los trimestres
            row_trim.append(np.zeros((124), dtype=int))

        start_trim = max_number_trim - est_group.shape[0]

        for num in range(est_group.shape[0]): #Aquí es cuando se ponen los valores en los trimestres.
            row_trim[start_trim + num ] = est_group.iloc[ num , 5:].values
        array_data.append(np.asarray(row_trim))

    return np.asarray(array_data)