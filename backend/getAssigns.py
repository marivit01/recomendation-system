import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.model_selection import train_test_split

def getAvailableSubjects(studentId):
    studentId = int(studentId)
    one_hot_path = os.path.abspath('..\\datos\\one_hot.csv')
    one_hot = pd.read_csv(one_hot_path)
    grouped = one_hot[one_hot['estudiante'] == studentId].sort_values('trimestre').groupby(['estudiante'])
    assigns_trim_target = []
    for est, est_group in grouped:
        for num in range(est_group.shape[0]):
            assigns_trim_target = np.append(assigns_trim_target, est_group.iloc[num, 2:].index[est_group.iloc[num, 2:] == 1].values.tolist(), axis=None)

    assigns_trim_target_aux = []
    for assign in assigns_trim_target:
        print(assign.split('_')[0])
        assigns_trim_target_aux = np.append(assigns_trim_target_aux, assign.split('_')[0], axis=None)
    print(np.asarray(assigns_trim_target_aux).tolist())

    #NUEVO
    seenSubjects = np.asarray(assigns_trim_target_aux)
    path = os.path.abspath('..\\datos\\subjectNames.csv')
    subjectNames = pd.read_csv(path)

    # Se obtienen las materias que el estudiante no ha visto
    mask = subjectNames['asignatura'].isin(seenSubjects)
    availableSubjects = subjectNames[~mask]

    # Se llama a la función para transformar las materias disponibles en un array con {code, name}
    availableSubjectsFormatted = getSubjectsNames(available)
    return availableSubjectsFormatted

# Función que recibe un array de las materias que un estudiante no ha visto, 
# y lo devuelve en formato code, name para pasarlo al manejador
def getSubjectsNames(availablesArray):
    subjectsArray = []
    for idx,subject in availablesArray.iterrows():
        print(subject.values)
        tmp = {'code':subject.values[1], 'name':subject.values[2]}
        subjectsArray.append(tmp)
    print(subjectsArray)
    return subjectsArray
